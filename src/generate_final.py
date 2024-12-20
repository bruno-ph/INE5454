import json
from pathlib import Path
import os

genres = {}
root_folder = Path(__file__).parents[1]

# Gera o dataset completo com base em todos os dados intermediários

with open(
    os.path.join(root_folder, "intermediate_data", "list_languages.json"), "r"
) as f:
    langs = json.load(f)
with open(os.path.join(root_folder, "src", "gamecrawl", "output.json"), "r") as f:
    genresfile = json.load(f)

    for g in genresfile:

        gkey = list(g.keys())[0]
        content = g[gkey]
        genres[gkey] = {
            "genres": content["genres"],
            "url": content["url"],
        }
with open(
    os.path.join(root_folder, "intermediate_data", "game_references.json"), "r"
) as f:
    game_references = json.load(f)

with open(os.path.join(root_folder, "initial_data", "currencies.json"), "r") as f:
    currencies = json.load(f)
f = open(os.path.join(root_folder, "intermediate_data", "list_total.json"), "r")
data = json.load(f)

for key in data.keys():
    if key in genres.keys() and key in langs.keys():
        data[key]["languages"] = langs[key]["languages"]
        data[key]["genres"] = genres[key]["genres"]
        data[key]["url"] = [langs[key]["url"], genres[key]["url"]]
    elif key in genres.keys():
        data[key]["genres"] = genres[key]["genres"]
        data[key]["url"] = [genres[key]["url"]]
    elif key in langs.keys():
        data[key]["languages"] = langs[key]["languages"]
        data[key]["url"] = [langs[key]["url"]]
    data[key]["prices"] = {}
workable_countries = open(
    os.path.join(str(root_folder), "intermediate_data", "workable_countries.txt"), "r"
)
for country in workable_countries:
    with open(
        os.path.join(
            root_folder,
            "intermediate_data",
            "prices_per_currency",
            f"prices_{currencies[country.strip()]['currency']}.json",
        )
    ) as curr_f:
        curr_data = json.load(curr_f)
        for key in data.keys():
            if (
                key in game_references.keys()
                and game_references[key] in curr_data.keys()
            ):
                data[key]["prices"][
                    "price_" + currencies[country.strip()]["currency"]
                ] = curr_data[game_references[key]]


with open(os.path.join(root_folder, "dataset.json"), "w") as f:
    print("Writing\n")
    json.dump(data, f, indent=4, ensure_ascii=False)
