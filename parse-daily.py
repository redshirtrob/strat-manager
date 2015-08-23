#!/usr/bin/env python

from bs4 import BeautifulSoup
from GameReport import GameReportParser

import json

def main(filename):
    with open(filename, 'r') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table')

    stories_index = len(tables)-3
    stories = tables[stories_index]
    stories_string = stories.prettify()

    boxscores_index = len(tables)-2
    boxscores = tables[boxscores_index]
    boxscores_string = boxscores.prettify()

    parser = GameReportParser(parseinfo=False)
    stories_ast = parser.parse(stories_string, 'game_story_table')
    boxscores_ast = parser.parse(boxscores_string, 'boxscore_table')

    dct = {'stories' : stories_ast, 'boxscores' : boxscores_ast}
    print json.dumps(dct, indent=2)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Daily parser for Strat-O-Matic Report files")
    parser.add_argument('file', metavar="FILE", help="the input file to parse")
    args = parser.parse_args()
    
    main(args.file)
