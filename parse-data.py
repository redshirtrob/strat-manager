#!/usr/bin/env python

import json

from bs4 import BeautifulSoup
from GameReport import GameReportParser
from pymongo import MongoClient

def parse_league_daily(content):
    soup = BeautifulSoup(content, 'html.parser')
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

    return {'stories' : stories_ast, 'boxscores' : boxscores_ast}

def parse_game_daily(content):
    soup = BeautifulSoup(content, 'html.parser')
    full_recap = soup.find('pre')
    full_recap_string = full_recap.prettify()

    parser = GameReportParser(parseinfo=False)
    ast = parser.parse(full_recap_string, 'full_recap')
    return ast

def main():
    client = MongoClient('mongodb://localhost:27017')
    db = client.get_database('extractor')
    collection = db.attachments

    for attachment in collection.find():
        print 'Processing {}'.format(attachment['filename'])
        ast = None
        if attachment['type'] == 'League Daily':
            ast = parse_league_daily(attachment['content'])
        elif attachment['type'] == 'Game Daily':
            ast = parse_game_daily(attachment['content'])
        else:
            print 'Skipping {}'.format(attachment['message_id'])

if __name__ == '__main__':
    main()
