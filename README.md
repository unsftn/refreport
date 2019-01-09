Alatka za generisanje html izveštaja sa referencama po projektima na osnovu bibtex
fajlova.


Instalacija
===========

Instalirati [Arpeggio](https://github.com/igordejanovic/arpeggio).

```
$ pip install Arpeggio
```

Instalirati jinja2 obrađivač šablona

```
$ pip install Jinja2
```

Uputstvo
========

BibTex fajlove smestiti u `bibtex-files` folder.

Pokrenuti alat sa:

```
$ python refreport.py <filter po godinama>
```

Gde je filter oblika: `2016` ili npr. `2015-2018`.

Biće generisan fajl `refreport.html`.

Ako se filter ne definiše biće uključene sve reference.

Informacije o nedostajućim poljima u bibtex fajlovima biće prikazane na
konzoli.

Možete ubaciti u repo i `refreport.html` ali proverite da ste ga dobro
generisali, tj. da je filtriran za tekući ciklus (trenutno za 2018 god.).

Za autore navodite prvo ime pa prezime. Autore razdvajajte sa rečju "and".

Koristite "naša" slova direktno. Izbegavajte bibtex format oblika `\'{c}`.

Pre unosa reference proverite prvo da li je neko od koautora već uneo. Nemojte
unositi duplo.

Primer:

```
@article{Dejanovic2017a,
    author = {Igor Dejanović and Renata Vaderna and Gordana Milosavljević and Željko Vuković},
    title = {{TextX: A Python tool for Domain-Specific Languages implementation}},
    journal = {Knowledge-Based Systems},
    publisher = {Elsevier},
    volume = {115},
    pages = {1--4},
    url = {http://www.sciencedirect.com/science/article/pii/S0950705116304178},
    doi = {10.1016/j.knosys.2016.10.023},
    issn = {0950-7051},
    year = {2017},

    rank = {M21},
    project = {III44010-PP1}
}
```

Ne morate brisati reference od ranije. Samo dodajte nove u već postojeće fajlove.

Trenutnu verziju iz repozitorijuma uvek možete videti na linku https://raw.githack.com/unsftn/refreport/master/refreport.html

Reference koje nisu potpune su obeležene crvenom bojom.

Na kraju, u izveštaju, proverite pod vašim imenom da li je sve ispravno.
