#! /bin/env python2.7
# -*- coding: utf-8 -*-

# Entropy encoding
# (C) 2010 Arkanosis
# arkanosis@gmail.com

# This work is in the public domain

import itertools
import math
import sys

# Helpers

def b(value, length = None):
    str = bin(value)[2:]
    if length is None:
        return str
    if length > len(str):
        return '0' * (length - len(str)) + str
    if length:
        return str[-length:]
    return ''

def flog(value):
    return int(math.floor(math.log(value, 2)))

def clog(value):
    return int(math.ceil(math.log(value + 1, 2)))

def pow(exp):
    return int(math.pow(2, exp))

# Encoders & decoders

def unary(value):
    return '1' * value + '0'

def optimalBinary(value, size):
    return b(value, clog(size))

def truncatedBinary(value, size):
    if not size:
        return ''
    if value < pow(flog(size) + 1) - size:
        return b(value, flog(size))
    return b(value + pow(size) - size, clog(size))

def gamma(value):
    if value:
        return (unary(flog(value)) + ' ' + b(value, flog(value))).rstrip()
    return '-'

def delta(value):
    if value:
        return (gamma(flog(value) + 1) + ' ' + b(value, flog(value))).rstrip()
    return '-'

def omega(value):
    if value:
        def romega(value):
            if value == 1:
                return ''
            return romega(clog(value) - 1) + ' ' + b(value, clog(value))
        return romega(value) + ' 0'
    return '-'

def zeta(value, k):
    if value:
        h = flog(value) / k
        return (unary(h) + ' ' + truncatedBinary(value - pow(h * k), pow((h + 1) * k) - pow(h * k))).rstrip()
    return '-'

def fibonacci(value):
    if value:
        values = [1, 2]
        while values[-1] <= value:
            values.append(values[-1] + values[-2])
        values.pop()
        code = '1'
        for i in xrange(1, len(values) + 1):
            if values[-i] <= value:
                code = '1 ' + code
                value -= values[-i]
            else:
                code = '0' + code
        return code
    return '-'

def levenshtein(value):
    rec = [0]
    def rlevenshtein(value):
        if value:
            rec[0] += 1
            return rlevenshtein(clog(value) - 1) + ' ' + b(value, flog(value))
        else:
            return ''
    code = rlevenshtein(value).strip(' ')
    return (unary(rec[0]) + ' ' + code).rstrip(' ')

def evenRodeh(value):
    pass

def stout(value):
    pass

def golomb(value, k):
    q = value / k
    return (unary(q) + ' ' + truncatedBinary(value - q * k, k)).rstrip()

def rice(value, k):
    q = value / pow(k)
    return (unary(q) + ' ' + b(value, k)).rstrip()

def shannonFano(value):
    pass

def huffman(value):
    pass

def shannonFanoElias(value):
    pass

def arithmetic(value):
    pass

def range(value):
    pass

def codes(number, size):
    return [
        ('Dec', str(number)),
#        ('Unary', unary(number)),
        ('Binary', optimalBinary(number, size)),
#        ('Trunc', truncatedBinary(number, size)),
#        ('Gamma', gamma(number)),
#        ('Delta', delta(number)),
#        ('Omega', omega(number)),
#        ('Zeta 1', zeta(number, 1)),
#        ('Zeta 2', zeta(number, 2)),
#        ('Zeta 3', zeta(number, 3)),
#        ('Zeta 4', zeta(number, 4)),
#        ('Fibo', fibonacci(number)),
#        ('Leven', levenshtein(number)),
#                 ('Erod', evenRodeh(number)),
#                 ('Stout', stout(number)),
#        ('Golo 1', golomb(number, 1)),
#        ('Golo 2', golomb(number, 2)),
#        ('Golo 3', golomb(number, 3)),
#        ('Golo 4', golomb(number, 4)),
#        ('Golo 5', golomb(number, 5)),
#        ('Golo 10', golomb(number, 10)),
#        ('Golo 16', golomb(number, 16)),
        ('Rice 1', rice(number, 1)),
        ('Rice 2', rice(number, 2)),
        ('Rice 3', rice(number, 3)),
        ('Rice 4', rice(number, 4)),
#                 ('Shfa', shannonFano(number)),
#                 ('Huff', huffman(number)),
#                 ('Shfael', shannonFanoElias(number)),
#                 ('Arith', arithmetic(number)),
#                 ('Rang', range(number)),
    ]

def showCode(code):
    return code
def showLen(code):
    return str(len(code.replace(' ', '')))

def main():
    start = 0
    show = showCode
    if '-len' in sys.argv:
        sys.argv.remove('-len')
        show = showLen

    wiki = False
    if '-wiki' in sys.argv:
        sys.argv.remove('-wiki')
        wiki = True

    if len(sys.argv) != 2:
        print 'Usage: entropyCoding.py <max> [-len]'
        sys.exit(1)

    size = int(sys.argv[1]) + 1
    if show == showLen:
        start = size - 1

    names = [name for name, code in codes(0, 0)]

    if wiki:
        print '{| class=\'wikitable\' style=\'text-align: right\''
        print '|+ Représentation des premiers entiers naturels'
        for name in names:
            print '!', name
        for number in xrange(start, size):
            print '|-'
            for _, code in codes(number, size):
                print '|', show(code)
        print '|}'
    else:
        lengths = [str(max(len(show(code)), len(name))) for name, code in codes(size - 1, size)]

        for rank in xrange(len(names)):
            print ('% ' + lengths[rank] + 's') % names[rank], '|',
        print
        for rank in xrange(len(names)):
            print '-' * int(lengths[rank]), '+',
        print

        for number in xrange(start, size):
            for (_, code), rank in itertools.izip(codes(number, size), itertools.count()):
                print ('% ' + lengths[rank] + 's') % show(code), '|',
            print

main()
