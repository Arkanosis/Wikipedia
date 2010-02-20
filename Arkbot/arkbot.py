#! /bin/env python2.7
# -*- coding: utf-8 -*-

# Arkbot (prototype)
# (C) 2010 Arkanosis
# arkanosis@gmail.com

# Ce bot est un *prototype* pour Arkbot et n'est pas destiné à un usage en production
# http://github.com/Arkanosis/Wikipedia/Arkbot (prototype)
# http://trac-git.assembla.com/arkbot/ (version architecturée)

# Ce bot est mis à disposition sous licence MIT
# http://www.opensource.org/licenses/mit-license.php


# [ Tâches ]
# - Conversion des règles de Salebot vers Abusefilter
# - Décompte automatique des votes de Contorcet / Schultze avec publication des résultats sur une page donnée
# - Recherche de fautes d'orthographe / grammaire courantes, d'expressions non neutres...
# - Génération automatique et remplissage des infoboxes / catégories à partir du texte et des interwikis
# - Recherche des articles déblanchis et des bandeaux admissibilité / suppression retirés par IP / newbie
# - Revert de toutes les contributions d'un vandale / spammeur
# - Recherche de copyvio (cf. copyright.py dans pywikipedia et équivalents sur en)
# - Recherche de spam (liens externes sous ip ou nouvel utilisateur)
# - Lutte contre les vandales (cf. Salebot et équivalents sur en., IA...)

# [ Notes ]
# - action=render pour n'avoir que la page (pas les menus, header, footer...)

# [ Utile ]
# - http://www.mediawiki.org/wiki/Manual:Parameters_to_index.php
# - http://www.mediawiki.org/wiki/API

import getpass
import gzip
import json
import logging
import logging.handlers
import os
import re
import string
import StringIO
import sys
import subprocess
import tempfile
import urllib
import urllib2
import xml.dom.minidom

_botName = 'Arkbot'
_trainerName = 'Arkanosis'

_version = '0.1 pre-alpha'
_userAgent = 'Arkbot/' + _version

_signature = ' — [[Utilisateur:%s|%s]]&nbsp;<sup>[[Discussion utilisateur:%s|✉]]</sup>&nbsp;<small><span class="plainlinks">[http://github.com/Arkanosis/Wikipedia/tree/master/Arkbot/ <nowiki>[mes sources]</nowiki>]</span></small>' % (_botName, _botName, _trainerName) + ' %s %s %s à %s:%s (CET)'

_diff = 'vimdiff'

_lang = 'fr'
_wiki = '%s.wikipedia.org'
_apiUrl = '/w/api.php?assert=user&'
_rawUrl = '/w/index.php?'
_searchUrl = _rawUrl + 'title=Spécial:Recherche&search='

_maxApiRequest = 500

_monthName = [
	'janvier', 'février',  'mars',  'avril',  'mai',  'juin',  'juillet',  'août',  'septembre',  'octobre',  'novembre',  'décembre',
]

_getHeaders = {
	'Accept-encoding': 'gzip',
	'User-Agent': _userAgent,
}

_postHeaders = {
	'Content-type': 'application/x-www-form-urlencoded',
	'Accept': 'text/plain',
	'Accept-encoding': 'gzip',
	'User-Agent': _userAgent,
}

_internalLink = re.compile(r'\[\[[^\]]+\]\]')

_categoryNamespace = {
	'en': 'category',
	'fr': 'catégorie',
	# TODO dump the different values
}

class ArkbotException(Exception):
	def __init__(self, reason):
		super(ArkbotException, self).__init__(reason)

class HttpException(ArkbotException):
	def __init__(self, reason):
		super(HttpException, self).__init__(reason)

class ApiException(ArkbotException):
	def __init__(self, reason):
		super(ApiException, self).__init__(reason)

class PageNotFoundException(ArkbotException):
	def __init__(self, reason):
		super(PageNotFoundException, self).__init__(reason)

class BadPasswordException(ArkbotException):
	pass

class ApiResponse(object):
	def __init__(self, dictionary):
		entries = {}
		for item in dictionary:
			try:
				int(item)
				if isinstance(dictionary[item], dict):
					entries[item] = ApiResponse(dictionary[item])
				else:
					entries[item] = dictionary[item]
			except ValueError:
				if not item.startswith('__'):
					if isinstance(dictionary[item], dict):
						dictionary[item] = ApiResponse(dictionary[item])
					elif isinstance(dictionary[item], list):
						items = []
						for entry in dictionary[item]:
							if isinstance(entry, dict):
								items.append(ApiResponse(entry))
							else:
								items.append(entry)
						dictionary[item] = items
		self.__dict__ = dictionary
		self.__entries = entries

	def __getattr__(self, attribute):
		return None

	def __getitem__(self, key):
		return self.__dict__[key]

	def __repr__(self):
		return repr(self.__dict__)

	def values(self):
		return self.__entries.values()

