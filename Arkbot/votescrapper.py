#! /bin/env python2.7
# -*- coding: utf-8 -*-

# VoteScrapper v0.2
# (C) 2010 Arkanosis
# arkanosis@gmail.com

# http://github.com/Arkanosis/Wikipedia/Arkbot

# Ce script est mis à disposition sous licence MIT
# http://www.opensource.org/licenses/mit-license.php

# TODO détecter les erreurs dans la page de vote
#  - un vote en * au lieu de #
#  - une personne qui vote deux fois
#  - une personne qui vote sans satisfaire les préconditions (n contributions, inscrit depuis t, ip, bloqué...)
# ... et proposer de les corriger automatiquement (uniquement quand lancé par Arkbot)
# idéal : vérifier dans l'historique qui a vraiment voté

# TODO envoyer un message aux gens qui n'ont pas voté pour toutes les questions (??? ; dans tous les cas, proposer au moins un opt-out à la badmood, sur la page du bot)

# TODO gérer quand la signature n'est pas sur la même ligne que le vote (5: pour)
# TODO gérer les votes de Condorcet quand les puces sont des '#'

import collections
import datetime
import getpass
import itertools
import logging
import re
import sys

import arkbot

_title = re.compile(r'^(?P<level>=+) *(?P<title>[^=]+?) *(?P=level)$')
_user = r'(\[\[(:w)?(:...?:)?([Dd]iscussion[ _])?[uU](tilisateur|ser)([ _][Tt]alk)?:(?P<user>[^\|/]+)(/[^\|]+)?(\|.+)?\]\]|{{[Nn]on signé\|(?P<user2>[^}]+)}})'
_countVote = re.compile(r'^#[^:].*%s.*$' % _user, re.UNICODE)
_condorcetOption = re.compile(r'') # TODO extraire les options
_condorcetVote = re.compile(r'^\*(\s*<!--\[vote\])?(?P<vote>\s*\w\s*([=,>/]+\s*\w\s*)*)(-->)?([^=,>/\w].*)?%s.*$' % _user, re.UNICODE)
_deletedText = re.compile(r'<(?P<tag>del|s)>.*</(?P=tag)>', re.UNICODE)

def translate(string, translations):
	for term in translations:
		string = string.replace(term, translations[term])
	return string

def extractVotes(page):
	lines = page.split('\n')

	for line in xrange(len(lines)):
		lines[line] = re.sub(_deletedText, '', lines[line])

	line = 0

	titleStack = []
	votes = collections.OrderedDict()

	def addVotes(titleStack, nbVotes, condorcetVotes, condorcetOptions):
		normalizedVotes = []
		condorcetOptions = sorted(condorcetOptions)
		for vote, user in condorcetVotes:
			separator = '>'
			for option in condorcetOptions:
				if vote.find(option) == -1:
					vote += ' %s %s' % (separator, option)
					separator = '='
			normalizedVotes.append((vote, user))

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
			dic[titleStack[-1]] = normalizedVotes

	onATitle = None
	while line < len(lines) and not onATitle:
		onATitle = _title.match(lines[line])
		line +=1

	while line < len(lines):
		title = onATitle.group('title')
		level = len(onATitle.group('level'))
		while level <= len(titleStack):
			titleStack.pop()
		titleStack.append(title)
		nbVotes = 0
		condorcetOptions = set()
		condorcetVotes = []
		while line < len(lines):
			onACountVote = _countVote.match(lines[line])
			if onACountVote:
				assert nbVotes >= 0, 'Mixed votes!'
				nbVotes += 1
			else:
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
					}).upper()
					while vote.find('>  > ') != -1:
						vote = vote.replace('>  >', '>')
					user = onACondorcetVote.group('user')
					if not user:
						user = onACondorcetVote.group('user2')
					for option in vote.replace(' ', '').replace('>', '').replace('=', ''):
						condorcetOptions.add(option)
					condorcetVotes.append((vote, user))
				else:
					onATitle = _title.match(lines[line])
					if onATitle:
						addVotes(titleStack, nbVotes, condorcetVotes, condorcetOptions)
						break
			line += 1

		line += 1
		addVotes(titleStack, nbVotes, condorcetVotes, condorcetOptions)
	return votes

