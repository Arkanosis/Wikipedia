#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

# CopyTraq v0.2
# (C) 2010-2011 Arkanosis
# arkanosis@gmail.com

# http://github.com/Arkanosis/Wikipedia/Arkbot

# Ce script est mis à disposition sous licence MIT
# http://www.opensource.org/licenses/mit-license.php

import datetime
import getpass
import logging
import subprocess
import sys

import arkbot
import utils

_webBrowser = 'firefox'
_diffUrl = 'https://fr.wikipedia.org/w/index.php?title=%s&diff=%s&oldid=%s'

if __name__ == '__main__':
	print 'CopyTraq 0.2'
	print '(C) 2010 Arkanosis'
	print 'arkanosis@gmail.com'
	print

	botflag = utils.getOption('botflag')

	timestamp = '2000-01-01T00:00:00Z'
	if len(sys.argv) == 3:
		timestamp = sys.argv[-1]
		sys.argv.remove(timestamp)

	if len(sys.argv) != 2:
		print 'Usage: copytraq.py [-botflag] <nbChanges> [timestamp]'
		sys.exit(1)

	date = datetime.datetime.now()
	logger = logging.getLogger('ArkbotLogger')
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%H:%M:%S')
	logger.setLevel(logging.INFO)

	bot = arkbot.Arkbot(arkbot._botName, arkbot._wiki, logger)
	try:
		if botflag:
			bot.login(getpass.getpass('Bot password ? '))

		print 'Keys:'
		print ' s: show diff'
		print ' p: pass'
		print ' r: restart'
		print ' q: quit'
		print

		while True:
			progress = utils.ProgressBar(int(sys.argv[1]))
			print
			progress.update(0, '[0]')

			changes = []
			for changeId, change in enumerate(bot.recent(rcnamespace=0, rcshow='anon|!redirect|!bot', rclimit=sys.argv[1], rcprop='title|ids|sizes|user|timestamp', rcend=timestamp)): # !patrolled
				if changeId == 0:
					timestamp = change.timestamp
				if change.newlen - change.oldlen > 500:
					added, _ = bot.diff(change.title.encode('utf8'), change.old_revid, change.revid)
					if added:
						longestAddition = max(len(add) for add in added)
						if longestAddition > 300:
							changes.append(change)
				progress.update(changeId + 1, '[%d] %s' % (len(changes), utils.fancyTime(change.timestamp)))

			print
			print 'Last timestamp is', timestamp
			print

			for changeId, change in enumerate(changes):
				print '[%d / %d] %s | %s | %s (+%s) [s/p/q] ' % (changeId + 1, len(changes), utils.fancyTime(change.timestamp), change.user, change.title, change.newlen - change.oldlen),
				while True:
					action = utils.getch()
					if action == 's':
						subprocess.call([_webBrowser, _diffUrl % (change.title, change.revid, change.old_revid)])
					elif action == 'q':
						sys.exit(0)
					elif action != 'p':
						continue
					print
					break

			print 'Restart? [r/q] ',
			while True:
				action = utils.getch()
				if action == 'r':
					print
					break
				elif action == 'q':
					sys.exit(0)

		if botflag:
			bot.logout()

	except (arkbot.ArkbotException), e:
		print e
		sys.exit(2)
