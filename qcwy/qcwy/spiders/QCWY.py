# -*- coding: utf-8 -*-
from scrapy import Spider,Request
from ..items import QcwyItem

class QcwySpider(Spider):
    name = 'QCWY'
    allowed_domains = ['www.51job.com']
    start_urls = 'https://www.51job.com/'

    def start_requests(self):
        url=self.start_urls
        yield Request(url=url,callback=self.parse, dont_filter=True)

    def parse(self, response):
        # print(response.text)
        next_page=response.xpath('//*[@id="rtNext"]/@href')[0].extract()#获取下一页url
        print('下一页链接：',next_page)
        if next_page:#翻页
            for div in response.xpath("//div[@class='el']//p//a"):#获取要爬的二级页面的url
                job_url=div.xpath(".//@href")[0].extract()
                print(job_url)
                yield Request(url=job_url,callback=self.parse_xinxi, dont_filter=True)#用二级页面url回调parse_xinxi函数获取招聘信息
            yield Request(url=next_page,callback=self.parse,dont_filter=True)#翻页

    def parse_xinxi(self,response):
        print('++++++++++++++++++++++++++++++++')
        # print(response.text)
        item = QcwyItem()
        # 爬取招聘信息标题
        item['title']=''.join(response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/h1/@title').extract()).strip()
        #爬取招聘信息公司名称
        item['com_name']=''.join(response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[1]/a[1]/text()').extract()).strip('\n\t\t\t\t\t').strip('\xa0').strip('\t\t\t\t\t\n')
        #爬取招聘信息资薪
        item['salary']=''.join(response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/strong/text()').extract()).strip()
        #爬取招聘信息工作城市
        item['city']=''.join(response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/text()[1]').extract()).strip('\n\t\t\t\t').strip('\xa0')
        #爬取招聘信息所需工作经验
        item['exp']=''.join(response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/text()[2]').extract()).strip('\xa0')
        #爬取招聘信息学历
        item['edu']=''.join(response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/text()[3]').extract()).strip('\xa0')
        #爬取招聘信息人数
        item['num']=''.join(response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/text()[4]').extract()).strip('\xa0').strip('\t')
        #爬取招聘信息发布时间
        item['time']=''.join(response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/text()[5]').extract()).strip('\xa0').strip('\t')
        # item['major']=response.xpath('').extract()
        #爬取招聘信息五金一险等福利
        item['fuli']={'fuli1':''.join(response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/div/div/span[1]/text()').extract()).strip(),
                       'fuli2': ''.join(response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/div/div/span[2]/text()').extract()).strip(),
                       'fuli3': ''.join(response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/div/div/span[3]/text()').extract()).strip(),
                       'fuli4': ''.join(response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/div/div/span[4]/text()').extract()).strip(),
                       'fuli5': ''.join(response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/div/div/span[5]/text()').extract()).strip(),
                       'fuli6': ''.join(response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/div/div/span[6]/text()').extract()).strip(),
                       'fuli7': ''.join(response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/div/div/span[7]/text()').extract()).strip(),
                       'fuli8': ''.join(response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/div/div/span[8]/text()').extract()).strip(),
                       'fuli9': ''.join(response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/div/div/span[9]/text()').extract()).strip(),
                       'fuli10': ''.join(response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/div/div/span[10]/text()').extract()).strip()
                      }
        #爬取招聘信息工作信息
        item['job_msg']=''.join(response.xpath('/html/body/div[3]/div[2]/div[3]/div[1]/div/p/text()').extract()).strip('\xa0').replace('\xa0','')\
                        +''.join(response.xpath('/html/body/div[3]/div[2]/div[3]/div[1]/div/p/b/text()').extract()).strip('\xa0').replace('\xa0','')
        #爬取招聘信息工作地址
        item['job_tel']='上班地址：'.join(response.xpath('/html/body/div[3]/div[2]/div[3]/div[2]/div/p/text()').extract()).strip()
        #爬取招聘信息公司介绍
        item['comp_msg']=''.join(response.xpath('/html/body/div[3]/div[2]/div[3]/div[3]/div/text()').extract()).strip().replace('\xa0','')
        #爬取招聘信息公司种类
        item['com_msg']={'com-type':''.join(response.xpath('/html/body/div[3]/div[2]/div[4]/div[1]/div[2]/p[1]/text()').extract()).strip(),
                          'com-peo':''.join(response.xpath('/html/body/div[3]/div[2]/div[4]/div[1]/div[2]/p[2]/text()').extract()).strip(),
                          'com-nat':''.join(response.xpath('/html/body/div[3]/div[2]/div[4]/div[1]/div[2]/p[3]/@title').extract()).strip()
                         }
        print(item)
        yield item