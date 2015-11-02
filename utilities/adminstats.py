#! /usr/bin/env python
# -*- coding: utf-8 -*-

import collections
import csv
import os
import sys
import xml.sax

# TODO, stats (dump) for:
# - (|re|un)block
# - (|re|un)protect
# - MediaWiki: edit
# - (|un)delete
# - (|un)hide
# - import
# - (add|remove)right
# - (create|edit|delete)filter
# - total
# TODO, additional infos (API):
# - blocked
# - groups
# - editcount

_columns = collections.OrderedDict([
    ('name', None),
    ('mw_edits', 0),
])

_mwNamespace = 0

class StatsHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        self._currentElement = None
        self._reset()
        self._stats = {}

    def _getStats(self, userName):
        return self._stats.setdefault(userName, collections.OrderedDict(_columns, name=userName))

    def startElement(self, name, attrs):
        self._currentElement = name

    def getStats(self):
        return self._stats

class HistoryHandler(StatsHandler):
    def _reset(self):
        self.__namespace = ''
        self.__userName = ''

    def characters(self, content):
        if self._currentElement == 'ns':
            self.__namespace += content
        elif self._currentElement == 'username':
            self.__userName += content

    def endElement(self, name):
        if name == 'username':
            if self.__namespace.strip() == str(_mwNamespace):
                self._getStats(self.__userName.strip().encode('utf-8'))['mw_edits'] += 1
            self._reset()

class LogsHandler(StatsHandler):
    def _reset(self):
        pass

    def characters(self, content):
        pass

    def endElement(self, name):
        pass

def analyze(fileName, parser, handlerType):
    parser.setContentHandler(handlerType())
    with open(fileName) as file:
        parser.parse(file)
    return parser.getContentHandler().getStats()

def getStats(historyFileName, logsFileName):
    parser = xml.sax.make_parser()
    stats = analyze(historyFileName, parser, HistoryHandler)
#    stats.update(analyze(logsFileName, parser, LogsHandler))
    return stats

def writeStats(stats, outputFileName):
    with open(outputFileName, 'wb') as outputFile:
        output = csv.writer(outputFile)
        output.writerow(_columns.keys())
        for userStats in stats.itervalues():
            output.writerow(userStats.values())

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print >> sys.stderr, 'Usage: %s <history.xml> <logs.xml> <output.csv>' % sys.argv[0].split(os.sep)[-1]
        sys.exit(1)

    writeStats(getStats(sys.argv[1], sys.argv[2]), sys.argv[3])
