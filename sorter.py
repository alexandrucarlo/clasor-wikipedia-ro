from lxml import html
import os
import sys
import shutil


if len(sys.argv) != 2:
    sys.exit("utilizare: sorter.py [o singură cale]")
start = sys.argv[1]

print("Loading list")
articole = [f for f in os.listdir(start) if os.path.isfile(os.path.join(start, f))]
ignore_files = ["sorter.py", "sorter2.py", "categorii"]
print("Now processing")
for a in articole:
    if a in ignore_files:
        continue
    #print(a)
    #if ".html" not in a:
    #    shutil.move(a, a + ".html")
    try:
        tree = html.parse(a)
    except:
        print(a + " nu poate fi parsat")
        continue
        
    root = tree.getroot()
   
    redirect = tree.xpath("//meta[@http-equiv='refresh']")
    
    if redirect:
        shutil.move(a, "redirects/")
        continue

    antet = root.find_class("antet")
    categorie = ""
    for i in antet:
        for j in i.classes:
            if j == "antet":
                continue
            categorie = j
        break; # numai primul antet
    if categorie == "":
        shutil.move(a, "fara_categorie/")
        continue
    try:
        os.makedirs(categorie)
        print(categorie)
    except FileExistsError:
        pass

    shutil.move(a, categorie + "/")

