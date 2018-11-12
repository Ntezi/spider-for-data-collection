# -*- coding: utf-8 -*-
import re

import scrapy

from crawler.UrlHelper import UrlHelper
from crawler.listing_item import ListingItem
from crawler.review_item import ReviewItem


class TripadvisorSpider(scrapy.Spider):
    name = 'tripadvisor'
    allowed_domains = ['tripadvisor.com']
    urls = UrlHelper.urls
    start_urls = urls

    def parse(self, response):
        self.log('I just visited: ' + response.url)
        company_name = response.css('h1.ui_header::text').extract_first()

        for review in response.css('div.review-container'):
            review_item = ReviewItem()
            review_item['title'] = review.css('span.noQuotes::text').extract_first()
            review_item['review'] = review.css('p.partial_entry::text').extract_first()
            review_item['date'] = review.css('span.ratingDate::attr(title)').extract_first()
            review_item['user'] = review.css('div.info_text > div::text').extract_first()
            review_item['company_name'] = company_name

            yield review_item

        # follow pagination link
        url = response.url
        if not re.findall(r'or\d', url):
            next_page = re.sub(r'(-Reviews-)', r'\g<1>or5-', url)
        else:
            page_number = int(re.findall(r'or(\d+)-', url)[0])
            page_number_next = page_number + 5
            next_page = url.replace('or' + str(page_number), 'or' + str(page_number_next))
        yield scrapy.Request(next_page, meta={'dont_redirect': True}, callback=self.parse)
