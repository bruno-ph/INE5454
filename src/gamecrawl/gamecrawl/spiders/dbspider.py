import json
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
from pathlib import Path
import os


def searchform(somestr):
    try:
        tmp = re.sub(r"[`']", "", somestr)
        tmp = re.sub(r"[^\w\s-]", "", tmp)  # Remove symbols (like ®, ™, ©) and emojis
        tmp = re.sub(r"[./]", "", tmp)  # Remove periods and slashes
    except TypeError:
        print(somestr)
        return
    separated = re.split(r"[-:,\s]+", tmp)
    newstr = "-".join(separated)
    return newstr.lower()


# open a json file
root_folder = Path(__file__).parents[4]
with open(
    os.path.join(str(root_folder), "intermediate_data", "list_total.json")
) as jsonFile:
    gamefile = json.load(jsonFile)
    gameids = gamefile.keys()
    gamenames = [gamefile[key]["title"] for key in gamefile.keys()]
    angamenames = {searchform(gn): gn for gn in gamenames}
    searchgames = {
        searchform(gamefile[identifier]["title"]): identifier for identifier in gameids
    }


class DBSpider(CrawlSpider):
    name = "dbspider"
    start_urls = [
        "https://rawg.io/",
    ]
    for gn in gamenames:
        start_urls.append("https://rawg.io/games/" + searchform(gn))
    allowed_domains = ["rawg.io"]
    rules = (
        Rule(
            LinkExtractor(allow=(r"rawg.io/games/[^/]+/?$")),
            callback="parse_rawg",
            follow=True,
        ),
        Rule(LinkExtractor(allow=(r"/games/")), callback=None, follow=True),
    )
    custom_settings = {"DEPTH_LIMIT": 2}

    def parse_rawg(self, response):
        html_doc = response.text
        gameid = re.search(r"\\u002Fapp\\u002F(\d+)\\u002F", html_doc)
        gamename = response.xpath(
            '//h1[@class="heading heading_1 game__title"]/text()'
        ).get()

        if gameid:
            appid = gameid.group(1)
            if appid not in gameids:
                return
            gamename = gamefile[appid]["title"]
        elif searchform(gamename) in angamenames.keys():
            appid = searchgames[searchform(gamename)]
        else:
            return
        genre_block = response.xpath('//meta[@itemprop="genre"]')
        genres = []
        for g in genre_block:
            genre = g.xpath("@content").get()
            genres.append(genre)
        yield {appid: {"title": gamename, "genres": genres, "url": response.url}}
