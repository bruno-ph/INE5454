from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
#https://store.steampowered.com/search/?category1=998&filter=topsellers&ndl=1
#https://store.steampowered.com/search/?query=&start=0&count=50&category1=998&filter=topsellers&ndl=1
#https://store.steampowered.com/search/?query=&start=5099&count=50&category1=998&filter=globaltopsellers&ndl=1
#https://store.steampowered.com/search/?sort_by=&sort_order=0&category1=998&filter=topsellers&page=[1-250]
class CrawlingSpider(CrawlSpider):
    name="steamcrawler"
    allowed_domains = ["steampowered.com"]

    def __init__(self,*args, **kwargs):
        for i in range(0,6300,197):
            super(CrawlingSpider, self).__init__(*args, **kwargs)
            self.start_urls.append(f"https://store.steampowered.com/search/?query=&start={i}&count=197&category1=998&filter=globaltopsellers&ndl=1")

    rules = (
        Rule(LinkExtractor(allow=r"/app/(.+)/",restrict_css='#search_result_container'),callback="parse_item", follow=True),
        
        Rule(LinkExtractor(allow='page=(d+)',restrict_css='.search_pagination_right'))      #allows for multiple pages of lookup
)
        #Rule(LinkExtractor(allow=r"/search/"), callback="parse_item", follow=True)
    