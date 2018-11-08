import scrapy


class HotelSentimentItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    stars = scrapy.Field()
