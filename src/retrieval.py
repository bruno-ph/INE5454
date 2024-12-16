def get_igdb_game(game_title):
    print(game_title)
    wrapper = IGDBWrapper(clientid, accesskey)
    byte_array = wrapper.api_request(
                'games',
                f'fields id, genres.name, themes.name, involved_companies.company.country; offset 0; where name="{game_title}";'
            )

    games = json.loads(byte_array)
    return games[0]



languages={"arabic",
"bulgarian",
"schinese",
"tchinese",
"czech",
"danish",
"dutch",
"english",
"finnish",
"french",
"german",
"greek",
"hungarian",
"italian",
"japanese",
"koreana",
"norwegian",
"polish",
"brazilian",
"portuguese",
"romanian",
"russian",
"spanish",
"swedish",
"thai",
"turkish",
"ukrainian",
"vietnamese"}

#def get_game_languages(game_id):


numberofpages=0
game_id_list=[]
while len(game_id_list)<10000:
    page=requests.get("https://steamspy.com/api.php?request=all&page="+str(numberofpages),{"request": "all"}).json()
    #parsed_html = BeautifulSoup(page.content, 'html.parser')
    game_id_list+=page
    numberofpages+=1
#print (game_id_list[9998])

for game in page:
    #TODO: FILTER NON-UTF8 CHARACTERS
    #   Convert to JSON file
    #   Organize files
    gamepage=requests.get("https://steamspy.com/api.php?request=appdetails&appid="+str(game),{"request": "appdetails"}).json()
    print(gamepage.keys())
    print(gamepage["name"],gamepage["appid"],gamepage["languages"],gamepage["price"])
    igdb_game_data=get_igdb_game(gamepage["name"])
    #print (igdb_game_data['genres'],igdb_game_data['themes'],igdb_game_data['involved_companies']['country'])
    if 'genres' in igdb_game_data:
        print([genre['name'] for genre in igdb_game_data['genres']])
    if 'themes' in igdb_game_data:
        print([themes['name'] for themes in igdb_game_data['themes']])
    if 'involved_companies' in igdb_game_data:
        print([involved_companies['company']['country'] for involved_companies in igdb_game_data['involved_companies'] if 'country' in involved_companies['company'].keys()])
    #print(igdb_game_data)
    print("\n")
    #Steamspy: ['appid', 'name', 'developer', 'publisher', 'score_rank', 'positive', 'negative', 'userscore', 'owners', 
    # 'average_forever', 'average_2weeks', 'median_forever', 'median_2weeks', 'price', 'initialprice', 'discount', 'ccu', 'languages', 'genre', 'tags'])
    #name,id, languages, genre, themes, prices

print(len(page))

#page= requests.get(f"http://api.steampowered.com/<interface name>/<method name>/v<version>/?key=<api key>&format=<format>.")
