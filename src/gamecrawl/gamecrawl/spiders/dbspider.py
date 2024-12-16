import csv
import scrapy
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
import re

class DBSpider(scrapy.Spider):
    name = 'dpspider'

    def start_requests(self):
        url="https://rawg.io/games/wild-animal-racing"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        html_doc=response.text
        gameid=(re.search(r"\\u002Fapp\\u002F(\d+)\\u002F", html_doc))
        if gameid:
            appid= gameid.group(1)
        else:
            raise Exception
        genre_block=response.xpath('//meta[@itemprop="genre"]')
        for g in genre_block:
            genre=g.xpath('@content').get()
            yield{appid:genre}

def dbspider_run():
    game_tag_results = []

    def crawler_results(item):
        print(item)
        game_tag_results.append(item)
    for tag in game_tag_results:
        print(tag)

    dispatcher.connect(crawler_results, signal=signals.item_scraped)
    crawler_process = CrawlerProcess()
    crawler_process.crawl(DBSpider)
    crawler_process.start()
    return game_tag_results


if __name__ == '__main__':
    tags=dbspider_run()

    keys = tags[0].keys()
    with open('books_data.csv', 'w', newline='') as output_file_name:
        writer = csv.DictWriter(output_file_name, keys)
        writer.writerows(tags)

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

#/class CrawlingSpider(CrawlSpider):
    #name="dpspider"
    #allowed_domains = ["rawg.io"]
    #start_urls=["https://rawg.io/"]

    ##rules = (
   #     Rule(LinkExtractor(allow=r"/games/(.+)/",restrict_css='#search_result_container'),callback="parse_item", follow=True),
  #      
 #       Rule(LinkExtractor(allow='page=(d+)',restrict_css='.search_pagination_right'))      #allows for multiple pages of lookup
#)
    
    #def parse(self, response):
     #   print("aaazz")
      #  tags=response.html
       # tags2=response.css
        #print(tags2)
        #print(tags)
        #Rule(LinkExtractor(allow=r"/search/"), callback="parse_item", follow=True)/#
    