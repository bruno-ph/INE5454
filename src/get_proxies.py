import get_regional_list
import json
import requests
import os


# Gera uma lista de países que podem ser usados no trabalho (tem proxies no serviço utilizado)
sensitive_file = open(os.path.join("initial_data", "sensitivedata.json"), "r")
sensitive_data = json.load(sensitive_file)
account_id = sensitive_data["account_id"]
zone_name = sensitive_data["zone_name"]
zone_password = sensitive_data["zone_password"]
file = open(os.path.join("intermediate_data", "workable_countries.txt"), "w")

countries = get_regional_list.get_countries()
for country in countries:
    proxies = {
        "http": f"http://brd-customer-{account_id}-zone-{zone_name}-country-{country.lower()}:{zone_password}@brd.superproxy.io:33335",
        "https": f"http://brd-customer-{account_id}-zone-{zone_name}-country-{country.lower()}:{zone_password}@brd.superproxy.io:33335",
    }
    html = requests.get(
        "http://store.steampowered.com/search/?sort_by=&sort_order=0&category1=998&filter=topsellers&page=1",
        proxies=proxies,
    )

    if html.status_code == 200:
        file.write(country + "\n")
        print(country)

file.close()
