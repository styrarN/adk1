import os
import struct
from collections import OrderedDict
from hashlib import sha1
import sys

HASH_TABLE_SIZE = 8*1024
def hash(word):
    return int(sha1(word).hexdigest(), 16)

class IndexWriter():

    def __init__(self, filename):
        
        f = open(filename, 'wb+')
        self.index_file = f
        self.index_file.seek(HASH_TABLE_SIZE*4)
        self.hash_table = OrderedDict()
        for i in range(HASH_TABLE_SIZE):
            self.hash_table[i] = 0

    def __del__(self):
        self.index_file.seek(0)
        for value in self.hash_table.values():
            self.index_file.write(struct.pack('i', value))
        self.index_file.close()

    def _write_word_link(self, word, offsets, next): 
        """ Creates new word, returns its address """
        offset_root = self._write_word_offsets(offsets)
        wl_addr = self.index_file.tell()

        wl_b = struct.pack('i', len(word))
        self.index_file.write(wl_b)

        self.index_file.write(word)
        
        offs_b = struct.pack('i', offset_root)
        self.index_file.write(offs_b)

        next_b = struct.pack('i', next)
        self.index_file.write(next_b)

        return wl_addr

    def _write_word_offsets(self, offsets):
        """ Creates now offset for a word and returns address """
        prev_addr = 0
        for offset in offsets:
            curr_addr = self.index_file.tell()
            b = struct.pack('ii', offset, prev_addr)
            self.index_file.write(b)
            prev_addr = curr_addr
            
        return prev_addr
     
    def index(self, word, offsets):

        hash_addr = (hash(word) % HASH_TABLE_SIZE)
        
        wl_root_addr = self.hash_table[hash_addr]
        self.hash_table[hash_addr] = self._write_word_link(word, offsets, wl_root_addr)


class IndexReader():

    def __init__(self, filename):
        sys.setrecursionlimit(10000)
        self.index_file = open(filename, 'rb')

    def __del__(self):
        self.index_file.close()

    def _find_word_link(self, word, addr):
        if addr:
            c_w, offset, next= self._read_word_link(addr)
            if word == c_w:
                return c_w, offset, next
            else:
                return self._find_word_link(word, next)

    def _read_word_link(self, address):
        wl = self._read_int(address)
        word = self.index_file.read(wl)
        offset = self._read_int(address + 4 + wl)
        next =  self._read_int(address + 8 + wl)
        return word, offset, next

    def _get_word_offsets(self, address):
        next = address
        offsets = []

        while next:
            offset, next = self._read_word_offset(next)
            offsets.append(offset)

        return offsets

    def _read_word_offset(self, addr):
        # Where is offset?

        # What is offset?
        return self._read_int(addr), self._read_int(addr + 4)

    def find(self, word):
        print(word) #testprint
        word = word.lower()
        print(word)
        hash_addr = (hash(word) % HASH_TABLE_SIZE) * 4
        
        wl_root = self._read_int(hash_addr) 
        if wl_root:
            wl = self._find_word_link(word, wl_root)
            if wl:
                word, offset, next = wl
                return self._get_word_offsets(offset)

        return []

    def _read_int(self, addr):
        self.index_file.seek(addr)
        return struct.unpack('i', self.index_file.read(4))[0]

if __name__ == '__main__':
    pass
