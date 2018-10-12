#! /usr/bin/env python3

# (C) 2016-2018 Arkanosis
# jroquet@arkanosis.net
#
# Mis à disposition sous licence MIT
# http://www.opensource.org/licenses/mit-license.php
#
# Version originale pour la WikiConvention francophone 2016 :
# https://github.com/Arkanosis/WikiConvFR16/blob/master/Datamining%20du%20dimanche%20sur%20les%20projets%20Wikimedia/src/wikidump.py

import sys
import xml.sax

class Page:

    def __init__(self, ns, title, text):
        self.ns = ns
        self.title = title
        self.text = text

class Handler(xml.sax.handler.ContentHandler):

    def __init__(self, callback):
        super().__init__()
        self.__pageContent = {}
        self.__currentTag = ''
        self.__callback = callback

    def startElement(self, name, attrs):
        if name == 'page':
            self.__pageContent = {}
        self.__currentTag = name

    def endElement(self, name):
        if name == 'page':
            self.__callback(Page(
                int(''.join(self.__pageContent.get('ns', []))),
                ''.join(self.__pageContent.get('title', [])),
                ''.join(self.__pageContent.get('text', []))
            ))
        self.__currentTag = ''

    def __append(self, content):
        self.__pageContent.setdefault(self.__currentTag, []).append(content)

    characters = __append
    ignorableWhiteSpace = __append

def parseWithCallback(callback):
    parser = xml.sax.make_parser()
    parser.setContentHandler(Handler(callback))
    parser.parse(sys.stdin)

def matchOn(string):
    match = [None]
    def on(reg):
        match[0] = reg.search(string)
        return match[0]
    def _(group):
        return match[0].group(group)
    return on, _

def matchOnLines(text):
    for line in text.split('\n'):
        on, _ = matchOn(line)
        yield line, on, _
