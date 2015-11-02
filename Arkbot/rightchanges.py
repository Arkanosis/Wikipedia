#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

# RightChanges v0.1
# (C) 2012 Arkanosis
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
	print 'RightChanges 0.1'
	print '(C) 2012 Arkanosis'
	print 'jroquet@arkanosis.net'
	print

	if len(sys.argv) != 2:
		print 'Usage: rightchanges.py <nbChanges>'
		sys.exit(1)

	date = datetime.datetime.now()
	logger = logging.getLogger('ArkbotLogger')
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%H:%M:%S')
	logger.setLevel(logging.INFO)

	bot = arkbot.Arkbot(arkbot._botName, arkbot._wiki, logger)
	try:
		bot.login(getpass.getpass('Bot password ? '))

		additions = []
		removals = []

		for rightchange in bot.logevents(letype='rights', lang='fr', lelimit=sys.argv[1], leprop='title|user|details|timestamp'):
			if rightchange.rights is None:
				rightchange.rights = arkbot.ApiResponse({
					'old': '',
					'new': 'sysop'
				})
			oldRights, newRights = set(rightchange.rights.old.replace(' ', '').split(',')), set(rightchange.rights.new.replace(' ', '').split(','))
			addedRights, removedRights = newRights - oldRights, oldRights - newRights
			if 'sysop' in addedRights:
				additions.append((rightchange.user.encode('utf-8'), rightchange.title.encode('utf-8'), rightchange.timestamp.encode('utf-8')))
			if 'sysop' in removedRights:
				removals.append((rightchange.user.encode('utf-8'), rightchange.title.encode('utf-8'), rightchange.timestamp.encode('utf-8')))

		print >> sys.stderr, '---'

		for rightchange in bot.logevents(letype='rights', lang='meta', lelimit=sys.argv[1], leprop='title|user|details|timestamp'):
			if rightchange.rights is None:
				rightchange.rights = arkbot.ApiResponse({
					'old': '',
					'new': 'sysop'
				})
			oldRights, newRights = set(rightchange.rights.old.replace(' ', '').split(',')), set(rightchange.rights.new.replace(' ', '').split(','))
			addedRights, removedRights = newRights - oldRights, oldRights - newRights
			if rightchange.title is None:
				print >> sys.stderr, 'Invalid: ', rightchange
				continue
			if rightchange.title.encode('utf-8').endswith('@frwiki'):
				if 'sysop' in addedRights:
					print >> sys.stderr, 'Add: ' + '|'.join((rightchange.user.encode('utf-8'), rightchange.title.encode('utf-8'), rightchange.timestamp.encode('utf-8')))
					additions.append((rightchange.user.encode('utf-8'), rightchange.title.encode('utf-8')[:-7], rightchange.timestamp.encode('utf-8')))
				if 'sysop' in removedRights:
					print >> sys.stderr, 'Del: ' + '|'.join((rightchange.user.encode('utf-8'), rightchange.title.encode('utf-8'), rightchange.timestamp.encode('utf-8')))
					removals.append((rightchange.user.encode('utf-8'), rightchange.title.encode('utf-8')[:-7], rightchange.timestamp.encode('utf-8')))

		print 'Sysoppages :'
		for addition in sorted(additions, key=lambda addition: addition[2], reverse=True):
			print '|'.join(addition)
		print 'Desysoppages :'
		for removal in sorted(removals, key=lambda removal: removal[2], reverse=True):
			print '|'.join(removal)

		bot.logout()

	except (arkbot.ArkbotException), e:
		print e
		sys.exit(2)
