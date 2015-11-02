#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Users v0.1
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
	print 'Users 0.1'
	print '(C) 2011 Arkanosis'
	print 'jroquet@arkanosis.net'
	print

	if len(sys.argv) != 2:
		print 'Usage: users.py <nbUsers>'
		sys.exit(1)

	date = datetime.datetime.now()
	logger = logging.getLogger('ArkbotLogger')
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%H:%M:%S')
	logger.setLevel(logging.INFO)

	bot = arkbot.Arkbot(arkbot._botName, arkbot._wiki, logger)
	try:
		bot.login(getpass.getpass('Bot password ? '))
		for user in bot.users(aulimit=sys.argv[1], auprop='blockinfo|groups|editcount'):
			if user.blockedby:
				groups = '—'
				if user.groups:
					groups = user.groups
				print '%s ||@|| %s ||@|| %s ||@|| %s ||@|| %d' % (user.blockedby.encode('utf-8'), user.name.encode('utf-8'), user.blockreason.encode('utf-8'), groups, user.editcount)
			#print u' || '.join(tuple((_str(property) for property in (user.name, user.groups, user.editcount, user.blockedby))))

		bot.logout()

	except (arkbot.ArkbotException), e:
		print e
		sys.exit(2)
