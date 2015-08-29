#!/usr/bin/env python

import json

from bs4 import BeautifulSoup
from GameReport import GameReportParser
from pymongo import MongoClient
from grako.exceptions import FailedToken

def parse_league_daily(content):
    soup = BeautifulSoup(content, 'html.parser')
    tables = soup.find_all('table')

    parser = GameReportParser(parseinfo=False)

    print '    -> Processing stories'
    stories_ast = None
    for table in tables:
        try:
            stories_ast = parser.parse(table.prettify(), 'game_story_table')
            break
        except FailedToken:
            pass

    print '    -> Processing boxscores'
    boxscores_ast = None
    for table in tables:
        try:
            boxscores_ast = parser.parse(table.prettify(), 'boxscore_table')
            break
        except FailedToken:
            pass

    if stories_ast is None or boxscores_ast is None:
        raise Exception

    return {'stories' : stories_ast, 'boxscores' : boxscores_ast}

def parse_game_daily(content):
    soup = BeautifulSoup(content, 'html.parser')
    full_recap = soup.find('pre')
    full_recap_string = full_recap.prettify()

    parser = GameReportParser(parseinfo=False)
    print '    -> Processing combined'
    ast = parser.parse(full_recap_string, 'full_recap')
    return ast

def main(reprocess=False):
    client = MongoClient('mongodb://localhost:27017')
    db = client.get_database('extractor')
    collection = db.attachments

    for attachment in collection.find():
        print 'Processing {}'.format(attachment['filename'])
        if attachment.has_key('ast'):
            if reprocess == False:
                print '    -> Already Processed'
                continue
            else:
                print '    -> Reprocessing'
        
        ast = None
        if attachment['type'] == 'League Daily':
            ast = parse_league_daily(attachment['content'])
        elif attachment['type'] == 'Game Daily':
            ast = parse_game_daily(attachment['content'])
        else:
            print '    -> Skipping {} ({})'.format(
                attachment['type'],
                attachment['message_id']
            )

        if ast is not None:
            attachment['ast'] = ast
            collection.save(attachment)

if __name__ == '__main__':
    import argparse

    parser= argparse.ArgumentParser(description="Batch parser for Strat-O-Matic Report files")
    parser.add_argument('-r', '--reprocess', help="Reprocess all attachment data", action="store_true")
    args = parser.parse_args()
    
    main(args.reprocess)
