import os
import sys
import requests
import bs4
import re

# baixar imagem do playbill
def get_playbill(show):
  search_url = ("http://www.playbill.com/searchpage/search?q=" + show + "&sort=Relevance&shows=on")
    
  req_search = requests.get(search_url) # this downloads entire page
  req_search.raise_for_status() # maybe work on Exception message? repeats below
  
  soup_search = bs4.BeautifulSoup(req_search.text, "html.parser") # this parses what has been downloaded
  show_element = soup_search.select(".bsp-list-promo-title > a")
  n = len(show_element)
  
  if n > 1:
    lista_limpa = [re.compile("\s+").sub(" ", a.text).strip() for a in show_element] # entender em detalhes depois
    print("Pick which show (by index):")

    for i in range(n):
      print(f"{i}. {lista_limpa[i]}")

    choice = int(input("> "))
    show_url = show_element[choice].get("href")

  else:
    show_url = show_element.get("href")

  # I could have gotten playbill IMG directly from show_url, but it'd be a lower quality
  req_show = requests.get("http://www.playbill.com" + show_url)
  req_show.raise_for_status()
  
  soup_show = bs4.BeautifulSoup(req_show.text, "html.parser")
  bill_element = soup_show.select_one('meta[property="og:image"]')
  bill_url = bill_element.get("content")
  
  req_bill = requests.get(bill_url) # downloading image
  req_bill.raise_for_status()

  image_file = open(os.path.join("..", "data", "playbills", f"{lista_limpa[choice]}.jpg"), "wb")
   
  for chunk in req_bill.iter_content(100000):
    image_file.write(chunk)
  image_file.close()

  # TODO:
  # p1: revisar e melhorar, eliminar duplicidades; aprender a usar path direito;
  # p2: entender "raise_for_status"; add comments all around; "pular" quando não houver playbill disponível
  # alternativas: procurar Google imagens; brute force achar site no playbill (e.g., chick flick); broadway.com

show = "+".join(sys.argv[1:])
get_playbill(show)

# def getSongs(show):
#   url = "https://www.ibdb.com/" # lista de músicas, somente para broadway
#   pass

# def getInfo(show):
#   url = "https://www.broadwayworld.com/" # everything else
#   pass

# # TODO input na fonte que já tenho (CSV da minha nota no Evernote), em vez de argv