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

Gde je filter oblika: `2016` ili npr. `2015-2017`.

Biće generisan fajl `refreport.html`.

Ako se filter ne definiše biće uključene sve reference.

Informacije o nedostajućim poljima u bibtex fajlovima biće prikazane na
konzoli.

Možete ubaciti u repo i `refreport.html` ali proverite da ste ga dobro
generisali, tj. da je filtriran za tekući ciklus (trenutno za 2017 god.).

Trenutnu verziju iz repozitorijuma uvek možete videti na [ovom linku](http://htmlpreview.github.io/?https://github.com/unsftn/refreport/blob/master/refreport.html).

