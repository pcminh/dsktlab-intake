import scrapy


class ProductsSpider(scrapy.Spider):
    name = 'products'
    allowed_domains = ['https://lazada.vn']

    def start_requests(self):
        urls = ['https://www.lazada.vn/products/sale-tet-0h-dem-nay-iphone-13-mini-hang-chinh-hang-i1525530449-s6407475955.html']
        for url in urls:
            yield
        
    def parse(self, response):
        # Retrieve URL parameters (= slug + i**** + s**** + ".html")
        url_param = response.url.split("/")[-1]
        # Remove ".html" suffix
        slug_str = url_param[:-5]
        slug_tokens = slug_str.split('-')
        
        # The two last tokens are the product id and the product sku id for the currently selected variant
        # product_sku string will be changed using the History API by the React application
        product_id = slug_tokens[-2]
        product_sku = slug_tokens[-1]
