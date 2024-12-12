import re
import pymongo
from scrapy import Request, crawler, FormRequest
from scrapy.spiders import CrawlSpider
from pokemonspider.items import PokemonCardItem, TrainerCardItem
from pokemonspider.settings import MONGO_URL,MONGO_DATABASE,MONGO_COLLECTION
from urllib.parse import urlencode
class PokemoncardsSpider(CrawlSpider):
    name = "trainercards"
    allowed_domains = ["limitlesstcg.com"]
    # base_url = "https://limitlesstcg.com/cards"

    # 单独设置MongoDB的pipeline
    custom_settings = {
        'ITEM_PIPELINES': {
        "pokemonspider.pipelines.MongoTrainerCardsPipeline": 301,
        },
        'SPIDER_MIDDLEWARES':{
        'pokemonspider.middlewares.CookieMiddleware': 543,
     }
    }

    params = {'q': 't:train', 'show': 'all'}

    def __init__(self, *args, **kwargs):
        super(PokemoncardsSpider, self).__init__(*args, **kwargs)
        # 连接到MongoDB
        self.client = pymongo.MongoClient(MONGO_URL)
        self.db = self.client[MONGO_DATABASE]
    def start_requests(self):
        urls = ['https://limitlesstcg.com/cards?q=t%3Atrain&show=all&page=1',
                'https://limitlesstcg.com/cards?q=t%3Atrain&show=all&page=2',
                'https://limitlesstcg.com/cards?q=t%3Atrain&show=all&page=3']

        for url in urls:
            # 构建完整的URL
            yield FormRequest(
                    url=url,
                    callback=self.parse_index,
                    priority=0,
                    method='GET'
                )

    def parse_index(self, response):
        # print(response.text)
        domain = "https://limitlesstcg.com"
        # 拿到每个初始页面里面的所有卡牌的URL链接
        cards_index = response.selector.xpath('//div[@class="card-search-grid"]//a/@href').getall()

        for card_url in cards_index:
            card_url = domain + card_url
            yield Request(card_url, callback=self.parse_card_item)

    def parse_card_item(self, response):
        # 初始化一个PokemonCardItem对象来存储提取的数据
        card_item = TrainerCardItem()
        # 提取卡片名称、类型
        card_item['name'] = response.xpath('.//p[@class="card-text-title"]/span/a/text()').get()
        type_tmp = response.xpath('.//p[@class="card-text-type"]//text()').get()
        card_item['type'] = re.sub(r'\s+', ' ', type_tmp)

        ability_tmp = response.xpath('(//div[@class="card-text-section"])[2]//text()').getall()
        card_item['card_ability'] = ''.join([re.sub(r'\s+', ' ', text.strip()) for text in ability_tmp]).strip()

        # 提取卡片编号
        card_number = response.xpath('.//p[@class="card-text-title"]/span/a/@href').get()
        card_item['card_number'] = card_number[7:] if card_number else None

        # 提取插画师信息
        illustrator = response.xpath('.//div[contains(@class,"card-text-artist")]/a/text()').get()
        card_item['illustrator'] = illustrator.strip() if illustrator else None

        #提取卡牌图片
        card_item['image_url'] =response.xpath('.//div[@class="card-image"]/img/@src').get()

        yield card_item