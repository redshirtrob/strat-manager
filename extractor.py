#!/usr/bin/env python

import base64
import datetime
import mailbox
import os
import quopri
import tnefparse

from pymongo import MongoClient

from strat.utils import get_report_type, get_title

def extract_html_from_text_html(part):
    return [part.get_payload(decode=True)]

def extract_html_from_application_ms_tnef(message=None, part=None):
    cte = part.get('Content-Transfer-Encoding')
    if cte == 'quoted-printable':
        decoded_part = quopri.decodestring(part.get_payload())
    elif cte == 'base64':
        decoded_part = base64.b64decode(part.get_payload())
    else:
        print "Don't know how to decode: '{}'".format(cte)
        
    tnef = tnefparse.TNEF(decoded_part)
    return [report.data for report in tnef.attachments]

def main(mbox_file, stash_directory=None, use_db=False):
    mbox = mailbox.mbox(mbox_file)
    should_stash = stash_directory is not None

    if use_db:
        client = MongoClient('mongodb://localhost:27017')
        db = client.get_database('extractor')
        client.drop_database(db)
        collection = db.reports

    total_report_count = 0
    report_count = 0
    current_message_index = 0
    for message in mbox:
        subject = message['subject']
        message_id = message['Message-ID']

        # Skip replies and forwards
        if subject.lower().startswith('re:') or subject.lower().startswith('fw:'):
            continue

        # Skip spring training and post-season games
        non_season = ['lcs', 'spring training', 'super series', 'ss', 'wcs']
        if any(x in subject.lower() for x in non_season):
            continue
        
        print "Processing: {}".format(message_id)
        print "\tSubject: {}".format(subject)

        count = 0
        parts = message.get_payload()
        for part in parts:
            if isinstance(part, str):
                continue

            reports = []
            content_type = part.get_content_type()
            if content_type == 'text/html':
                reports = extract_html_from_text_html(part)
            elif content_type == 'application/ms-tnef':
                reports = extract_html_from_application_ms_tnef(message, part)
            else:
                if content_type != 'text/plain' and content_type != 'multipart/alternative':
                    print "Skipping: {}".format(content_type)

            for report in reports:
                report_type = get_report_type(report)
                print "\tTitle: {} ({})".format(get_title(report), report_type)
                
                document = {'message_id' : message_id,
                            'subject' : subject,
                            'content' : report,
                            'type' : report_type}
                if should_stash:
                    filename = '{}.dat'.format(report_count)
                    full_path = os.path.join(stash_directory, filename)
                    document['filename'] = full_path
                    with open(full_path, 'w') as f:
                        f.write(report)
                    print "\t\tFile: {}".format(filename)

                if use_db:
                    collection.insert_one(document)
                report_count += 1
                count += 1
            total_report_count += len(reports)
                
        if count == 0:
            print "\tERROR: Couldn't extract data from {}".format(subject)
        else:
            print "\tExtracted {} data file(s) from {}".format(count, subject)
        current_message_index += 1
    print "Extracted {} reports from data set".format(total_report_count)
    if use_db:
        client.close()
            
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Extract Strat-O-Matic Report files from email')
    parser.add_argument('--stash', nargs='?', dest='dir',
                        help='directory to dump report contents')
    parser.add_argument('--use-db', action='store_true', default=False,
                        help='insert data files into a database')
    parser.add_argument('file', metavar='FILE', help='the mailbox file to parse')
    args = parser.parse_args()

    main(args.file, args.dir, args.use_db)
