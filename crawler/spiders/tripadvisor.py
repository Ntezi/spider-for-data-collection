# -*- coding: utf-8 -*-
import re

import scrapy


class TripadvisorSpider(scrapy.Spider):
    name = 'tripadvisor'
    allowed_domains = ['tripadvisor.com']
    # start_urls = ['https://www.tripadvisor.com/Hotels-g3685401-Northern_Province-Hotels.html']
    # start_urls = ['https://www.tripadvisor.com/Hotels-g3685404-Western_Province-Hotels.html']
    # start_urls = ['https://www.tripadvisor.com/Hotels-g3685403-Southern_Province-Hotels.html']
    # start_urls = ['https://www.tripadvisor.com/Hotels-g3685402-Eastern_Province-Hotels.html']


    # start_urls = ['https://www.tripadvisor.com/Restaurants-g293829-Kigali_Kigali_Province.html']

    start_urls = ['https://www.tripadvisor.com/Attractions-g293829-Activities-Kigali_Kigali_Province.html']

    def parse(self, response):
        self.log('I just visited: ' + response.url)
        for listing in response.css('div.listing'):
            item = {
                # 'name': listing.css('div.listing_title > a::text').extract_first(),
                # 'url': 'https://www.tripadvisor.com' + listing.css('a.property_title::attr(href)').extract_first()
                'url': 'https://www.tripadvisor.com' + listing.css('div.listing_title > a::attr(href)').extract_first()
            }
            yield item

        # follow pagination link
        url = response.url
        if not re.findall(r'oa\d+', url):
            next_page = re.sub(r'(-g293829-)', r'\g<1>oa30-', url)
        else:
            page_number = int(re.findall(r'oa(\d+)-', url)[0])
            page_number_next = page_number + 30
            next_page = url.replace('oa' + str(page_number), 'oa' + str(page_number_next))
        yield scrapy.Request(next_page, meta={'dont_redirect': True}, callback=self.parse)
