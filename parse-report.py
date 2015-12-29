#!/usr/bin/env python

from pymongo import MongoClient
import json
import os

from strat.parse import parse_league_daily, parse_game_daily
from strat.utils import get_report_type, get_title, flatten
from strat.utils import REPORT_TYPE_LEAGUE_DAILY, REPORT_TYPE_GAME_DAILY

def main(filename, stash_directory=None, use_db=False, skip_clean=False):
    should_stash = stash_directory is not None
    
    with open(filename, 'r') as f:
        html = f.read()

    report_type = get_report_type(html)
    print "Report Type: {}".format(report_type)
    if report_type == REPORT_TYPE_LEAGUE_DAILY:
        ast = parse_league_daily(html)
    elif report_type == REPORT_TYPE_GAME_DAILY:
        ast = parse_game_daily(html)
    else:
        raise Exception("Invalid Type: {}".format(report_type))

    if not skip_clean:
        flat_ast = flatten(ast)

    if use_db:
        client = MongoClient('mongodb://localhost:27017')
        db = client.get_database('extractor')
        collection = db.reports

        document = {'filename': os.path.basename(filename),
                    'subject': '',
                    'content': html,
                    'type': report_type,
                    'ast': ast
        }

        if not skip_clean:
            document['flat_ast'] = flat_ast
            
        collection.insert_one(document)
        client.close()
        
    if should_stash:
        rootname = os.path.splitext(os.path.basename(filename))[0]
        dst_filename = '{}-ast.dat'.format(rootname)
        full_path = os.path.join(stash_directory, dst_filename)
        stash_ast = ast if skip_clean else flat_ast
        with open(full_path, 'w') as f:
            json.dump(stash_ast, f, indent=2)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="League daily parser for Strat-O-Matic Report files")
    parser.add_argument('--stash', nargs='?', dest='dir',
                        help='directory to dump ASTs to')
    parser.add_argument('--skip-clean', action='store_true', default=False,
                        help='don\'t clean the AST before writing')
    parser.add_argument('--use-db', action='store_true', default=False,
                        help='insert AST into a database')
    parser.add_argument('file', metavar="FILE", help="the input file to parse")
    args = parser.parse_args()
    
    main(args.file, args.dir, args.use_db, args.skip_clean)
