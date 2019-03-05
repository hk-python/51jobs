# from scrapy.cmdline import execute
# import sys
# import os
#
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(["scrapy","crawl","QCWY"])

from scrapy import cmdline

cmdline.execute("scrapy crawl QCWY".split())


#鼠标右击run即可运行爬虫项目

