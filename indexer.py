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

class KorpusHandler():
    
    def __init__(self, filename):
        self.korpus = open(filename, 'r', encoding='iso-8859-1')
        self.offset_max = os.stat(filename).st_size - 2
        print(self.offset_max)

    def __del__(self):
        self.korpus.close()

    def read(self, offset, b=20, a=20):
        b = min(offset, b)
        a = min(a, self.offset_max - offset)
        self.korpus.seek(offset-b)
        text = self.korpus.read(b + a + 1)

        return text.replace('\n', ' ')

if __name__ == '__main__':
    ih = index('index')
