#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

# VoteScrapper v0.2
# (C) 2010-2012 Arkanosis
# jroquet@arkanosis.net

# http://github.com/Arkanosis/Wikipedia/Arkbot

# Ce script est mis à disposition sous licence MIT
# http://www.opensource.org/licenses/mit-license.php

# TODO détecter les erreurs dans la page de vote
#  - un vote en * au lieu de #
#  - une personne qui vote deux fois
#  - une personne qui vote sans satisfaire les préconditions (n contributions, inscrit depuis t, ip, bloqué...)
#  - une personne qui oublie de signer
#  - une personne qui vote pour une option qui n'est pas proposée
# ... et proposer de les corriger automatiquement (uniquement quand lancé par Arkbot) et / ou envoyer un message à la personne suivant les cas
# idéal : vérifier dans l'historique qui a vraiment voté

# TODO gérer quand la signature n'est pas sur la même ligne que le vote
# TODO gérer les votes de Condorcet quand les puces sont des '#'
# TODO gérer les votes numériques, calculer moyenne, médianne, équart-type, interquartile, gérer les multiples en base heure (jours, semaines, mois, années...) et les nombres en toutes lettres

import collections
import copy
import datetime
import getpass
import itertools
import logging
import re
import sys

import arkbot
import utils

_title = re.compile(r'^(?P<level>=+) *(?P<title>[^=]+?) *(?P=level)$')
_user = r'((\[\[|{{)(:?w)?(:...?:)?([Dd]iscussion[ _])?[uU](tilisat(eur|rice)|ser)([ _][Tt]alk)?:\s*(?P<user>[^\|/]+)(/[^\|]+)?(\|.+)?(\]\]|}})|{{(?:[Nn]on signé|[Uu]\'?)\|\s*(?P<user2>[^}]+)}})'
_countVote = re.compile(r'FIXME^#[^:].*%s.*$' % _user, re.UNICODE)
_condorcetOption = re.compile(r'^\*\s*(\'\'\')?(?P<option>\w\w?)\s*[-–—:]\s*(\'\'\')?(?P<description>.+)')
_condorcetVote = re.compile(r'^(\*|#)(\s*<!--\[vote\])?(?P<vote>\s*[A-E]\s*([=,>/]+\s*\w\s*)*)(-->)?([^=,>/\w].*)?%s.*$' % _user, re.UNICODE)
_nonCondorcetVote = re.compile(r'^\*[^:].*%s.*$' % _user, re.UNICODE)
_deletedText = re.compile(r'<(?P<tag>del|s|strike|ref)>.*</(?P=tag)>', re.UNICODE)

_none = 'Z'

_sectionsToIgnore = [
]
_sectionsToHigher = [
]

def translate(string, translations):
	for term in translations:
		string = string.replace(term, translations[term])
	return string

def extractVotes(page):
	lines = page.split('\n')

	for line in xrange(len(lines)):
		lines[line] = re.sub(_deletedText, '', lines[line])

	line = 0

	options = {}
	options['A'] = 'Mettre par défaut des crochets autour des appels de notes'
	options['B'] = 'Mettre par défaut des parenthèses autour des appels de notes'
	options['C'] = 'Conserver les appels de notes sans caractères séparateurs (\'\'statu quo\'\')'
