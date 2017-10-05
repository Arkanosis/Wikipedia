#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Post v0.1
# (C) 2010-2011 Arkanosis
# jroquet@arkanosis.net

# http://github.com/Arkanosis/Wikipedia/Arkbot

# Ce script est mis à disposition sous licence MIT
# http://www.opensource.org/licenses/mit-license.php

# TODO Ajouts de portail auto :
#  - sur les articles dont le titre est en .*(film.*)
#  - en faisant ressortir les catégories / infoboxes les plus présentes
# TODO généraliser le script pour publier n'importe quelle liste d'articles
#  - ./publishList.py -root 'Projet:Portails' -first 1 -last 127 -delay 10 -dump '3 novembre 2010' -subject 'Articles sans portail'
#  - ./publishList.py -root 'Projet:Relance' -first 1 -last 5 -delay 10 -dump '3 novembre 2010' -subject 'Articles rarement modifiés' -transform 'contrib'
# + faire des scripts shell pour chacune des lignes de paramètres fréquemment utilisées
# TODO accepter plusieurs fichiers en entrée (pour différentes sous pages : musique, acteurs), les traiter à la suite et générer une palette commune

import datetime
import getpass
import logging
import sys
import time

import arkbot
import utils

_secondsBetweenEdits = int(utils.getValue('delay', '1'))

def identity(line):
	return line

def link(line):
	if line[0] == '/':
		return '[[:%s]]' % line
	return '[[%s]]' % line

def contrib(line):
	parts = line.split(' || ')
	if parts[4] == 'homo':
		return False
	return '%s — {{a-court|%s}} ({{u\'|%s}})' % (parts[0], parts[2], parts[3])

def edits(line):
	parts = line.split(' || ')
	return '{{formatnum:%s}} — {{a-court|%s}}' % (parts[0], parts[1])

def editOrDebug(bot, page, summary, text, debug, minor=False, botEdit=False):
	# try:
	# 	parts = page.split('/')
	# 	nb = int(parts[-1])
	# 	oldPage = page
	# 	page = page.replace('Projet:Portails/', 'Projet:')
	# 	if debug:
	# 		print 'move', oldPage, page
	# 	else:
	# 		bot.move(oldPage, page, 'Déplacement de la liste des articles sans portail')
	# except Exception, e:
	# 	pass

	if debug:
		print 'Page: ', page
		print 'Summary: ', summary
		print 'Text: ', text
		print 'Minor: ', minor
		print 'bot: ', botEdit
	else:
		bot.edit(page, summary, text, minor, botEdit)

def publishPage(bot, dump, text, first, last, page, debug, firstPage, lastPage, root, summary, introPath):
	if page < firstPage:
		return
	print 'Mise à jour de la page %i sur %i (%i restantes) @%ippm' % (page, lastPage, lastPage - page, 60 / _secondsBetweenEdits)
	editOrDebug(bot, root + '/%i' % page, '%s au %s, %i à %i' % (summary, dump, first, last), ("""{{Mise à jour bot|Arkanosis}}

== %s (%i à %i) ==\n\n{{%s}}\n\nDernière mise à jour le ~~~~~ avec le dump du %s.""" % (summary, first, last, introPath, dump)) + text + """

{{Palette %s}}
""" % summary, debug, botEdit=True)
	time.sleep(_secondsBetweenEdits)

def clearPage(bot, dump, page, firstPage, lastPage, root, summary, introPath):
	if page < firstPage:
		return
	print 'Vidage de la page %i sur %i (%i restantes) @%ippm' % (page, lastPage, lastPage - page, 60 / _secondsBetweenEdits)
	editOrDebug(bot, root + '/%i' % page, '%s au %s, page vide' % (summary, dump), """{{Mise à jour bot|Arkanosis}}

{{%s}}\n\nDernière mise à jour le ~~~~~ avec le dump du %s.""" % (introPath, dump), debug, botEdit=True)
	time.sleep(_secondsBetweenEdits)

