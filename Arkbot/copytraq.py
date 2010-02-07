#! /bin/env python2.7
# -*- coding: utf-8 -*-

# CopyTraq v0.1
# (C) 2010 Arkanosis
# arkanosis@gmail.com

# http://github.com/Arkanosis/Wikipedia/Arkbot

# Ce script est mis à disposition sous licence MIT
# http://www.opensource.org/licenses/mit-license.php

# TODO accepter des dates du genre '5 minutes', '1 heure'... et des intervalles de temps

import datetime
import getpass
import logging
import sys

import arkbot

if __name__ == '__main__':
	print 'CopyTraq 0.1'
	print '(C) 2010 Arkanosis'
	print 'arkanosis@gmail.com'
	print

	if '-publish' in sys.argv:
		publish = True
		sys.argv.remove('-publish')
	else:
		publish = False
	if '-interactive' in sys.argv:
		interactive = True
		sys.argv.remove('-interactive')
	else:
		interactive = False

	if len(sys.argv) != 2:
		print 'Usage: votescrapper.py [-publish] [-interactive] <nbChanges>'
		sys.exit(1)

	date = datetime.datetime.now()
	logger = logging.getLogger('ArkbotLogger')
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%H:%M:%S')
	logger.setLevel(logging.INFO)

	bot = arkbot.Arkbot(arkbot._botName, arkbot._wiki, logger)
	try:
		if publish or interactive:
			bot.login(getpass.getpass('Bot password ? '))

		for change in bot.recent(rcnamespace=0, rcshow='anon|!redirect|!bot', rclimit=sys.argv[1], rcprop='title|ids|sizes|user'): # !patrolled
			if change.newlen - change.oldlen > 300:
				added, _ = bot.diff(change.title.encode('utf8'), change.old_revid, change.revid)
				if added:
					longestAddition = max(len(add) for add in added)
					if longestAddition > 1000:
						print longestAddition, 'http://fr.wikipedia.org/w/index.php?title=%s&diff=%s&oldid=%s' % (change.title, change.revid, change.old_revid), change.user

                res = ''
                # TODO Iterate on recent changes
                # Detect potential copyvio
                # Look for parts against some search engine
                # Discard potential sources that are known mirrord
                # Discard potential sources that refer to Wikipedia
                # Build a report with
                #  - link to the original
                #  - link to the addition
                #  - link to revert the addition
                #  - link to ask for an history cleanup

                # Interactive mode: open the potential sources in a web browser, revert automatically, and ask for an history cleanup automatically too

		if publish:
			bot.append('Discussion_utilisateur:' + arkbot._botName, res + 'Machinalement' + arkbot._signature % (date.day, arkbot._monthName[date.month - 1], date.year, date.hour, date.minute), 'Rapport de violations possibles de droits d\'auteur')
			bot.logout()
		elif interactive:
			bot.logout()
		else:
			print res

	except (arkbot.ArkbotException), e:
		print e
		sys.exit(2)
