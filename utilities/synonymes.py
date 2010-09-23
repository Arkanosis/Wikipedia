#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Synonymes v0.1
# (C) 2010 Arkanosis
# arkanosis@gmail.com

# http://github.com/Arkanosis/Wikipedia/utilities/synonymes.py

# Ce script est mis à disposition sous licence MIT
# http://www.opensource.org/licenses/mit-license.php

# Ce script extrait d'un dump du Wiktionnaire (en français) les synonymes (ou les antonymes)
# de tous les termes d'une catégorie (nom, verbe, adjectif...) ou de tous les termes
# Il ne prend pas en compte les thésaurus qui ne sont pas assez spécifiques (et de toutes façons peu nombreux)

import re
import sys

def reg(exp):
    return re.compile(exp, re.UNICODE)

_keepConsidering = reg(r'^\s*(?:\{\{(?:\(|-|\))\}\})?$')

#_link = reg(r'^(?:\*|\#)+\s*(?:\{\{(?:angl|anglicisme|archaïque|argot|contemporain|courant|dés|m-cour|pl-cour|familier|très familier|figuré|formel|gallicisme|hapax|hispanisme|hist|idotisme|informel|injurieux|ironique|littéraire|mélioratif|métaphore|néologisme|néo litt|péjoratif|poétique|populaire|proverbial|soutenu|rare|pl-rare|ex-rare|vieilli|vulgaire)(?:\|fr|\|nocat=oui)*\}\})?\s*\[\[[^\]]+\]\]')
_link = reg(r'^(?:\*|\#)+.*?\[\[[^\]]+\]\]')
_linkIter = reg(r'\[\[(?P<link>[^\]]+)\]\]')

_skippableNamespace = reg(r'^:?(?:Aide|Catégorie|Fichier|MediaWiki|Modèle|Portail|Projet|Référence|Wiktionnaire):')

_wordKind = 'adj|adv|aff|art|aux|conj|interf|interj|lettre|loc|nom|onoma|part|post|préf|prénom|prép|pronom|prov|racine|radical|sigle|sin|suf|symb|verb'
_skippableWordKind = reg(r'\{\{-(?:' + _wordKind + ')-')

_title = reg(r'<title>(?P<title>.*?)<')

if __name__ == '__main__':
	print 'Synonymes 0.1'
	print 'Extraction de synonymes, quasi-synonymes, antonymes...'
	print '(C) 2010 Arkanosis'
	print 'arkanosis@gmail.com'
	print

	if len(sys.argv) not in [3, 4]:
		print 'Usage: synonymes.py <dump> <syn|q-syn|ant> [wordKind]'
                print 'Values for wordKind are adj, adv... defaults to all'
		sys.exit(1)

consider = False
considerWords = False
match = None
title = ''
words = []

category = reg(r'\{\{-' + sys.argv[2] + r'-\}\}')

if len(sys.argv) == 4:
    wordKind = reg(r'\{\{-' + sys.argv[3] + r'-\|fr\}\}')
else:
    wordKind = reg(r'\{\{-(?:' + _wordKind + r')-\|fr\}\}')

def displayWords():
    global title, words
    if words:
        print '  <SynonymSet originalExpr="%s" lang="fr">' % title
        for word in words:
            print '    <Synonym alternativeExpr="%s"/>' % word
        print '  </SynonymSet>'
        title = ''
        words = []

with open(sys.argv[1]) as dump:
    for line in dump:
        def on(reg):
            global match
            match = reg.search(line.rstrip())
            return match

        if on(_title):
            displayWords()
            title = match.group('title')
            if _skippableNamespace.search(title):
                title = ''

        elif title:
            if considerWords and on(_link):
                for word in re.findall(_linkIter, line):
                    words.append(word)

            elif consider and on(category):
                considerWords = True

            elif on(_skippableWordKind):
                consider = on(wordKind)
                considerWords = False

            elif considerWords and not on(_keepConsidering):
                considerWords = False

    displayWords()
