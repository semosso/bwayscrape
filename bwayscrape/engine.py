import sys
from pathlib import Path
import bill_scrape as bill
import info_scrape as info

PROJECT_FOLDER = Path.cwd().parent

# starteia a porra toda, chamando a busca de playbill
if len(sys.argv) > 1:
     show = "+".join(sys.argv[1:])
     show, show_url, indice = bill.find_site(show, 0)
     bill.find_playbill(show, show_url, indice)
     show, show_url = info.find_site(show)
     info.find_info(show, show_url)

else:
    file_CSV = open(f"{PROJECT_FOLDER}/CSV-file.txt", "r").read()
    show_list = file_CSV.split("\n")

    for i in show_list:
        show = i
        show, show_url, indice = bill.find_site(show, 0)
        bill.find_playbill(show, show_url, indice)
        show, show_url = info.find_site(show)
        info.find_info(show, show_url)

# adicionar outros módulos e funções

# sample data structure

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