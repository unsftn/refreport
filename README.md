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
$ python refreport.py
```

Biće generisan fajl `refreport.html`.

Informacije o nedostajućim poljima u bibtex fajlovima biće prikazane na
konzoli.


