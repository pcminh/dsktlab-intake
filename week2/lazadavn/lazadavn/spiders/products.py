import datetime
import functools
import scrapy
import js2xml
import lxml.etree
import chompjs
import json
from parsel import Selector

from lazadavn.items import ProductItem

def p2f(x):
    return float(x.strip('%'))/100

class ProductsSpider(scrapy.Spider):
    name = 'products'
    allowed_domains = ['lazada.vn']

    def start_requests(self):
        urls = ['https://www.lazada.vn/products/sale-tet-0h-dem-nay-iphone-13-mini-hang-chinh-hang-i1525530449-s6407475955.html',
                'https://www.lazada.vn/products/sale-tet-macbook-air-2020-133-inches-m1-hang-chinh-hang-i1040858590-s3520978989.html']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # @param unparsed_js_text Raw text content extracted from <script> tag in HTML DOM
    # @param var_name Name of the desired variable to extract
    # @returns <dict> content of the object, mapped to Python dictionary
    @staticmethod
    def extract_primitive_from_js(unparsed_js_text, var_name):
        # Code snippets below found here: https://docs.scrapy.org/en/latest/topics/dynamic-content.html#topics-parsing-javascript

        # Use js2xml to convert the JavaScript code into an XML document
        script_xml = lxml.etree.tostring(
            js2xml.parse(unparsed_js_text), encoding='unicode')
        # Using parsel.Selector to parse to converted XML document as text
        xml_script_selector = Selector(text=script_xml)
        # Select a variable named {var_name} and extracts it
        xml_variable = xml_script_selector.css(f'var[name="{var_name}"]').get()
        return xml_variable

    def parse(self, response):
        # Retrieve URL parameters (= slug + i**** + s**** + ".html")
        url_param = response.url.split("/")[-1]
        # Remove ".html" suffix
        slug_str = url_param[:-5]
        slug_tokens = slug_str.split('-')

        # The two last tokens are the product id and the product sku id for the currently selected variant
        # product_sku string will be changed using the History API by the React application
        product_id = slug_tokens[-2][1:]
        product_sku = slug_tokens[-1][1:]
        product_slug = functools.reduce(lambda x, y: x + '-' + y, slug_tokens[:-3])

        # Lazada Product Page dynamically loads content from their server

        # Extract JSON+LD from HTML DOM
        # This page JSON+LD data contains information about
        #   - Product:
        #     name, url, category, brand, sku, mpn (=prod id), description
        #     review aggregation (min, max, avg, count)
        #     price (min, max, variants count)
        #     seller
        #   - BreadcumbList
        linked_data_json = response.css(
            'script[type="application/ld+json"]::text').getall()
        product_data = json.loads(linked_data_json[0])
        breadcrumb_list_data = json.loads(linked_data_json[1])

        # Tracking data from product page contains the following information:
        #   - Category
        #   - Discount Percentage
        #   - Brand Name+ID
        #   - Product ID (misnamed: pdt_sku)
        #   - Product Name
        #   - Regional Category ID (used with getRecommendations API)
        #   - Original Product Price (pdt_price)
        # Tracking data are hard-coded into a script that can be found below
        pdp_tracking_data_jscript = response.css(
            'script[type="text/javascript"]::text').get()
        tracking_data_str = self.extract_primitive_from_js(
            pdp_tracking_data_jscript, 'pdpTrackingData')
        tracking_data = chompjs.parse_js_object(tracking_data_str)

        # This <script> has the __moduleData__ var containing all the information
        # needed to render the product page client-side (by calling the //laz-g-cdn.alicdn.com/lzdfe/pdp-platform/0.1.22/pc.js)
        module_data_jscript = response.xpath(
            '/html/body/script[14]/text()').get()
        js_lines = module_data_jscript.split('\n')
        module_data = chompjs.parse_js_object(js_lines[63])
        module_data_fields = module_data['data']['root']['fields']

        loaded_sku_ids = module_data_fields['primaryKey']['loadedSkuIds']
        sku_base = module_data_fields['productOption']['skuBase']['skus']
        sku_info = module_data_fields['skuInfos']

        skus = []

        for sku in sku_base:
            sku_id = sku['skuId']
            inner_sku_id = sku['innerSkuId']
            prop_path = sku['propPath']
            price = sku_info[sku_id]['price']
            stock = sku_info[sku_id]['stock']

            skus.append({
                'skuId': sku_id,
                'innerSkuId': inner_sku_id,
                'propPath': prop_path,
                'price': price,
                'stock': stock
            })

        product = ProductItem()
        product['_id'] = f'product_{product_id}'
        product['type'] = 'product'
        product['crawledAt'] = datetime.datetime.now()
        product['productName'] = module_data_fields['product']['title']
        product['productId'] = product_id
        product['slug'] = product_slug
        product['description'] = product_data['description']
        product['categories'] = product_data['category']
        product['breadcrumbs'] = module_data_fields['Breadcrumb']
        product['brand'] = module_data_fields['product']['brand']
        product['seller'] = {
            'sellerId': module_data_fields['seller']['sellerId'],
            'shopId': module_data_fields['seller']['shopId'],
            'sellerName': module_data_fields['seller']['name'],
            'chatResponsiveRate': p2f(module_data_fields['seller']['chatResponsiveRate']['value']),
            'positiveSellerRate': p2f(module_data_fields['seller']['positiveSellerRating']['value']),
            'shipOnTimeRate': p2f(module_data_fields['seller']['shipOnTime']['value'])
        }
        product['productOptions'] = module_data_fields['productOption']['skuBase']['properties']
        product['productSkus'] = skus

        yield product


    def parse_fat(self, response):
        # Retrieve URL parameters (= slug + i**** + s**** + ".html")
        url_param = response.url.split("/")[-1]
        # Remove ".html" suffix
        slug_str = url_param[:-5]
        slug_tokens = slug_str.split('-')

        # The two last tokens are the product id and the product sku id for the currently selected variant
        # product_sku string will be changed using the History API by the React application
        product_id = slug_tokens[-2][1:]
        product_sku = slug_tokens[-1][1:]

        # Lazada Product Page dynamically loads content from their server

        # Extract JSON+LD from HTML DOM
        # This page JSON+LD data contains information about
        #   - Product:
        #     name, url, category, brand, sku, mpn (=prod id), description
        #     review aggregation (min, max, avg, count)
        #     price (min, max, variants count)
        #     seller
        #   - BreadcumbList
        linked_data_json = response.css(
            'script[type="application/ld+json"]::text').getall()
        product_data = json.loads(linked_data_json[0])
        breadcrumb_list_data = json.loads(linked_data_json[1])

        # Tracking data from product page contains the following information:
        #   - Category
        #   - Discount Percentage
        #   - Brand Name+ID
        #   - Product ID (misnamed: pdt_sku)
        #   - Product Name
        #   - Regional Category ID (used with getRecommendations API)
        #   - Original Product Price (pdt_price)
        # Tracking data are hard-coded into a script that can be found below
        pdp_tracking_data_jscript = response.css(
            'script[type="text/javascript"]::text').get()
        tracking_data_str = self.extract_primitive_from_js(
            pdp_tracking_data_jscript, 'pdpTrackingData')
        tracking_data = chompjs.parse_js_object(tracking_data_str)

        # This <script> has the __moduleData__ var containing all the information
        # needed to render the product page client-side (by calling the //laz-g-cdn.alicdn.com/lzdfe/pdp-platform/0.1.22/pc.js)
        module_data_jscript = response.xpath(
            '/html/body/script[14]/text()').get()
        js_lines = module_data_jscript.split('\n')
        module_data = chompjs.parse_js_object(js_lines[63])

        with open(f'product_{product_id}_{product_sku}.html', 'wb') as f:
            f.write(response.body)

        yield {
            '_id': f'product_{product_id}_{product_sku}',
            'product': product_data,
            'tracking': tracking_data,
            'breadcrumbs': breadcrumb_list_data,
            'moduleData': module_data,
        }
