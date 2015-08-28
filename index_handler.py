import os
import sys
import struct
import pickle


def iso(str):
    return bytes(str, encoding='iso-8859-1')



class IndexWriter():

    def __init__(self, filename):
        
        self.index_file = open(filename, 'wb+')
        self.pseudo_hash = []

    def __del__(self):
        self.index_file.close()
        with open('pseudo_hash', 'wb') as f:
            pickle.dump(self.pseudo_hash, f)

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
        start_addr = self.index_file.tell()
        self.index_file.write(struct.pack('i', len(offsets)))
        for offset in offsets:
            b = struct.pack('i', offset)
            self.index_file.write(b)
        return start_addr
     
    def index(self, word, offsets):

        # Pseudo hash keeps track of where words are located
        if self.pseudo_hash[-1:] != [word[:3]]:
            self.pseudo_hash.append((word[:3], -1))

        wl_root_addr = self.pseudo_hash[-1][1]

        self.pseudo_hash[-1] = (self.pseudo_hash[-1][0],
                                self._write_word_link(word, offsets, wl_root_addr))


class IndexReader():

    def __init__(self, filename):
        self.index_file = open(filename, 'rb')
        with open('pseudo_hash', 'rb') as f:
            self.pseudo_hash = pickle.load(f)

    def __del__(self):
        self.index_file.close()

    def _find_word_link(self, word, addr):
        if addr != -1:
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
        off_l = self._read_int(address)
        return struct.unpack('i'*off_l, self.index_file.read(off_l*4))


    def find(self, word):
        word = iso(word.lower())
        wl_root = -1
        for prefix, wl_root_cand in self.pseudo_hash:
            if word[:3] == prefix:
                wl_root = wl_root_cand
                break
        
        if wl_root != -1:
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
