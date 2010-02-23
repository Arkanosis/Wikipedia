#! /bin/env python2.7
# -*- coding: utf-8 -*-

# SUL v0.1
# (C) 2010 Arkanosis
# arkanosis@gmail.com

# http://github.com/Arkanosis/Wikipedia/Arkbot

# Ce script est mis à disposition sous licence MIT
# http://www.opensource.org/licenses/mit-license.php

# TODO créer la page utilisateur
# TODO régler les préférences (français, signature, apparence...)
# TODO créer le monobook.js (pour les requêtes XHR notamment)

import datetime
import getpass
import logging
import sys

import arkbot
import wikipedia

if __name__ == '__main__':
	print 'SUL 0.1'
	print '(C) 2010 Arkanosis'
	print 'arkanosis@gmail.com'
	print

	if len(sys.argv) != 2:
		print 'Usage: sul.py <login>'
		sys.exit(1)

	date = datetime.datetime.now()
	logger = logging.getLogger('ArkbotLogger')
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%H:%M:%S')
	logger.setLevel(logging.INFO)

	bot = arkbot.Arkbot(sys.argv[1], arkbot._wiki, logger)
	try:
		bot.login(getpass.getpass('Bot password ? '))
		for version in wikipedia._wikis:
			bot.read('%s:Special:Version' % version)
		bot.logout()

	except (arkbot.ArkbotException), e:
		print e
		sys.exit(2)
