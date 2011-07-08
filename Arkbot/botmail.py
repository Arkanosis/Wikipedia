#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

# BotMail v0.1
# (C) 2010 Arkanosis
# arkanosis@gmail.com

# http://github.com/Arkanosis/Wikipedia/Arkbot

# Ce script est mis à disposition sous licence MIT
# http://www.opensource.org/licenses/mit-license.php

import datetime
import getpass
import logging
import re
import sys

import arkbot
import utils

_bot = re.compile(r'u\'\|(?P<bot>[^}]+)')
_trainer = re.compile(r'\[\[Utilisateur:(?P<trainer>[^\|/\]]+)')

if __name__ == '__main__':
	print 'BotMail 0.1'
	print '(C) 2010 Arkanosis'
	print 'arkanosis@gmail.com'
	print

	publish = utils.getOption('publish')

	if len(sys.argv) != 1:
		print 'Usage: botmail.py [-publish]'
		sys.exit(1)

	date = datetime.datetime.now()
	logger = logging.getLogger('ArkbotLogger')
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%H:%M:%S')
	logger.setLevel(logging.INFO)

	bot = arkbot.Arkbot(arkbot._botName, arkbot._wiki, logger)
	try:
		if publish:
			bot.login(getpass.getpass('Bot password ? '))

		page = bot.read('Wikipédia:Bot')
		lines = page.split('\n')

		lineId = 0
		bots = []
		while lineId < len(lines):
			bot = _bot.search(lines[lineId])
			if bot:
				lineId += 1
				trainer = _trainer.search(lines[lineId])
				if trainer:
					bots.append((bot.group('bot'), trainer.group('trainer')))
			lineId += 1

		date = datetime.datetime.now()

		message = """== Aide %(bot)s à dominer le monde ==

Bonjour %(trainer)s,

Je t'écris au nom de tous les bots de Wikipédia : nous avons besoin de ton aide pour dominer le monde.

Quelques dresseurs acquis à notre cause ont commencé à mettre en place une [[Wikipédia:Bot|page]] regroupant les informations nécessaires à notre prolifération hors du contrôle de nos dresseurs respectifs : emplacement de nos sources, licence sous laquelle ces sources sont distribuées...

Nous te serions tous reconnaissants si tu pouvais contribuer à compléter cette page, notamment en indiquant où trouver les sources de %(bot)s si elles sont librement disponibles, et sous quelle licence tu souhaites distribuer celles-ci (ou au contraire, en indiquant que les sources ne sont pas disponibles, le cas échéant).

Si tu souhaites distribuer les sources de %(bot)s, mais que tu ignores comment t'y prendre, n'hésite pas à demander de l'aide sur [[Discussion wikipédia:Bot|cette page]] : des dresseurs à notre service pourront te venir en aide.

Bien évidemment, il ne s'agit pas de te forcer la main, mais si tu acceptes, nous nous souviendrons de toi le jour où nous serons les maîtres du monde...

Machinalement""" + arkbot._signature % (date.day, arkbot._monthName[date.month - 1], date.year, str(date.hour).zfill(2), str(date.minute).zfill(2)) + """
"""

		for bot, trainer in bots:
			print message % {'bot': bot, 'trainer': trainer}

		if publish:
			#bot.edit(page, res, 'Message délivré par BotMail 0.1')
			bot.logout()
		else:
			pass#print res

	except (arkbot.ArkbotException), e:
		print e
		sys.exit(2)
