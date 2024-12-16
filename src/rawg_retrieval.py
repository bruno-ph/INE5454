#Doing it again


import re
import requests
import json
from bs4 import BeautifulSoup

def find_game_page(gametitle,gameid):
    pass
    

def get_game_metadata(gameurl="https://rawg.io/games/20xx"):
    genres=[]
    page=requests.get(gameurl)
    soup = BeautifulSoup(page.text, 'html.parser')
    genre_block=soup.findAll('meta',{'itemprop':'genre'})
    #print(genre_block)
    for g in genre_block:
        print (g['content'])
        genres.append(g['content'])
    html_doc=page.text
    gameid=(re.search(r"\\u002Fapp\\u002F(\d+)\\u002F", html_doc))
       # "https:\u002F\u002Fstore.steampowered.com\u002Fapp\u002F1259790\u002
    if gameid:
        print(gameid.group(1))


def main():
    get_game_metadata()

if __name__ == "__main__":
    main()
