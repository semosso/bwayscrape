from pathlib import Path
import sys
import requests
import bs4 

PROJECT_FOLDER = Path.cwd().parent
BILL_FOLDER = PROJECT_FOLDER / "data" / "playbills"
BILL_FOLDER.mkdir(exist_ok=True, parents=True)

# baixar imagem do playbill
def find_site(show, indice):
  search_source = [
  f"http://www.playbill.com/searchpage/search?q={show}&sort=Relevance&shows=on",
  f"https://www.broadway.com/search/?q={show}&category=shows",
  f"https://www.broadwayworld.com/search/index.php?search_type%5B%5D=shows&q={show}"
  ]

  show_HTML = [
    ".bsp-list-promo-title > a",
    # FIGURE OUT 1,
    # FIGURE OUT 2
  ]

  url = search_source[indice]
    
  req_search = requests.get(url)
  req_search.raise_for_status()
  soup_search = bs4.BeautifulSoup(req_search.text, "html.parser")
  matches = soup_search.select(show_HTML[indice])
  
  n = len(matches)

  if n == 0:
    indice += 1

    if indice <= 2:
      print(f"Wait a little longer, trying to find the playbill in other sources...")
      find_site(show, indice)
    else:
      show, show_url, indice = 0, 0, 0
  
  elif n == 1:
    show_url = matches[0].get("href") # SHOULDN'T CHANGE BETWEEN SITES, BUT YOU NEVER KNOW...
    show = matches[0].text.strip()
  
  else:
    results = [a.text.strip() for a in matches] # works for playbill, but who knows for other ones...
    
    print("Pick which show (by index):")
    for i in range(min(n, 10)):
      print(f"{i}. {results[i]}")
    
    choice = int(input("> "))
    show = results[choice]
    show_url = matches[choice].get("href") # SHOULDN'T CHANGE BETWEEN SITES, BUT YOU NEVER KNOW... 

  return show, show_url, indice
  
def find_playbill(show, show_url, indice):
  show_source = [
    f"http://www.playbill.com{show_url}",
    # FIGURE OUT 1,
    # FIGURE OUT 2
    ]
  
  playbill_HTML = [
    'meta[property="og:image"]',
    # FIGURE OUT 1,
    # FIGURE OUT 2
  ]
  
  playbill_URL = [
    "content",
    # FIGURE OUT 1,
    # FIGURE OUT 2
  ]

  if (show == 0): # how to make it match all three params?
    print(f"Couldn't find a playbill based on {sys.argv[1:]} keywords :(")
    exit(1)

  else:
    req_show = requests.get(show_source[indice])
    req_show.raise_for_status()
  
    soup_show = bs4.BeautifulSoup(req_show.text, "html.parser")
    bill = soup_show.select_one(playbill_HTML[indice])
    bill_url = bill.get(playbill_URL[indice])
  
    req_bill = requests.get(bill_url)
    req_bill.raise_for_status()

    image_file = open(f"{BILL_FOLDER}/{show}.jpg", "wb") 

    for chunk in req_bill.iter_content(100000):
      image_file.write(chunk)
    image_file.close()
    print(f"Playbill for '{show}' has been downloaded!")

  # TODO:
  # p1: eliminar duplicidades (funções repetidas como em autolog?); aprender a usar path direito;
  # p2: add comments all around