#	options['1'] = '30 septembre 2010 - soit la terminer immédiatement'
#	options['2'] = '30 septembre 2010 - soit pour un total d\'une semaine'
#	options['3'] = '7 octobre 2010 - soit pour un total de deux semaines'
#	options['4'] = '14 octobre 2010 - soit pour un total de trois semaines'
#	options['5'] = '23 octobre 2010 - soit pour un total d\'un mois'
#	options['6'] = '23 novembre 2010 - soit pour un total de deux mois'
#	options['7'] = 'jusqu\'à ce que le 1 050 000e article soit atteint - mais ne pourra pas dépasser le 7 novembre'
	titleStack = []
	votes = collections.OrderedDict()

	def addVotes(titleStack, nbVotes, condorcetVotes):
		if not nbVotes:
			return

		dic = votes
		for level in titleStack[:-1]:
			if level not in dic:
				dic[level] = collections.OrderedDict()
			dic = dic[level]
		if nbVotes > 0:
			dic[titleStack[-1]] = nbVotes
		elif nbVotes < 0:
			normalizedVotes = []
			#options[_none] = 'Aucune de ces propositions'
			condorcetOptions = sorted(options)
			for vote, user in condorcetVotes:
				separator = '>'
				for option in condorcetOptions:
					if vote.find(option) == -1:
						vote += ' %s %s' % (separator, option)
						separator = '='
				normalizedVotes.append((vote, user))

			dic[titleStack[-1]] = copy.deepcopy(options), normalizedVotes
			options.clear()
			global _countVote
			_countVote = re.compile(r'^#[^:].*%s.*$' % _user, re.UNICODE)

	onATitle = None
	while line < len(lines) and not onATitle:
		onATitle = _title.match(lines[line])
		line +=1
	nbVotes = 0
	while line < len(lines):
		while True:
			title = onATitle.group('title')
			level = len(onATitle.group('level'))

			if title in _sectionsToIgnore:
				print 'Ignoring', title
				while line < len(lines):
					line += 1
					onATitle = _title.match(lines[line])
					if onATitle and len(onATitle.group('level')) <= level:
						break
				continue
			elif title in _sectionsToHigher:
				print 'Highering', title
				level -= 1
			break

		while len(titleStack) >= level - 1:
			titleStack.pop()
		titleStack.append(title)

		oldNbVotes = nbVotes
		nbVotes = 0
		condorcetVotes = []

		while line < len(lines):

			onACountVote = _countVote.match(lines[line])
			if onACountVote:
				assert nbVotes >= 0, 'Mixed votes!'
				nbVotes += 1

				line +=1
				continue

			lines[line] = lines[line].replace('D, le', 'D')
			onACondorcetVote = _condorcetVote.match(lines[line])
			if onACondorcetVote:
				assert nbVotes <= 0, 'Mixed votes!'
				nbVotes -= 1
				vote = translate(onACondorcetVote.group('vote'), {
					',': '=',
					'/': '>',
					' ': '',
					'\t': '',
					'>': ' > ',
					'=': ' = ',
				}).upper().replace('D > D > D > D > D', 'D').replace('D = D = D = D = D', 'D').replace('C = C = C = C = C', 'C')
				while vote.find('>  > ') != -1:
					vote = vote.replace('>  >', '>')
				user = onACondorcetVote.group('user')
				if not user:
					user = onACondorcetVote.group('user2')
				user = user.rstrip()
				for option in vote.replace(' ', '').replace('>', '=').split('='):
					if option not in options:
						print '%s has voted %s in section %s, which is not a possible option (possibles options are %s)' % (user, option, titleStack, options.keys())
						vote = translate(vote, {
							option + ' > ': '',
							option + ' = ': '',
							' > ' + option: '',
							' = ' + option: '',
						}).replace(option, '')
				condorcetVotes.append((vote, user))

				line +=1
				continue

			onANonCondorcetVote = _nonCondorcetVote.match(lines[line])
			if onANonCondorcetVote and nbVotes < 0:
				nbVotes -= 1
				user = onANonCondorcetVote.group('user')
				if not user:
					user = onANonCondorcetVote.group('user2')
				print '%s has voted "none of this options" in section %s' % (user, titleStack)
				condorcetVotes.append((_none, user))

				line += 1
				continue

			onACondorcetOption = _condorcetOption.match(lines[line])
			if onACondorcetOption:
				assert nbVotes == 0, 'Condorcet option in a vote'
				options[onACondorcetOption.group('option')] = onACondorcetOption.group('description')

				line += 1
				continue

			onATitle = _title.match(lines[line])
			if onATitle:
				break

			line += 1

		line += 1
		addVotes(titleStack, nbVotes, condorcetVotes)

		if titleStack[-1] == "Groupe ''abusefilter'' dont les administrateurs":
			titleStack[-1] = "Total groupe ''abusefilter''"
			addVotes(titleStack, nbVotes + oldNbVotes, condorcetVotes)

	return votes

