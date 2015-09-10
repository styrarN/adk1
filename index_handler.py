import struct
import pickle


def iso(str):
    return bytes(str, encoding='iso-8859-1')

CHAR_DICT = { char: i for i, char in enumerate(" abcdefghijklmnopqrstuvwxyzåäö") }
HASH_LENGTH = 900*30


def hash(str):
    val = sum(map( lambda x: x[0]*CHAR_DICT[(x[1])], zip([900, 30, 1], str)))

    return val

class IndexWriter():

    def __init__(self):

        self.index_file = open('index_file', 'wb+')
        self.offset_file = open('offset_file', 'wb+')
        self.pseudo_hash = [-1 for _ in range(HASH_LENGTH)]

    def __del__(self):
        self.index_file.close()
        self.offset_file.close()
        with open('pseudo_hash', 'wb') as f:
            for h in self.pseudo_hash:
                f.write(struct.pack('i', h))

    def _write_word_link(self, word, offsets):
        """ Creates new word, returns its address """
        offset_root = self._write_word_offsets(offsets)
        wl_addr = self.index_file.tell()

        wl_b = struct.pack('i', len(word))
        self.index_file.write(wl_b)

        self.index_file.write(word)

        offs_b = struct.pack('i', offset_root)
        self.index_file.write(offs_b)

        return wl_addr

    def _write_word_offsets(self, offsets):
        """ Creates now offset for a word and returns address """
        start_addr = self.offset_file.tell()
        offs_len = len(offsets)
        self.offset_file.write(struct.pack('i', offs_len))
        self.offset_file.write(struct.pack('i'*offs_len, *offsets))
        return start_addr

    def index(self, word, offsets):

        h = hash(word)
        addr = self._write_word_link(iso(word), offsets)

        if self.pseudo_hash[hash(word)] < 0:
            self.pseudo_hash[h] = addr
            

class IndexReader():

    def __init__(self):
        self.index_file = open("index_file", 'rb')
        self.offset_file = open('offset_file', 'rb')
        self.pseudo_hash = open('pseudo_hash', 'rb')

    def __del__(self):
        self.index_file.close()
        self.offset_file.close()
        self.pseudo_hash.close()

    def _find_word_link(self, word, addr):
        self.index_file.seek(addr)
        wl = struct.unpack('i', self.index_file.read(4))[0]
        while wl:
            c_w = self.index_file.read(wl)
            if not c_w:
                return
            if c_w[:3] != word[:3]:
                return
            offs = struct.unpack('i', self.index_file.read(4))[0]
            if c_w == word:
                return offs
            wl = struct.unpack('i', self.index_file.read(4))[0]
        return



    def _read_word_link(self, address):
        wl = self._read_int(address)
        word = self.index_file.read(wl)
        offset = self._read_int(address + 4 + wl)
        return word, offset

    def _get_word_offsets(self, address):
        self.offset_file.seek(address)
        off_l = struct.unpack('i', self.offset_file.read(4))[0]
        return struct.unpack('i'*off_l, self.offset_file.read(off_l*4))

    def find(self, word):
    
        word = word.lower()
        self.pseudo_hash.seek(hash(word)*4)
        w_addr = struct.unpack('i', self.pseudo_hash.read(4))[0]
        if w_addr == -1:
            return []

        word = iso(word)
        offs = self._find_word_link(word, w_addr)
        if offs:
            return self._get_word_offsets(offs)

        return []

    def _read_int(self, addr):
        self.index_file.seek(addr)
        return struct.unpack('i', self.index_file.read(4))[0]

if __name__ == '__main__':
    pass
