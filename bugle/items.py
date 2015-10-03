# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class NewsItem(Item):
    raw_date = Field()
    url = Field()
    raw_title = Field()
    raw_description = Field()
