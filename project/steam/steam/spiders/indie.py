# -*- coding: utf-8 -*-
import scrapy


class IndieSpider(scrapy.Spider):
    name = 'indie'
    allowed_domains = ['https://store.steampowered.com/tags/en/Indie/']
    start_urls = ['http://https://store.steampowered.com/tags/en/Indie//']

    def parse(self, response):
        pass
