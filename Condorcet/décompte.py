#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Décompte de Condorcet
# (C) 2009 Arkanosis
# jroquet@arkanosis.net

# Suivant la méthode expliquée sur
#  http://fr.wikipedia.org/wiki/Méthode_Condorcet

# Ce script est placé dans le domaine public

import itertools
import sys

if len(sys.argv) != 2:
    print 'Usage: décompte.py <votes.txt>'
    sys.exit(1)

votes = []

with open(sys.argv[1]) as votes_bruts:
    for vote_brut in votes_bruts:
        votes.append({})
        rangs = vote_brut.replace(' ', '').split('|')[1].split('>')
        for valeur, rang in enumerate(rangs):
            for option in rang.replace(',', '=').split('='):
                votes[-1][option.strip()] = valeur

options = votes[0].keys()
options.sort()

print 'Décompte selon la méthode Condorcet'
print 'Options possibles : ', options

scores = {}
score_max = len(options) - 1
for option in options:
    scores[option] = 0

duels = itertools.combinations(options, 2)

for duel in duels:
    print 'Duel entre %s et %s' % duel,
    score = [0, 0, 0]
    for vote in votes:
        if vote[duel[0]] < vote[duel[1]]:
            score[0] += 1
        elif vote[duel[0]] > vote[duel[1]]:
            score[1] += 1
        else:
            score[2] += 1
    if score[0] == score[1]:
        print '=> match nul'
    else:
        print '=> %s' % duel[score[0] < score[1]], '(à %d contre %d, %d indifférents)' % (max(score[:-1]), min(score[:-1]), score[2])
    scores[duel[0]] += score[0] >= score[1]
    scores[duel[1]] += score[0] <= score[1]

vainqueurs = filter(lambda option: scores[option] == score_max, options)

print 'Vainqueurs potentiels :', vainqueurs

if len(vainqueurs) != 1:
    print 'La prise de décision n\'a pas abouti'
