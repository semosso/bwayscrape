import os
import sys
import requests
import bs4 # seems I could import only BeautifulSoup from bs4; why not?

# baixar imagem do playbill
def get_playbill(show):
  url = ("http://www.playbill.com/searchpage/search?q=" + show + "&sort=Relevance&shows=on")
    
  req_search = requests.get(url) # this downloads entire page
  req_search.raise_for_status()
  
  soup_search = bs4.BeautifulSoup(req_search.text, "html.parser") # this parses what has been downloaded
  matches = soup_search.select(".bsp-list-promo-title > a")
  n = len(matches)
  results = [a.text.strip() for a in matches]
  # entendendo ln acima: each "a in matches" is a bs4.Tag element, so a.text returns their text
  # all strip does is remove leading/trailing whitespaces; originally I was using regex, but don't need it here
  
  if n == 0:
    print(f"There isn't a Playbill.com page for a show based on {sys.argv[1:]} keywords.")
    exit(1) # só "funciona" se eu input por argv input; se CSV, fecha o programa mas quero que continue
            # quebrar funções em mais de uma "resolve" esse problema (uma acha o site, outra pega imagem)
  elif n > 1:
    print("Pick which show (by index):")
    for i in range(n):
      print(f"{i}. {results[i]}")
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

  print(f"Downloading the playbill for {results[choice]}...")
  image_file = open(os.path.join("..", "data", "playbills", f"{results[choice]}.jpg"), "wb")
   
  for chunk in req_bill.iter_content(100000):
    image_file.write(chunk)
  image_file.close()

#input can be by argv or CSV
# ARGV
# show = "+".join(sys.argv[1:])
# get_playbill(show)

#CSV
file_CSV = open("CSV-file.txt").read()
show_list = file_CSV.split("\n")

for i in show_list:
  show = i
  get_playbill(show)

# CSV for real this time
# to come

  # TODO:
  # p1: eliminar duplicidades (funções repetidas como em autolog?); aprender a usar path direito;
  # p2: add comments all around; entender regex em ln 17; e quando não tiver playbill disponível?
  # try Google imagens, brute force site playbill (e.g., chick flick), broadway.com