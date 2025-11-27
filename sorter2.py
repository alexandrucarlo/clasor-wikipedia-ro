import os
import sys
import shutil


categorii = []
with open("categorii", "r") as c:
    categorii = [f.rstrip() for f in c]

foldere = [f for f in os.listdir(".") if os.path.isdir(os.path.join(".", f)) and f not in categorii]

for a in foldere:
    fisiere = [f for f in os.listdir(a) if os.path.isfile(os.path.join(a, f))]
    print(a, fisiere) 
    for i in fisiere:
        #print(os.path.join(a, i))
        shutil.move(os.path.join(a, i), os.getcwd())

    input()

