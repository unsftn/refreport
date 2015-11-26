# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
import sys
import os
import re
import glob
import jinja2
import codecs
from arpeggio import NoMatch
from parser import parse_bibtex

AUTHOR="Igor Dejanović"

sys.stdout = codecs.getwriter('utf8')(sys.stdout)


def isbn_issn(ref):
    return ref.get('isbn', ref.get('issn', ''))


def booktitle_journal(ref):
    return ref.get('booktitle', ref.get('journal', ''))


def authors_editors(ref):
    if 'author' in ref:
        return ref['author']
    else:
        return ref['editor']


def authors_emph(ref):
    authors = authors_editors(ref)
    authors = ["<b>{}</b>".format(author)
                if author == AUTHOR else author for author in authors]
    return ", ".join(authors)

def uloga(ref):
    authors = authors_editors(ref)
    return "аутор" if authors[0] == AUTHOR else "коаутор"


def ref_format(ref):
    return "{}. {}. {}{}{}".format(
            authors_emph(ref),
            ref['title'],
            " {},".format(booktitle_journal(ref)),
            " pp. {},".format(ref['pages']) if 'pages' in ref else "",
            " {}.".format(ref['year'])
            )

def check_keys(refs):
    """
    Check mandatory keys.
    """
    mandatory = [('project',), ('rank',), ('title',), ('booktitle', 'journal'),
                 ('author',), ('year',), ('isbn', 'issn'),
                 ('publisher',), ('pages',)]
    for r in refs:
        for key in mandatory:
            if all([x not in r or not r[x] for x in  key]):
                print("  Polje {} ne postoji u referenci {}"
                      .format(" ili ".join(key), r['bibkey']))

def gen_html(refs):

    # Sort by year in ascending order
    refs.sort(key=lambda x: x['year'])

    # Initialize template engine.
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

    # Filters
    jinja_env.filters['ref_format'] = ref_format
    jinja_env.filters['uloga'] = uloga

    # Load Java template
    template = jinja_env.get_template('refreport.template')

    # For each entity generate java file
    with codecs.open('refreport.html', 'w', encoding="utf-8") as f:
        f.write(template.render(references=refs))


if __name__ == "__main__":
    refs = []
    bibtex_dir = os.path.join(os.path.dirname(__file__), 'bibtex-files')
    bibtex_files = glob.glob(os.path.join(bibtex_dir, '*.bib'))

    for f in bibtex_files:
        print(f)
        try:
            refs_f = parse_bibtex(f)
            for r in refs_f:
                print(r['title'])
                if 'author' in r:
                    r['author'] = [x.strip() for x in
                                re.split(' and |,', r['author'])]
                else:
                    r['editor'] = [x.strip() for x in
                                    re.split(' and |,', r['editor'])]

            check_keys(refs_f)
            refs.extend(refs_f)
        except NoMatch as e:
            print(unicode(e))

    gen_html(refs)






