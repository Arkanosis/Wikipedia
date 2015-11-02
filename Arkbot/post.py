#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Post v0.1
# (C) 2010 Arkanosis
# jroquet@arkanosis.net

# http://github.com/Arkanosis/Wikipedia/Arkbot

# Ce script est mis à disposition sous licence MIT
# http://www.opensource.org/licenses/mit-license.php

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

if _mode == 1:
	_page = 'Projet:Pages en impasse/liste des pages en impasse'
	_summary = 'Pages en impasse au %s' % _dump
	_pages = 'en impasse'
elif _mode == 2:
	_page = 'Projet:Pages vides/liste des pages vides'
	_summary = 'Pages vides au %s' % _dump
	_pages = 'vides'
elif _mode == 3:
	_page = 'Utilisateur:Arkbot/Pages redirigeant hors de l\'espace de nom principal'
	_summary = 'Pages redirigeant hors de l\'espace de nom principal au %s' % _dump
	_pages = 'redirigeant hors de l\'espace de nom principal'
else:
	print 'Unknown mode', _mode
	sys.exit(1)

if __name__ == '__main__':
	print 'Post 0.1'
	print '(C) 2010 Arkanosis'
	print 'jroquet@arkanosis.net'
	print

	if len(sys.argv) != 2:
		print 'Usage: post.py <fichier>'
		sys.exit(1)

	date = datetime.datetime.now()
	logger = logging.getLogger('ArkbotLogger')
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%H:%M:%S')
	logger.setLevel(logging.INFO)

	bot = arkbot.Arkbot(arkbot._botName, arkbot._wiki, logger)
	try:
		if not _debug:
			bot.login(getpass.getpass('Bot password ? '))


                #with open(sys.argv[1]) as f:
		#	bot.edit(sys.argv[2], 'contribs47', f.read(), bot=True)
		#	bot.edit(sys.argv[2], '-contribs47', '.', bot=True)


		text = """{{Mise à jour bot|Arkanosis}}

== Pages %s ==\n\nDernière mise à jour le ~~~~~ avec le dump du %s.

""" % (_pages, _dump)
		with open(sys.argv[1]) as inputFile:
			for line in inputFile:
				text += '# [[:%s]]\n' % line.rstrip()

		if _debug:
			print(_page, _summary, text, True)
		else:
			bot.edit(_page, _summary, text, bot=True)
			bot.logout()

	except (arkbot.ArkbotException), e:
		print e
		sys.exit(2)
