import scrapy


class ReviewItem(scrapy.Item):
    title = scrapy.Field()
    review = scrapy.Field()
    date = scrapy.Field()
    user = scrapy.Field()
    company_name = scrapy.Field()
