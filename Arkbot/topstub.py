#! /bin/env python2.7
# -*- coding: utf-8 -*-

# TopStub v0.1
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

_resultPage = 'Utilisateur:Arkbot/Ébauches dans le top 1000'
_source = 'http://stats.grok.se/fr/top au 200912'

_stub = re.compile('\{.{1,3}bauche', re.UNICODE)

if __name__ == '__main__':
	print 'TopStub 0.1'
	print '(C) 2010 Arkanosis'
	print 'arkanosis@gmail.com'
	print

	if len(sys.argv) != 2:
		print 'Usage: topstub.py <fichier>'
		sys.exit(1)

	date = datetime.datetime.now()
	logger = logging.getLogger('ArkbotLogger')
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%H:%M:%S')
	logger.setLevel(logging.INFO)

	bot = arkbot.Arkbot(arkbot._botName, arkbot._wiki, logger)
	try:
		bot.login(getpass.getpass('Bot password ? '))

		stubs = ''

		n = 2
                with open(sys.argv[1]) as articles:
			for article in articles.readlines()[2:]:
				n += 1
				try:
					page = bot.read(article)
					if not article.startswith('Spécial') and not article.startswith('Special') and not article.startswith('Portail') and not article.startswith('Aide') and not article.startswith('Wikipédia') and not article.startswith('Http') and _stub.search(page):
						stubs += '# [[%s]] (%i)' % (article, n)
						print article.rstrip(), 'IS a stub ***********'
					else:
						print article.rstrip(), 'is not a stub'
				except:
					print 'Exception on', article
					pass

		bot.edit(_resultPage, 'Ébauches dans le top 1000', """
{{Mise à jour bot|Arkanosis}}

== Ébauches dans le top 1000 ==

Données extraites de %s

%s
""" % (_source, stubs))

		bot.logout()

	except (arkbot.ArkbotException), e:
		print e
		sys.exit(2)
