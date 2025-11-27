from lxml import html
import re, os


stopwords = []
with open("stopwords-ro.txt", "r") as f:
    stopwords = [w.rstrip() for w in f]



foldere = [f for f in os.listdir(".") if os.path.isdir(os.path.join(".", f))]

for a in foldere:
    fisiere = [f for f in os.listdir(a) if os.path.isfile(os.path.join(a, f))]
    print(a) 
    for fil in fisiere:
        cale = os.path.join(a, fil)
        root = html.parse(cale).getroot()

        with open(cale, "w") as f:
            paragraphs = root.xpath("//p[not(ancestor::*[@class='navbox'])]") #toate paragrafele care nu sunt în tabelul de la finalul paginii
            for p in paragraphs:
                # vrem si hyperlink-urile
                text = ''.join(p.xpath('.//text()')).strip()
                if text:
                    # facem totul lowercase
                    text = text.lower()
                    
                    #eliminam referintele (e.g.[]) si semnele de punctuatie cele mai relevante
                    text = re.sub(r"(\[[a-zA-Z0-9]*\])|[.,:;?!/\"\(\)]", ' ', text)
                    text = text.replace("„", ' ') 
                    text = text.replace("”", ' ')
                    text = text.replace("«", ' ') 
                    text = text.replace("»", ' ')
                    # eliminam cuvintele foarte comune (stopwords)
                    temp = text.split(' ')
                    text = ' '.join(filter(lambda a: a not in stopwords, temp))
                   
                    # normalizam spatiile
                    #text = ' '.join(text.split()) #nu stiu de ce asta imi lipeste cuvintele dar regex-ul nu??????
                    text = re.sub(r'\s+', ' ', text)
                    f.write(text)

