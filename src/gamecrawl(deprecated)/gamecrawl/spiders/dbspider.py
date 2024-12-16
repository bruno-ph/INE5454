from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
class CrawlingSpider(CrawlSpider):
    name="dpspider"
    allowed_domains = ["rawg.io"]

    def __init__(self,*args, **kwargs):
        for i in range(0,6300,197):
            super(CrawlingSpider, self).__init__(*args, **kwargs)

    rules = (
        Rule(LinkExtractor(allow=r"/games/(.+)/",restrict_css='#search_result_container'),callback="parse_item", follow=True),
        
        Rule(LinkExtractor(allow='page=(d+)',restrict_css='.search_pagination_right'))      #allows for multiple pages of lookup
)
        #Rule(LinkExtractor(allow=r"/search/"), callback="parse_item", follow=True)
    