# -*- coding: utf-8 -*-

import scrapy


class LianJiaWangItem(scrapy.Item):
    # 存入MongoDB所用字段
    _id = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # URL
    url = scrapy.Field()
    # 总价
    total_price = scrapy.Field()
    # 单价
    unit_price = scrapy.Field()
    # 房屋户型
    house_type = scrapy.Field()
    # 所在楼层
    floor = scrapy.Field()
    # 建筑面积
    house_size = scrapy.Field()
    # 户型结构
    house_struct = scrapy.Field()
    # 套内面积
    area_in = scrapy.Field()
    # 建筑类型
    build_type = scrapy.Field()
    # 房屋朝向
    house_direction = scrapy.Field()
    # 建筑结构
    build_struct = scrapy.Field()
    # 装修情况
    fit_up = scrapy.Field()
    # 梯户比例
    ladder_ratio = scrapy.Field()
    # 配备电梯
    lift = scrapy.Field()
    # 产权年限
    property_right_time = scrapy.Field()
    # 挂牌时间
    listing_time = scrapy.Field()
    # 交易权属
    transaction_belong = scrapy.Field()
    # 上次交易
    previous_transaction = scrapy.Field()
    # 房屋用途
    house_purpose = scrapy.Field()
    # 房屋年限
    house_years = scrapy.Field()
    # 产权所属
    property_right_belong = scrapy.Field()
    # 抵押信息
    mortgage = scrapy.Field()
    # 房本备件
    house_backup = scrapy.Field()
