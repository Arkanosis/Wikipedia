#! /bin/env python2.7
# -*- coding: utf-8 -*-

from __future__ import with_statement

import json
import httplib
import sys

if len(sys.argv) != 3:
    print 'Usage: creations.py <wiki> <username>'
    sys.exit(1)

wiki = sys.argv[1]
username = sys.argv[2]

print 'Créations de l\'utilisateur "%s" sur Wikipédia %s' % (username, wiki)

creations = []
redirects = []

connection = httplib.HTTPConnection(wiki + '.wikipedia.org')
ucstart = ''

while True:

    connection.request('GET', '/w/api.php?action=query&list=usercontribs&ucuser=' + username + '&uclimit=300&ucdir=older&format=json&ucnamespace=0&ucprop=title|flags|size' + ucstart)
    response = connection.getresponse()

    if response.status != 200:
        print 'Erreur %i lors du traitement de la requête' % response.status
        sys.exit(2)

    results = json.loads(response.read())

    for contribution in results['query']['usercontribs']:
        if 'new' in contribution:
            if contribution['size'] > 140: # heuristic: if it's smaller than a twitt, then this must be a redirect ;-)
                creations.append(contribution['title'])
            else:
                redirects.append(contribution['title'])

    if 'query-continue' not in results:
        break
    ucstart = '&ucstart=' + results['query-continue']['usercontribs']['ucstart']

connection.close()

print 'Articles créés (%i) :' % len(creations)
for creation in creations:
    print '\t' + creation

print 'Redirections créées (%i) :' % len(redirects)
for redirect in redirects:
    print '\t ' + redirect
