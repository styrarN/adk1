#! coding=utf-8

import os
import unittest

from index_handler import IndexReader

class BasicTests(unittest.TestCase):
    
    def setUp(self):
        self.ih = IndexReader('index')

    def test_search(self):
        self.assertEqual(self.ih.find('hiphopApottamus'), [])
        f = self.ih.find('för')
        self.assertNotEqual(f, [])
        self.assertEqual(self.ih.find('fÖr'), f)
        self.assertNotEqual(self.ih.find('regering'), [])
        self.assertEqual(self.ih.find(' '), [])
        self.assertEqual(self.ih.find(''), [])
        self.assertEqual(self.ih.find('telefonkontakt'), self.ih.find('teleFonkONTAkt'))
        self.assertEqual(len(self.ih.find('telefonkontakt')), 6)
        
        
    def test_program(self):
        #os.system('cat ../korpus | tokenizer/tokenizer | grep telefonkontakt | wc -l >tmp.txt')
        #self.assertEqual( int(open('tmp.txt').read()), 8)
        self.assertEqual(os.system('python3 reader.py tågpladder nostupid 1> /dev/null'), 0)
        self.assertEqual(os.system('python3 reader.py för nostupid 1> /dev/null '), 0)
        self.assertEqual(os.system('python3 reader.py regering nostupid 1> /dev/null'), 0)
            

if __name__=='__main__':
    unittest.main()
