#!/usr/bin/env python

from bs4 import BeautifulSoup
from GameReport import GameReportParser

import json

def main(filename):
    with open(filename, 'r') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    full_recap = soup.find('pre')
    full_recap_string = full_recap.prettify()

    parser = GameReportParser(parseinfo=False)
    ast = parser.parse(full_recap_string, 'full_recap')
    print json.dumps(ast, indent=2)

if __name__ == '__main__':
    import argparse

    parser= argparse.ArgumentParser(description="Single game parser for Strat-O-Matic Report files")
    parser.add_argument('file', metavar="FILE", help="the input file to parse")
    args = parser.parse_args()
    
    main(args.file)
