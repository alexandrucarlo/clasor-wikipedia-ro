import copy
import math
import os
import pickle
from collections import Counter


class model_bayes:
    alfa = 1
    prob_categorie = {}  # cat de probabila este categoria data?
    prob_cuvinte = {}  # cat de probabil este un cuvant dintr-o categorie?
    nr_total_cuvinte = {}  # care este numarul de cuvinte (nedistincte) dintr-o categorie?
    scor_necunoscut = {}  # care este probabilitatea unui cuvant necunoscut?
    nr_vocabular = 0  # care este numarul de cuvinte distincte in tot setul de date?

    def train(self):
        print("Antrenare")
        nr_articole = {}  # care este numarul de articole pentru fiecare categorie?
        nr_cuvinte = {}  # care este frecventa unui cuvant dintr-o categorie?
        foldere = [
            f
            for f in os.listdir(".")
            if os.path.isdir(os.path.join(".", f)) and not f.startswith(".")
        ]  # categoriile ascunse (cu . la început) nu intra in setul de training, le pastram pentru teste

        # Tehnic și aici facem "prelucrarea datelor" :v

        # Numararea cuvintelor
        for categorie in foldere:
            fisiere = [
                f
                for f in os.listdir(categorie)
                if os.path.isfile(os.path.join(categorie, f))
            ]
            print("Dupa", categorie, "avem: ", end="")

            # numarul articolelor
            nr_articole[categorie] = len(fisiere)
            print(nr_articole[categorie], "articole și ", end="")

            # contor pentru orice cuvant in fiecare categorie
            nr_cuvinte[categorie] = Counter()
            for articol in fisiere:
                cale = os.path.join(categorie, articol)
                with open(cale, "r") as f:
                    continut = f.read()  # tot textul se copiaza in continut

                    nr_cuvinte[categorie].update(continut.split())

            print(len(nr_cuvinte[categorie]), "cuvinte")

        ## Acum trecem la calcule

        # Numărul de cuvinte (nedistincte) dintr-o categorie
        nr_total_articole = 0
        for i in nr_articole:
            nr_total_articole += nr_articole[i]
        print("Total: ", nr_total_articole, "articole")
        # Numărul de cuvinte distincte, doar că ăsta e de show
        nr_vocabular = 0
        for i in nr_cuvinte:
            nr_vocabular += len(nr_cuvinte[i])
        print("Total: ", nr_vocabular, "cuvinte distincte")

        # Probabilitatea fiecărei clase/categorii (nu a scris un llm codul, asa am ales să scriu comentariile:)))
        self.prob_categorie = nr_articole
        for i in self.prob_categorie:
            self.prob_categorie[i] = math.log(
                self.prob_categorie[i] / nr_total_articole
            )

        # Reducem vocabularul din motive de performanță (nu aveam chef să stau mai mult de 2 minute pentru o simulare întreagă)
        self.prob_cuvinte = copy.deepcopy(
            nr_cuvinte
        )  # facem o copie deep pentru ca Python nu vrea sa copieze 1 la 1 structuri by default pentru ca e costisitor :)

        for i in self.prob_cuvinte:
            self.prob_cuvinte[i] = dict(
                self.prob_cuvinte[i]
            )  # transformam counter-ul in dict

            self.prob_cuvinte[i] = {
                k: v for k, v in self.prob_cuvinte[i].items() if v > 2
            }  # eliminam cuvintele cu aparitie mai mica de 2 (de la 2894804 cuv la 941534 cuv)

        # Numărul de cuvinte distincte, doar că ăsta e de show
        self.nr_vocabular = 0
        for i in self.prob_cuvinte:
            self.nr_vocabular += len(self.prob_cuvinte[i])
        print("Total: ", self.nr_vocabular, "cuvinte distincte după reducție")

        # Probabilitatea fiecarui cuvant | categorie

        for categ in self.prob_cuvinte:
            nr_cuv = 0  # N total de cuvinte in categorie
            for c in self.prob_cuvinte[categ]:
                nr_cuv += self.prob_cuvinte[categ][c]

            self.nr_total_cuvinte[categ] = (
                nr_cuv  # stocam rezultatele pentru predictie :P
            )
            self.scor_necunoscut[categ] = math.log(
                self.alfa / (nr_cuv + self.alfa * self.nr_vocabular)
            )
            for c in self.prob_cuvinte[categ]:
                self.prob_cuvinte[categ][c] = math.log(
                    (self.prob_cuvinte[categ][c] + self.alfa)
                    / (nr_cuv + self.alfa * nr_vocabular)
                )  # cu Laplace smoothing

        # putem stoca calculele obtinute intr-un fisier in caz de orice (dar la mine oricum a durat foarte putin train-ul)
        # with open("prob_categorie","wb") as f: # wb pentru ca pickle functioneaza la nivel binar
        #    pickle.dump(self.prob_categorie, f)

        # with open("prob_cuvinte","wb") as f:
        #    pickle.dump(self.prob_cuvinte, f)

    def predict(self, cale):
        with open(cale, "r") as f:
            continut = f.read()  # tot textul se copiaza in continut
            nr_cuvinte_nou = Counter()
            nr_cuvinte_nou.update(continut.split())

            # nr_cuvinte_nou = dict(nr_cuvinte_nou) # altfel nu ne merge iterarea cu for
        # Pentru fiecare categorie vom calcula probabilitatea ei conditionata de articol
        prob_articole = {}
        # print(self.prob_cuvinte)
        for categ in self.prob_cuvinte:
            # nr_cuv = self.nr_total_cuvinte[
            #    categ
            # ]  # recalculam N total de cuvinte in categorie (mulțumesc laplace!)

            # pentru fiecare cuvant din nr_cuvinte
            # prob_articole[categ] = 0
            prob_articole[categ] = self.prob_categorie[categ]
            for cuvant in nr_cuvinte_nou:
                if (
                    cuvant in self.prob_cuvinte[categ]
                ):  # daca cuvantul apare in categorie...
                    prob_articole[categ] += (
                        self.prob_cuvinte[categ][cuvant] * nr_cuvinte_nou[cuvant]
                    )  # ...Xi * P(Xi | categorie)
                else:  # cuvantul nu apare (probabilitatea tinde la 0)
                    # prob_articol[categ] += 0
                    # prob_articole[categ] += math.log(self.alfa / (nr_cuv + self.alfa * self.nr_vocabular )) * nr_cuvinte_nou[cuvant]
                    prob_articole[categ] += (
                        self.scor_necunoscut[categ]
                        * nr_cuvinte_nou[
                            cuvant
                        ]  # ecuatia cu log de mai sus cache-uita in training
                    )
        # întoarcem un dicționar sortat descrescător după probabilitatea categoriei
        return dict(sorted(prob_articole.items(), key=lambda x: x[1], reverse=True))


## COD PRINCIPAL

model = model_bayes()
model.train()
nr_articole_test = 0
nr_articole_hits = 0


foldere = [
    f
    for f in os.listdir(".")
    if os.path.isdir(os.path.join(".", f)) and f.startswith(".")
]  # acum luam setul exclus din cel de antrenament

print("Testare model:")
for categorie in foldere:
    fisiere = [
        f for f in os.listdir(categorie) if os.path.isfile(os.path.join(categorie, f))
    ]
    print("Dupa", categorie, end="")
    for articol in fisiere:
        nr_articole_test += 1
        cale = os.path.join(categorie, articol)
        predictii = model.predict(cale)
        for i in predictii:
            if ("." + i) == categorie:
                nr_articole_hits += 1
            break

    print(" acuratetea modelului este:", nr_articole_hits / nr_articole_test)
