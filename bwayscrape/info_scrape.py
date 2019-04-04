from pathlib import Path
import requests
import bs4
import json
import re

# do I need this? still haven't figured out how to use/work with paths properly
PROJECT_FOLDER = Path.cwd().parent
BILL_FOLDER = PROJECT_FOLDER / "data" / "production info"
BILL_FOLDER.mkdir(exist_ok=True, parents=True)

def find_site(show):
    url = f"https://www.broadwayworld.com/search/index.php?search_type%5B%5D=shows&q={show}"

    req = requests.get(url)
    req.raise_for_status()
    soup = bs4.BeautifulSoup(req.text, "html.parser")
    matches = soup.select('span a[href^="/shows/?showid="]')
  
    n = len(matches)

    if n == 0: # i.e., if no site for show was found
        show, show_url = 0, 0
  
    elif n == 1: # i.e., if it only found one matching show
        show = matches[0].text.strip()
        show_url = "https://www.broadwayworld.com" + matches[0].get("href")
    
    else: # i.e., if multiple (> 1) shows were found, prints a list and lets me choose between them
        parents = [i.parent for i in matches] # comment this so I remember it later
        results = [a.text.strip() for a in parents]
    
        print("Pick which show (by index):")
        for i in range(min(n, 15)):
            print(f"{i}. {results[i]}")
    
        choice = int(input("> "))
        show = matches[choice].text.strip()
        show_url = "https://www.broadwayworld.com" + matches[choice].get("href")

    return show, show_url

def find_info(show, show_url):
    
    show_info = {
    "show": {
        "cast": {}, # however many each show needs
        "staff": {}, # however many each show needs
        "synopsis": "",
        "market": "",
        "type": "",
        "location": "",
        "dates": {},
        "songs": "" # I can create a specific song_scrape() function here in this archive;
    }                # however many each show needs (actually, this might be a list)
}

    if (show == 0): # i.e., if no show was found on the site
                    # how to make it match all three params? don't need it, but it seems sloppy not to 
        print(f"Couldn't find the info for {show} :(")

    else:
        req = requests.get(show_url)
        req.raise_for_status()
        soup = bs4.BeautifulSoup(req.text, "html.parser")
        info_JSON = soup.find(type="application/ld+json").text.strip() # not all have this
        
        if info_JSON == None:
            pass
        
        else:
            info = json.loads(info_JSON[:-1])

            # show
            show = info["name"]
            show_info[show] = show_info.pop("show")

        # cast      
        #cast = soup.select(html_blocks["cast"])

        # staff
        #taff = soup.select(html_blocks["staff"])

        # market
        #market = soup.select(html_blocks["market"])

        # type
        #type_ = soup.select(html_blocks["type"])

            #location
            location = info["location"]["name"]
            show_info[location] = show_info.pop("location")

            # dates     
            opening = info["startDate"][:10]
            # adapted because there's currently no OPENING key under the dict value of DATES
            show_info["dates"]["opening"] = opening
        
        #dates = soup.select(html_blocks["dates"])

        # running time
        #time = soup.find("Running Time:")
        
        #TODO:
        # "automatizar/consolidar" a busca conforme possível
        # e.g., "for i in html_blocks.keys()" e tentar não usar tantas sub-buscas diferentes
    
        with open("teste.py", "a") as f:
            data = show_info[show]
            f.write(data)

def find_songs(show):
    pass