#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Models v0.1
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
	print 'Models 0.1'
	print '(C) 2010 Arkanosis'
	print 'arkanosis@gmail.com'
	print

	if '-publish' in sys.argv:
		publish = True
		sys.argv.remove('-publish')
	else:
		publish = False

	if '-test' in sys.argv:
		test = True
		publish = False
		sys.argv.remove('-test')
	else:
		test = False

	if len(sys.argv) != 2:
		print 'Usage: models.py [-publish|-test] <category>'
		sys.exit(1)

	date = datetime.datetime.now()
	logger = logging.getLogger('ArkbotLogger')
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%H:%M:%S')
	logger.setLevel(logging.INFO)

	bot = arkbot.Arkbot(arkbot._botName, arkbot._wiki, logger)
	try:
		if publish or test:
			bot.login(getpass.getpass('Bot password ? '))

		for article in bot.articles(cmtitle=sys.argv[1], cmlimit=50000, cmprop='title'):
			res += '%s\n' % article

		if publish:
			bot.logout()
                elif test:
			bot.logout()
		else:
			print res

	except (arkbot.ArkbotException), e:
		print e
		sys.exit(2)