def results(votes, date, temp):
	def recResults(votes, level=3, title=''):
		result = ''
		for title, content in votes.items():
			try:
				int(content)
				continue
			except TypeError:
				pass
			#result += '=' * level + title + '=' * level + '\n'
			if False and isinstance(next(iter(content.values())), collections.OrderedDict):
				result += recResults(content, level + 1, title) + '\n'
			elif False and isinstance(content.values()[0], int):
				totalVotes = sum(content.values())
				result += """{| style="text-align:left; border:1px solid gray;"
|- {{ligne grise}}
|colspan="2"| \'\'\'%s\'\'\' ([[%s#%s|\'\'%s votes\'\']])
""" % (title, sys.argv[1], title.replace('\'\'\'', '').replace('\'\'', ''), totalVotes)
				votes = content.items()
				winner = max(votes, key=lambda x: x[1])[1]
				for option, nbVotes in votes:
					if nbVotes == winner:
						if option in ['Pour', 'Oui']:
							result += '|-{{ligne verte}}\n|\'\'\'%s : %s\'\'\'\n|{{Avancement|%.f}}\n' % (option, nbVotes, float(nbVotes) / totalVotes * 100)
						elif option in ['Contre', 'Non']:
							result += '|-{{ligne rouge}}\n|\'\'\'%s : %s\'\'\'\n|{{Avancement|%.f}}\n' % (option, nbVotes, float(nbVotes) / totalVotes * 100)
						elif option in ['Neutre', 'Neutre/Autres']:
							result += '|-{{ligne grise}}\n|\'\'\'%s : %s\'\'\'\n|{{Avancement|%.f}}\n' % (option, nbVotes, float(nbVotes) / totalVotes * 100)
						else:
							result += '|-{{ligne jaune}}\n|\'\'\'%s : %s\'\'\'\n|{{Avancement|%.f}}\n' % (option, nbVotes, float(nbVotes) / totalVotes * 100)
					else:
						result += '|-\n|%s : %s\n|{{Avancement|%.f}}\n' % (option, nbVotes, float(nbVotes) / totalVotes * 100)
				if tuple((vote[0] for vote in votes)) in [('Pour', 'Contre'), ('Pour', 'Neutre'), ('Contre', 'Neutre'), ('Pour', 'Contre', 'Neutre'), ('Pour', 'Contre', 'Neutre/Autres'), ('Oui', 'Non'), ('Oui', 'Neutre'), ('Non', 'Neutre'), ('Oui', 'Non', 'Neutre')]: # TODO faire plus simple
					result += '|-\n|colspan="2"|\n'
					if votes[1][0] in ['Neutre', 'Neutre/Autres']:
						votes[1] = ({ 'Pour': 'Contre', 'Contre': 'Pour', 'Oui': 'Non', 'Non': 'Oui' }[votes[0][0]], 0)
					ratio = float(votes[0][1]) / (votes[0][1] + votes[1][1]) * 100
					if ratio > 60:
						result += '|-{{ligne verte}}\n|\'\'\'%s / (%s + %s) \'\'\'\n|{{Avancement|%.f}}\n' % (votes[0][0], votes[0][0], votes[1][0], ratio)
					elif ratio < 60:
						result += '|-{{ligne rouge}}\n|\'\'\'%s / (%s + %s) \'\'\'\n|{{Avancement|%.f}}\n' % (votes[0][0], votes[0][0], votes[1][0], ratio)
					else:
						result += '|-{{ligne grise}}\n|\'\'\'%s / (%s + %s) \'\'\'\n|{{Avancement|%.f}}\n' % (votes[0][0], votes[0][0], votes[1][0], ratio)
				result += '|}\n'
			else:
				# TODO contrôler que personne n'a voté deux fois, si c'est le cas, ne pas prendre le vote en compte, et le marquer à côté
				# TODO déposer un message sur la PDD de ceux qui auraient voté plusieurs fois
				votes = content#.values()[0]
				condorcetVotes = []
				result += '{{boîte déroulante/début|titre=Votes normalisés ([[%s#%s|\'\'%s votes\'\']])}}\n' % (sys.argv[1], title.replace('\'\'\'', '').replace('\'\'', ''), len(votes[1]))
				for vote, user in votes[1]:
					result += '# %s | {{u\'|%s}}\n' % (vote, user)
					condorcetVotes.append({})
					rangs = vote.replace(' ', '').split('>')
					for valeur, rang in enumerate(rangs):
						for option in rang.split('='):
							condorcetVotes[-1][option] = valeur
				result += '{{boîte déroulante/fin}}\n'

				options = condorcetVotes[0].keys()
				options.sort()

				result += '{{boîte déroulante/début|titre=Décompte selon la [[méthode Condorcet]]}}\n'
				result += '\'\'Options possibles :\'\'\n'
				for option in options:
					result += '* %s — %s\n' % (option, votes[0][option])

				result += '\n\'\'Duels :\'\'\n'

				scores = {}
				maxScore = len(options) - 1
				for option in options:
					scores[option] = 0

				pairs = itertools.combinations(options, 2)

				for pair in pairs:
					result += ('* Duel entre %s et %s ' % pair)
					score = [0, 0, 0]
					for vote in condorcetVotes:
						if vote[pair[0]] < vote[pair[1]]:
							score[0] += 1
						elif vote[pair[0]] > vote[pair[1]]:
							score[1] += 1
						else:
							score[2] += 1
					if score[0] == score[1]:
						result += ('⇒ %s' % pair[score[0] < score[1]]) + (' (à %d contre %d, %d indifférents) ⇒ match nul\n' % (max(score[:-1]), min(score[:-1]), score[2]))
					else:
						result += ('⇒ %s' % pair[score[0] < score[1]]) + (' (à %d contre %d, %d indifférents)\n' % (max(score[:-1]), min(score[:-1]), score[2]))
					scores[pair[0]] += score[0] > score[1]
					scores[pair[1]] += score[0] < score[1]

				result += '{{boîte déroulante/fin}}\n'

				winners = filter(lambda option: scores[option] == maxScore, options)

				if winners:
					result += '\nVainqueurs potentiels :\n'
					for winner in winners:
						result += '* %s — %s\n' % (winner, votes[0][winner])
				else:
					result += '\nPas de vainqueur potentiel {{=/}}.\n'

		return result
