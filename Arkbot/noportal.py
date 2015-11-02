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

_dump = utils.getValue('dump')
_mode = int(utils.getValue('mode'))
_debug = utils.getOption('debug')

_secondsBetweenEdits = int(utils.getValue('delay', '5'))

_firstPage = int(utils.getValue('first', 1))
_lastPage = sys.maxint

_nbColumns = 3
_nbArticlesPerSection = 100
_nbSectionsPerPage = 5

_subPage = False

if _debug:
	_secondsBetweenEdits = .1

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

_transform = link

if _mode == 1:
	_firstPage = 1
	_lastPage = 1
	_root = 'Projet:Articles sans portail'
	_subject = 'Articles sans portail'
elif _mode == 2:
	_lastPage = 1
	_root = 'Projet:Articles sans portail/Album musical'
	_subject = 'Articles sans portail/Album musical'
elif _mode == 3:
	_lastPage = 1
	_root = 'Projet:Articles sans portail/Acteur'
	_subject = 'Articles sans portail/Acteur'
elif _mode == 4:
	_lastPage = 1
	_root = 'Projet:Articles sans portail/Homonymies'
	_subject = 'Articles sans portail/Homonymies'
elif _mode == 5:
	_nbColumns = 1
	_nbSectionsPerPage = 6
	_nbArticlesPerSection = 50
	_lastPage = 2
	_root = 'Projet:Pages les moins modifiées'
	_subject = 'Pages les moins modifiées'
	_transform = contrib
elif _mode == 6:
	_nbColumns = 1
	_nbSectionsPerPage = 6
	_nbArticlesPerSection = 50
	_lastPage = 1
	_root = 'Utilisateur:Arkbot/Pages les plus modifiées'
	_subject = 'Pages les plus modifiées'
	_transform = edits
elif _mode == 7:
	_lastPage = 3
	_root = 'Projet:Articles sans infobox'
	_subject = 'Articles sans infobox'
elif _mode == 8:
	_lastPage = 1
	_root = 'Projet:Articles sans infobox/Album musical'
	_subject = 'Articles sans infobox/Album musical'
elif _mode == 9:
	_lastPage = 1
	_root = 'Projet:Articles sans infobox/Acteur'
	_subject = 'Articles sans infobox/Acteur'
elif _mode == 10:
	_lastPage = 10
	_root = 'Projet:Articles non liés depuis Wikidata'
	_subject = 'Articles non liés depuis Wikidata'
	_transform = identity
elif _mode == 11:
	_lastPage = 1
	_root = 'Utilisateur:Arkbot/Titres contenant une parenthèse non précédée d\'une espace'
	_subject = 'Titres contenant une parenthèse non précédée d\'une espace'
elif _mode == 12:
	_lastPage = 45
	_root = 'Projet:Articles dont le nom est à vérifier'
	_subject = 'Articles dont le nom est à vérifier'
elif _mode == 13:
	_lastPage = 1
	_root = 'Utilisateur:Arkbot/Homonymies à renommer'
	_subject = 'Homonymies à renommer'
elif _mode == 14:
	_lastPage = 4
	_root = 'Utilisateur:Arkbot/Caractères spéciaux à vérifier'
	_subject = 'Caractères spéciaux à vérifier'
else:
	assert False, 'Invalid mode'

if _subPage:
	_rootPage = _root + '/' + _subject
else:
	_rootPage = _root

_summary = _subject.split('/')[0]
_introPath = '../' * (_subject.count('/') + 1) + 'intro'

if _nbColumns > 1:
	_columns = ' style="-moz-column-count:%i; column-count:%i;"' % (_nbColumns, _nbColumns)
else:
	_columns = ''

_nbArticlesPerSubSection = _nbArticlesPerSection / _nbColumns
_nbArticlesPerSection = _nbColumns * _nbArticlesPerSubSection
_nbArticlesPerPage = _nbArticlesPerSection * _nbSectionsPerPage

def editOrDebug(page, summary, text, minor=False, bot=False):
	# try:
	# 	parts = page.split('/')
	# 	nb = int(parts[-1])
	# 	oldPage = page
	# 	page = page.replace('Projet:Portails/', 'Projet:')
	# 	if _debug:
	# 		print 'move', oldPage, page
	# 	else:
	# 		_bot.move(oldPage, page, 'Déplacement de la liste des articles sans portail')
	# except Exception, e:
	# 	pass

	if _debug:
		print 'Page: ', page
		print 'Summary: ', summary
		print 'Text: ', text
		print 'Minor: ', minor
		print 'bot: ', bot
	else:
		_bot.edit(page, summary, text, minor, bot)

