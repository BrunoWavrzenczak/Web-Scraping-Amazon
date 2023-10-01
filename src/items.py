import scrapy

from itemloaders.processors import TakeFirst

class AmazonItems(scrapy.Item):
    url = scrapy.Field(output_processor=TakeFirst())
    page = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(output_processor=TakeFirst())
    rating = scrapy.Field(output_processor=TakeFirst())
    total_rating = scrapy.Field(output_processor=TakeFirst())
    brand = scrapy.Field(output_processor=TakeFirst())
    seller = scrapy.Field(output_processor=TakeFirst())
    features_bullets = scrapy.Field(output_processor=TakeFirst())