class Arkbot(object):

	def __init__(self, name, site, logger):
		self.__logger = logger
		self.__name = name
		self.__connect(site)

	def __connect(self, site):
		self.__site = site
		self.__opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
		urllib2.install_opener(self.__opener)

	def __request(self, url, data=None, headers=_getHeaders, lang=_lang):
		try:
			self.__logger.debug('Requesting http://' + (self.__site % lang) + url)
			response = self.__opener.open(urllib2.Request('http://' + (self.__site % lang) + url,  data, headers))
			for header, value in response.headers.items():
				if header.lower() == 'content-encoding' and value == 'gzip':
					response = gzip.GzipFile(fileobj=StringIO.StringIO(response.read()))
					break
			return response # TODO response.close() somewhere?
		except urllib2.HTTPError, e:
			raise HttpException('%s: (on query "%s")' % (e.code, url))

	def __handleApiResponse(self, response, query, noReturn=False):
		jsonResponse = json.load(response)
		if not jsonResponse:
			if noReturn:
				return None
			raise PageNotFoundException('Page not found (on query "%s")' % query)
		apiResponse = ApiResponse(jsonResponse)
		if apiResponse.error:
			raise ApiException('%s: %s (on query "%s")' % (apiResponse.error.code, apiResponse.error.info, query))
		return apiResponse

	def __internalLinks(self, text):
		return [link[2:-2] for link in re.findall(_internalLink, text)]

	def __categories(self, links, lang):
		return filter(lambda link: link.startWith(_categoryNamespace[lang] + ':'), links)

	def __interWikis(self, links):
		return filter(lambda link: 0 < link.find(':') < 4 or link.startswith('simple:') or link.startswith('tokipona:'), links)

	def __recent(self, rclimit=10, *args, **kwargs):
		while rclimit > 0:
			query = 'action=query&list=recentchanges&'
			for arg in kwargs.items():
				query += '%s=%s&' % arg
			query += 'format=json&rclimit=%s' % min(int(rclimit), _maxApiRequest)
			response = self.__handleApiResponse(self.__request(_apiUrl + query.replace(' ', '_')), query)
			for change in response.recentchanges:
				yield change
			rclimit = int(rclimit) - _maxApiRequest
			kwargs['rcstart'] = response['query-continue'].recentchanges.rcstart

	def __diff(self, page, oldid, newid, lang=_lang):
		query = 'title=%s&diff=%s&oldid=%s' % (page.replace(' ', '_'), newid, oldid)
		document = xml.dom.minidom.parse(self.__request(_rawUrl + query, lang=lang))
		added, removed = [], []
		for diffLine in document.getElementsByTagName('td'):
			if diffLine.getAttribute('class').find('diff-addedline') != -1:
				if diffLine.firstChild:
					added.append(diffLine.firstChild.toxml().encode('utf8'))
			elif diffLine.getAttribute('class').find('diff-deletedline') != -1:
				if diffLine.firstChild:
					removed.append(diffLine.firstChild.toxml().encode('utf8'))

		def filterChanges(changes):
			filtered = []
			for change in changes:
				diffchanges = re.findall('<span class="diffchange">(.+?)</span>', change)
				if diffchanges:
					filtered += diffchanges
				else:
					filtered.append(change[5:-6])
			return filtered

		document.unlink()
		return filterChanges(added), filterChanges(removed)

	def __search(self, query, *args, **kwargs):
		query = query.replace(' ', '+')
		for arg in kwargs.items():
			query += '&%s=%s' % arg
		document = xml.dom.minidom.parse(self.__request(_searchUrl + query))
		results = []
		for unorderedList in document.getElementsByTagName('ul'):
			if unorderedList.getAttribute('class').find('mw-search-results') != -1:
				for result in unorderedList.getElementsByTagName('li'):
					results.append(result.firstChild.firstChild.nodeValue.encode('utf8'))
				break
		document.unlink()
		return results

	def __fetch(self, page, lang=_lang):
		return self.__request(_rawUrl + 'action=raw&title=' + page.replace(' ', '_'), lang=lang).read()

	def __get(self, action='query', *args, **kwargs):
		query = ''
		if action:
			query = 'action=%s&' % action
		for arg in kwargs.items():
			if arg[1]:
				query += '%s=%s&' % arg
		query += 'format=json'
		return self.__handleApiResponse(self.__request(_apiUrl + query.replace(' ', '_')), query).query

	def __post(self, noReturn=False, *args, **kwargs):
		kwargs['format'] = 'json'
		query = {}
		for parameter, value in kwargs.items():
			if kwargs[parameter]:
				query[parameter] = value
		query = urllib.urlencode(query)
		return self.__handleApiResponse(self.__request(_apiUrl, query, _postHeaders), query, noReturn=noReturn)

	def __shouldStop(self):
		response = self.__get(meta='userinfo', uiprop='hasmsg')
		if response.userinfo.anon is not None:
			return True
		return False

	def __confirm(self, page, oldText, newText, summary):
		def dumpVersion(text):
			with tempfile.NamedTemporaryFile(delete=False) as dump:
				dump.write(text)
				return dump.name
		old = dumpVersion(oldText)
		new = dumpVersion(newText)
		subprocess.call([_diff, old, new])
		while True:
			answer = raw_input('Edit "%s" with summary "%s"? ' % (page, summary))
			if answer == 'y':
				return True
			elif answer == 'n':
				return False
		os.unlink(old)
		os.unlink(new)

	def __clean(self, text):
		# TODO
		# http://wikipedia/art => art
		# [[foo_bar]] => [[foo bar]]
		# == foo === => == Foo ==
		# suppr. <ref>wikipedia</ref>
		# suppr [[autolien]] ou [[auto-redir]]
		# ajout <references /> si <ref>
		# {{ISBN}}
		# {{formatnum:}}
		# {{siècle}}
		# {{date}}
		# [[Image: // [[Fichier: ...
		# fixes.py et cosmetic_change.py de pywikipedia
		return text

	def login(self, password):
		apiResponse = self.__post(action='login', lgname=self.__name, lgpassword=password)
		if not apiResponse.login:
			raise ApiException('%s (on login)' % apiResponse)
		if apiResponse.login.result in ['NoName', 'NotExists', 'Illegal']:
			raise ApiException('Bad user name (on login)')
		if apiResponse.login.result in ['EmptyPass', 'WrongPass']:
			raise ApiException('Bad password (on login)')
		if apiResponse.login.result == 'Throttled':
			raise ApiException('Too many login attempts, please wait for %s seconds and retry (on login)' % apiResponse.login.wait)

	def logout(self):
		self.__post(action='logout', noReturn=True)

	def info(self, *pages):
		return self.__get(titles=string.join(pages, '|'))

	def read(self, page):
		return self.__fetch(page)

	def diff(self, page, oldid, newid):
		return self.__diff(page, oldid, newid)

	def edit(self, page, summary, text, minor=False, bot=False, oldText=None):
		text = self.__clean(text)
		summary = 'bot : ' + summary
		self.__logger.info('Editing page "%s" with summary "%s"' % (page, summary))
		if oldText and not self.__confirm(page, oldText, text, summary):
			self.__logger.info('  => edition not confirmed by user')
			return
		if self.__shouldStop():
			raise ApiException('The bot has been asked to stop editing the wiki, or is not logged in anymore')
		pageInfo = self.__get(titles=page, prop='info|revisions', intoken='edit').pages.values()[0]

		apiResponse = self.__post(action='edit', title=page, summary=summary, text=text, token=pageInfo.edittoken, basetimestamp=pageInfo.starttimestamp, minor=minor, bot=bot)
		if apiResponse.edit.result != 'Success':
			raise ApiException('Unable to edit page "%s" with summary "%s" and text "%s"' % (page, summary, text))

	def replace(self, page, pattern, replacement, summary=None, reason='', minor=False, bot=False, confirm=True):
		if not summary:
			summary = 'Remplacement de "%s" par "%s"' % (pattern, replacement)
			if reason:
				summary += ' (%s)' % reason
		self.__logger.info('Replacing "%s" with "%s" with summary "%s" on page %s"' % (pattern, replacement, summary, page))
		oldText = self.read(page)
		newText = re.sub(pattern, replacement, oldText)
		if newText == oldText:
			self.__logger.info('  => no change after replacement')
			return
		if not confirm:
			oldText = None
		self.edit(page, summary, newText, minor, bot, oldText)

	def append(self, page, summary, text, bot=False, confirm=True):
		self.__logger.info('Appending "%s" with summary "%s" on page %s"' % (text, summary, page))
		oldText = self.read(page)
		if oldText:
			if oldText[-1] != '\n':
				oldText += '\n\n'
			elif len(oldText) > 1 and oldText[-2] != '\n':
				oldText += '\n'
		newText = oldText + text
		if newText == oldText:
			self.__logger.info('  => no change after appending')
			return
		if not confirm:
			oldText = None
		self.edit(page, summary, newText, False, bot, oldText)

	def consolidate(self, page):
		text = {
			_lang: self.__fetch(page)
		}
		links = self.__internalLinks(text.values()[0])

		oldInterWikis = self.__interWikis(links)
		newInterWikis = oldInterWikis[:]

		# Consolidate interWikis, and fetch all texts
		while oldInterWikis:
			for interWiki in oldInterWikis:
				cut = interWiki.find(':')
				lang = interWiki[:cut]
				text[lang] = self.__fetch(interWiki[cut + 1:], lang)
				otherLinks = self.__internalLinks(text[lang])
				otherInterWikis = self.__interWikis(otherLinks)
				for otherInterWiki in otherInterWikis:
					if otherInterWiki not in newInterWikis and not otherInterWiki.startswith(_lang + ':'):
						newInterWikis.append(otherInterWiki)
			oldInterWikis = [interWiki for interWiki in newInterWikis if interWiki not in oldInterWikis]
		newInterWikis.sort()

		# Extract infoboxes
		# TODO iter on all texts, extract infoboxes if available, extract informations from the infoboxes

		# Extract categories
		# TODO iter on all texts, extract categories if available

		# Extract portals if availables
		# TODO iter on all texts, extract portals if available

		# Extract introduction paragraph if available
		# TODO iter on all texts, extract introduction paragraph, extract informations from the paragraph

		# Infer stub if applicable
		# TODO if the text is very short, add a stub banner with the correct theme (from the portals, then categories)

		# Insert informations
		# TODO rewrite the introduction paragraph
		# TODO add the infoboxes with the right values
		# TODO add the portals
		# TODO add the categories
		# TODO add the interwikis

		print newInterWikis

	def interwikis(self, page):
		return self.__interWikis(self.__internalLinks(self.__fetch(page)))

	def search(self, query, *args, **kwargs):
		self.__logger.info('Searching for "%s" with parameters %s' % (query, kwargs))
		return self.__search(query, *args, **kwargs)

	def recent(self, *args, **kwargs):
		return self.__recent(*args, **kwargs)

