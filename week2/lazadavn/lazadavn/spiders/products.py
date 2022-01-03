import scrapy


class ProductsSpider(scrapy.Spider):
    name = 'products'
    allowed_domains = ['https://lazada.vn']
    start_urls = ['https://lazada.vn/']

    def parse(self, response):
        pass
