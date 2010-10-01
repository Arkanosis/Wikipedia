#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Translations v0.1
# (C) 2010 Arkanosis
# arkanosis@gmail.com

# Ce script est mis à disposition sous licence MIT
# http://www.opensource.org/licenses/mit-license.php

import itertools
import re
import sys

def reg(exp):
    return re.compile(exp, re.UNICODE)

#_title = reg(r'<title>(?P<title>[^\(]+?(?:\((?P<translatable>.*?)\))?)<')
_title = reg(r'<title>(?P<title>[^\(]+?(?:\((?P<translatable>homonymie|film|album|France|rivière|groupe|roman|jeu vidéo|chanson|série télévisée)\))?)<')
_interWiki = reg(r'(\[\[(?P<lang>[a-z][a-z].?(?:x?-[^\]]+)?|simple|tokipona):(?P<name>[^\]\(]+?(?:\((?P<translation>.*?)\))?)\]\])')

if __name__ == '__main__':
	print 'Translations 0.1'
	print '(C) 2010 Arkanosis'
	print 'arkanosis@gmail.com'
	print

	if len(sys.argv) != 4:
		print 'Usage: translations.py <dump> <dumpLang> <otherLang1[,otherlang2[...]]>'
		sys.exit(1)

_lang = sys.argv[2]
_langs = sys.argv[3].split(',')

match = None
translatable = None

translations = {}

def select(translations):
    # TODO discard rare entries (threshold to be determined)
    # TODO discard empty entries
    # TODO discard entries where there is at most one term per language, the same for every language
    return translations

def pertinent(possibilities):
    string = ''
    for possibility, frequency in sorted(possibilities.items(), key=lambda x: x[1], reverse=True):
        if frequency > 10:
            string += '\'%s\', ' % possibility
    if string:
        return string[:-2]
    else:
        return ''

with open(sys.argv[1]) as dump:
    for line in dump:
        def on(reg):
            global match
            match = reg.search(line.rstrip())
            return match

        if on(_title):
            translatable = match.group('translatable')
            translations.setdefault(translatable, {})

        elif translatable and on(_interWiki):
            lang = match.group('lang')
            translation = match.group('translation')
            if lang in _langs and translation:
                translations[translatable].setdefault(lang, {})
                translations[translatable][lang][translation] = translations[translatable][lang].get(translation, 0) + 1

translations = select(translations)

print '['
for term, info in translations.items():
    if not info:
        continue
    print '  {'
    for lang, possibilities in itertools.chain([(_lang, { term: 1 })], info.items()):
        print '    \'%s\': [%s],' % (lang, pertinent(possibilities))
    print '  },'
print '];'
