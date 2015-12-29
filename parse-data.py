#!/usr/bin/env python

import sys
from pymongo import MongoClient

from strat.parse import parse_league_daily, parse_game_daily
from strat.utils import flatten
from strat.utils import REPORT_TYPE_LEAGUE_DAILY, REPORT_TYPE_GAME_DAILY

def main(reprocess=False):
    client = MongoClient('mongodb://localhost:27017')
    db = client.get_database('extractor')
    collection = db.reports

    for report in collection.find():
        if report.has_key('filename'):
            print >> sys.stderr, 'Processing {}'.format(report['filename'])
        else:
            print >> sys.stderr, 'Processing {}'.format(report['message_id'])

        if report.has_key('ast'):
            if reprocess == False:
                print '    -> Already Processed'
                continue
            else:
                print '    -> Reprocessing'
        
        ast = None
        if report['type'] == REPORT_TYPE_LEAGUE_DAILY:
            ast = parse_league_daily(report['content'])
        elif report['type'] == REPORT_TYPE_GAME_DAILY:
            ast = parse_game_daily(report['content'])
        else:
            print '    -> Skipping {} ({})'.format(
                report['type'],
                report['message_id']
            )

        if ast is not None:
            report['ast'] = ast
            report['flat_ast'] = flatten(ast)
            collection.save(report)

if __name__ == '__main__':
    import argparse

    parser= argparse.ArgumentParser(description="Batch parser for Strat-O-Matic Report files")
    parser.add_argument('-r', '--reprocess', help="Reprocess all report data", action="store_true")
    args = parser.parse_args()
    
    main(args.reprocess)
