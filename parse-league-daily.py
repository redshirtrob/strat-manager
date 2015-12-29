#!/usr/bin/env python

from bs4 import BeautifulSoup
from pymongo import MongoClient
import json
import os

from GameReport import GameReportParser
from strat.utils import get_report_type, get_title, flatten
from strat.utils import REPORT_TYPE_LEAGUE_DAILY

def main(filename, stash_directory=None, use_db=False, skip_clean=False):
    with open(filename, 'r') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')

    should_stash = stash_directory is not None
    report_type = get_report_type(html)
    print "Report Type: {}".format(report_type)
    if report_type != REPORT_TYPE_LEAGUE_DAILY:
        raise Exception("Invalid Type: {}".format(report_type))
    
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

    ast = {'stories' : stories_ast, 'boxscores' : boxscores_ast}
    if not skip_clean:
        flat_ast = flatten(ast)

    if use_db:
        client = MongoClient('mongodb://localhost:27017')
        db = client.get_database('extractor')
        collection = db.attachments

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
