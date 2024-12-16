import sys
from pathlib import Path
import json
import os


max_per_country=10000000 #incerto se vai precisar ou não disso

def main():

    root_folder = Path(__file__).parents[1]
    print(root_folder)

    #total_file=open(str(root_folder)+ "/src/regional_lists/regional_lists/list_total.json","w",encoding="utf-8")
    #total_file=open(str(root_folder)+ "\src\regional_lists\regional_lists\list_total.json","w",encoding="utf-8")
    total_file=open(os.path.join(root_folder,"src","list_total.json"),"w",encoding="utf-8")
    country_list =list(( open(os.path.join(root_folder,"workable_countries.txt"), "r")).readlines())
    total_games={}
    
    for country in country_list:
        game_counter=1
        print(country)
        #regional_file=open(str(root_folder)+ "\src\regional_lists\regional_lists\list_"+country+".json","r")
        #regional_file=open(str(root_folder)+ "/src/regional_lists/regional_lists/list_"+country+".json","r")
        regional_file=open(os.path.join(root_folder,"src","regional_lists",f"list_{country.strip()}.json"),"r",encoding="utf-8")
        regional_data=json.load(regional_file)
        for game_app in regional_data:
            if game_counter>max_per_country:
                break
            game_appid=game_app["appid"]
            gametitle=game_app["title"]
            if game_appid not in total_games.keys():
                total_games[str(game_appid)]={"title":gametitle}
                total_games[str(game_appid)]["ranks"]={"rank_"+country.strip():game_counter}
            else:
                total_games[str(game_appid)]["ranks"]["rank_"+country.strip()]=game_counter
            game_counter+=1
    for appid in total_games:
        print(total_games[appid])
        for country in country_list:
            if "rank_"+country.strip() not in total_games[appid]['ranks']:
                total_games[appid]["ranks"]["rank_"+country.strip()] = -1

    json.dump(total_games, total_file, ensure_ascii=False, indent=4)
    


if __name__ == "__main__":
    main()