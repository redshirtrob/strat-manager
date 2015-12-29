#!/usr/bin/env python

import sys
import json
import operator

from pymongo import MongoClient

from strat.utils import flatten

def main(reprocess=False):
    client = MongoClient('mongodb://localhost:27017')
    db = client.get_database('extractor')
    collection = db.reports

    for report in collection.find():
        if report.has_key('filename'):
            print >> sys.stderr, 'Cleaning {}'.format(report['filename'])
        else:
            print >> sys.stderr, 'Cleaning {}'.format(report['message_id'])
        if not report.has_key('ast'):
            print '    -> Nothing to clean'
            continue
        else:
            if report.has_key('flat_ast'):
                if reprocess == False:
                    print '    -> Already Clean'
                    continue
                else:
                    print '    -> Recleaning'
            else:
                print '    -> Cleaning'
        ast = report['ast']
        report['flat_ast'] = flatten(ast)
        collection.save(report)

if __name__ == '__main__':
    import argparse

    parser= argparse.ArgumentParser(description="Batch parser for cleaning Strat-O-Matic ASTs")
    parser.add_argument('-r', '--reprocess', help="Reprocess all ASTs", action="store_true")
    args = parser.parse_args()
    
    main(args.reprocess)
