#! /usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import os
import os.path
import requests
import urllib

_wikidata = 'http://www.wikidata.org/w/api.php?'
_commons = 'http://commons.wikimedia.org/w/api.php?'
_wmflabs = 'http://tools.wmflabs.org/autolist/download_query.php?'

_properties = {
	'instance-of': 'P31',
}

_entities = {
	'commune-of-france': 'Q484170',
}

class Properties(object):
	def __init__(self, claims):
		self.__claims = claims

	def __getitem__(self, claim):
		return self.__claims[_properties[claim]][0]['mainsnak']['datavalue']['value']

def request(site, **query):
	return requests.get(site + urllib.urlencode(query))

def search(property, entity):
	return request(_wmflabs,
		q='CLAIM[%s:%s]' % (property[1:], entity[1:])
	).content

def getProperties(country):
	return Properties(request(_wikidata,
		action='wbgetentities',
		ids=country,
		props='claims',
		languages='fr',
		format='json'
	).json['entities'].values()[0]['claims'])

continents = {}
for foo in sorted(list(csv.reader(search(
	_properties['instance-of'],
	_entities['commune-of-france']
).split('\n')[1:-1], delimiter='\t')), cmp=lambda x, y: cmp(x[1], y[1])):
	print foo
        sys.exit(42)
	print 'Getting information on %s (%s)' % (country, entity)
	properties = getProperties(entity)
	try:
		continent = str(properties['continent']['numeric-id'])
		countries = continents.get(continent, '')
		iso3166 = properties['iso-3166'].encode('utf-8').lower()
		itue164 = properties['itu-e164'][1:].encode('utf-8')
		flag = properties['flag'].encode('utf-8')
	except KeyError:
		continue