if __name__ == '__main__':
	print 'Arkbot %s (prototype)' % _version
	print '(C) 2009-2010 Arkanosis'
	print 'arkanosis@gmail.com'
	print

	login = False
	logger = logging.getLogger('ArkbotLogger')
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%H:%M:%S')
	logger.setLevel(logging.INFO)

	def addHandler(filename, level):
		handler = logging.handlers.TimedRotatingFileHandler('arkbot-%s.log' % filename, when='midnight', backupCount=100)
		handler.setFormatter(formatter)
		handler.setLevel(level)
		logger.addHandler(handler)

	addHandler('info', logging.INFO)
	addHandler('errors', logging.WARNING)

	handler = logging.StreamHandler()
	handler.setFormatter(formatter)
	handler.setLevel(logging.INFO)
	logger.addHandler(handler)

	for arg in sys.argv[1:]:
		if arg == '-login':
			login = True
		elif arg == '-debug':
			logger.setLevel(logging.DEBUG)
			addHandler('debug', logging.DEBUG)
		else:
			print 'Error: unknown option "%s"' % arg
			sys.exit(1)

	bot = Arkbot(_botName, _wiki, logger)
	logger.info('Starting')
	try:
		if login:
			logger.info('Logging in with user name %s' % _botName)
			bot.login(getpass.getpass('Bot password ? '))

		# TASKS
		#print bot.info('Compression de données', 'Pondération de contextes')
		#print bot.read('en:Data compression')
		#for result in bot.search('"charmant village"'):
		#	print result
		#bot.replace('Utilisateur:Arkbot/test', r'((^|\s)[t|T]ext)(\s|$)', r'\1e\3')
		#bot.replace('Utilisateur:Arkbot/test', r'(^|\W)[cC]harmant(\s+)village(\W|$)', r'\1village\3', reason='non neutre')

		#assert login, 'Login needed for replacement'
		#for result in bot.search('"charmant village"'):
		#	bot.replace(result, r'(^|\W)[cC]harmant(\s+)village(\W|$)', r'\1village\3', reason='non neutre')
		#bot.consolidate('Buddy Rogers (catcheur)')

		if login:
			logger.info('Logging out')
			bot.logout()
	except (ArkbotException), e:
		logger.error('%s' % e)
	logger.info('Finishing')

	logging.shutdown()
