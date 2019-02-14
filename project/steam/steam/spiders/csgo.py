# -*- coding: utf-8 -*-
import scrapy
from steam.items import CsgoItem

class CsgoSpider(scrapy.Spider):
    name = 'csgo'
    allowed_domains = ['steamcommunity.com']
    start_urls = ['https://steamcommunity.com/app/730/positivereviews/?browsefilter=toprated',
        'https://steamcommunity.com/app/730/negativereviews/?browsefilter=toprated']

    page = {
        'pos': 'page1',
        'neg': 'page1'
    }

    def parse(self, response):
        """ For the first page: 
        find the page1 div and form which are nested in some html. 
        Extract the review data. 
        Extract the form data, and then submit the for to get the next page
        of review. 
        """
        pos = (response.url.split("/")[5] == "positivereviews")
        page = response.xpath('//div[@id="page1"]')
        review_cards = page.css('.apphub_Card')
        for card in review_cards:
            yield self.create_item(card)
        form = response.xpath('//form[@id="MoreContentForm1"]')
        data,_ = self.get_form_data(form)
        yield scrapy.FormRequest(url='https://steamcommunity.com/app/730/homecontent/', formdata=data, callback=self.parse_form)

    def parse_form(self, response):
        """ The first div contains the review cards,
        extract review data and submit form for next page. 
        """
        first_div = response.css('div')[0]
        div_id = first_div.attrib['id']

        form = response.css('form')
        data, label = self.get_form_data(form)
        
        if div_id == self.page[label]:
            print("%s has already been at %s" % (label, div_id))
            yield

        review_cards = first_div.css('.apphub_Card')
        for card in review_cards:
            yield self.create_item(card)
    
        self.page[label] = div_id
        print("%s is now at %s" % (label, div_id))
        
        yield scrapy.FormRequest(url='https://steamcommunity.com/app/730/homecontent/', formdata=data, callback=self.parse_form)

    def get_form_data(self, form):
        """ Extract all the form data 
        required for getting the next page.
        Returns the formdata and label of review.
        """
        data = dict()
        for html_input in form.css('input'):
            name = html_input.attrib['name']
            value = html_input.attrib['value']
            data[name] = value
        
        label = ""
        if data['appHubSubSection'] == "16":
            label = 'pos'
        else:
            label = 'neg'
        return data, label
    
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
