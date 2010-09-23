#! /usr/bin/env python2.7
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
import time

import arkbot

if __name__ == '__main__':
	print 'Post 0.1'
	print '(C) 2010 Arkanosis'
	print 'arkanosis@gmail.com'
	print

	if len(sys.argv) != 3:
		print 'Usage: post.py <fichier> <page>'
		sys.exit(1)

	date = datetime.datetime.now()
	logger = logging.getLogger('ArkbotLogger')
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%H:%M:%S')
	logger.setLevel(logging.INFO)

	bot = arkbot.Arkbot(arkbot._botName, arkbot._wiki, logger)
	try:
		bot.login(getpass.getpass('Bot password ? '))


                #with open(sys.argv[1]) as f:
		#	bot.edit(sys.argv[2], 'contribs47', f.read(), bot=True)
		#	bot.edit(sys.argv[2], '-contribs47', '.', bot=True)



		# for page in ['', '/xaa', '/xab', '/xac', '/xad', '/xae', '/xaf', '/xag', '/xah', '/xai', '/xaj', '/xak', '/xal', '/xam', '/xan', '/xao', '/xap', '/xaq', '/xar', '/xas', '/xat', '/xau']:
		# 	bot.edit('Utilisateur:Arkbot/Articles sans portail%s' % page, 'Transformation en redirection vers [[Projet:Portails/Articles sans portail]]', '#REDIRECT[[Projet:Portails/Articles sans portail]]', bot=True)
		# 	time.sleep(6)


		_dump = '15 septembre 2010'
		text = """{{Mise à jour bot|Arkanosis}}

== Pages en impasse ==\n\nDernière mise à jour le ~~~~~ avec le dump du %s.

""" % _dump
		with open(sys.argv[1]) as inputFile:
			for line in inputFile:
				text += '# [[%s]]\n' % line.rstrip()
		bot.edit('Projet:Pages en impasse/liste des pages en impasse', 'Pages en impasse au %s' % _dump, text, bot=True)


		bot.logout()

	except (arkbot.ArkbotException), e:
		print e
		sys.exit(2)
