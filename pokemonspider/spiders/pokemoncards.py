import random
import re
import time
import pymongo
import scrapy
from gerapy_selenium import SeleniumRequest
from scrapy import Request, crawler
from scrapy.spiders import CrawlSpider
from pokemonspider.items import PokemonCardItem
from pokemonspider.settings import MONGO_URL,MONGO_DATABASE,MONGO_COLLECTION
class PokemoncardsSpider(CrawlSpider):
    name = "pokemoncards"
    allowed_domains = ["limitlesstcg.com"]
    base_url = "https://limitlesstcg.com/cards?q=pokemon:"
    item_field = 'name'

    # 单独设置MongoDB的pipeline
    custom_settings = {
        'ITEM_PIPELINES': {
        "pokemonspider.pipelines.MongoCardsPipeline": 301,
        },
    #     'DOWNLOADER_MIDDLEWARES':{
    #     'scrapy_proxies.RandomProxy': 100,
    #     'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    # },
        'SPIDER_MIDDLEWARES' :{
        'pokemonspider.middlewares.CookieMiddleware': 543,
     }
    }

    def __init__(self, *args, **kwargs):
        super(PokemoncardsSpider, self).__init__(*args, **kwargs)
        # 连接到MongoDB
        self.client = pymongo.MongoClient(MONGO_URL)
        self.db = self.client[MONGO_DATABASE]
    def start_requests(self):
        # #从Pokemon的库里取名字，构成初始页面
        # items = self.db[MONGO_COLLECTION].distinct(self.item_field)
        items = ['zacian-crowned','zamazenta-crowned','urshifu-gmax','urshifu-rapid-strike-gmax','urshifu-rapid-strike','calyrex-ice-rider',"calyrex-shadow-rider"]

        # 使用列表推导式生成所有初始请求
        requests = [
            Request(
                url=self.base_url + f'{item}',
                callback=self.parse_index,
                priority=0
            )
            for item in items
        ]
        # 如果items数量较大，可以分批发送请求以避免过多的并发请求数量
        batch_size = 10  # 根据实际情况调整
        for i in range(0, len(requests), batch_size):
            yield from requests[i:i + batch_size]
        # #测试
        # yield Request(
        #         url="https://limitlesstcg.com/cards?q=pokemon:Zamazenta",
        #         callback=self.parse_index,
        #         dont_filter=True,
        #         priority=0
        #     )

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
        card_item = PokemonCardItem()

        # 提取卡片名称、类型、HP 和进化信息
        title_info = ''.join(response.xpath('.//p[@class="card-text-title"]//text()').getall()).strip()
        title_parts = re.split(r'\s*-\s*', title_info)
        card_item['name'] = response.xpath('.//p[@class="card-text-title"]/span/a/text()').get()
        card_item['type'] = response.xpath('.//p[@class="card-text-title"]/text()[2]').get().split('-')[1].strip()
        card_item['hp'] = re.sub(r'[^0-9]', '', title_parts[-1]) if len(title_parts) > 2 else None  # 只保留数字作为HP值

        evolves_link = response.xpath('.//p[@class="card-text-type"]//text()').getall()
        cleaned_evolves_info = ''.join([i.strip().replace('\n', '').replace('  ', ' ') for i in evolves_link])
        card_item['Evolves_link'] = ' '.join(cleaned_evolves_info.split())

        # 提取能力信息（如果有）
        ability_info = response.xpath('.//p[@class="card-text-ability-info"]/text()').get()
        card_item['ability_info'] = re.sub(r'\s+', ' ', ability_info.strip()) if ability_info else None
        ability_effect = response.xpath('.//p[@class="card-text-ability-effect"]//text()').get()
        card_item['ability_effect'] = re.sub(r'\s+', ' ', ability_effect.strip()) if ability_effect else None

        # 提取攻击描述
        attacks = []
        for attack in response.xpath('.//div[@class="card-text-attack"]'):
            attack_energy = attack.xpath('.//p[@class="card-text-attack-info"]/span/text()').get()
            attack_name_damage = ''.join(attack.xpath('.//p[@class="card-text-attack-info"]//text()[2]').getall()).strip()
            attack_effect_tmp = attack.xpath('.//p[@class="card-text-attack-effect"]//text()').getall()
            # 合并所有字符串，并移除多余的空白字符
            combined_text = ''.join(attack_effect_tmp)
            # 使用正则表达式去除多余的空白字符（包括换行符和多个空格）
            attack_effect = re.sub(r'\s+', ' ', combined_text).strip()


            attack_parts = re.split(r'\s*(?=[0-9]+$)', attack_name_damage)  # 尝试分离名字和伤害值
            attack_name = attack_parts[0].strip()
            attack_damage = re.sub(r'[^0-9]', '', attack_name_damage) if len(attack_parts) > 1 else None

            attacks.append({
                'attack_energy': attack_energy.strip() if attack_energy else None,
                'attack_name': attack_name if attack_name else None,
                'attack_damage': attack_damage if attack_damage else None,
                'attack_effect': attack_effect if attack_effect else None,
            })
        card_item['attacks'] = attacks

        # 提取弱点、抵抗力和撤退费用
        wrr_info = response.xpath('.//p[@class="card-text-wrr"]/text()').getall()
        # 清理每一条wrr信息，并构建字典
        wrr_dict = {}
        for info in wrr_info:
            cleaned_info = re.sub(r'\s+', ' ', info).strip()
            if ':' in cleaned_info:
                parts = cleaned_info.split(':', 1)
                key = parts[0].strip().lower()
                value = parts[1].strip() if len(parts) > 1 else None
                wrr_dict[key] = value

        # 更新 card_item 字段
        card_item['weakness'] = wrr_dict.get('weakness')
        card_item['resistance'] = wrr_dict.get('resistance')
        card_item['retreat_cost'] = wrr_dict.get('retreat')

        # 提取卡片编号
        card_number = response.xpath('.//p[@class="card-text-title"]/span/a/@href').get()
        card_item['card_number'] = card_number[7:] if card_number else None

        # 提取插画师信息
        illustrator = response.xpath('.//div[contains(@class,"card-text-artist")]/a/text()').get()
        card_item['illustrator'] = illustrator.strip() if illustrator else None

        #提取卡牌图片
        card_item['image_url'] =response.xpath('.//div[@class="card-image"]/img/@src').get()

        yield card_item