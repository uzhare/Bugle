# Scrapy settings for bugle project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'bugle'

SPIDER_MODULES = ['bugle.spiders']
NEWSPIDER_MODULE = 'bugle.spiders'

ITEM_PIPELINES = {
    'bugle.pipelines.JsonNewsPipeline': 300,
}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'testcrawler (+http://www.yourdomain.com)'
