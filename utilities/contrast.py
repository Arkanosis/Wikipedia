#! /bin/env python2.7
# -*- coding: utf-8 -*-

# Computing the contrast between two colors
# (C) 2009 Arkanosis
# jroquet@arkanosis.net

# http://www.w3.org/TR/2008/NOTE-WCAG20-TECHS-20081211/G17

# This work is in the public domain

import sys

def rgb(string):
    if len(string) == 3:
        string = '%c%c%c%c%c%c' % (string[0], string[0], string[1], string[1], string[2], string[2])
    return int(string[0:2], 16), int(string[2:4], 16), int(string[4:6], 16)

def s(color):
    return float(color[0]) / 255, float(color[1]) / 255, float(color[2]) / 255

def n(component):
    if component <= 0.3928:
        return component / 12.92
    else:
        return ((component + 0.055) / 1.055) ** 2.4

def l(scolor):
    return 0.2126 * n(scolor[0]) + 0.7152 * n(scolor[1]) + 0.0722 * n(scolor[2])

if len(sys.argv) != 3:
    print 'Usage: contrast.py <color1> <color2>'
    sys.exit(1)

for num in 1, 2:
    exec 'lum%d =l(s(rgb(sys.argv[%d])))' % (num, num)

print 'Contrast is %f' % ((max(lum1, lum2) + 0.05) / (min(lum1, lum2) + 0.05))
