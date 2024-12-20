from copy import deepcopy
import json
from pathlib import Path
import requests
import os

root_folder = Path(__file__).parents[1]


# Obtem os preços dos jogos em múltiplas regiões e moedas com base em uma API


# Primeiramente, obtem-se os IDs de jogos nessa API, que são diferentes dos coletadas para a Steam
def get_uuids():
    sensitive_file = open(os.path.join("initial_data", "sensitivedata.json"), "r")
    sensitive_data = json.load(sensitive_file)
    game_file = open(
        os.path.join(str(root_folder), "intermediate_data", "list_total.json"), "r"
    )
    game_list = json.load(game_file)
    game_list = list(game_list)
    game_uuids = {}
    progress = 0
    for steam_id in game_list:
        game_info = requests.get(
            url="https://api.isthereanydeal.com/games/lookup/v1",
            params={
                "key": sensitive_data[
                    "api_key"
                ],  # Key para acessar API pode ser obtida em https://isthereanydeal.com/apps/my/
                "appid": steam_id,
            },
        )
        if not game_info.content or game_info.status_code != 200:
            continue
        game_info_json = json.loads(game_info.content.decode("utf-8"))
        game_uuids[steam_id] = game_info_json["game"]["id"]

        new_progress = (len(game_uuids) * 100) / len(game_list)
        if new_progress > progress:
            progress = new_progress
            print(
                "Progress: {:.2f}% --- {}/{}".format(
                    progress, len(game_uuids), len(game_list)
                )
            )

    return game_uuids


def get_prices(game_uuids, country):
    country_prices_dict = {}
    game_uuids_copy = deepcopy(game_uuids)
    while len(game_uuids_copy) > 0:
        if len(game_uuids_copy) >= 200:
            game_uuids_pack = game_uuids_copy[0:200]
            del game_uuids_copy[0:200]
        else:
            game_uuids_pack = game_uuids_copy[0 : len(game_uuids_copy)]
            del game_uuids_copy[0 : len(game_uuids_copy)]
        game_prices = requests.post(
            url="https://api.isthereanydeal.com/games/prices/v3",
            params={
                "key": "f5650820ffe914c3c5f60ee8685535416278ff23",
                "country": country,
                "shops": [61],
            },
            json=game_uuids_pack,
        )
        if game_prices.status_code != 200:
            return None
        game_prices_dict = json.loads(game_prices.content.decode("UTF-8"))
        for game in game_prices_dict:
            for deal in game["deals"]:
                if deal["shop"]["name"] == "Steam":
                    country_prices_dict[game["id"]] = deal["regular"]["amount"]
    return country_prices_dict


def create_game_references(game_references):
    with open(
        os.path.join(str(root_folder), "intermediate_data", "game_references.json"),
        "w",
        encoding="utf-8",
    ) as json_file:  # dump to json file
        json.dump(game_references, json_file, ensure_ascii=False, indent=4)


def create_prices_dict(country_prices_dict, currency):
    with open(
        os.path.join(
            str(root_folder),
            "intermediate_data",
            "prices_per_currency",
            "prices_" + currency + ".json",
        ),
        "w",
        encoding="utf-8",
    ) as json_file:  # dump to json file
        json.dump(country_prices_dict, json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    game_references = get_uuids()
    create_game_references(game_references)
    game_uuids = list(game_references.values())
    workable_countries = open(
        os.path.join(str(root_folder), "intermediate_data", "workable_countries.txt"),
        "r",
    )
    currencies = open(
        os.path.join(str(root_folder), "initial_data", "currencies.json"), "r"
    )
    currencies_dict = json.load(currencies)
    for country in workable_countries:
        country = country.strip("\n")
        currency = currencies_dict[country]["currency"]
        country_prices_dict = get_prices(game_uuids, country)
        if country_prices_dict == None:
            continue
        create_prices_dict(country_prices_dict, currency)
