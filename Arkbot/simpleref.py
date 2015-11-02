#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

# SimpleRef v0.1
# (C) 2010 Arkanosis
# jroquet@arkanosis.net

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

_ref = re.compile(r'<ref((\s+group="(?P<group>[^"]+)")|(\s+name="(?P<name>[^"]+)")?)*>(?P<ref>.+?)</ref>', re.UNICODE)

if __name__ == '__main__':
	print 'SimpleRef 0.1'
	print '(C) 2010 Arkanosis'
	print 'jroquet@arkanosis.net'
	print

	publish = utils.getOption('publish')

	if len(sys.argv) != 2:
		print 'Usage: simpleref.py [-publish] <article>'
		sys.exit(1)

	date = datetime.datetime.now()
	logger = logging.getLogger('ArkbotLogger')
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%H:%M:%S')
	logger.setLevel(logging.INFO)

        page = sys.argv[1]

	bot = arkbot.Arkbot(arkbot._botName, arkbot._wiki, logger)
	try:
		if publish:
			bot.login(getpass.getpass('Bot password ? '))

		refs = {}

		oldText = bot.read(page)
                ref = _ref.search(oldText)
                if ref:
			key = ref.group('ref'), ref.group('group')
			if key in refs:
				print 'ref already found with name', refs[key]
			else:
				if ref.group('name'):
					name = ref.group('name')
				else:
					name = 'newname'
				print 'adding ref with name', name
				refs[key] = name

		if publish:
			bot.edit(page, res, 'Nettoyage des références')
			bot.logout()
		else:
			pass#print res

	except (arkbot.ArkbotException), e:
		print e
		sys.exit(2)
