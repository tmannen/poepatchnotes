# Crawl all the forum pages on poe patch notes
# TODO: need to login
# also write some ohjeita etta miten alotetaan skrapeus ja debug scraping jne linkextrator jne.

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from scrapy import Item
from scrapy import Field
import hashlib

class POEPatchForumSpider(CrawlSpider):
    name = 'poepatchnotes'
    allowed_domains = ['pathofexile.com']
    start_urls = ['https://www.pathofexile.com/forum/view-forum/patch-notes/page/' + str(i) for i in range(1, 5)]

    rules = (
        Rule(LinkExtractor(restrict_xpaths=["//div[@class='title']/a"]), follow=True, callback='parse_url'),
    )

    def parse_url(self, response):
        filename = response.url.split("/")[-1]
        html = open("patchnotes/" + filename, "w")
        html.write(response.text)
        html.close()