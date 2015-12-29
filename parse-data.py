#!/usr/bin/env python

import sys
from pymongo import MongoClient

from strat.parse import parse_league_daily, parse_game_daily
from strat.utils import flatten
from strat.utils import REPORT_TYPE_LEAGUE_DAILY, REPORT_TYPE_GAME_DAILY

def main(reprocess=False):
    client = MongoClient('mongodb://localhost:27017')
    db = client.get_database('extractor')
    collection = db.attachments

    for attachment in collection.find():
        if attachment.has_key('filename'):
            print >> sys.stderr, 'Processing {}'.format(attachment['filename'])
        else:
            print >> sys.stderr, 'Processing {}'.format(attachment['message_id'])

        if attachment.has_key('ast'):
            if reprocess == False:
                print '    -> Already Processed'
                continue
            else:
                print '    -> Reprocessing'
        
        ast = None
        if attachment['type'] == REPORT_TYPE_LEAGUE_DAILY:
            ast = parse_league_daily(attachment['content'])
        elif attachment['type'] == REPORT_TYPE_GAME_DAILY:
            ast = parse_game_daily(attachment['content'])
        else:
            print '    -> Skipping {} ({})'.format(
                attachment['type'],
                attachment['message_id']
            )

        if ast is not None:
            attachment['ast'] = ast
            attachment['flat_ast'] = flatten(ast)
            collection.save(attachment)

if __name__ == '__main__':
    import argparse

    parser= argparse.ArgumentParser(description="Batch parser for Strat-O-Matic Report files")
    parser.add_argument('-r', '--reprocess', help="Reprocess all attachment data", action="store_true")
    args = parser.parse_args()
    
    main(args.reprocess)
