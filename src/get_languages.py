import requests
import time
from bs4 import BeautifulSoup
import sys
import os
import json
from pathlib import Path


def read_lang_table(page):
    languages = []
    soup = BeautifulSoup(page.text, "html.parser")
    lang_table = soup.find("table", {"class": "game_language_options"})
    for language_block in lang_table.findAll("tr")[1:]:
        if language_block["class"] == "unsupported":
            pass
        else:
            collumns = language_block.findAll("td")
            language_name = collumns[0].text
            print(collumns[1].text)
            if collumns[1].text.strip() == "✔":
                languages.append(language_name.strip())
    return languages


def get_languages():
    root_folder = Path(__file__).parents[0]
    games_file = open(os.path.join(root_folder, "list_total.json"), "r")
    games_dict = json.load(games_file)
    for appid in games_dict.keys():
        gameurl = "https://store.steampowered.com/app/" + appid
        page = requests.get(gameurl)
        game_langs = read_lang_table(page)
        print(appid, games_dict[appid]["title"], game_langs, gameurl)


if __name__ == "__main__":
    get_languages()
