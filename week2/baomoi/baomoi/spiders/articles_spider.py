import scrapy
from scrapy.loader import ItemLoader
from baomoi.items import ArticleItem
import functools

class ArticlesSpider(scrapy.Spider):
    name = 'articles'
    allowed_domains = ['baomoi.com']

    def start_requests(self):
        # Baomoi only stores 3000 of the most recent articles
        # Each page contains 18 article links
        # Therefore, maximum of 167 pages (166*18 + 12)

        pages_count = 10
        if self.pages is not None:
            param_pages = int(self.pages)
            pages_count = param_pages if param_pages <= 167 else 167

        for x in range(1, pages_count + 1):
            url = f'https://baomoi.com/tin-moi/trang{x}.epi'
            yield scrapy.Request(url=url, callback=self.parse_articles_page)

    def parse_articles_page(self, response):
        # # https://baomoi.com/tin-moi/trang1.epi --> 'trang1.epi'
        # path_info = response.url.split('/')[-1]

        # # 'trang1.epi' --> 'trang1', 'epi'
        # page_name = path_info.split('.')[0]

        # # 'trang1' --> '1'
        # page_count = page_name[5:]

        # filename = f'tin-moi-{page_count}.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)

        for anchor in response.css('h4.bm_L a'):
            normalized_link = 'https://baomoi.com' + anchor.css('::attr(href)').get()
            yield scrapy.Request(url=normalized_link, callback=self.parse_article)

    def parse_article(self, response):
        title = response.css('h1.bm_L::text').get()
        short_text = response.css('h3.bm_L.bm_AH::text').get()
        
        paragraphs = response.css('div.bm_Cc p.bm_V::text').getall()
        content_text = functools.reduce(lambda x, y: x + '\n' + y, paragraphs)

        time = response.css('div.bm_AN time::attr(datetime)').get()
        cached_link = response.url
        publisher_link = response.css('p.bm_Bk span::text')[-1].get()
        tags = response.css('li.bm_BI a::text').getall()
        breadcrumbs = response.css('a.bm_c::text').getall()

        article_id = cached_link.split('/')[-1].split('.')[0]
        article_slug = cached_link.split('/')[-3]

        item = ArticleItem()
        item['id'] = article_id
        item['slug'] = article_slug
        item['type'] = 'article'

        item['title'] = title
        item['short_text'] = short_text
        item['content_text'] = content_text
        item['time'] = time
        item['cached_link'] = cached_link
        item['publisher_link'] = publisher_link
        item['tags'] = tags
        item['breadcrumbs'] = breadcrumbs
        
        item['_id'] = f'article_{article_id}'

        yield item
