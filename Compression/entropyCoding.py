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

def zeta(value):
    pass

def fibonacci(value):
    pass

def levenshtein(value):
    pass

def evenRodeh(value):
    pass

def stout(value):
    pass

def golomb(value, parameter):
    pass

def rice(value, parameter):
    pass

def shannonFano(value):
    pass

def huffman(value):
    pass

def shannonFanoElias(value):
    pass

def arithmetic(value):
    pass

def interval(value):
    pass

# Tests

def codes(number, size):
    return [
        str(number),
        unary(number),
        optimalBinary(number, size),
        truncatedBinary(number, size),
        gamma(number),
        delta(number),
        omega(number),
#                 zeta(number),
#                 fibonacci(number),
#                 levenshtein(number),
#                 evenRodeh(number),
#                 stout(number),
#                 golomb(number, parameter),
#                 rice(number, parameter),
#                 shannonFano(number),
#                 huffman(number),
#                 shannonFanoElias(number),
#                 arithmetic(number),
#                 interval(number),
    ]

def main():
    if len(sys.argv) != 2:
        print 'Usage: entropyCoding.py <size>'
        sys.exit(1)

    size = int(sys.argv[1])

    lengths = [str(len(code)) for code in codes(size, size)]

    for number in xrange(0, size):
        for code, rank in itertools.izip(codes(number, size), itertools.count()):
            print ('% ' + lengths[rank] + 's') % code, '|',
        print

main()
