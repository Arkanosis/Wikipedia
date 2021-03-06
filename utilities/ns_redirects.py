#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
When run as a script, takes one argument indicating the location of an XML
dump from a media wiki, and parses the entire file, searching for <page>
elements.

Each <page> is turned into a WikiPage object. A callback can be defined to
receive the page.

Read more about dumps here: http://meta.wikimedia.org/wiki/Data_dumps
"""

import sys
from xml.sax import handler, make_parser
from xml.sax.saxutils import XMLFilterBase

class WikiPage(object):
    """
    Holds data related to one <page> element parsed from the dump
    """
    def __init__(self):
        self.title = ''
        self.id = ''
        self.text = ''
        self.redirect = ''

    def __str__(self):
        return 'ID %s TITLE %s' % (self.id, self.title)

class text_normalize_filter(XMLFilterBase):
    """
    SAX filter to ensure that contiguous texts nodes are merged into one
    That hopefully speeds up the parsing process a lot, specially when reading
    revisions with long text
    Receip by Uche Ogbuji, James Kew and Peter Cogolo
    Retrieved from "Python Cookbook, 2nd ed., by Alex Martelli, Anna Martelli
    Ravenscroft, and David Ascher (O'Reillly Media, 2005) 0-596-00797-3"
    """
    def __init__(self, upstream, downstream):
        XMLFilterBase.__init__(self, upstream)
        self._downstream=downstream
        self._accumulator=[]
    def _complete_text_node(self):
        if self._accumulator:
            self._downstream.characters(''.join(self._accumulator))
            self._accumulator=[]
    def characters(self, text):
        self._accumulator.append(text)
    def ignorableWhiteSpace(self, ws):
        self._accumulator.append(text)
def _wrap_complete(method_name):
    def method(self, *a, **k):
        self._complete_text_node()
        getattr(self._downstream, method_name)(*a, **k)
    method.__name__= method_name
    setattr(text_normalize_filter, method_name, method)
for n in '''startElement endElement endDocument'''.split():
    _wrap_complete(n)

class WikiDumpHandler(handler.ContentHandler):
    """
    A ContentHandler designed to pull out page ids, titles and text from
    Wiki pages. These are assembled into WikiPage objects and sent off
    to the supplied callback.
    """
    def __init__(self, pageCallBack=None):
        handler.ContentHandler.__init__(self)
        self.currentTag = ''
        self.ignoreIdTags = False
        self.pageCallBack = pageCallBack
        self.pagesProcessed = 0

    def startElement(self, name, attrs):
        self.currentTag = name
        if (name == 'page'):
            # add a page
            self.currentPage = WikiPage()
        elif (name == 'revision'):
            # when we're in revision, ignore ids
            self.ignoreIdTags = True
        elif (name == 'redirect'):
            self.currentPage.redirect = attrs.getValue('title')

    def endElement(self, name):
        if (name == 'page'):
            if self.pageCallBack is not None:
                self.pageCallBack(self.currentPage)
            self.pagesProcessed += 1
        elif (name == 'revision'):
            # we've finished the revision section
            self.ignoreIdTags = False
        self.currentTag = ''

    def characters(self, content):
        if (self.currentTag == 'id' and not self.ignoreIdTags):
            self.currentPage.id = content
        elif (self.currentTag == 'title'):
            self.currentPage.title = content
        elif self.currentTag == 'text':
            self.currentPage.text = content

    def endDocument(self):
        pass
        #print "Processed %d pages" % self.pagesProcessed

def parseWithCallback(callback):
    parser = make_parser()
    parser.setFeature(handler.feature_namespaces, 0)

    # apply the text_normalize_filter
    wdh = WikiDumpHandler(pageCallBack=callback)
    filter_handler = text_normalize_filter(parser, wdh)

    filter_handler.parse(sys.stdin)

def processPage(page):
    if page.title.endswith(('.js', '.css')):
        print('Found', page.title)
        with open('data/sitecode/' + page.title.replace('/', '_'), 'w') as f:
            f.write(page.text)

def processPageMW(page):
    if page.title.startswith('MediaWiki:'):
        print('Found', page.title)
        with open('data/siteadmin/' + page.title.replace('/', '_'), 'w') as f:
            f.write(page.text)

import re

_ref = re.compile(r'<ref\b')

def processPageRef(page):
    print(len(re.findall(_ref, page.text)), page.title)

def processPageCommercial(page):
    for c in 'Ⓡ®℗™℠':
        if c in page.text:
            print(page.title)
            return

def hasNamespace(title):
    for namespace in [
            'Média',
            'Spécial',
            'Discussion',
            'Utilisateur',
            'Discussion utilisateur',
            'Wikipédia',
            'Discussion Wikipédia',
            'Fichier',
            'Discussion fichier',
            'MediaWiki',
            'Discussion MediaWiki',
            'Modèle',
            'Discussion modèle',
            'Aide',
            'Discussion aide',
            'Catégorie',
            'Discussion catégorie',
            'Portail',
            'Discussion Portail',
            'Projet',
            'Discussion Projet',
            'Référence',
            'Discussion Référence',
            'Module',
            'Discussion module',
            'Sujet',
    ]:
        if title.startswith(namespace + ':'):
            return True
    return False

def processRedirectsOutsideMain(page):
    if hasNamespace(page.redirect) and not hasNamespace(page.title):
        if not page.title.startswith('P:'): # filter project redirects, for now
            print(page.title)

if __name__ == "__main__":
    """
    When called as script, argv[1] is assumed to be a filename and we
    simply print pages found.
    """
#    parseWithCallback(processPage)
#    parseWithCallback(processPageMW)
#    parseWithCallback(processPageRef)
#    parseWithCallback(processPageCommercial)
    parseWithCallback(processRedirectsOutsideMain)
