import scrapy
from scrapy.http import HtmlResponse
from ads_parser.items import AdsParserItem
from scrapy.loader import ItemLoader

class OlxkzSpider(scrapy.Spider):
    name = 'olxkz'
    allowed_domains = ['olx.kz']
    start_urls = ['https://www.olx.kz/d/list/q-iphone/']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://www.olx.kz/d/list/q-{kwargs.get("search")}/']

    def parse(self, response: HtmlResponse):
        print()
        links = response.xpath("//div[@data-cy='l-card']/a")
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response:HtmlResponse):
        loader = ItemLoader(item=AdsParserItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('price', "//h3//text()")
        loader.add_xpath('photos', "//div[@class='swiper-zoom-container']/img/@src | "
                                   "//div[@class='swiper-zoom-container']/img/@data-src")
        loader.add_value('url', response.url)
        yield loader.load_item()


        # name = response.xpath("//h1/text()").get()
        # price = response.xpath("//h3/text()").getall()
        # photos = response.xpath("//div[@class='swiper-zoom-container']/img/@src |"
        #                         " //div[@class='swiper-zoom-container']/img/@data-src").getall()
        # url = response.url
        # yield AdsParserItem(name=name, price=price, photos=photos)
