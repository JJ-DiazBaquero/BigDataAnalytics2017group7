from spider import MySpider

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging


def correrCrawler():
    print "entraaaaaa"
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    runner = CrawlerRunner()

    d = runner.crawl(MySpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()