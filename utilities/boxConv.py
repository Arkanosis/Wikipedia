#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

# (C) 2010 Arkanosis
# arkanosis@gmail.com

import re
import sys

_var = re.compile(r'(\{{3}.*?\|?\}{3}|\'{3}.*?\'{3})')
_numbered = re.compile(r'(.*?)(?:\d*| actuel(?:le)?)$')

with open(sys.argv[1]) as inputFile:
    last = None
    for line in inputFile:
        for var in re.findall(_var, line):
            current = var[3:-3]
            if current[-1] == '|':
                current = current[:-1]
            if current != last:
                if var[0] == '{':
                    match = _numbered.match(current)
                    entry = match.group(1)
                    entry = entry[0].upper() + entry[1:]
                    print '{{Infobox/Ligne mixte optionnel|%s|{{{%s}}}}}' % (entry, current)
                else:
                    print '{{Infobox/Sous-titre|%s}}' % current
                last = current

#{{Infobox/Sous-titre|Sous-titre 1}}
#{{Infobox/Notice|Infobox Pays}}
