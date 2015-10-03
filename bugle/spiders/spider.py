import urlparse

from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spider import Spider
from bugle.items import NewsItem


class NewsSpider(Spider):
    
    """ """
    def __init__(self, source, *args, **kwargs):  
        self.name = "news_spider"
        self.allowed_domains =  (str(source['ALLOWED_DOMAINS']).split())
        self.start_urls = (str(source['URL']).split())
        self.source = source
        
        super(TestSpider, self).__init__(source, *args, **kwargs)
          
    
    def parse(self, response):
        sel = Selector(response)

        total_items = sel.xpath(str(self.source['SECTION_XPATH'])) # xpath to the section
        items = []
        date = ''
        for news in total_items:
            news_item = news.xpath(str(self.source['LINK_XPATH'])).extract() # xpath to the link
            if isinstance(news_item, list):
                news_item = ''.join(news_item)

            if str(self.source['DATE_XPATH']) == 'MP':
                date = news.xpath(str(self.source['DATE_XPATH'])).extract() # xpath to the date, if date on main page
                if isinstance(date, list):
                    date = ''.join(date)
            result = news_item, date
            items.append(result)

        for link in items:
            item = NewsItem()

            if isinstance(link, tuple):
                item['url'] = urlparse.urljoin(response.url, link[0])
                item['raw_date'] = link[1]
                link = link[0]
            else:
                item['url'] = urlparse.urljoin(response.url, link)

            yield Request(urlparse.urljoin(response.url, link),
                          meta={'item': item}, callback=self.parse_data)

    def parse_data(self, response):
        sel = Selector(response)
        item = response.request.meta['item']

        title = sel.xpath(str(self.source['TITLE_XPATH'])).extract() # xpath to the title
        description = sel.xpath(str(self.source['DESCRIPTION_XPATH'])).extract() # xpath to the description

        if str(self.source['DATE_LOCATION']) == 'RP':
            date = sel.xpath(str(self.source['DATE_XPATH'])).extract() # xpath to the date if on release page
            if isinstance(date, list):
                date = ''.join(date)
            item['raw_date'] = date
        elif str(self.source['DATE_LOCATION']) == 'NA':
            item['raw_date'] = "Date of press release not available"

        if isinstance(description, list):
            description = ' '.join(description)

        if isinstance(title, list):
            title = ' '.join(title)

        item['raw_title'] = title
        item['raw_description'] = description

        yield item
