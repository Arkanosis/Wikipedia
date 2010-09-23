#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

# CatDump v0.1
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

if __name__ == '__main__':
	print 'CatDump 0.1'
	print '(C) 2010 Arkanosis'
	print 'arkanosis@gmail.com'
	print

	recursive = False
	if '-R' in sys.argv:
		recursive = True
		sys.argv.remove('-R')

	if len(sys.argv) != 3:
		print 'Usage: catdump.py [-R] <category> <outputFile>'
		sys.exit(1)

	date = datetime.datetime.now()
	logger = logging.getLogger('ArkbotLogger')
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%H:%M:%S')
	logger.setLevel(logging.INFO)

	bot = arkbot.Arkbot(arkbot._botName, arkbot._wiki, logger)
	try:
		#bot.login(getpass.getpass('Bot password ? '))

		with open(sys.argv[2], 'w') as outputFile:
			for article in bot.articles(cmtitle=sys.argv[1], recurse=recursive, cmlimit=5000):
				outputFile.write(article.title.encode('utf8') + '\n')

		#bot.logout()

	except (arkbot.ArkbotException), e:
		print e
		sys.exit(2)
