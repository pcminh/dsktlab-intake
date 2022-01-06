# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LazadavnItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ProductItem(scrapy.Item):
    _id = scrapy.Field()
    type = scrapy.Field()
    crawledAt = scrapy.Field()
    productName = scrapy.Field()
    productId = scrapy.Field()
    slug = scrapy.Field()
    description = scrapy.Field()
    categories = scrapy.Field()
    breadcrumbs = scrapy.Field()
    brand = scrapy.Field()
    seller = scrapy.Field()
    productOptions = scrapy.Field()
    productSkus = scrapy.Field()
    prices = scrapy.Field()
    

