#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Rename v0.1
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

if __name__ == '__main__':
	print 'Rename 0.1'
	print '(C) 2011 Arkanosis'
	print 'jroquet@arkanosis.net'
	print

	if len(sys.argv) != 1:
		print 'Usage: rename.py'
		sys.exit(1)

	date = datetime.datetime.now()
	logger = logging.getLogger('ArkbotLogger')
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%H:%M:%S')
	logger.setLevel(logging.INFO)

	bot = arkbot.Arkbot(arkbot._botName, arkbot._wiki, logger)
	try:
		bot.login(getpass.getpass('Bot password ? '))
		bot.move('Projet:Portails/Articles sans portail/intro', 'Projet:Articles sans portail/intro', 'Déplacement de la liste des articles sans portail')
		bot.move('Projet:Portails/Articles sans portail', 'Projet:Articles sans portail', 'Déplacement de la liste des articles sans portail')
		bot.logout()

	except (arkbot.ArkbotException), e:
		print e
		sys.exit(2)
