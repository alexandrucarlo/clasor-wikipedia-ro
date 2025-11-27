from lxml import html
import re, os, random, shutil

foldere = [f for f in os.listdir(".") if os.path.isdir(os.path.join(".", f))]

for categorie in foldere:
    fisiere = [f for f in os.listdir(categorie) if os.path.isfile(os.path.join(categorie, f))]
    # am ales arbitrar 10% din fișiere pentru testarea modelului 
    nr_samples = len(fisiere)//10
    tests = random.sample(fisiere, nr_samples) 
    
    print(categorie, nr_samples)
    # punem articolele de test în alt folder ascuns (cu . la început pt. că așa funcționează pe UNIX)
    hidden_categorie = "." + categorie
    try:
        os.makedirs(hidden_categorie)
    except FileExistsError:
        pass
    
    for fil in tests:
        cale = os.path.join(categorie, fil)
        
        
        shutil.move(cale, hidden_categorie)
        
