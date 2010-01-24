#! /bin/env python2.7
# -*- coding: utf-8 -*-

import SocketServer
import SimpleHTTPServer
import urllib

_port = 8080

class Proxy(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.copyfile(urllib.urlopen(self.path), self.wfile)

SocketServer.ForkingTCPServer(('', _port), Proxy).serve_forever()
