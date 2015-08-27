import os
import unittest

from index_handler import IndexReader

def iso(str):
    return bytes(str, encoding='iso-8859-1') 

class BasicTests(unittest.TestCase):
    
    def setUp(self):
        self.ih = IndexReader('index')

    def test_search(self):
        self.assertEqual(self.ih.find(iso('hiphopApottamus')), [])
        self.assertNotEqual(self.ih.find(iso('för')), [])
        #self.assertNotEqual(self.ih.find(iso('fÖr')), [])
        self.assertNotEqual(self.ih.find(iso('regering')), [])
        self.assertEqual(self.ih.find(iso(' ')), [])
        self.assertEqual(self.ih.find(iso('')), [])
        self.assertEqual(self.ih.find(iso('telefonkontakt')), self.ih.find(iso('teleFonkONTAkt')))
        
    def test_program(self):
        # self.assertEqual(os.system('python3 reader.py tågpladder nostupid 1> /dev/null'), 0)
        print(  self.ih.find(iso('fÖr')))
        # self.assertEqual(os.system('python3 reader.py för nostupid 1> /dev/null '), 0)
        # self.assertEqual(os.system('python3 reader.py regering nostupid 1> /dev/null'), 0)
            

if __name__=='__main__':
    unittest.main()
