# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BaomoiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ArticleItem(scrapy.Item):
    id = scrapy.Field()
    slug = scrapy.Field()
    title = scrapy.Field()
    short_text = scrapy.Field()
    content_text = scrapy.Field()
    time = scrapy.Field()
    cached_link = scrapy.Field()
    publisher_link = scrapy.Field()
    tags = scrapy.Field()
    breadcrumbs = scrapy.Field()