def publishPage(text, first, last, page):
	if page < _firstPage:
		return
	print 'Mise à jour de la page %i sur %i (%i restantes) @%ippm' % (page, _lastPage, _lastPage - page, 60 / _secondsBetweenEdits)
	editOrDebug(_rootPage + '/%i' % page, '%s au %s, %i à %i' % (_summary, _dump, first, last), ("""{{Mise à jour bot|Arkanosis}}

== %s (%i à %i) ==\n\n{{%s}}\n\nDernière mise à jour le ~~~~~ avec le dump du %s.""" % (_summary, first, last, _introPath, _dump)) + text + """

{{Palette %s}}
""" % _summary, bot=True)
	time.sleep(_secondsBetweenEdits)

def clearPage(page):
	if page < _firstPage:
		return
	print 'Vidage de la page %i sur %i (%i restantes) @%ippm' % (page, _lastPage, _lastPage - page, 60 / _secondsBetweenEdits)
	editOrDebug(_rootPage + '/%i' % page, '%s au %s, page vide' % (_summary, _dump), """{{Mise à jour bot|Arkanosis}}

{{%s}}\n\nDernière mise à jour le ~~~~~ avec le dump du %s.""" % (_introPath, _dump), bot=True)
	time.sleep(_secondsBetweenEdits)

if __name__ == '__main__':
	print 'NoPortal 0.1'
	print '(C) 2010 Arkanosis'
	print 'jroquet@arkanosis.net'
	print

	if len(sys.argv) != 2:
		print 'Usage: noportal.py -dump <dumpDate> -mode <mode> [-debug] <fichier>'
		sys.exit(1)

	date = datetime.datetime.now()
	logger = logging.getLogger('ArkbotLogger')
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%H:%M:%S')
	logger.setLevel(logging.INFO)

	_bot = arkbot.Arkbot(arkbot._botName, arkbot._wiki, logger)
	try:
		if not _debug:
			_bot.login(getpass.getpass('Bot password ? '))

                with open(sys.argv[1]) as articles:
			page = ''
			model = """{{Méta palette de navigation
 | modèle     = Palette %s
 | titre      = [[%s|%s]]
 | styleliste = text-align:center
 | liste1     = {{liste horizontale|""" % (_subject, _rootPage, _summary)
			section = ''
			subSection = ''
			number = 0
			startPage = 1
			startSection = 1
			startSubSection = 1
			pageNumber = 1
			for article in articles:
				name = _transform(article.rstrip())
				if not name:
					continue
				subSection += '<li>%s</li>\n' % name
				number += 1
				if not number % _nbArticlesPerSubSection:
					section += '\n<!-- %i à %i -->\n\n%s' % (startSubSection, number, subSection)
					subSection = ''
					startSubSection = number + 1
				if not number % _nbArticlesPerSection:
					page += '\n\n=== %i à %i ===\n\n<ol start="%i"%s>\n%s</ol>' % (startSection, number, startSection, _columns, section)
					section = ''
					startSection = number + 1
				if not number % _nbArticlesPerPage:
					publishPage(page, startPage, number, pageNumber)
					model += '\n* [[%s/%i|%i à %i]]' % (_rootPage, pageNumber, startPage, number)
					pageNumber += 1
					page = ''
					startPage = number + 1
					if pageNumber > _lastPage:
						break
			if number >= startPage and pageNumber <= _lastPage:
				if number >= startSection:
					if number % _nbArticlesPerSubSection:
						section += '\n<!-- %i à %i -->\n\n%s' % (startSubSection, number, subSection)
					page += '\n\n=== %i à %i ===\n\n<ol start="%i"%s>\n%s</ol>' % (startSection, number, startSection, _columns, section)
				publishPage(page, startPage, number, pageNumber)
				model += '\n* [[%s/%i|%i à %i]]' % (_rootPage, pageNumber, startPage, number)
				pageNumber += 1
		model += """
  }}
}}<noinclude>{{Documentation palette}}
[[Catégorie:Palette de navigation espace non encyclopédique|%s]]
</noinclude>""" % _subject

		if _lastPage != sys.maxint:
			for pageNumber in xrange(max(_firstPage, pageNumber), _lastPage + 1):
				clearPage(pageNumber)

		if _mode in [1, 4, 7, 8, 9, 10, 11, 12, 13]:
			editOrDebug('Modèle:Palette %s' % _subject, '%s au %s' % (_summary, _dump), model, bot=True)

		if not _debug:
			_bot.logout()

	except (arkbot.ArkbotException), e:
		print e
		sys.exit(2)
