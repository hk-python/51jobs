# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class QcwyItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_url=Field()
    title=Field()#标题
    com_name=Field()#公司名称
    salary=Field()#资薪
    city=Field()#城市
    exp=Field()#经验
    edu=Field()#学历
    num=Field()#人数
    time=Field()#发布时间
    major=Field()#专业
    fuli=Field()#福利
    job_msg=Field()#职位信息
    job_tel=Field()#联系方式
    comp_msg=Field()#公司介绍
    com_msg=Field()#公司信息


