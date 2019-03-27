import os
import sys
import requests
import bs4

# baixar imagem do playbill
def getPlaybill (show):
  search_url = ("http://www.playbill.com/productions?q=" + show)
    
  req_search = requests.get(search_url) # this downloads entire page
  req_search.raise_for_status() # maybe work on Exception message? repeats below
  
  soup_search = bs4.BeautifulSoup(req_search.text, "html.parser") # this parses what has been downloaded
  show_element = soup_search.select_one(".pb-pl-tile-text-box > a")
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
  # p1: revisar e melhorar, eliminar duplicidades; show and confirm search results in ln 14;
  # p2: entender "raise_for_status"; better name for file in ln 27; add comments all around;
  # "pular" quando não houver playbill disponível (ou melhor, procurar Google imagens);

show = "+".join(sys.argv[1:])
getPlaybill(show)

# def getSongs(show):
#   url = "https://www.ibdb.com/" # lista de músicas, somente para broadway
#   pass

# def getInfo(show):
#   url = "https://www.broadwayworld.com/" # everything else
#   pass

# # TODO input na fonte que já tenho (CSV da minha nota no Evernote), em vez de argv
