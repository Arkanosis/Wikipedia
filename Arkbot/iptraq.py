#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Replica v0.1
# (C) 2010 Arkanosis
# jroquet@arkanosis.net

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

if __name__ == '__main__':
	print 'IpTraq 0.1'
	print '(C) 2010 Arkanosis'
	print 'jroquet@arkanosis.net'
	print

	if len(sys.argv) != 2:
		print 'Usage: iptraq.py <nbChanges>'
		sys.exit(1)

	date = datetime.datetime.now()
	logger = logging.getLogger('ArkbotLogger')
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%H:%M:%S')
	logger.setLevel(logging.INFO)

	bot = arkbot.Arkbot(arkbot._botName, arkbot._wiki, logger)
	try:
		bot.login(getpass.getpass('Bot password ? '))
		for change in bot.recent(rcnamespace=0, rctype='edit', rcshow='anon|!minor|!redirect', rclimit=sys.argv[1], rcprop='user|timestamp'):
			print change.user, change.timestamp

		bot.logout()

	except (arkbot.ArkbotException), e:
		print e
		sys.exit(2)
