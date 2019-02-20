# 调试方法二

from scrapy import cmdline


name = 'airasia'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())