from pathlib import Path
import requests
import bs4 

# do I need this? still haven't figured out how to use/work with paths properly
PROJECT_FOLDER = Path.cwd().parent
BILL_FOLDER = PROJECT_FOLDER / "data" / "production info"
BILL_FOLDER.mkdir(exist_ok=True, parents=True)

SHOW_INFO = {
    "show": {
        "cast": {}, # however many each show needs
        "staff": {}, # however many each show needs
        "market": "",
        "type": "",
        "dates": {},
        "running time": "",
        "songs": "" # I can create a specific song_scrape() function here in this archive; however many each show needs (actually, this might be a list)
    }
}

def find_site(show):
    url = f"https://www.broadwayworld.com/search/index.php?search_type%5B%5D=shows&q={show}"

    req = requests.get(url)
    req.raise_for_status()
    soup = bs4.BeautifulSoup(req.text, "html.parser")
    matches = soup.select("") # add from Evernote
  
    n = len(matches)

    if n == 0: # i.e., if no site for show was found
        show, show_url = 0, 0
  
    elif n == 1: # i.e., if it only found one matching show
        show = matches[0].text.strip() # is this duplicative? bill.find_info() will have already found this
                                       # pros of deleting: more integration; migght eliminate need for "else" below
                                       # cons of deleting: maybe some small change in how each site names shows will "crash" this function
                                       # test to see if it would really be a problem not having it, after it already works
        show_url = "https://www.broadwayworld.com" + matches[0].get("href") # might as well work...
    
    else: # i.e., if multiple (> 1) shows were found, prints a list and lets me choose between them
        results = [a.text.strip() for a in matches] # might as well work...
    
        print("Pick which show (by index):")
        for i in range(min(n, 10)):
            print(f"{i}. {results[i]}")
    
        choice = int(input("> "))
        show = results[choice]
        show_url = "https://www.broadwayworld.com" + matches[choice].get("href") # might as well work...

    return show, show_url

def find_info(show, show_url):
    html_blocks = {
        "cast": "",
        "staff": "",
        "market": "",
        "type": "",
        "dates": "",
        "running time": ""
    }
    
    if (show == 0): # i.e., if no show was found on any site
                    # how to make it match all three params? don't need it, but it seems sloppy not to 
        print(f"Couldn't find the info for {show} :(")
        exit(1)

    else:
        req = requests.get(show_url) # makes request to URL and downloads/stores everything 
        req.raise_for_status() # checks to see if request was successful (code 200)
        soup = bs4.BeautifulSoup(req.text, "html.parser") # parses the whole site
        
        # show
        SHOW_INFO[f"{show}"] = SHOW_INFO.pop("show")

        # see if find_all (or some other method) wouldn't be more appropriate
        # cast
        cast = soup.select(html_blocks["cast"])

        # staff
        staff = soup.select(html_blocks["staff"])

        # market
        market = soup.select(html_blocks["market"])

        # type
        type_ = soup.select(html_blocks["type"])

        # dates
        dates = soup.select(html_blocks["dates"])

        # running time
        time = soup.select(html_blocks["running time"])
        
        #TODO:
        # "automatizar/consolidar" a busca conforme possível
        # e.g., "for i in html_blocks.keys()" e tentar não usar tantas sub-buscas diferentes

def find_songs(show):
    pass