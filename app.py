import os
import web
import json

from scrapy import signals
from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

from bugle.spiders.spider import NewsSpider

urls = (
  '/','Spider',
  '/(js|css|images)/(.*)', 'static'
)

app = web.application(urls, globals())

render = web.template.render('templates/')

def call_spider(spider):
    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
    reactor.run()


class Spider(object):
    def GET(self):
        return render.data_form()

    def POST(self):
        form = web.input()
        source_data = dict(form)

        spider = NewsSpider(source=source_data)
        call_spider(spider)
        
        with open('scraped_data_utf8.json', 'r') as f:
            result_data = f.read()
        
        result_data = json.loads(json.dumps(result_data))

        return render.result(data=result_data, source=source_data)


class static:
    def GET(self, media, file):
        try:
            cwd = os.path.dirname(__file__)+'/'
            f = open(cwd+'templates/'+media+'/'+file)
            return f.read()
        except:
            return ''


if __name__ == "__main__":
    app.run()