def noportal(bot, filename, dump, mode, debug):
	transform = link

	firstPage = int(utils.getValue('first', 1))
	lastPage = sys.maxint

	nbColumns = 3
	nbArticlesPerSection = 100
	nbSectionsPerPage = 5

	if mode == 1:
		firstPage = 1
		lastPage = 1
		root = 'Projet:Articles sans portail'
		subject = 'Articles sans portail'
	elif mode == 2:
		lastPage = 1
		root = 'Projet:Articles sans portail/Album musical'
		subject = 'Articles sans portail/Album musical'
	elif mode == 3:
		lastPage = 1
		root = 'Projet:Articles sans portail/Acteur'
		subject = 'Articles sans portail/Acteur'
	elif mode == 4:
		lastPage = 1
		root = 'Projet:Articles sans portail/Homonymies'
		subject = 'Articles sans portail/Homonymies'
	elif mode == 5:
		nbColumns = 1
		nbSectionsPerPage = 6
		nbArticlesPerSection = 50
		lastPage = 2
		root = 'Projet:Pages les moins modifiées'
		subject = 'Pages les moins modifiées'
		transform = contrib
	elif mode == 6:
		nbColumns = 1
		nbSectionsPerPage = 6
		nbArticlesPerSection = 50
		lastPage = 1
		root = 'Utilisateur:Arkbot/Pages les plus modifiées'
		subject = 'Pages les plus modifiées'
		transform = edits
	elif mode == 7:
		lastPage = 3
		root = 'Projet:Articles sans infobox'
		subject = 'Articles sans infobox'
	elif mode == 8:
		lastPage = 1
		root = 'Projet:Articles sans infobox/Album musical'
		subject = 'Articles sans infobox/Album musical'
	elif mode == 9:
		lastPage = 1
		root = 'Projet:Articles sans infobox/Acteur'
		subject = 'Articles sans infobox/Acteur'
	elif mode == 10:
		lastPage = 10
		root = 'Projet:Articles non liés depuis Wikidata'
		subject = 'Articles non liés depuis Wikidata'
		transform = identity
	elif mode == 11:
		lastPage = 1
		root = 'Utilisateur:Arkbot/Titres contenant une parenthèse non précédée d\'une espace'
		subject = 'Titres contenant une parenthèse non précédée d\'une espace'
	elif mode == 12:
		lastPage = 45
		root = 'Projet:Articles dont le nom est à vérifier'
		subject = 'Articles dont le nom est à vérifier'
	elif mode == 13:
		lastPage = 1
		root = 'Utilisateur:Arkbot/Homonymies à renommer'
		subject = 'Homonymies à renommer'
	elif mode == 14:
		lastPage = 5
		root = 'Utilisateur:Arkbot/Caractères spéciaux à vérifier'
		subject = 'Caractères spéciaux à vérifier'
	else:
		assert False, 'Invalid mode'

	summary = subject.split('/')[0]
	introPath = '../' + 'intro'

	nbArticlesPerSubSection = nbArticlesPerSection / nbColumns
	nbArticlesPerSection = nbColumns * nbArticlesPerSubSection
	nbArticlesPerPage = nbArticlesPerSection * nbSectionsPerPage

	if nbColumns > 1:
		columns = ' style="-moz-column-count:%i; column-count:%i;"' % (nbColumns, nbColumns)
	else:
		columns = ''
        
	with open(filename) as articles:
		page = ''
		model = """{{Méta palette de navigation
 | modèle     = Palette %s
 | titre      = [[%s|%s]]
 | styleliste = text-align:center
 | liste1     = {{liste horizontale|""" % (subject, root, summary)
		section = ''
		subSection = ''
		number = 0
		startPage = 1
		startSection = 1
		startSubSection = 1
		pageNumber = 1
		for article in articles:
			name = transform(article.rstrip())
			if not name:
				continue
			subSection += '<li>%s</li>\n' % name
			number += 1
			if not number % nbArticlesPerSubSection:
				section += '\n<!-- %i à %i -->\n\n%s' % (startSubSection, number, subSection)
				subSection = ''
				startSubSection = number + 1
			if not number % nbArticlesPerSection:
				page += '\n\n=== %i à %i ===\n\n<ol start="%i"%s>\n%s</ol>' % (startSection, number, startSection, columns, section)
				section = ''
				startSection = number + 1
			if not number % nbArticlesPerPage:
				publishPage(bot, dump, page, startPage, number, pageNumber, debug, firstPage, lastPage, root, summary, introPath)
				model += '\n* [[%s/%i|%i à %i]]' % (root, pageNumber, startPage, number)
				pageNumber += 1
				page = ''
				startPage = number + 1
				if pageNumber > lastPage:
					break
		if number >= startPage and pageNumber <= lastPage:
			if number >= startSection:
				if number % nbArticlesPerSubSection:
					section += '\n<!-- %i à %i -->\n\n%s' % (startSubSection, number, subSection)
				page += '\n\n=== %i à %i ===\n\n<ol start="%i"%s>\n%s</ol>' % (startSection, number, startSection, columns, section)
			publishPage(bot, dump, page, startPage, number, pageNumber, debug, firstPage, lastPage, root, summary, introPath)
			model += '\n* [[%s/%i|%i à %i]]' % (root, pageNumber, startPage, number)
			pageNumber += 1
	model += """
  }}
}}<noinclude>{{Documentation palette}}
[[Catégorie:Palette de navigation espace non encyclopédique|%s]]
</noinclude>""" % subject

	if lastPage != sys.maxint:
		for pageNumber in xrange(max(firstPage, pageNumber), lastPage + 1):
			clearPage(bot, dump, pageNumber, firstPage, lastPage, root, summary, introPath)

	if mode in [1, 4, 7, 8, 9, 10, 11, 12, 13]:
		editOrDebug(bot, 'Modèle:Palette %s' % subject, '%s au %s' % (summary, dump), model, debug, botEdit=True)

if __name__ == '__main__':
	print 'NoPortal 0.1'
	print '(C) 2010 Arkanosis'
	print 'jroquet@arkanosis.net'
	print

	dump = utils.getValue('dump')
	mode = int(utils.getValue('mode'))
	debug = utils.getOption('debug')

	if len(sys.argv) != 2:
		print 'Usage: noportal.py -dump <dumpDate> -mode <mode> [-debug] <fichier>'
		sys.exit(1)

	date = datetime.datetime.now()
	logger = logging.getLogger('ArkbotLogger')
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%H:%M:%S')
	logger.setLevel(logging.INFO)

	bot = arkbot.Arkbot(arkbot._botName, arkbot._wiki, logger)
	try:
		if not debug:
			bot.login(getpass.getpass('Bot password ? '))

		noportal(bot, sys.argv[1], dump, mode, debug)

		if not debug:
			bot.logout()

	except (arkbot.ArkbotException), e:
		print e
		sys.exit(2)
