#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

# WatchPage v0.1
# (C) 2011 Arkanosis
# jroquet@arkanosis.net

# http://github.com/Arkanosis/Wikipedia/Arkbot

# Ce script est mis à disposition sous licence MIT
# http://www.opensource.org/licenses/mit-license.php

import datetime
import getpass
import logging
import sys
import time

import dbus

import arkbot
import utils

if __name__ == '__main__':
	print 'WatchPage 0.1'
	print '(C) 2011 Arkanosis'
	print 'jroquet@arkanosis.net'
	print

	if len(sys.argv) != 3:
		print 'Usage: watchpage.py <page> <delay>'
		sys.exit(1)

	date = datetime.datetime.now()
	logger = logging.getLogger('ArkbotLogger')
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%H:%M:%S')
	logger.setLevel(logging.INFO)

	# http://library.gnome.org/devel/notification-spec/
	bus = dbus.SessionBus()
	notifier = dbus.Interface(bus.get_object('org.freedesktop.Notifications',
						 '/org/freedesktop/Notifications'),
				  dbus_interface='org.freedesktop.Notifications')

	bot = arkbot.Arkbot(arkbot._botName, arkbot._wiki, logger)
	try:
		lastId = 0
		while True:
			for page in bot.revisions(titles='Wikipédia:Demande de purge d\'historique', rvexcludeuser='Arkanosis'):
				revision = page.revisions[0]
				if revision.revid != lastId:
					lastId = revision.revid
					notifier.Notify('WatchPage', 0, '/data/compil/Wikipedia/Arkbot/data/Wikipedia-logo.svg', 'Nouvelle requête',
							'<b>%s</b> (%s)\n<i>%s</i>' % (revision.user, utils.fancyTime(revision.timestamp), revision.comment),
							[], {}, 2)
					print u'At %s: changed by %s at %s with comment “%s”' % (datetime.datetime.now(), revision.user, utils.fancyTime(revision.timestamp), revision.comment)
				else:
					print 'At %s: No change' % datetime.datetime.now()
			time.sleep(int(sys.argv[2]))

	except (arkbot.ArkbotException), e:
		print e
		sys.exit(2)
