#!/usr/bin/env python

import sys
import json
import operator

from pymongo import MongoClient

INT_KEYS = ('part', 'game_count', 'season_count', )

def clean(item, key, keypath):
    if item is None and key in INT_KEYS:
        item = '1'
    elif isinstance(item, str) or isinstance(item, unicode):
        item = item.strip()
        if (key == 'name' or key == 'player_name') and item.endswith('-'):
            item = item.rstrip('-')
            
    return item

def flatten(item, key=None, keypath=None):
    flat_item = item
    if isinstance(item, dict):
        flat_item = dict()
        for k, v in item.iteritems():
            kp = k if key is None else '{}.{}'.format(keypath, k)
            flat_item[k] = flatten(v, k, kp)
    elif isinstance(item, list):
        flat_item = list()
        index = 0
        for value in item:
            kp = '{}[{}]'.format(keypath, index)
            nv = flatten(value, keypath=kp)
            if isinstance(nv, list):
                flat_item += nv
            else:
                flat_item.append(nv)
            index += 1
    else:
        flat_item = clean(item, key, keypath)
    return flat_item

def main(reprocess=False):
    client = MongoClient('mongodb://localhost:27017')
    db = client.get_database('extractor')
    collection = db.attachments

    for attachment in collection.find():
        print >> sys.stderr, 'Cleaning {}'.format(attachment['filename'])
        if not attachment.has_key('ast'):
            print '    -> Nothing to clean'
            continue
        else:
            if attachment.has_key('flat_ast'):
                if reprocess == False:
                    print '    -> Already Clean'
                    continue
                else:
                    print '    -> Recleaning'
            else:
                print '    -> Cleaning'
        ast = attachment['ast']
        attachment['flat_ast'] = flatten(ast)
        collection.save(attachment)

if __name__ == '__main__':
    import argparse

    parser= argparse.ArgumentParser(description="Batch parser for cleaning Strat-O-Matic ASTs")
    parser.add_argument('-r', '--reprocess', help="Reprocess all ASTs", action="store_true")
    args = parser.parse_args()
    
    main(args.reprocess)