def results(votes, date, temp):
	def recResults(votes, level=3, title=''):
		result = ''
		for title, content in votes.items():
			result += '=' * level + title + '=' * level + '\n'
			if isinstance(next(iter(content.values())), collections.OrderedDict):
				result += recResults(content, level + 1, title) + '\n'
			elif isinstance(content.values()[0], int):
				totalVotes = sum(content.values())
				result += """{| style="text-align:left; border:1px solid gray;"
|- {{ligne grise}}
|colspan="2"| \'\'\'%s\'\'\' ([[%s#%s|\'\'%s votes\'\']])
""" % (title, sys.argv[1], title, totalVotes)
				votes = sorted(content.items(), lambda x, y: cmp(y[1], x[1]))
				result += '|-\n|\'\'\'%s : %s\'\'\'\n|{{Avancement|%.f}}\n' % (votes[0][0], votes[0][1], float(votes[0][1]) / totalVotes * 100)
				for option, nbVotes in votes[1:]:
					result += '|-\n|%s : %s\n|{{Avancement|%.f}}\n' % (option, nbVotes, float(nbVotes) / totalVotes * 100)
				result += '|}\n'
			else:
				# TODO contrôler que personne n'a voté deux fois, si c'est le cas, ne pas prendre le vote en compte, et le marquer à côté
				# TODO déposer un message sur la PDD de ceux qui auraient voté plusieurs fois
				condorcetVotes = []
				result += '{{boîte déroulante/début|titre=Votes normalisés ([[%s#%s|\'\'%s votes\'\']])}}\n' % (sys.argv[1], title, len(content.values()[0]))
				for vote, user in content.values()[0]:
					result += '* %s | %s\n' % (vote, user)
					condorcetVotes.append({})
					rangs = vote.replace(' ', '').split('>')
					for rang, valeur in itertools.izip(rangs, xrange(len(rangs))):
						for option in rang.split('='):
							condorcetVotes[-1][option] = valeur
				result += '{{boîte déroulante/fin}}\n'

				options = condorcetVotes[0].keys()
				options.sort()

				result += '{{boîte déroulante/début|titre=Décompte selon la [[méthode Condorcet]]}}\n'
				result += '\'\'Options possibles : '
				for option in options[:-1]:
					result += '%s, ' % option
				result += options[-1] + '\'\'\n\n'

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
						result += '⇒ match nul\n'
					else:
						result += ('⇒ %s' % pair[score[0] < score[1]]) + (' (à %d contre %d, %d indifférents)\n' % (max(score[:-1]), min(score[:-1]), score[2]))
					scores[pair[0]] += score[0] >= score[1]
					scores[pair[1]] += score[0] <= score[1]

				result += '{{boîte déroulante/fin}}\n'

				winners = filter(lambda option: scores[option] == maxScore, options)

				if winners:
					result += '\nVainqueurs potentiels :\n'
					for winner in winners[:-1]:
						result += '* %s\n' % winner
					result += '* %s\n' % winners[-1]
				else:
					result += '\nPas de vainqueur potentiel'

		return result
	while len(votes.items()) == 1:
		votes = votes.values()[0]
	return '== Décompte%s des votes au %s %s %s à {{Heure|%s|%s}} ==\n' % (temp, date.day, arkbot._monthName[date.month - 1], date.year, date.hour, date.minute) + recResults(votes)

if __name__ == '__main__':
	print 'VoteScrapper 0.2'
	print '(C) 2010 Arkanosis'
	print 'arkanosis@gmail.com'
	print

	if '-temp' in sys.argv:
		temp = ' \'\'\'provisoire\'\'\''
		sys.argv.remove('-temp')
	else:
		temp = ''
	if '-publish' in sys.argv:
		publish = True
		sys.argv.remove('-publish')
	else:
		publish = False

	if len(sys.argv) != 2:
		print 'Usage: votescrapper.py [-temp] [-publish] <Wikipédia:Page de vote>'
		sys.exit(1)

	date = datetime.datetime.now()
	logger = logging.getLogger('ArkbotLogger')
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%H:%M:%S')
	logger.setLevel(logging.INFO)

	bot = arkbot.Arkbot(arkbot._botName, arkbot._wiki, logger)
	try:
		if publish:
			bot.login(getpass.getpass('Bot password ? '))

		page = bot.read(sys.argv[1])
		votes = extractVotes(page)

		res = results(votes, date, temp)

		if publish:
			#bot.append('Discussion_' + sys.argv[1], res + 'Machinalement' + arkbot._signature % (date.day, arkbot._monthName[date.month - 1], date.year, date.hour, date.minute), 'Décompte provisoire des votes')
			bot.append('Utilisateur:Arkbot/test', res + 'Avec mes salutations les plus automatiques' + arkbot._signature % (date.day, arkbot._monthName[date.month - 1], date.year, date.hour, date.minute), 'Décompte provisoire des votes')
			bot.logout()
		else:
			print res

	except (arkbot.ArkbotException), e:
		print e
		sys.exit(2)
