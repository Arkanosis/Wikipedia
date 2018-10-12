#! /usr/bin/env python3

# (C) 2016-2018 Arkanosis
# jroquet@arkanosis.net
#
# Mis à disposition sous licence MIT
# http://www.opensource.org/licenses/mit-license.php
#
# Version originale pour la WikiConvention francophone 2016 :
# https://github.com/Arkanosis/WikiConvFR16/blob/master/Datamining%20du%20dimanche%20sur%20les%20projets%20Wikimedia/src/count_synonyms.py

import re
import sys
import wikidump

_lang = re.compile(r'=+\s*\{\{langue\|(?P<lang>.+?)\}\}\s*=+')
_synonyms = re.compile(r'=+\s*\{\{S\|synonymes\}\}\s*=+')
_title = re.compile(r'^=+\s*=+')
_word = re.compile(r'^\*\s*\[\[(.+?\|)?(?P<word>.+?)\]\]')

words = set()
relations = set()

def processPage(page):

    if page.ns == 0:

        keepWords = False
        lang = 'fr'

        for line, on, _ in wikidump.matchOnLines(page.text):

            if on(_synonyms):
                keepWords = True
            elif on(_lang):
                lang = _('lang')
            elif on(_title):
                keepWords = False

            if keepWords and lang == 'fr' and on(_word):
                words.add(page.title)
                words.add(_('word'))
                relations.add(tuple(sorted([page.title, _('word')])))

if __name__ == '__main__':

    if len(sys.argv) != 1:
        print('Usage: input | {}'.format(sys.argv[0].split(os.sep)[-1]))
        sys.exit(1)

    wikidump.parseWithCallback(processPage)

    print('words', len(words))
    print('relations', len(relations))
