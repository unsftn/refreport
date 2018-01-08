# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
import os
import sys
import re
import glob
import jinja2
import codecs
import argparse
from arpeggio import NoMatch
from parser import parse_bibtex


class MyParser(argparse.ArgumentParser):
    """
    Custom arugment parser for printing help message in case of error.
    See http://stackoverflow.com/questions/4042452/display-help-message-with-python-argparse-when-script-is-called-without-any-argu
    """
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()


points_table = {
    'M11': '15',
    'M12': '10',
    'M13': '6',
    'M14': '4',
    'M21a': '10',
    'M21': '8',
    'M22': '5',
    'M23': '3',
    'M24': '3',
    'M31': '3',
    'M32': '1.5',
    'M33': '1',
    'M34': '0.5',
    'M41': '7',
    'M42': '5',
    'M43': '3',
    'M44': '2',
    'M45': '1.5',
    'M51': '2',
    'M52': '1.5',
    'M53': '1',
    'M55': '2',
    'M56': '1',
    'M61': '1.5',
    'M62': '1',
    'M63': '0.5',
    'M71': '6',
    'M72': '3',
    'M81': '8',
    'M82': '6',
    'M83': '4',
    'M84': '3',
    'M85': '2',
    'M91': '10',
    'M92': '8',
}


def points(type):
    return points_table.get(type, '')


def allauthors_filter(author_list):
    return ", ".join(author_list)


def coauthors_filter(author_list):
    return ", ".join(author_list[1:])


def isbn_issn_doi(ref):
    return ref.get('isbn', ref.get('issn', ref.get('doi', '')))


def booktitle_journal(ref):
    return ref.get('booktitle', ref.get('journal', ref.get('series', '')))


def check_keys(refs):
    """
    Check mandatory keys.
    """
    mandatory = [('project',), ('rank',), ('title',),
                 ('booktitle', 'journal', 'series'),
                 ('author',), ('year',), ('isbn', 'issn', 'doi'),
                 ('publisher',), ('pages', 'series')]
    for r in refs:
        for key in mandatory:
            if all([x not in r or not r[x] for x in key]):
                print("  Polje {} ne postoji u referenci {}"
                      .format(" ili ".join(key), r['bibkey']))
                r['uncomplete'] = True


def gen_md(refs):

    # Initialize template engine.
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

    # Filters
    jinja_env.filters['points'] = points
    jinja_env.filters['allauthors'] = allauthors_filter
    jinja_env.filters['isbn_issn_doi'] = isbn_issn_doi
    jinja_env.filters['booktitle_journal'] = booktitle_journal

    # Generate report
    template = jinja_env.get_template('refreport_md.template')
    with codecs.open('refreport.md', 'w', encoding="utf-8") as f:
        f.write(template.render(refs=refs))


def gen_html(refs):

    # References by projects
    authors = {}
    projects = {}

    for r in refs:

        # by project
        project = r.get('project', None)
        if not project:
            project = "Bez projekta"
        r['project'] = project
        projects.setdefault(project, [])
        projects[project].append(r)

        # by authors/projects
        for author in r['author']:
            auth_projects = authors.setdefault(author, {})
            auth_project = auth_projects.setdefault(project, [])
            auth_project.append(r)
            auth_project.sort(key=lambda x: x['title'])

    # Sort projects
    projects = list(projects.items())
    projects.sort(key=lambda x: x[0])
    for _, project in projects:
        project.sort(key=lambda x: x['title'])

    # Sort authors
    for author_name, auth_projects in authors.items():
        auth_projects = list(auth_projects.items())
        auth_projects.sort(key=lambda x: x[0])
        authors[author_name] = auth_projects

    authors = list(authors.items())
    authors.sort(key=lambda x: x[0])

    # Initialize template engine.
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

    # Filters
    jinja_env.filters['points'] = points
    jinja_env.filters['coauthors'] = coauthors_filter
    jinja_env.filters['isbn_issn_doi'] = isbn_issn_doi
    jinja_env.filters['booktitle_journal'] = booktitle_journal

    # Generate report
    template = jinja_env.get_template('refreport.template')
    with codecs.open('refreport.html', 'w', encoding="utf-8") as f:
        f.write(template.render(projects=projects, authors=authors))


if __name__ == "__main__":

    arg_parser = MyParser(
        description="Alat za generisanje izveštaja za Ministarstvo.")
    arg_parser.add_argument(
        'yearfilter', help="Filter po godinama (npr. 2011 ili 2010-2015)",
        nargs="?")

    args = arg_parser.parse_args()

    def check_year(yearfilter):
        def filter_for_years(ref):
            if '-' in yearfilter:
                _from, to = yearfilter.split('-')
                _from, to = int(_from), int(to)
                return _from <= int(ref['year']) <= to
            else:
                return int(ref['year']) == int(yearfilter)
        return filter_for_years

    refs = []
    bibtex_dir = os.path.join(os.path.dirname(__file__), 'bibtex-files')
    bibtex_files = glob.glob(os.path.join(bibtex_dir, '*.bib'))

    for f in bibtex_files:
        print(f)
        try:
            refs_f = parse_bibtex(f)
            # If year filter is given do the filtering
            if args.yearfilter:
                refs_f = list(filter(check_year(args.yearfilter), refs_f))
            if not refs_f:
                print("Nema referenci za zadate uslove.")
                continue
            for r in refs_f:
                r['author'] = r['author'].replace(',', '')
                r['author'] = [x.strip() for x in
                               re.split(' and |,', r['author'])]
            check_keys(refs_f)
            refs.extend(refs_f)
        except NoMatch as e:
            print(str(e))

    gen_html(refs)
    gen_md(refs)
