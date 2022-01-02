import scrapy
from scrapy.loader import ItemLoader
from baomoi.items import ArticleItem
import functools

class ArticlesSpider(scrapy.Spider):
    name = 'articles'
    allowed_domains = ['baomoi.com']


    def start_requests(self):
        # urls = [
        # 'https://baomoi.com/tin-moi/trang1.epi'
        # ]

        # for url in urls:
        #     yield scrapy.Request(url=url, callback=self.parse)

        for x in range(1, 2):
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
            # yield {
            #     'title': anchor.css('::attr(title)').get(),
            #     'link': anchor.css('::attr(href)').get()
            # }

            normalized_link = 'https://baomoi.com' + anchor.css('::attr(href)').get()
            yield scrapy.Request(url=normalized_link, callback=self.parse_article)

    def parse_article(self, response):
        l = ItemLoader(item=ArticleItem(), response=response)

        title = response.css('h1.bm_L::text').get()
        short_text = response.css('h3.bm_L.bm_AH::text').get()
        
        paragraphs = response.css('div.bm_Cc p.bm_V::text').getall()
        content_text = functools.reduce(lambda x, y: x + ' ' + y, paragraphs)

        time = response.css('div.bm_AN time::attr(datetime)').get()
        cached_link = response.url
        publisher_link = response.css('p.bm_Bk span::text')[-1].get()
        tags = response.css('li.bm_BI a::text').getall()
        breadcrumbs = response.css('a.bm_c::text').getall()

        article_id = cached_link.split('/')[-1].split('.')[0]
        article_slug = cached_link.split('/')[-3]

        l.add_value('id', article_id)
        l.add_value('slug', article_slug)
        l.add_value('title', title)
        l.add_value('short_text', short_text)
        l.add_value('content_text', content_text)
        l.add_value('time', time)
        l.add_value('cached_link', cached_link)
        l.add_value('publisher_link', publisher_link)
        l.add_value('tags', tags)
        l.add_value('breadcrumbs', breadcrumbs)

        return l.load_item()

        # yield {
        #     'id': article_id,
        #     'slug': article_slug,
        #     'title': title,
        #     'short_text': short_text,
        #     'content_text': content_text,
        #     'time': time,
        #     'cached_link': cached_link,
        #     'publisher_link': publisher_link,
        #     'tags': tags,
        #     'breadcrumbs': breadcrumbs
        # }
