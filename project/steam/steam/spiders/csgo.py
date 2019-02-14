# -*- coding: utf-8 -*-
import scrapy
from steam.items import CsgoItem

class CsgoSpider(scrapy.Spider):
    name = 'csgo'
    allowed_domains = ['steamcommunity.com']
    start_urls = ['https://steamcommunity.com/app/730/positivereviews/?browsefilter=toprated',
        'https://steamcommunity.com/app/730/negativereviews/?browsefilter=toprated']

    def parse(self, response):
        page = response.xpath('//div[@id="page1"]')
        review_cards = page.css('.apphub_Card')
        for review in review_cards:
            author = review.css('.apphub_CardContentAuthorName > a::text').extract_first()
            recommended_text = review.css('.title::text').extract_first().lower()
            recommended = (recommended_text == "recommended")
            text = " ".join(review.css('.apphub_CardTextContent::text').extract()).strip()
            item = CsgoItem()
            item['author'] = author
            item['recommended'] = recommended
            item['review'] = text
            yield item
        form = response.xpath('//form[@id="MoreContentForm1"]')
        data = dict()
        for html_input in form.css('input'):
            name = html_input.attrib['name']
            value = html_input.attrib['value']
            data[name] = value
        yield scrapy.FormRequest(url='https://steamcommunity.com/app/730/homecontent/', formdata=data, callback=self.parse_form)

    def parse_form(self, response):
        first_div = response.css('div')[0]
        div_id = first_div.attrib['id']
        print(div_id)
        if not div_id:
            return
        
        review_cards = first_div.css('.apphub_Card')
        for review in review_cards:
            author = review.css('.apphub_CardContentAuthorName > a::text').extract_first()
            recommended_text = review.css('.title::text').extract_first().lower()
            recommended = (recommended_text == "recommended")
            text = " ".join(review.css('.apphub_CardTextContent::text').extract()).strip()
            item = CsgoItem()
            item['author'] = author
            item['recommended'] = recommended
            item['review'] = text
            yield item

        form = response.css('form')
        data = dict()
        for html_input in form.css('input'):
            name = html_input.attrib['name']
            value = html_input.attrib['value']
            data[name] = value
        yield scrapy.FormRequest(url='https://steamcommunity.com/app/730/homecontent/', formdata=data, callback=self.parse_form)