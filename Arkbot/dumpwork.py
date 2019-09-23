#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# DumpWork v0.1
# (C) 2017-2019 Arkanosis
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
import noportal
import post
import utils

if __name__ == '__main__':
	print('DumpWork 0.1')
	print('(C) 2017-2019 Arkanosis')
	print('jroquet@arkanosis.net')
	print()

	dump = utils.getValue('dump')
	debug = utils.getOption('debug')

	if len(sys.argv) != 2:
		print('Usage: dumpWork.py <dump>')
		sys.exit(1)

	date = datetime.datetime.now()
	logger = logging.getLogger('ArkbotLogger')
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%H:%M:%S')
	logger.setLevel(logging.INFO)

	bot = arkbot.Arkbot(arkbot._botName, arkbot._wiki, logger)
	try:
		if not debug:
			bot.login(getpass.getpass('Bot password ? '))

		#post.post(bot, 'data/pagesEnImpasse-{}.txt'.format(sys.argv[1]), dump, 1, debug)
		post.post(bot, 'data/pagesVides-{}.txt'.format(sys.argv[1]), dump, 2, debug)
		post.post(bot, 'data/frwiki-ns_redirects-{}.txt'.format(sys.argv[1]), dump, 3, debug)

		noportal.noportal(bot, 'data/lastEdit-{}.txt'.format(sys.argv[1]), dump, 5, debug)
		#noportal.noportal(bot, 'data/mostEdit-{}.txt'.format(sys.argv[1]), dump, 6, debug)

		#noportal.noportal(bot, 'data/articlesSansPortail-musique-{}.txt'.format(sys.argv[1]), dump, 2, debug)
		#noportal.noportal(bot, 'data/articlesSansPortail-acteurs-{}.txt'.format(sys.argv[1]), dump, 3, debug)
		#noportal.noportal(bot, 'data/articlesSansPortail-homo-{}.txt'.format(sys.argv[1]), dump, 4, debug)
		noportal.noportal(bot, 'data/articlesSansPortail-{}.txt'.format(sys.argv[1]), dump, 1, debug)

		noportal.noportal(bot, 'data/articlesSansInfobox-musique-{}.txt'.format(sys.argv[1]), dump, 8, debug)
		noportal.noportal(bot, 'data/articlesSansInfobox-acteurs-{}.txt'.format(sys.argv[1]), dump, 9, debug)
		noportal.noportal(bot, 'data/articlesSansInfobox-{}.txt'.format(sys.argv[1]), dump, 7, debug)

		#noportal.noportal(bot, 'data/articlesACreer-{}.txt'.format(sys.argv[1]), dump, 10, debug)

		noportal.noportal(bot, 'data/frwiki-commercials-{}.txt'.format(sys.argv[1]), dump, 14, debug)

		if not debug:
			bot.logout()

	except (arkbot.ArkbotException) as e:
		print(e)
		sys.exit(2)
