import os
import sys
import requests
import bs4
import re

# baixar imagem do playbill
def get_playbill(show):
  url = ("http://www.playbill.com/searchpage/search?q=" + show + "&sort=Relevance&shows=on")
    
  req_search = requests.get(url) # this downloads entire page
  req_search.raise_for_status() # maybe work on Exception message? repeats below
  
  soup_search = bs4.BeautifulSoup(req_search.text, "html.parser") # this parses what has been downloaded
  matches = soup_search.select(".bsp-list-promo-title > a")
  n = len(matches)
  lista = [re.compile("\s+").sub(" ", a.text).strip() for a in matches] # entender em detalhes depois
  
  if n > 1:
    print("Pick which show (by index):")
    for i in range(n):
      print(f"{i}. {lista[i]}")
    choice = int(input("> "))
  else:
    choice = 0
  
  show_url = matches[choice].get("href")

  # I could get playbill IMG directly from show_url, but it'd be a lower quality
  req_show = requests.get("http://www.playbill.com" + show_url)
  req_show.raise_for_status()
  
  soup_show = bs4.BeautifulSoup(req_show.text, "html.parser")
  bill = soup_show.select_one('meta[property="og:image"]')
  bill_url = bill.get("content")
  
  req_bill = requests.get(bill_url) # downloading image
  req_bill.raise_for_status()

  print(f"Downloading the playbill for {lista[choice]}...")
  image_file = open(os.path.join("..", "data", "playbills", f"{lista[choice]}.jpg"), "wb")
   
  for chunk in req_bill.iter_content(100000):
    image_file.write(chunk)
  image_file.close()

# input can be by argv or CSV
# ARGV
show = "+".join(sys.argv[1:])
get_playbill(show)

# CSV (nas coxas, not actual CSV file)
show_list = open("source.txt").read()
listz = show_list.split(",")

for i in listz:
  show = i
  get_playbill(show)

# CSV for real this time
# to come

  # TODO:
  # p1: eliminar duplicidades (funções repetidas como em autolog?); aprender a usar path direito;
  # p2: entender "raise_for_status"; add comments all around; entender regex em ln 17
  # "pular" quando não tiver (Google imagens; brute force site playbill (e.g., chick flick); broadway.com)