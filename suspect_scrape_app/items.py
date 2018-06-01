import scrapy

class TrackItem(scrapy.Item):

    name = scrapy.Field()
    link = scrapy.Field()
    role = scrapy.Field()
    firm = scrapy.Field()
    location = scrapy.Field()
    details = scrapy.Field()
    testing = scrapy.Field()
    ident = scrapy.Field()
