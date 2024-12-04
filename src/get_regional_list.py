import requests
import time
from bs4 import BeautifulSoup
import re
import json
from pathlib import Path
#Arquivo obtém lista de jogos populares (em ordem) no país em que é executado
#https://store.steampowered.com/search/?sort_by=&sort_order=0&category1=998&filter=topsellers&page=[1-250]
sorted_game_list=[]
root_folder = Path(__file__).parents[1]
def get_regional_list():
    base_url="https://store.steampowered.com/search/?sort_by=&sort_order=0&category1=998&filter=topsellers&page="
    for i in range(1,251): #Iteração pelas páginas da lista de produtos populares (fazer até 251, em média)
        response=requests.get(base_url+str(i))
        while response.status_code!=200: #Insiste até receber uma resposta válida
            time.sleep(3)
            response=requests.get(base_url+str(i))
        soup = BeautifulSoup(response.text, 'html.parser')
        product_tags = soup.find_all('a', {'data-ds-appid':True}) #Encontra tags com id de produto (ordenadas por relevância)
        for tag in product_tags: #Itera pelas tags de cada página
                print('entrou\n') #terminal
                appid=tag.get('data-ds-appid').rsplit(',')[0] #ID do produto (se for bundle, apenas ID do primeiro, talvez reconsiderar isso)
                gametitle = tag.find('span', class_='title').text.strip() #Encontra título (sensível a região)
                sorted_game_list.append({"appid": appid, "title": gametitle}) #Adiciona a lista
                print(str(i) + " " + appid + " : " + gametitle) #terminal
            
    print(sorted_game_list)
def main():
    get_regional_list()

    with open(str(root_folder)+"/src/regional_lists/list_br.json", "w", encoding="utf-8") as json_file: #dump to json file
        json.dump(sorted_game_list, json_file, ensure_ascii=False, indent=4)

if __name__=="__main__":
    main()