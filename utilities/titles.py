#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import xml.sax

class WikipediaDumpHandler(xml.sax.handler.ContentHandler):
    def __reset(self):
        self.__title = ''
        self.__namespace = ''
        self.__redirect = False

    def __init__(self, skipRedirects):
        self.__currentElement = None
        self.__reset()
        self.__skipRedirects = skipRedirects

    def startElement(self, name, attrs):
        self.__currentElement = name
        if name == 'redirect':
            self.__redirect = True

    def characters(self, content):
        if self.__currentElement == 'title':
            self.__title += content
        elif self.__currentElement == 'ns':
            self.__namespace += content

    def endElement(self, name):
        if self.__currentElement == 'text':
            if self.__namespace.strip() == '0' and not (self.__skipRedirects or self.__redirect):
                print self.__title.rstrip().encode('utf-8')
            self.__reset()

def analyze(inputFileName, skipRedirects):
    parser = xml.sax.make_parser()
    parser.setContentHandler(WikipediaDumpHandler(skipRedirects))
    with open(inputFileName) as inputFile:
        parser.parse(inputFile)

if __name__ == '__main__':
    analyze(sys.argv[1], sys.argv[-1] == '--skip-redirects')
