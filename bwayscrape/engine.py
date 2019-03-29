import sys
from pathlib import Path
import bill_scrape

PROJECT_FOLDER = Path.cwd().parent # should this be globally defined in every module, or is one enough? read on scopes

if len(sys.argv) > 1:
     show = "+".join(sys.argv[1:])
     bill_scrape.find_site(show)
else:
    file_CSV = open(f"{PROJECT_FOLDER}/CSV-file.txt", "r").read()
    show_list = file_CSV.split("\n")

    for i in show_list:
        show = i
        bill_scrape.find_site(show)

# adicionar outros módulos e funções