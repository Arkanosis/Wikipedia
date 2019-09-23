#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import termios
import tty

class ProgressBar(object):
    __width = 80

    def __init__(self, size):
        self.__size = size

    def update(self, progression, text=''):
        ratio = float(progression) / self.__size
        percentage = int(100 * ratio)
        barSize = int(ProgressBar.__width * ratio)
        print((chr(27) + '[A%3d%%[' % percentage + '=' * barSize  + '>' + ' ' * (ProgressBar.__width - barSize) + '] %d / %d' % (progression, self.__size), text))

def getch():
	stdin = sys.stdin.fileno()
	stdinAttr = termios.tcgetattr(stdin)
	try:
		tty.setraw(stdin)
		c = sys.stdin.read(1)
	finally:
		termios.tcsetattr(stdin, termios.TCSADRAIN, stdinAttr)
		return c

def fancyTime(timestamp):
	return timestamp[:-4].replace('T', ' ')

def getOption(name, valueIfPresent=True, valueIfAbsent=False):
    name = '-' + name
    if name in sys.argv:
        sys.argv.remove(name)
        return valueIfPresent
    return valueIfAbsent

def getValue(name, default=None):
    name = '-' + name
    if name in sys.argv:
        index = sys.argv.index(name)
        if index + 1 == len(sys.argv):
            assert default is not None
            sys.argv.remove(name)
            return default
        value = sys.argv[index + 1]
        sys.argv = sys.argv[:index + 1] + sys.argv[index + 2:]
        sys.argv.remove(name)
        return value
    return default
