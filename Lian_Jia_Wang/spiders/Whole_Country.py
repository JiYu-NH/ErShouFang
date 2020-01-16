# -*- coding: utf-8 -*-
import re
import scrapy
from ..items import LianJiaWangItem
from ..citys import Citys
from scrapy_redis.spiders import RedisSpider


class WholeCountrySpider(RedisSpider):
    name = 'Whole_Country'
    redis_key = 'Whole_Country:start_urls'

    def parse(self, response):
        # 全国省市
        citys = Citys.citys
        city_url = 'https://{}.lianjia.com/ershoufang/co32/'
        for city in citys.values():
            yield scrapy.Request(url=city_url.format(city), callback=self.region_url_parse, dont_filter=True)

    # 省市中的各区域
    def region_url_parse(self, response):
        # 省市URL
        city_url = response.url.split('/ershoufang')[0]
        # 区域URL
        region_urls = response.css('[data-role="ershoufang"]').xpath('./div/a/@href').extract()
        # 区域名
        region_names = response.css('[data-role="ershoufang"]').xpath('./div/a/text()').extract()

        for url_temp, name in zip(region_urls, region_names):
            # 区域URL = 省市URl + 后缀
            region_url = city_url + url_temp

            print(name, region_url)
            # 对区域发起请求
            yield scrapy.Request(region_url, callback=self.house_url_parse, dont_filter=True)
            # 测试的时候、请求一次便退出、用一个区域实验即可
            break

    # 区域中二手房的URL
    def house_url_parse(self, response):
        # 二手房的URL
        house_urls = response.xpath('//div[@class="info clear"]/div[1]/a/@href').extract()
        # 访问二手房详情页（只有这里的URL去重了）
        for house_url in house_urls:
            yield scrapy.Request(house_url, callback=self.house_detail_page)

        # 本页有30条才请求下一页
        if len(house_urls) == 30:
            page = re.findall(r'ershoufang/.*?/.*?(\d*)co32/', response.url)[0]
            # 第一页链接中不包含 pg1
            if page:
                # 为100页时，退出
                if int(page) == 100: return
                # 下一页
                next_page = re.sub(r'pg(\d*)', 'pg%d' % (int(page) + 1), response.url)
            else:
                # 第二页
                next_page = re.sub(r'co32', 'pg2co32', response.url)

            # 访问下一页
            yield scrapy.Request(next_page, callback=self.house_url_parse, dont_filter=True)

    # 二手房详情页
    def house_detail_page(self, response):
        # 标题
        title = response.xpath('//div[@class="content"]/div[1]/h1/text()').extract_first()
        # URL
        url = response.url
        # 总价
        total_price = response.xpath('//div[contains(@class,"price")]/span/text()').get() + '万'
        # 单价
        unit_price = response.xpath('//span[@class="unitPriceValue"]/text()').get() + '元/平米'
        # 房屋户型
        house_type = response.xpath('//div[@class="content"]/ul/li[1]/text()').get()
        # 所在楼层
        floor = response.xpath('//div[@class="content"]/ul/li[2]/text()').get()
        # 建筑面积
        house_size = response.xpath('//div[@class="content"]/ul/li[3]/text()').get()
        # 户型结构
        house_struct = response.xpath('//div[@class="content"]/ul/li[4]/text()').get()
        # 套内面积
        area_in = response.xpath('//div[@class="content"]/ul/li[5]/text()').get()
        # 建筑类型
        build_type = response.xpath('//div[@class="content"]/ul/li[6]/text()').get()
        # 房屋朝向
        house_direction = response.xpath('//div[@class="content"]/ul/li[7]/text()').get()
        # 建筑结构
        build_struct = response.xpath('//div[@class="content"]/ul/li[8]/text()').get()
        # 装修情况
        fit_up = response.xpath('//div[@class="content"]/ul/li[9]/text()').get()
        # 梯户比例
        ladder_ratio = response.xpath('//div[@class="content"]/ul/li[10]/text()').get()
        # 配备电梯
        lift = response.xpath('//div[@class="content"]/ul/li[11]/text()').get()
        # 产权年限
        property_right_time = response.xpath('//div[@class="content"]/ul/li[12]/text()').get()
        # 挂牌时间
        listing_time = response.xpath('//div[@class="transaction"]/div[2]/ul/li[1]/span[2]/text()').get()
        # 交易权属
        transaction_belong = response.xpath('//div[@class="transaction"]/div[2]/ul/li[2]/span[2]/text()').get()
        # 上次交易
        previous_transaction = response.xpath('//div[@class="transaction"]/div[2]/ul/li[3]/span[2]/text()').get()
        # 房屋用途
        house_purpose = response.xpath('//div[@class="transaction"]/div[2]/ul/li[4]/span[2]/text()').get()
        # 房屋年限
        house_years = response.xpath('//div[@class="transaction"]/div[2]/ul/li[5]/span[2]/text()').get()
        # 产权所属
        property_right_belong = response.xpath('//div[@class="transaction"]/div[2]/ul/li[6]/span[2]/text()').get()
        # 抵押信息
        mortgage = response.xpath('//div[@class="transaction"]/div[2]/ul/li[7]/span[2]/text()').get().strip()
        # 房本备件
        house_backup = response.xpath('//div[@class="transaction"]/div[2]/ul/li[8]/span[2]/text()').get()

        items = LianJiaWangItem()
        items['title'] = title
        items['url'] = url
        items['total_price'] = total_price
        items['unit_price'] = unit_price
        items['house_type'] = house_type
        items['floor'] = floor
        items['house_size'] = house_size
        items['house_struct'] = house_struct
        items['area_in'] = area_in
        items['build_type'] = build_type
        items['house_direction'] = house_direction
        items['build_struct'] = build_struct
        items['fit_up'] = fit_up
        items['ladder_ratio'] = ladder_ratio
        items['lift'] = lift
        items['property_right_time'] = property_right_time
        items['listing_time'] = listing_time
        items['transaction_belong'] = transaction_belong
        items['previous_transaction'] = previous_transaction
        items['house_purpose'] = house_purpose
        items['house_years'] = house_years
        items['property_right_belong'] = property_right_belong
        items['mortgage'] = mortgage
        items['house_backup'] = house_backup
        yield items
