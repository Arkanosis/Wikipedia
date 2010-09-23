#! /usr/bin/python

from __future__ import with_statement

import sys

if len(sys.argv) != 4:
    print 'Usage:', sys.argv[0], '<input> <output> <column>'
    sys.exit(1)

column = int(sys.argv[3])
currentColumn = 0

with open(sys.argv[1]) as inputFile:
	with open(sys.argv[2], 'w') as outputFile:
            for line in inputFile:
                if currentColumn == column:
                    outputFile.write(line)
                if line.startswith('|-'):
                    currentColumn = 1
                else:
                    currentColumn += 1
