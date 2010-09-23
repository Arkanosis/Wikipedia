#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Post v0.1
# (C) 2010 Arkanosis
# arkanosis@gmail.com

# http://github.com/Arkanosis/Wikipedia/Arkbot

# Ce script est mis à disposition sous licence MIT
# http://www.opensource.org/licenses/mit-license.php

# TODO Ajouts de portail auto :
#  - sur les articles dont le titre est en .*(film.*)
#  - en faisant ressortir les catégories / infoboxes les plus présentes

import datetime
import getpass
import logging
import sys
import time

import arkbot

_nbArticlesPerSubSection = 33
_nbArticlesPerSection = 99
_nbArticlesPerPage = 495

_secondsBetweenEdits = 30

_rootPage = 'Projet:Portails/Articles sans portail'
_dump = '15 septembre 2010'

_firstPage = 1
_lastPage = 137 # 189

def publishPage(text, first, last, page):
	if page < _firstPage:
		return
	print 'Mise à jour de la page %i sur %i (%i restantes) @%ippm' % (page, _lastPage, _lastPage - page, 60 / _secondsBetweenEdits)
	bot.edit(_rootPage + '/%i' % page, 'Articles sans portail au %s, %i à %i' % (_dump, first, last), ("""{{Mise à jour bot|Arkanosis}}

== Articles sans portail (%i à %i) ==\n\n{{../intro}}\n\nDernière mise à jour le ~~~~~ avec le dump du %s.""" % (first, last, _dump)) + text + """

{{Palette Articles sans portail}}
""", bot=True)
	time.sleep(_secondsBetweenEdits)

def clearPage(page):
	if page < _firstPage:
		return
	bot.edit(_rootPage + '/%i' % page, 'Articles sans portail au %s, page vide' % _dump, """{{Mise à jour bot|Arkanosis}}

{{../intro}}\n\nDernière mise à jour le ~~~~~ avec le dump du %s.""" % _dump, bot=True)
	time.sleep(_secondsBetweenEdits)

if __name__ == '__main__':
	print 'NoPortal 0.1'
	print '(C) 2010 Arkanosis'
	print 'arkanosis@gmail.com'
	print

	if len(sys.argv) != 2:
		print 'Usage: noportal.py <fichier>'
		sys.exit(1)

	date = datetime.datetime.now()
	logger = logging.getLogger('ArkbotLogger')
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%H:%M:%S')
	logger.setLevel(logging.INFO)

	bot = arkbot.Arkbot(arkbot._botName, arkbot._wiki, logger)
	try:
		bot.login(getpass.getpass('Bot password ? '))

                with open(sys.argv[1]) as articles:
			page = ''
			index = """{{Mise à jour bot|Arkanosis}}

== Articles sans portail ==\n\n{{/intro}}\n\nDernière mise à jour le ~~~~~ avec le dump du %s.
""" % _dump
			model = """{{Méta palette de navigation
 | modèle    = Palette Articles sans portail
 | étatboîte = autocollapse
 | titre     = [[%s|Articles sans portail]]
 | liste1    = """ % _rootPage
			section = ''
			subSection = ''
			number = 0
			startPage = 1
			startSection = 1
			startSubSection = 1
			pageNumber = 1
			for article in articles:
				number += 1
				subSection += '<li>[[%s]]</li>\n' % article.rstrip()
				if not number % _nbArticlesPerSubSection:
					section += '\n<!-- %i à %i -->\n\n%s' % (startSubSection, number, subSection)
					subSection = ''
					startSubSection = number + 1
				if not number % _nbArticlesPerSection:
					page += '\n\n=== %i à %i ===\n\n<ol start="%i" style="-moz-column-count:3; column-count:3;">\n%s</ol>' % (startSection, number, startSection, section)
					section = ''
					startSection = number + 1
				if not number % _nbArticlesPerPage:
					publishPage(page, startPage, number, pageNumber)
					index += '\n# [[%s/%i|%i à %i]]' % (_rootPage, pageNumber, startPage, number)
					model += '[[%s/%i|%i à %i]]{{·}}' % (_rootPage, pageNumber, startPage, number)
					pageNumber += 1
					page = ''
					startPage = number + 1
			if number >= startPage:
				if number >= startSection:
					page += '\n\n=== %i à %i ===\n\n<ol start="%i" style="-moz-column-count:3; column-count:3;">\n%s</ol>' % (startSection, number, startSection, section)
				publishPage(page, startPage, number, pageNumber)
				index += '\n# [[%s/%i|%i à %i]]' % (_rootPage, pageNumber, startPage, number)
				model += '[[%s/%i|%i à %i]]{{·}}' % (_rootPage, pageNumber, startPage, number)
				pageNumber += 1
		model = model[:-6] + """
}}"""

		for pageNumber in xrange(max(_firstPage, pageNumber), _lastPage + 1):
			clearPage(pageNumber)

		#bot.edit(_rootPage, 'Articles sans portail au %s' % _dump, index, bot=True)
		bot.edit('Modèle:Palette Articles sans portail', 'Articles sans portail au %s' % _dump, model, bot=True)

		bot.logout()

	except (arkbot.ArkbotException), e:
		print e
		sys.exit(2)
