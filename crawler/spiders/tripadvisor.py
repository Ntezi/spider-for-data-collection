# -*- coding: utf-8 -*-
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

        reviews = []
        for review in response.css('div.review-container'):
            review_item = ReviewItem()
            review_item['title'] = review.css('span.noQuotes::text').extract_first()
            review_item['review'] = review.css('p.partial_entry::text').extract_first()
            review_item['date'] = review.css('span.ratingDate::attr(title)').extract_first()
            review_item['user'] = review.css('div.info_text > div::text').extract_first()

            reviews.append(review_item)

        yield scrapy.Request(response.url, meta={'reviews': reviews}, callback=self.parse_reviews)

    def parse_reviews(self, response):
        review_item = response.meta['reviews']

        listing_item = ListingItem()
        listing_item['name'] = response.css('h1.ui_header::text').extract_first()
        listing_item['reviews'] = review_item

        return {"listing": listing_item}
