import os
import sys
import requests
import bs4

# baixar imagem do playbill
def get_playbill(show):
  search_url = ("http://www.playbill.com/searchpage/search?q=" + show + "&sort=Relevance&shows=on")
    
  req_search = requests.get(search_url) # this downloads entire page
  req_search.raise_for_status() # maybe work on Exception message? repeats below
  
  soup_search = bs4.BeautifulSoup(req_search.text, "html.parser") # this parses what has been downloaded
  show_element = soup_search.select_one(".bsp-list-promo-title > a")
  show_url = show_element.get("href")

  req_show = requests.get("http://www.playbill.com" + show_url)
  req_show.raise_for_status()
  
  soup_show = bs4.BeautifulSoup(req_show.text, "html.parser")
  bill_element = soup_show.select_one('meta[property="og:image"]')
  bill_url = bill_element.get("content")
  
  req_bill = requests.get(bill_url) # downloading image
  req_bill.raise_for_status()

  image_file = open(os.path.join("..", "data", f"{show}.jpg"), "wb")
   
  for chunk in req_bill.iter_content(100000):
    image_file.write(chunk)
  image_file.close()

  # TODO:
  # p1: revisar e melhorar, eliminar duplicidades; show and confirm search results in ln 14
  # (maybe bsp-list-promo-title na busca geral, mostrando os nomes, seja a resposta);
  # aprender a usar path direito (não dá pra ficar dependendo de .., precisa ser absolute);
  # p2: entender "raise_for_status"; better name for file in ln 27; add comments all around;
  # "pular" quando não houver playbill disponível (ou melhor, procurar Google imagens);
  # tentar brute force achar site no playbill (e.g., chick flick?); broadway.com para playbills tbm

show = "+".join(sys.argv[1:])
get_playbill(show)

# def getSongs(show):
#   url = "https://www.ibdb.com/" # lista de músicas, somente para broadway
#   pass

# def getInfo(show):
#   url = "https://www.broadwayworld.com/" # everything else
#   pass

# # TODO input na fonte que já tenho (CSV da minha nota no Evernote), em vez de argv