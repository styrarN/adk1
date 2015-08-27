import io 
import os
import sys
import codecs
import cProfile
import datetime
import pstats

from index_handler import IndexWriter


def iso(s):
    return bytes(s, encoding='iso-8859-1')


def index(filename):

    stdin = io.TextIOWrapper(sys.stdin.buffer, encoding = 'iso-8859-1')
    handler = IndexWriter(filename)

    offsets = []
    current_word = ''
    for line in stdin:
        line = line.rstrip('\n').split(' ')
        word = iso(line[0])
        offset = int(line[1])
        if word != current_word:
            if current_word:
                handler.index(current_word, offsets)
            current_word = word
            offsets = []

        offsets.append(offset)

if __name__ == '__main__':
    index('index')
