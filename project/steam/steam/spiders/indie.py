# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from steam.items import SteamItem

class IndieSpider(CrawlSpider):
    name = 'indie'
    allowed_domains = ['store.steampowered.com', 'steamcommunity.com']
    start_urls = ['https://store.steampowered.com/tags/en/Indie/']

    count = 0

    rules = (
        Rule(
            LinkExtractor(allow=(), restrict_css=('.tab_item',)),
             callback="parse_item",
             follow=True
             ),)

    def parse_item(self, response):
        self.count += 1
        print(self.count)
        com = 'https://steamcommunity.com/app/'
        rev = "/reviews/?browsefilter=toprated"
        app_id = response.url.split('/')[4]
        if not app_id.isdigit():
            return
        a = com + app_id + rev
        yield scrapy.Request(a, callback=self.parse_detail_page)
    
    def parse_detail_page(self, response):
        app_id = response.url.split('/')[4]
        reviews = response.css('.apphub_Card')
        for review in reviews:
            author = review.css('.apphub_CardContentAuthorName > a::text').extract_first()
            recommended_text = review.css('.title::text').extract_first().lower()
            recommended = (recommended_text == "recommended")
            text = " ".join(review.css('.apphub_CardTextContent::text').extract()).strip()
            item = SteamItem()
            item['app_id'] = app_id
            item['author'] = author
            item['recommended'] = recommended
            item['review'] = text
            yield item
        