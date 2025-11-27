# Predicția și testarea modelului

La logaritm, totuși, apare altă problemă: funcția noastră este definită pe intervalul (0; +inf), adică logaritmul nu știe ce să facă atunci când îi dai 0!
Soluția cea mai comună (pe care am și ales-o) este "netezirea" Laplace^1, cu alfa = 1, o soluție pe care nu am înțeles-o complet, dar care ne previne de cazurile nenule (adică nu mai avem probabilitatea ca logaritmul să crape, și am mărit probabilitatea (foarte puțin) a unui cuvânt "obscur", care nu face parte din setul de antrenament).

Putem, așadar, să considerăm toate probabilitățile ce urmează ca fiind logaritmate.
## Predicție

Predicția este făcută calculând pentru un articol oarecare fiecare probabilitate de categorie, de unde vrem să alegem cea mai mare probabilitate din cele pe care le-am calculat, rezultând cea mai probabilă categorie pentru acel articol.

În script-ul main.py, metoda predict() ia ca argument o cale, iar pentru a obține probabilitatea unei categorii, calculează frecvența fiecărui cuvânt și o înmulțește cu probabilitatea cuvântului în categoria respectivă, rezultat care va fi adunat (dacă nu aveam logaritm, înmulțit) cu probabilitatea (necondiționată) a categoriei. Dacă un cuvânt nu se află într-o categorie, acesta va avea o valoare foarte mică de alfa / (Ntotal(C) + alfa * vocabular).
După ce am calculat probabilitatea pentru fiecare categorie, aceste valori vor ajunge într-un dicționar Python, care va fi sortat descrescător, prima cheie fiind cea mai probabilă categorie.

## Testare

Am reușit să obțin o acuratețe de 0.8804 (88.04%), care deși nu atinge un ideal de 100%, consider că este un rezultat adecvat, mai ales având în vedere natura foarte naivă prin care clasifică. De asemenea, am remarcat faptul că acuratețea crește cu 0.3% procente dacă nu mai luăm în calcul probabilitatea categoriei (am aflat asta pentru că am realizat la un moment dat că am uitat să includ și acea probabilitate în calcul :] ) Pentru a analiza mai ușor diferențele subtile între cele două, am pus pe repository outputurile, mai exact în fișierele output1.txt (cu P(categ)) și output2.txt (fără P(categ))
