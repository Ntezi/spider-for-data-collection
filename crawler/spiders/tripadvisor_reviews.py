# -*- coding: utf-8 -*-
import re

import scrapy


class TripadvisorReviewsSpider(scrapy.Spider):
    name = 'tripadvisor_reviews'
    allowed_domains = ['www.tripadvisor.com']
    start_urls = [
        'https://www.tripadvisor.com/Hotel_Review-g293829-d6966018-Reviews-or5-Five_to_Five_Hotel-Kigali_Kigali_Province.html']

    def parse(self, response):
        self.log('I just visited: ' + response.url)
        for review in response.css('div.review-container'):
            item = {
                'author_name': review.css('span.noQuotes::text').extract_first(),
                'text': review.css('p.partial_entry::text').extract_first(),
            }
            yield item

        # follow pagination link
        url = response.url
        if not re.findall(r'or\d', url):
            next_page = re.sub(r'(-Reviews-)', r'\g<1>or5-', url)
        else:
            page_number = int(re.findall(r'or(\d+)-', url)[0])
            page_number_next = page_number + 5
            next_page = url.replace('or' + str(page_number), 'or' + str(page_number_next))
        yield scrapy.Request(
            next_page,
            meta={'dont_redirect': True},
            callback=self.parse
        )

