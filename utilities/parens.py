#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys

if __name__ == '__main__':
    with open(sys.argv[1]) as inputFile:
        previous = []
        for line in inputFile:
            line = line.rstrip()
            while previous and not line.startswith(previous[-1]):
                previous.pop()
            if line.endswith(')') and '(' in line[1:]:
                prefixFound = False
                for prefix in previous:
                    if line.startswith(prefix + ' ('):
                        prefixFound = True
                        break
                if not prefixFound:
                    print line
            else:
                previous.append(line)
