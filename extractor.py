#!/usr/bin/env python

from bs4 import BeautifulSoup
import base64
import datetime
import mailbox
import os
import quopri
import tnefparse

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

def main():
    mbox = mailbox.mbox('BLB-Sirk.mbox')

    total_attachment_count = 0
    attachment_count = 0
    current_message_index = 0
    for message in mbox:
        subject = message['subject']
        message_id = message['Message-ID']

        # Skip replies
        if subject.lower().startswith('re:'):
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
                filename = '{}.dat'.format(attachment_count)
                print "\tTitle: {} ({})".format(get_title(attachment), filename)
                full_path = os.path.join('data-files', filename)
                with open(full_path, 'w') as f:
                    f.write(attachment)
                attachment_count += 1
            total_attachment_count += len(attachments)
                
        if count == 0:
            print "\tERROR: Couldn't extract data from {}".format(subject)
        else:
            print "\tExtracted {} data file(s) from {}".format(count, subject)
        current_message_index += 1
    print "Extracted {} attachments from data set".format(total_attachment_count)
            
if __name__ == '__main__':
    main()
