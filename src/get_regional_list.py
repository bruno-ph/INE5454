import requests
import time
from bs4 import BeautifulSoup
import sys
import json
from pathlib import Path

# Arquivo obtém lista de jogos populares (em ordem) no país em que é executado
# https://store.steampowered.com/search/?sort_by=&sort_order=0&category1=998&filter=topsellers&page=[1-250]
sorted_game_list = []
root_folder = Path(__file__).parents[1]


def get_proxies():
    country_list = open("countries.json", "r")
    list = json.load(country_list)
    for item in list.keys():
        if "proxy" in list[item].keys():
            yield [list[item]["proxy"], list[item]["code"], item]


def get_countries():
    countries = []
    country_list = open("countries.json", "r")
    list = json.load(country_list)
    for item in list.keys():
        countries.append(list[item]["code"])
    return countries


def print_countries():
    c = get_countries()
    for country in c:
        print(country)


def get_regional_list(country_code="br"):
    print(country_code)
    sensitive_file = open("sensitivedata.json", "r")
    sensitive_data = json.load(sensitive_file)
    account_id = sensitive_data["account_id"]
    zone_name = sensitive_data["zone_name"]
    zone_password = sensitive_data["zone_password"]
    # proxy = {"http": proxy, "https": proxy, "socks4": proxy, "socks5": proxy}
    proxies = {
        "http": f"http://brd-customer-{account_id}-zone-{zone_name}-country-{country_code.lower()}:{zone_password}@brd.superproxy.io:33335",
        "https": f"http://brd-customer-{account_id}-zone-{zone_name}-country-{country_code.lower()}:{zone_password}@brd.superproxy.io:33335",
    }

    # URL Para busca de categoria jogos em ordem de popularidade atual separados por páginas
    base_url = "http://store.steampowered.com/search/?sort_by=&sort_order=0&category1=998&filter=topsellers&page="
    for i in range(
        1, 151
    ):  # Iteração pelas páginas da lista de produtos populares (fazer até 251, em média)
        response = requests.get(base_url + str(i), proxies=proxies)
        print(response.status_code)

        while response.status_code != 200:  # Insiste até receber uma resposta válida
            time.sleep(0.1)
            print("eepy\n")
            response = requests.get(base_url + str(i), proxies=proxies)
        soup = BeautifulSoup(response.text, "html.parser")
        product_tags = soup.find_all(
            "a", {"data-ds-appid": True}
        )  # Encontra tags com id de produto (ordenadas por relevância)
        for tag in product_tags:  # Itera pelas tags de cada página
            print("entrou\n")  # terminal
            appid = tag.get("data-ds-appid").rsplit(",")[
                0
            ]  # ID do produto (se for bundle, apenas ID do primeiro, talvez reconsiderar isso)
            gametitle = tag.find(
                "span", class_="title"
            ).text.strip()  # Encontra título (sensível a região)
            sorted_game_list.append(
                {"appid": appid, "title": gametitle}
            )  # Adiciona a lista
            print(str(i) + " " + appid + " : " + gametitle)  # terminal

    print(sorted_game_list)
    return sorted_game_list


def make_regional_lists(country_code="br"):
    get_regional_list(country_code)

    with open(
        str(root_folder) + "/src/regional_lists/list_" + country_code + ".json",
        "w",
        encoding="utf-8",
    ) as json_file:  # dump to json file
        json.dump(sorted_game_list, json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    # country_list = get_countries()
    # print(country_list)
    # for country in country_list:
    #     make_regional_lists(country)
    cc = sys.argv[1]
    make_regional_lists(cc)
