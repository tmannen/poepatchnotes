# Crawl all the GGG employee forum posts

from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from scrapy import Item
from scrapy import Field
import hashlib
import os

class GGGEmployeeForumSpider(CrawlSpider):
    name = 'gggemployees'
    allowed_domains = ['pathofexile.com']
    # List from https://github.com/ccbrown/gggtracker/blob/master/server/forum_indexer.go
    employees = [
		"Chris", "Jonathan", "Erik", "Mark_GGG", "Samantha", "Rory", "Rhys", "Qarl", "Andrew_GGG",
		"Damien_GGG", "Joel_GGG", "Ari", "Thomas", "BrianWeissman", "Edwin_GGG", "Support", "Dylan",
		"MaxS", "Ammon_GGG", "Jess_GGG", "Robbie_GGG", "GGG_Neon", "Jason_GGG", "Henry_GGG",
		"Michael_GGG", "Bex_GGG", "Cagan_GGG", "Daniel_GGG", "Kieren_GGG", "Yeran_GGG", "Gary_GGG",
		"Dan_GGG", "Jared_GGG", "Brian_GGG", "RobbieL_GGG", "Arthur_GGG", "NickK_GGG", "Felipe_GGG",
		"Alex_GGG", "Alexcc_GGG", "Andy", "CJ_GGG", "Eben_GGG", "Emma_GGG", "Ethan_GGG",
		"Fitzy_GGG", "Hartlin_GGG", "Jake_GGG", "Lionel_GGG", "Melissa_GGG", "MikeP_GGG", "Novynn",
		"Rachel_GGG", "Rob_GGG", "Roman_GGG", "Sarah_GGG", "SarahB_GGG", "Tom_GGG", "Natalia_GGG",
		"Jeff_GGG", "Lu_GGG", "JuliaS_GGG", "Alexander_GGG", "SamC_GGG", "AndrewE_GGG", "Kyle_GGG",
		"Stacey_GGG", "Jatin_GGG"
    ]

    base = "https://www.pathofexile.com/account/view-posts/{}/"
    employee_pages = [base.format(employee) for employee in employees]

    rules = (
        Rule(LinkExtractor(allow=[r'page/\d+']), follow=True, callback='parse_url'),
    )

    def parse_url(self, response):
        filename = response.url.split("/")[-1]
        dirname = "employee_posts"
        os.makedirs(dirname)    
        html = open(os.path.join(dirname, filename), "w")
        html.write(response.text)
        html.close()