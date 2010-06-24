#! /bin/env python2.7
# -*- coding: utf-8 -*-

# Post v0.1
# (C) 2010 Arkanosis
# arkanosis@gmail.com

# http://github.com/Arkanosis/Wikipedia/Arkbot

# Ce script est mis à disposition sous licence MIT
# http://www.opensource.org/licenses/mit-license.php

import datetime
import getpass
import logging
import sys

import arkbot

_nbArticlesPerSubSection = 33
_nbArticlesPerSection = 99
_nbArticlesPerPage = 495

# TODO
# Publier dans
#   Projet:Portails/Articles sans portail/Palette (palette apposée à toutes les pages)

def publishPage(text, first, last, page):
	bot.edit('Utilisateur:Arkbot/test', 'Articles sans portail, %i à %i (page %i)' % (first, last, page), ("""{{Mise à jour bot|Arkanosis}}

== Articles sans portail (%i à %i) ==\n\nVous pouvez utiliser [[Utilisateur:Dr Brains/PagesSansBandeauDePortail.js|ce script]] pour ajouter rapidement des portails sur ces articles.\n\nDernière mise à jour le ~~~~~""" % (first, last)) + text + """

{{Palette Articles sans portail}}
""")

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

== Articles sans portail ==\n\nVous pouvez utiliser [[Utilisateur:Dr Brains/PagesSansBandeauDePortail.js|ce script]] pour ajouter rapidement des portails sur ces articles.\n\nDernière mise à jour le ~~~~~
"""
			model = """{{Méta palette de navigation
 | modèle    = Palette Articles sans portail
 | étatboîte = autocollapse
 | titre     = [[Projet:Portails/Articles sans portail|Articles sans portail]]
 | liste1    = """
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
					index += '\n# [[Projet:Portails/Articles sans portail/%i|%i à %i]]' % (pageNumber, startPage, number)
					model += '[[Projet:Portails/Articles sans portail/%i|%i à %i]]{{·}}' % (pageNumber, startPage, number)
					pageNumber += 1
					page = ''
					startPage = number + 1
				if not number % (2 * _nbArticlesPerPage):
					break
			if number >= startPage:
				if number >= startSection:
					page += '\n\n=== %i à %i ===\n\n<ol start="%i" style="-moz-column-count:3; column-count:3;">\n%s</ol>' % (startSection, number, startSection, section)
				publishPage(page, startPage, number, pageNumber)
				pageNumber += 1
		model = model[:-6] + """
}}"""
		bot.edit('Utilisateur:Arkbot/test', 'Articles sans portail, index', index)
		bot.edit('Utilisateur:Arkbot/test', 'Articles sans portail, palette', model)

		bot.logout()

	except (arkbot.ArkbotException), e:
		print e
		sys.exit(2)
