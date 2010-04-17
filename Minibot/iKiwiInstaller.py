#! /bin/env python2.7
# -*- coding: utf-8 -*-

# Minibot
# (C) 2010 Arkanosis
# arkanosis@gmail.com

# http://github.com/Arkanosis/Wikipedia/Minibot

# Ce bot est mis à disposition sous licence MIT
# http://www.opensource.org/licenses/mit-license.php

import getpass
import gzip
import json
import re
import StringIO
import sys
import urllib
import urllib2

###########################################################################################
# Settings, change here
###########################################################################################

# The user name of your SUL account
userName = 'Arktest'

# The wikis you want iKiwi to be installed to
iKiwiDistantWikis = ['de', 'en', 'es', 'fr', 'it', 'ja', 'nl', 'pl', 'pt', 'ru', 'sv']

# If you want to add the articles to your watchlist after using iKiwi
iKiwiWatchMain = True

# If you want to add the any page to your watchlist after using iKiwi
iKiwiWatchOthers = True

###########################################################################################

_app = 'iKiwi 0.4 installer'
_version = '0.1 alpha'
_userAgent = 'Minibot/' + _version

_get = {
	'Accept-encoding': 'gzip',
	'User-Agent': _userAgent,
}

_post = {
	'Content-type': 'application/x-www-form-urlencoded',
	'Accept': 'text/plain',
	'Accept-encoding': 'gzip',
	'User-Agent': _userAgent,
}

_install = re.compile(r'\s*importScript\s*\(\s*(?P<quote>\'|")User:Arkanosis/iKiwi.js(?P=quote)\s*\)\s*;\s*')
_distantWikis = re.compile(r'\s*iKiwiDistantWikis\s+=\s+\[(\s*(?P<quote>\'|")[^\'"]+(?P=quote)\s*,?)*\s*\]\s*;\s*')
_iKiwiWatchMain = re.compile(r'\s*var\s+iKiwiWatchMain\s+=\s+(true|false)\s*;\s*')
_iKiwiWatchOthers = re.compile(r'\s*var\s+iKiwiWatchOthers\s+=\s+(true|false)\s*;\s*')

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
urllib2.install_opener(opener)

def request(wiki, action, parameters, mode='get', src='api'):
	def read(url, data, headers):
		return gzip.GzipFile(fileobj=StringIO.StringIO(opener.open(urllib2.Request(url, data, headers)).read()))

	url = 'http://%s.wikipedia.org/w/%s.php?' % (wiki, src)
	if mode == 'get':
		data = None
		parameters = 'action=%s&format=json' % action + parameters
		headers = _get
		if src == 'index':
			return read(url + parameters, data, headers).read()
	else:
		parameters.update({
			'action': action,
			'format': 'json',
		})
		data = urllib.urlencode(parameters)
		parameters = ''
		headers = _post
	return json.load(read(url + parameters, data, headers))

def install(wiki):
	print 'Installing on', wiki,
	try:
		monobook = request(wiki, 'raw', '&title=User:%s/monobook.js' % userName, src='index')
	except urllib2.HTTPError, e:
		if e.code == 404:
			monobook = ''
		else:
			print '→ ERROR'
			return

	installed = _install.search(monobook)
	if not installed:
		monobook += '\nimportScript(\'User:Arkanosis/iKiwi.js\');'

	# TODO handle options
	print '→ OK'

if not userName:
	print 'Please edit the script first to set the right configuration values'
	sys.exit(1)

print """%s (%s)
(C) 2010 Arkanosis
arkanosis@gmail.com
""" % (_app, _userAgent)

#response = request('fr', 'login', {'lgname': userName, 'lgpassword': getpass.getpass('Password for user %s? ' % userName)}, _post)
response = request('fr', 'login', {'lgname': userName, 'lgpassword': 'snpi3039'}, _post)
if response['login']['result'] in ['NoName', 'NotExists', 'Illegal']:
	print 'Bad user name'
	sys.exit(2)
elif response['login']['result'] in ['EmptyPass', 'WrongPass']:
	print 'Bad password'
	sys.exit(2)
elif response['login']['result'] in ['Throttled']:
	print 'Too many login attempts, please wait for %s seconds and retry' % response['login']['wait']
	sys.exit(2)

for wiki in iKiwiDistantWikis:
	install(wiki)
