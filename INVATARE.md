# Definirea și învățarea modelului
Aici am detaliat modelul Bayes multinomial, pe care l-am implementat în Python (fără numpy; știu, este absurd!) din motive de înțelegere mai ușoară a conceptelor.

Site-ul care m-a ajutat foarte mult să diger acest concept este listat mai jos. ^1

## Dar ce este modelul (teorema) Bayes?
Conform articolului de pe Wikipedia în limba română (care, în mod ironic, nu a fost categorisit de către sorter), "Teorema lui Bayes este una din teoremele fundamentale ale teoriei probabilităților, care determină probabilitatea apartenenței evenimentelor și a obiectelor la o anumită grupă."^2 Ca și idee de bază, ea este folosită pentru "inversarea" probabilităților condiționate; de exemplu, dacă știm rata rebuturilor produse de hala 1 a fabricii Faur de pe vremea comunismului, precum și rata rebuturilor totale și volumul de producție al fiecărei hale, atunci putem afla cât de probabil este ca hala 1 să producă un rebut:
(introdu fracție aici)

În cazul nostru, vom calcula probabilitatea unei categorii condiționată de un articol (care este format din, evident, cuvinte) folosind probabilitățile acelei categorii (adică cele a priori), și articolului/documentelor (care aparțin clasei).
(introdu ecuație aici)
Probabilitatea articolului a dispărut din numitor pentru că orice articol este unic, și va avea o probabilitate extrem de mică atunci când îl alegem din lista întreagă de articole. Totuși, nu mai putem folosi semnul de egalitate, dar proporționalitatea rămâne aceeași.

Pentru a calcula probabilitatea condiționată a unui articol, vom folosi această formulă:
(introdu formulă aici)

unde x i bla bla

În antrenare, vom calcula pentru fiecare categorie probabilitățile cuvintelor din fiecare articol.


## Implementarea în Python

Programul este implementat în fișierul main.py, ce are la bază clasa "model_bayes", cu 2 metode: train(), și predict() (despre care vorbim în TESTARE.md).
Metoda train se duce în fiecare folder/categorie, calculează probabilitatea unei categorii prin numărarea articolelor/categorie împărțită la numărul total de articole, apoi folosește un obiect de tip Counter pentru a afla frecvența fiecărui cuvânt în categoria dată, pe baza căruia putem calcula probabilitatea unui cuvânt condiționată de categorie. Cuvintele care nu aveau mai mult de 2 apariții nu au mai fost luate în considerare ()


## Probleme cu abacul nostru electric
Din păcate, viața nu este așa roz, iar calculatoarele nu se pricep la numere mici (underflow)^3, și există riscul ca unele probabilități să atingă 0 (iar prin înmulțire totul devine 0!) deci am fost nevoit să logaritmez numerele cu care lucrăm. Conceptul va rămâne același pentru că funcția logaritm poate fi distribuită (log a + log b = log a*b), iar rezultatul logaritmului va fi un număr negativ, care tinde spre 0 odată cu probabilitatea, care tinde spre 1.

De aici vom continua mai departe spre predicția și testarea modelului.

^1: https://taijusanagi.com/multinomial-naive-bayes
^2: https://ro.wikipedia.org/wiki/Teorema_lui_Bayes?useskin=vector
^3: https://en.wikipedia.org/wiki/Underflow
