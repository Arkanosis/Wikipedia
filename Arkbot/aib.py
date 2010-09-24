#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Aib v0.1
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

_entry = re.compile(r'^\s*\|\s*(.*?)\s*=\s*(.*?)\s*(?:\|.*)?$', re.MULTILINE)

def _emptyEntry(entry):
	return re.compile(r'^\|\s*%s\s*=\s*$' % entry, re.MULTILINE)

_mapping = {
	'Wappen':  'imageblason',
	'lat_deg':  'latitude',
	'lon_deg':  'longitude',
	'Fläche':  'superficie',
	'area':  'superficie',
	'PLZ':  'cp',
	'postal_code':  'cp',
	'Höhe': 'altitude',
	'elevation': 'altitude',
	'Vorwahl':  'indicatiftel',
	'Kfz':  'immatriculation',
	'Gemeindeschlüssel':  'codecomm',
	'Website':  'weblabel',
	'Bürgermeister':  'maire',
	'Partei':  'partis',
	'population': 'population',
	'Einwohner': 'population',
	'Stand': 'date-pop',
}

if __name__ == '__main__':
	print 'Aib 0.1'
	print '(C) 2010 Arkanosis'
	print 'arkanosis@gmail.com'
	print

	if len(sys.argv) != 2:
		print 'Usage: aib.py <pageNames>'
		sys.exit(1)

	date = datetime.datetime.now()
	logger = logging.getLogger('ArkbotLogger')
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%H:%M:%S')
	logger.setLevel(logging.INFO)

	bot = arkbot.Arkbot(arkbot._botName, arkbot._wiki, logger)
	try:
		bot.login(getpass.getpass('Bot password ? '))

		with open(sys.argv[1]) as pageNames:
			for pageName in pageNames:
				pageName = pageName.rstrip()
				page = bot.read(pageName)
				oldPage = page
				for interWiki in re.findall(arkbot._interWiki, page):
					if interWiki[1] == 'en':
						pageEn = bot.read(interWiki[2], lang='en')
						for entry in re.findall(_entry, pageEn):
							if entry[0] in _mapping:
								page = re.sub(_emptyEntry(_mapping[entry[0]]), '\g<0>' + entry[1], page)
				bot.edit(pageName, 'Remplissage automatique d\'infobox (test, surveillé par le dresseur)', page, oldText=oldPage)
				break

		bot.logout()

	except (arkbot.ArkbotException), e:
		print e
		sys.exit(2)
