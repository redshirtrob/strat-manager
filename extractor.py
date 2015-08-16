#!/usr/bin/env python

import base64
import datetime
import mailbox
import os
import quopri
import tnefparse

from bs4 import BeautifulSoup

from pymongo import MongoClient

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
    return [attachment.data for attachment in tnef.attachments]

def get_title(html):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('title')
    if title is not None:
        return title.contents[0]
    return "UNKNOWN"

def main(mbox_file, stash_directory=None):
    mbox = mailbox.mbox(mbox_file)
    should_stash = stash_directory is not None

    client = MongoClient('mongodb://localhost:27017')
    db = client.get_database('extractor')
    client.drop_database(db)

    collection = db.attachments

    total_attachment_count = 0
    attachment_count = 0
    current_message_index = 0
    for message in mbox:
        subject = message['subject']
        message_id = message['Message-ID']

        # Skip replies and forwards
        if subject.lower().startswith('re:') or subject.lower().startswith('fw:'):
            continue
        
        print "Processing: {}".format(message_id)
        print "\tSubject: {}".format(subject)

        count = 0
        parts = message.get_payload()
        for part in parts:
            if isinstance(part, str):
                continue

            attachments = []
            content_type = part.get_content_type()
            if content_type == 'text/html':
                attachments = extract_html_from_text_html(part)
                count += 1
            elif content_type == 'application/ms-tnef':
                attachments = extract_html_from_application_ms_tnef(message, part)
                count += 1
            else:
                if content_type != 'text/plain' and content_type != 'multipart/alternative':
                    print "Skipping: {}".format(content_type)

            for attachment in attachments:
                print "\tTitle: {}".format(get_title(attachment))
                
                document = {'message_id' : message_id,
                            'subject' : subject,
                            'content' : attachment}
                if should_stash:
                    filename = '{}.dat'.format(attachment_count)
                    full_path = os.path.join(stash_directory, filename)
                    document['filename'] = full_path
                    with open(full_path, 'w') as f:
                        f.write(attachment)
                collection.insert_one(document)
                attachment_count += 1
            total_attachment_count += len(attachments)
                
        if count == 0:
            print "\tERROR: Couldn't extract data from {}".format(subject)
        else:
            print "\tExtracted {} data file(s) from {}".format(count, subject)
        current_message_index += 1
    print "Extracted {} attachments from data set".format(total_attachment_count)
    client.close()
            
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Extract Strat-O-Matic Report files from email')
    parser.add_argument('--stash', nargs='?', dest='dir',
                        help='directory to dump attachment contents')
    parser.add_argument('file', metavar='FILE', help='the mailbox file to parse')
    args = parser.parse_args()

    main(args.file, args.dir)
