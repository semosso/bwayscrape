from pathlib import Path
import requests
import bs4 

# do I need this? still haven't figured out how to use/work with paths properly
PROJECT_FOLDER = Path.cwd().parent
BILL_FOLDER = PROJECT_FOLDER / "data" / "playbills"
BILL_FOLDER.mkdir(exist_ok=True, parents=True)

# tries to find a website for the show; if there's no site on Playbill.com, tries alternatives
# "trying alternatives" is done with a "list index counter"; if it goes up, changes site
def find_site(show, indice):
  search_source = [
  f"http://www.playbill.com/searchpage/search?q={show}&sort=Relevance&shows=on",
  f"https://www.broadway.com/search/?q={show}&category=shows",
  f"https://www.broadwayworld.com/search/index.php?search_type%5B%5D=shows&q={show}"
  ]

  show_HTML = [
    ".bsp-list-promo-title > a",
    # FIGURE OUT 1, FIGURE OUT 2
  ]

  url = search_source[indice]
    
  req = requests.get(url) # makes request to URL and downloads/stores everything 
  req.raise_for_status() # checks to see if request was successful (code 200)
  soup = bs4.BeautifulSoup(req.text, "html.parser") # parses the whole site
  matches = soup.select(show_HTML[indice]) # searches parsed site for "blocks" 
  
  n = len(matches)

  if n == 0: # i.e., if no site for show was found
    indice += 1
    if indice <= 2:
      print(f"Wait a little longer, trying to find the playbill in other sources...")
      find_site(show, indice)
    else:
      show, show_url, indice = 0, 0, 0 # pass these to find_playbill() so it knows no site was found
  
  elif n == 1: # i.e., if it only found one matching show
    show = matches[0].text.strip()
    show_url = matches[0].get("href")
  
  else: # i.e., if multiple (> 1) shows were found, prints a list and lets me choose between them
    results = [a.text.strip() for a in matches] # takes away all HTML, returns only text
    print("Pick which show (by index):")
    for i in range(min(n, 15)):
      print(f"{i}. {results[i]}")
    
    choice = int(input("> "))
    show = results[choice]
    show_url = matches[choice].get("href") 

  return show, show_url, indice

# finds and downloads the actual playbill IMG on each site
# alternative sites are searched based on whatever "index" is passed by find_site()
def find_playbill(show, show_url, indice):
  show_source = [
    f"http://www.playbill.com{show_url}",
    # FIGURE OUT 1, FIGURE OUT 2
    ]
  
  playbill_HTML = [
    'meta[property="og:image"]',
    # FIGURE OUT 1, FIGURE OUT 2
  ]
  
  playbill_URL = [
    "content",
    # FIGURE OUT 1, FIGURE OUT 2
  ]

  if (show == 0): # i.e., if no show was found on any site
                  # how to make it match all three params? don't need it, but it seems sloppy not to 
    print(f"Couldn't find the playbill for {show} :(")
    exit(1)

  else:
    req = requests.get(show_source[indice])
    req.raise_for_status()
    soup = bs4.BeautifulSoup(req.text, "html.parser")
    bill = soup.select_one(playbill_HTML[indice])
    
    bill_url = bill.get(playbill_URL[indice])
    req = requests.get(bill_url)
    req.raise_for_status()

    image_file = open(f"{BILL_FOLDER}/{show}.jpg", "wb") # "w" (or "a", for that matter) creates if there's nothing there

    for chunk in req.iter_content(100000): # from ABSWP: write in chunks, useful for larger things
      image_file.write(chunk)
    image_file.close()
    print(f"Playbill for '{show}' has been downloaded!")

  # TODO:
  # p1: eliminar duplicidades (funções repetidas como em autolog?); aprender a usar path direito;
  # p2: lista de enderecos no retorno de matches (facilita distinguir entre producoes)
  # p3: NDA na escolha da lista de matches, resultando em indice += 1