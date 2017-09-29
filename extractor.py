#!/usr/bin/env python

import base64
import datetime
import mailbox
import os
import quopri
import tnefparse

from strat.utils import (
    get_report_type,
    get_title,
    is_game_report
)

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

def get_filename_from_part(part):
    filename = part.get_filename()
    if filename == 'winmail.dat':
        index = part.as_string().find('.htm')
        filename = part.as_string()[index-11:index+4]
    if len(filename) == 0:
        filename = None
    return filename

def main(mbox_file, stash_directory=None):
    mbox = mailbox.mbox(mbox_file)
    should_stash = stash_directory is not None

    total_report_count = 0
    report_count = 0
    for message in mbox:
        subject = message['subject']
        message_id = message['Message-ID']

        # Skip spring training and post-season games
        non_season = ['lcs', 'spring training', 'super series', 'ss', 'wcs', 'preseason']
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
                if not is_game_report(report_type):
                    continue
                
                print "\tTitle: {} ({})".format(get_title(report), report_type)
                
                if should_stash:
                    filename = get_filename_from_part(part)
                    if filename is not None:
                        print "\t\tFile: {}".format(filename)
                        full_path = os.path.join(stash_directory, filename)
                        with open(full_path, 'w') as f:
                            f.write(report)

                report_count += 1
                count += 1
            total_report_count += len(reports)
                
        if count == 0:
            print "\tERROR: Couldn't extract data from {}".format(subject)
        else:
            print "\tExtracted {} data file(s) from {}".format(count, subject)
    print "Extracted {} reports from data set".format(total_report_count)
            
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Extract Strat-O-Matic Report files from email')
    parser.add_argument('--stash', nargs='?', dest='dir',
                        help='directory to dump report contents')
    parser.add_argument('file', metavar='FILE', help='the mailbox file to parse')
    args = parser.parse_args()

    main(args.file, args.dir)
