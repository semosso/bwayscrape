import re

csv_file = "CSV-file.txt"
original = open("messy-source.txt").read()

bway_regex = re.compile(r"^\d+\.\d+\.\d+\W+|.//(.*)", re.MULTILINE)
clean = bway_regex.sub("", original).strip()

with open(csv_file, "w") as f:
    f.write(clean)