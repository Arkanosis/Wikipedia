#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
import xml.sax

class WikidataDumpHandler(xml.sax.handler.ContentHandler):
    def __reset(self):
        self.__title = ''
        self.__namespace = ''
        self.__json = ''

    def __init__(self):
        self.__currentElement = None
        self.__reset()

    def startElement(self, name, attrs):
        self.__currentElement = name

    def characters(self, content):
        if self.__currentElement == 'title':
            self.__title += content
        elif self.__currentElement == 'ns':
            self.__namespace += content
        elif self.__currentElement == 'text':
            self.__json += content

    def endElement(self, name):
        if self.__currentElement == 'text':
            if self.__namespace.strip() == '0':
                item = json.loads(self.__json)
                if 'frwiki' not in item['links']:
                    if 'enwiki' in item['links']:
                        lang, link = 'en', item['links']['enwiki']
                    else:
                        if not isinstance(item['links'], dict):
                            self.__reset()
                            return
                        lang, link = next(item['links'].iteritems())
                    if len(item['links']) > 1:
                        print '%d : [[:d:%s]] ([[:%s:%s]])' % (len(item['links']), self.__title.strip().encode('utf-8'), lang.encode('utf-8').replace('wiki', ''), link.encode('utf-8'))
            self.__reset()

def analyze(inputFileName):
    parser = xml.sax.make_parser()
    parser.setContentHandler(WikidataDumpHandler())
    with open(inputFileName) as inputFile:
        parser.parse(inputFile)

if __name__ == '__main__':
    analyze(sys.argv[1])
