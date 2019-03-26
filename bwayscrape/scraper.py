import os
import sys
import requests
import bs4

show = " ".join(sys.argv[1:])

# baixar imagem do playbill
def getPlaybill (show):
  search_url = ("http://www.playbill.com/productions?q=" + show) # search result page
  
  req_search = requests.get(search_url) # this downloads entire page
  req_search.raise_for_status() # understand better; maybe work on Exception message? repeats below
  
  soup_search = bs4.BeautifulSoup(req_search.text) # this parses what has been downloaded
  matches = soup_search.select("pb-pl-tile-text-box a") # returns a list of all "production" matches from result page
  
  choice = input("Is the show one of the following? Choose by index.", matches)
  show_url = (matches[choice].get("href")) # extracts URL from list entry I choose
  
  req_show = requests.get("http://www.playbill.com/production" + show_url) # do I need domain here, or only show_url?
  req_show.raise_for_status()
  
  soup_show = bs4.BeautifulSoup(req_show.text)
  # will need formatting on this "syntax" to make it work, I'm sure
  # also need to check if every playbill is stored like this (sample was TOJC)
  # also appers in several other sections, maybe one of them would be better (and why)
  bill_element = soup_show.select('property="og:image"')
  bill_url = bill_element.get("content")
  
  # alternatively: class="data-bsp-share-options", then VALUE of "image" KEY; fazer testes com diferentes params e prints
  
  req_bill = requests.get(bill_url) # downloading image
  req_bill.raise_for_status()
  
  image_file = open(os.path.join("path/to/folder", show, wb) # será que seria sempre bom usar search terms?
  for chunk in req_bill.iter_content(100000):
    image_file.write(chunk)
  image_file.close()

# TODO scrape de informações

def getSongs(show):
  url = "https://www.ibdb.com/" # lista de músicas, somente para broadway
  pass

def getInfo(show):
  url = "https://www.broadwayworld.com/" # everything else

# TODO buscar input na fonte que já tenho (CSV da minha nota no Evernote)
