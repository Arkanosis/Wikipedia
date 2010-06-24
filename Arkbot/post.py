#! /bin/env python2.7
# -*- coding: utf-8 -*-

# Post v0.1
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
	print 'Post 0.1'
	print '(C) 2010 Arkanosis'
	print 'arkanosis@gmail.com'
	print

	if len(sys.argv) != 3:
		print 'Usage: post.py <fichier> <page>'
		sys.exit(1)

	date = datetime.datetime.now()
	logger = logging.getLogger('ArkbotLogger')
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%H:%M:%S')
	logger.setLevel(logging.INFO)

	bot = arkbot.Arkbot(arkbot._botName, arkbot._wiki, logger)
	try:
		bot.login(getpass.getpass('Bot password ? '))
                #with open(sys.argv[1]) as f:
		#	bot.edit(sys.argv[2], 'Pages liées à aucun portail', f.read())
		bot.edit(sys.argv[2], 'Pages liées à aucun portail', """{{Mise à jour bot|Arkanosis}}

== Articles sans portail au 1{{er}} avril 2010 ==
# [[Utilisateur:Arkbot/Articles sans portail/xaa]]
# [[Utilisateur:Arkbot/Articles sans portail/xab]]
# [[Utilisateur:Arkbot/Articles sans portail/xac]]
# [[Utilisateur:Arkbot/Articles sans portail/xad]]
# [[Utilisateur:Arkbot/Articles sans portail/xae]]
# [[Utilisateur:Arkbot/Articles sans portail/xaf]]
# [[Utilisateur:Arkbot/Articles sans portail/xag]]
# [[Utilisateur:Arkbot/Articles sans portail/xah]]
# [[Utilisateur:Arkbot/Articles sans portail/xai]]
# [[Utilisateur:Arkbot/Articles sans portail/xaj]]
# [[Utilisateur:Arkbot/Articles sans portail/xak]]
# [[Utilisateur:Arkbot/Articles sans portail/xal]]
# [[Utilisateur:Arkbot/Articles sans portail/xam]]
# [[Utilisateur:Arkbot/Articles sans portail/xan]]
# [[Utilisateur:Arkbot/Articles sans portail/xao]]
# [[Utilisateur:Arkbot/Articles sans portail/xap]]
# [[Utilisateur:Arkbot/Articles sans portail/xaq]]
# [[Utilisateur:Arkbot/Articles sans portail/xar]]
# [[Utilisateur:Arkbot/Articles sans portail/xas]]
# [[Utilisateur:Arkbot/Articles sans portail/xat]]
# [[Utilisateur:Arkbot/Articles sans portail/xau]]
""")

		bot.logout()

	except (arkbot.ArkbotException), e:
		print e
		sys.exit(2)
