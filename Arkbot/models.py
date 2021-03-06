#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Models v0.1
# (C) 2010 Arkanosis
# jroquet@arkanosis.net

# http://github.com/Arkanosis/Wikipedia/Arkbot

# Ce script est mis à disposition sous licence MIT
# http://www.opensource.org/licenses/mit-license.php

import datetime
import getpass
import logging
import sys

import arkbot
import utils

if __name__ == '__main__':
	print 'Models 0.1'
	print '(C) 2010 Arkanosis'
	print 'jroquet@arkanosis.net'
	print

	publish = utils.getOption('publish')
	test = utils.getOption('test')
	if test:
		publish = False

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
