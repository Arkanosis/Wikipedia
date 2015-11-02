#! /usr/bin/env python
# -*- coding: utf-8 -*-

# ./orphans.awk data/frwiki-20130420-stub-meta-current.xml | sort

import sys

last = ''

with open(sys.argv[1]) as source:
    for line in source:
        line = line.rstrip()
        skip = False
        for sub in [ '/Suppression', '/À faire', '/Article de qualité', '/Traduction', '/Droit d\'auteur', '/Neutralité', '/Archive', '/Bon article']:
            if line.find(sub) != -1:
                skip = True
                break
        if skip:
            continue
        if line.endswith(' !!!') and not line.startswith(last):
            print line
        last = line
