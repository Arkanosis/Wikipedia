#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

# UserContribs v0.1
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

if __name__ == '__main__':
	print 'UserContribs 0.1'
	print '(C) 2010 Arkanosis'
	print 'jroquet@arkanosis.net'
	print

	if len(sys.argv) != 3:
		print 'Usage: usercontribs.py <userName> <nbContribs>'
		sys.exit(1)

	date = datetime.datetime.now()
	logger = logging.getLogger('ArkbotLogger')
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%H:%M:%S')
	logger.setLevel(logging.INFO)

	bot = arkbot.Arkbot(arkbot._botName, arkbot._wiki, logger)
	try:
		bot.login(getpass.getpass('Bot password ? '))
		for contrib in bot.contributions(ucuser=sys.argv[1], ucnamespace=0, uclimit=sys.argv[2], ucprop='title'):
			print contrib.title.encode('utf-8')

		bot.logout()

	except (arkbot.ArkbotException), e:
		print e
		sys.exit(2)
