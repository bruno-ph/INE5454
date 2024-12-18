import json
from pathlib import Path
import time
from bs4 import BeautifulSoup
import requests


root_folder = Path(__file__).parents[1]

def get_uuids():
    game_file = open(str(root_folder) + "/src/list_total.json", 'r')
    game_list = json.load(game_file)
    game_list = list(game_list)
    game_uuids = {}
    for steam_id in game_list:
        game_info = requests.get(
            url="https://api.isthereanydeal.com/games/lookup/v1",
            params={
                "key":"f5650820ffe914c3c5f60ee8685535416278ff23",
                "appid":steam_id
                }
            )
        game_info_json = json.loads(game_info.content.decode("utf-8"))
        game_uuids[steam_id] = game_info_json["game"]["id"]

        print(len(game_uuids))
        # Break provisorio
        if len(game_uuids) >= 50:
            break
    return game_uuids

def get_prices(game_uuids, country):
    game_prices = requests.post(
        url="https://api.isthereanydeal.com/games/prices/v3",
        params={
            "key":"f5650820ffe914c3c5f60ee8685535416278ff23",
            "country":country,
            "shops":61,
        },
        json=game_uuids
    )
    print(game_prices)


if __name__ == "__main__":
    game_uuids = json.dumps(list(get_uuids().values()))
    get_prices(game_uuids, "BR")