#	while len(votes.items()) == 1:
#		votes = votes.values()[0]
	return '== Décompte%s des votes au %s %s %s à {{Heure|%s|%s}} ==\n' % (temp, date.day, arkbot._monthName[date.month - 1], date.year, str(date.hour).zfill(2), str(date.minute).zfill(2)) + recResults(votes)

if __name__ == '__main__':
	print 'VoteScrapper 0.2'
	print '(C) 2010 Arkanosis'
	print 'jroquet@arkanosis.net'
	print

	temp = utils.getOption('temp', ' \'\'\'provisoire\'\'\'', '')
	publish = utils.getOption('publish')
	test = utils.getOption('test')
	if test:
		publish = False
	reminder = utils.getOption('poll', ' (rappel : ceci \'\'n\'est pas\'\' une prise de décision)', '')

	if len(sys.argv) != 2:
		print 'Usage: votescrapper.py [-temp] [-poll] [-publish|-test] <Wikipédia:Page de vote>'
		sys.exit(1)

	date = datetime.datetime.now()
	logger = logging.getLogger('ArkbotLogger')
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%H:%M:%S')
	logger.setLevel(logging.INFO)

	bot = arkbot.Arkbot(arkbot._botName, arkbot._wiki, logger)
	try:
		if publish or test:
			bot.login(getpass.getpass('Bot password ? '))

		page = bot.read(sys.argv[1])
		votes = extractVotes(page)

		res = results(votes, date, temp) + 'Vous qui êtes humains, n\'oubliez pas de prendre en compte les commentaires de vote%s.\n\nMachinalement' % reminder + arkbot._signature % (date.day, arkbot._monthName[date.month - 1], date.year, str(date.hour).zfill(2), str(date.minute).zfill(2))

		if publish:
			bot.append('Discussion_' + sys.argv[1], 'Décompte %sdes votes' % temp, res)
			bot.logout()
		elif test:
			bot.edit('Utilisateur:Arkbot/test', 'Décompte %sdes votes (test)' % temp, res)
			bot.logout()
		else:
			print res

	except (arkbot.ArkbotException), e:
		print e
		sys.exit(2)
