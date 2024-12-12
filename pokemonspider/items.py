# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PokemonItem(scrapy.Item):
    # define the fields for your item here like:
    number = scrapy.Field()
    name = scrapy.Field()
    slug = scrapy.Field()
    detail_page_url = scrapy.Field()
    thumbnail_alt_text = scrapy.Field()
    thumbnail_image = scrapy.Field()
    type = scrapy.Field()
    abilities = scrapy.Field()
    weakness = scrapy.Field()
    weight = scrapy.Field()
    height = scrapy.Field()
    featured = scrapy.Field()
    collectibles_slug = scrapy.Field()
    id = scrapy.Field()


class PokemonCardItem(scrapy.Item):
    # 定义卡片的基本信息
    name = scrapy.Field()  # 卡片名称
    type = scrapy.Field()  # 卡片类型（如：Basic, Stage 1, Stage 2）
    hp = scrapy.Field()  # 卡片的HP值
    Evolves_link = scrapy.Field()  # 进化自哪张卡片的信息链接
    # 定义能力信息
    ability_info = scrapy.Field()  # 能力名称和能量消耗
    ability_effect = scrapy.Field()  # 能力效果描述
    # 定义攻击信息列表
    attacks = scrapy.Field()  # 攻击信息，每个攻击是一个字典，包含attack_energy, attack_name, attack_damage, attack_effect
    # 定义弱点、抵抗力和撤退费用
    weakness = scrapy.Field()  # 弱点类型及倍率
    resistance = scrapy.Field()  # 抵抗力类型及倍率
    retreat_cost = scrapy.Field()  # 撤退费用
    # 定义卡片编号
    card_number = scrapy.Field()  # 卡片编号
    # 定义插画师信息
    illustrator = scrapy.Field()  # 插画师姓名
    image_url = scrapy.Field() #image图片


class TrainerCardItem(scrapy.Item):
    # 定义卡片的基本信息
    name = scrapy.Field()  # 卡片名称
    type = scrapy.Field()  # 卡片类型（如：Basic, Stage 1, Stage 2）
    # 定义能力信息
    card_ability = scrapy.Field()
    # 定义卡片编号
    card_number = scrapy.Field()  # 卡片编号
    # 定义插画师信息
    illustrator = scrapy.Field()  # 插画师姓名
    image_url = scrapy.Field() #image图片