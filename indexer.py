import io 
import os
import sys
import codecs
import cProfile
import datetime
import pstats

from index_handler import IndexWriter



def index():

    stdin = io.TextIOWrapper(sys.stdin.buffer, encoding = 'iso-8859-1')
    handler = IndexWriter()

    offsets = []
    current_word = ''
    for line in stdin:
        line = line.rstrip('\n').split(' ')
        word = line[0]
        offset = int(line[1])
        if word != current_word:
            if current_word:
                handler.index(current_word, offsets)
            current_word = word
            offsets = []

        offsets.append(offset)

if __name__ == '__main__':
    index()
