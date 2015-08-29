#!/usr/bin/env python

import sys
import json
import operator

from pymongo import MongoClient

INT_KEYS = ('part', 'game_count', 'season_count', )

def clean(item, key):
    if item is None and key in INT_KEYS:
        item = 1
    return item

def flatten(item, key=None):
    flat_item = item
    if isinstance(item, dict):
        flat_item = dict()
        for key, value in item.iteritems():
            flat_item[key] = flatten(value, key)
    elif isinstance(item, list):
        flat_item = list()
        for value in item:
            nv = flatten(value)
            if isinstance(nv, list):
                flat_item += nv
            else:
                flat_item.append(nv)
    else:
        flat_item = clean(item, key)
    return flat_item

def main(reprocess=False):
    client = MongoClient('mongodb://localhost:27017')
    db = client.get_database('extractor')
    collection = db.attachments

    for attachment in collection.find():
        print >> sys.stderr, 'Flattening {}'.format(attachment['filename'])
        if not attachment.has_key('ast'):
            print '    -> Nothing to flatten'
            continue
        else:
            if attachment.has_key('flat_ast'):
                if reprocess == False:
                    print '    -> Already Flattened'
                    continue
                else:
                    print '    -> Reflattening'

        ast = attachment['ast']
        print '    -> Flattening'
        attachment['flat_ast'] = flatten(ast)
        collection.save(attachment)

if __name__ == '__main__':
    import argparse

    parser= argparse.ArgumentParser(description="Batch parser for cleaning Strat-O-Matic ASTs")
    parser.add_argument('-r', '--reprocess', help="Reprocess all ASTs", action="store_true")
    args = parser.parse_args()
    
    main(args.reprocess)
