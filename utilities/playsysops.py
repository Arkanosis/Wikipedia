#! /usr/bin/env python2.7

# -*- coding: utf-8 -*-

# (C) 2012 Arkanosis
# arkanosis@gmail.com

import datetime
import locale
import sys

locale.setlocale(locale.LC_ALL, 'fr_FR.UTF8')

sysops = []
times = {}

def toTime(timestamp):
    return datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')

for line in open(sys.argv[1]):
    timestamp, sysop = line[:20], line[21:].rstrip()
    times[sysop] = toTime(timestamp)

alreadySysop = set()

for line in open(sys.argv[2]):
    timestamp, sysop, action = line.rstrip().split('|')
    if action == 'ADD' and sysop not in alreadySysop:
        alreadySysop.add(sysop)
        sysopTime = toTime(timestamp)
        age = sysopTime - times[sysop]
        print '				[' + sysopTime.strftime('%Y + %m. / 12 + %d / 365.24').replace('+ 0', '+  ') + ', ' + str(age.days) + ', \'' + sysop + '\', \'' + sysopTime.strftime('%B %Y') + '\'],'
