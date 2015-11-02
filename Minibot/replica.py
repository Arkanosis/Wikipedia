#! /bin/env python2.7
# -*- coding: utf-8 -*-

# Minibot
# (C) 2010 Arkanosis
# jroquet@arkanosis.net

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

# The wiki that you want to copy from
sourceWiki = 'fr'

# The wikis that you want to copy to
destinationWikis = ['de', 'en', 'es', 'it', 'ja', 'nl', 'pl', 'pt', 'ru', 'sv']

# The page to copy
pageName = 'User:%s/iKiwi.js' % userName

###########################################################################################

_app = 'iKiwi 0.4 replica'
_version = '0.1 alpha 2'
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
	print 'Copying to', wiki,
	try:
		page = request(wiki, 'edit', '&titles=%s&prop=info|revisions&intoken=edit' % pageName)
		page = request(wiki, 'edit', '&title=%s' % pageName, src='index')
	except urllib2.HTTPError, e:
		if e.code == 404:
			page = ''
		else:
			print '→ ERROR'
			return

	# TODO handle options
	print '→ OK'

if not userName:
	print 'Please edit the script first to set the right configuration values'
	sys.exit(1)

print """%s (%s)
(C) 2010 Arkanosis
jroquet@arkanosis.net
""" % (_app, _userAgent)

response = request('fr', 'login', {'lgname': userName, 'lgpassword': getpass.getpass('Password for user %s? ' % userName)}, _post)
print response
if response['login']['result'] in ['NoName', 'NotExists', 'Illegal']:
	print 'Bad user name'
	sys.exit(2)
elif response['login']['result'] in ['EmptyPass', 'WrongPass']:
	print 'Bad password'
	sys.exit(2)
elif response['login']['result'] in ['Throttled']:
	print 'Too many login attempts, please wait for %s seconds and retry' % response['login']['wait']
	sys.exit(2)

print 'Copying from', sourceWiki
try:
	page = request(sourceWiki, 'raw', '&title=%s' % pageName, src='index')
except urllib2.HTTPError, e:
	print '→ ERROR: unable to read the source page'
	sys.exit(1)

print page

for wiki in destinationWikis:
	install(wiki)
