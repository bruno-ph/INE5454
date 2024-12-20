import requests
from bs4 import BeautifulSoup
import os
import json
from pathlib import Path


# Obtem a lista de idiomas para os jogos em list_total.json
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
            # print(collumns[1].text)
            if collumns[1].text.strip() == "✔":
                languages.append(language_name.strip())
    return languages


def get_languages():
    return_dict = {}
    root_folder = Path(__file__).parents[1]
    games_file = open(
        os.path.join(root_folder, "intermediate_data", "list_total.json"), "r"
    )
    games_dict = json.load(games_file)
    for appid in list(games_dict.keys())[:10]:
        try:
            print(len(return_dict), "-", (appid))
            gameurl = "https://store.steampowered.com/app/" + appid
            page = requests.get(gameurl)
            game_langs = read_lang_table(page)
            return_dict[appid] = {"languages": game_langs, "url": gameurl}

        except:
            print("Error on " + appid)
    with open(
        os.path.join(root_folder, "intermediate_data", "list_languages.json"), "w"
    ) as returnfile:
        json.dump(return_dict, returnfile, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    get_languages()
