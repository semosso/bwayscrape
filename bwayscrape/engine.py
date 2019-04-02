import sys
from pathlib import Path
import bill_scrape as bs

PROJECT_FOLDER = Path.cwd().parent

# starteia a porra toda, chamando a busca de playbill
if len(sys.argv) > 1:
     show = "+".join(sys.argv[1:])
     show, show_url, indice = bs.find_site(show, 0)
     bs.find_playbill(show, show_url, indice)
else:
    file_CSV = open(f"{PROJECT_FOLDER}/CSV-file.txt", "r").read()
    show_list = file_CSV.split("\n")

    for i in show_list:
        show = i
        show, show_url, indice = bs.find_site(show, 0)
        bs.find_playbill(show, show_url, indice)

# adicionar outros módulos e funções
