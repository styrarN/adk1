#! coding=utf-8

import os
import sys
import argparse
from datetime import datetime

from index_handler import IndexReader


def main():

    parser = argparse.ArgumentParser(description='Sök efter hur svenska ord används')
    parser.add_argument('-s', '--stupid',
                        action='store_true',
                        help='Bekräfta innan utskrift av många träffar')
    parser.add_argument('ORD',
                        nargs='?',
                        help='Ordet att söka efter')

    args = parser.parse_args()

    index_reader = IndexReader('index')    
    korpus_handler = KorpusHandler('korpus')
        
    if args.ORD:
        korpus_search(index_reader, korpus_handler, args.ORD, stupid=args.stupid)
        return
    
    welcome = '\nVälkommen till: \n\n' \
              '___________.__  .__       .__     __            _____    __  .__            \n' \
              '\_   _____/|  | |__| ____ |  |___/  |_    _____/ ____\ _/  |_|  |__   ____  \n' \
              ' |    __)  |  | |  |/ ___\|  |  \   __\  /  _ \   __\  \   __\  |  \_/ __ \ \n' \
              ' |     \   |  |_|  / /_/  >   Y  \  |   (  <_> )  |     |  | |   Y  \  ___/ \n' \
              ' \___  /   |____/__\___  /|___|  /__|    \____/|__|     |__| |___|  /\___  >\n' \
              '     \/           /_____/      \/                                 \/     \/ \n' \
              '     ____  __.             __                   .___                         \n' \
              '    |    |/ _|____   ____ |  | _____________  __| _/____    ____   ______    \n' \
              '    |      < /  _ \ /    \|  |/ /  _ \_  __ \/ __ |\__  \  /    \ /  ___/    \n' \
              '    |    |  (  <_> )   |  \    <  <_> )  | \/ /_/ | / __ \|   |  \\___ \     \n' \
              '    |____|__ \____/|___|  /__|_ \____/|__|  \____ |(____  /___|  /____  >    \n' \
              '            \/          \/     \/                \/     \/     \/     \/     \n\n' \
              'Skriv ett ord för att finna dess konkordans \n' \
              'Ctrl-D för att avsluta \n'
    print(welcome)
    print('> ', end='')
    sys.stdout.flush()
    for line in sys.stdin:
        word = line.rstrip('\n').lower()
        milliseconds = korpus_search(index_reader, korpus_handler, word, stupid=args.stupid)
        print('Sökningen tog {} millisekunder.'.format(milliseconds))
        print('> ', end='')
        sys.stdout.flush()


def korpus_search(index_reader, korpus_handler, word, stupid=True):

    start_time = datetime.now()
    offsets = index_reader.find(word)
    end_time = datetime.now()

    if offsets:
        print('Hittade {} förekomster i texten.'.format(len(offsets)))
    else:
        print('Inga träffar')
        

    if len(offsets) > 25 and stupid:
        while True:
            print('Det finns mer än 25 förekomster, vill du skriva ut alla? (j/n)')
            sys.stdout.flush()
            reply = sys.stdin.readline().rstrip('\n').lower()
            if reply in ['n','nej','no']:
                offsets = offsets[:25]
                break
            elif reply in ['y', 'yes', 'j', 'ja', 'fuck you']:
                break
            else:
                print('Inte ett giltigt svar')

    if offsets:
        for offset in offsets:
            print(korpus_handler.read(offset, b=30, a=len(word)+30))

    return (end_time - start_time).microseconds / 1000


class KorpusHandler():

    def __init__(self, filename):
        self.korpus = open(filename, 'r', encoding='iso-8859-1')
        self.offset_max = os.stat(filename).st_size - 2

    def __del__(self):
        self.korpus.close()

    def read(self, offset, b=20, a=20):
        b = min(offset, b)
        a = min(a, self.offset_max - offset)
        self.korpus.seek(offset-b)
        text = self.korpus.read(b + a + 1)

        return text.replace('\n', ' ')


if __name__ == '__main__':
    main()
