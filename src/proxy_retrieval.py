import requests
from bs4 import BeautifulSoup
import tabulate
import json
import time


def proxy_retrieval(delay=10):
    count = 0
    # open json file
    country_list = open("countries.json", "r")
    list = json.load(country_list)
    workable_country_codes = []
    workable_countries_file = open("workable_countries.txt", "w")
    for item in list.keys():
        country_code = list[item]["code"].lower().strip()
        print(country_code)
        html = requests.get(
            "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&country="
            + country_code
            + "&proxy_format=protocolipport&format=text&timeout=20000"
        )
        print(html.text)
        if len(html.text) > 0 and html.status_code == 200:
            workable_country_codes.append(country_code)
            count += 1
            list[item]["proxy"] = (html.text).split()[-1]
        else:
            print("No proxies found\n")
        time.sleep(delay)
    for code in workable_country_codes:
        workable_countries_file.write(code + "\n")
    with open("countries.json", "w") as returnfile:
        json.dump(list, returnfile, indent=4, ensure_ascii=False)

    print(workable_country_codes)
    print(count)


if __name__ == "__main__":
    proxy_retrieval(delay=0.5)
