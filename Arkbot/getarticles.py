#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

# GetArticles v0.1
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

if __name__ == '__main__':
#	print 'GetArticles 0.1'
#	print '(C) 2010 Arkanosis'
#	print 'jroquet@arkanosis.net'
#	print

	if len(sys.argv) < 2:
		print 'Usage: getarticles.py <article1> [article2 [...]]'
		sys.exit(1)

	date = datetime.datetime.now()
	logger = logging.getLogger('ArkbotLogger')
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%H:%M:%S')
	logger.setLevel(logging.INFO)

	bot = arkbot.Arkbot(arkbot._botName, arkbot._wiki, logger)
	try:
            for article in sys.argv[1:]:
                 print bot.read(article, followRedirect=True)

	except (arkbot.ArkbotException), e:
		print e
		sys.exit(2)
