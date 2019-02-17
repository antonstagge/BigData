# -*- coding: utf-8 -*-
import scrapy
from steam.items import CsgoItem

class CsgoSpider(scrapy.Spider):
    name = 'csgo'
    allowed_domains = ['steamcommunity.com']
    start_urls = ['https://steamcommunity.com/app/730/positivereviews/?browsefilter=toprated', # CS:GO
        'https://steamcommunity.com/app/730/negativereviews/?browsefilter=toprated',
        'https://steamcommunity.com/app/271590/positivereviews/?browsefilter=toprated', # GTAV
        'https://steamcommunity.com/app/271590/negativereviews/?browsefilter=toprated',
        'https://steamcommunity.com/app/570/positivereviews/?browsefilter=toprated', # Dota
        'https://steamcommunity.com/app/570/negativereviews/?browsefilter=toprated',
        'https://steamcommunity.com/app/578080/positivereviews/?browsefilter=toprated', # PubG
        'https://steamcommunity.com/app/578080/negativereviews/?browsefilter=toprated',
        'https://steamcommunity.com/app/252490/positivereviews/?browsefilter=toprated', # Rust 
        'https://steamcommunity.com/app/252490/negativereviews/?browsefilter=toprated',
        'https://steamcommunity.com/app/346110/positivereviews/?browsefilter=toprated', # ARK 
        'https://steamcommunity.com/app/346110/negativereviews/?browsefilter=toprated',
        'https://steamcommunity.com/app/550/positivereviews/?browsefilter=toprated', # left4dead2 
        'https://steamcommunity.com/app/550/negativereviews/?browsefilter=toprated',
        'https://steamcommunity.com/app/304930/positivereviews/?browsefilter=toprated', # Unturned 
        'https://steamcommunity.com/app/304930/negativereviews/?browsefilter=toprated',
        'https://steamcommunity.com/app/555570/positivereviews/?browsefilter=toprated', # Infestation 
        'https://steamcommunity.com/app/555570/negativereviews/?browsefilter=toprated',
        'https://steamcommunity.com/app/201510/positivereviews/?browsefilter=toprated', # Flat out 3: Chaos & Destuction 
        'https://steamcommunity.com/app/201510/negativereviews/?browsefilter=toprated',
        'https://steamcommunity.com/app/577800/positivereviews/?browsefilter=toprated', # NBA 2k18
        'https://steamcommunity.com/app/577800/negativereviews/?browsefilter=toprated']
    
    scrape_count = 0

    def parse(self, response):
        """ For the first page: 
        find the page1 div and form which are nested in some html. 
        Extract the review data. 
        Extract the form data, and then submit the for to get the next page
        of review. 
        """
        url_split = response.url.split("/")
        app_id = url_split[4]
        page = response.xpath('//div[@id="page1"]')
        review_cards = page.css('.apphub_Card')
        for card in review_cards:
            yield self.create_item(card)
        self.scrape_count += 10

        form = response.xpath('//form[@id="MoreContentForm1"]')
        data = self.get_form_data(form)
        yield scrapy.FormRequest(url='https://steamcommunity.com/app/' + app_id + '/homecontent/', formdata=data, callback=self.parse_form)

    def parse_form(self, response):
        """ The first div contains the review cards,
        extract review data and submit form for next page. 
        """
        first_div = response.css('div')[0]
        div_id = first_div.attrib['id']

        form = response.css('form')
        data = self.get_form_data(form)

        review_cards = first_div.css('.apphub_Card')
        for card in review_cards:
            yield self.create_item(card)
        self.scrape_count += 10

        if self.scrape_count % 1000 == 0:
            print("Scrape count is: %d" % self.scrape_count)
        if self.scrape_count > 1000000:
            print("Final scrape count is: %d" % self.scrape_count)
            return
        
        yield scrapy.FormRequest(url=response.url, formdata=data, callback=self.parse_form)

    def get_form_data(self, form):
        """ Extract all the form data 
        required for getting the next page.
        """
        data = dict()
        for html_input in form.css('input'):
            name = html_input.attrib['name']
            value = html_input.attrib['value']
            data[name] = value
        
        return data
    
    def create_item(self, card):
        """ Create the csv item which
        is going to be stored. 
        """
        author = card.css('.apphub_CardContentAuthorName > a::text').extract_first()
        recommended_text = card.css('.title::text').extract_first().lower()
        recommended = (recommended_text == "recommended")
        text = " ".join(card.css('.apphub_CardTextContent::text').extract()).strip()
        item = CsgoItem()
        item['author'] = author
        item['recommended'] = recommended
        item['review'] = text
        return item
