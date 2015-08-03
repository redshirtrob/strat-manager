#!/usr/bin/env python

import datetime
import mailbox
import os
import quopri
import tnefparse

UNKNOWN_COUNT=0

def extract_html_from_text_html(part):
    html = part.get_payload(decode=True)
    return html

def extract_html_from_application_ms_tnef(message=None, part=None):
    html = None

    cte = part.get('Content-Transfer-Encoding')
    if cte == 'quoted-printable':
        decoded_part = quopri.decodestring(part.get_payload())
        tnef = tnefparse.TNEF(decoded_part)
        if len(tnef.attachments) == 0:
            print "Didn't find any attachments: {}".format(len(tnef.attachments))
        elif len(tnef.attachments) > 1:
            print "Found more than one attatchment: {}".format(len(tnef.attachments))
        else:
            attachment = tnef.attachments[0]
            html = attachment.data
    else:
        print "Don't know how to decode: '{}'".format(cte)
        
    return html

def gen_filename(subject, count):
    global UNKNOWN_COUNT

    try:
        _, date = subject.split()
        m, d, y = map(int, date.split('/'))
        d = datetime.datetime(y+2000, m, d)
        base = '{:%Y%m%d}'.format(d)
    except ValueError as e:
        base = 'UNKNOWN{}'.format(UNKNOWN_COUNT)
        UNKNOWN_COUNT += 1
        
    if count > 0:
        filename = '{}{}DAY.htm'.format(base, count)
    else:
        filename = '{}DAY.htm'.format(base)

    return filename

def main():
    mbox = mailbox.mbox('BLB-Sirk.mbox')

    current_message_index = 0
    for message in mbox:
        subject = message['subject']

        if subject.lower().startswith('re'):
            continue
        
        print "Processing: {}".format(subject)

        count = 0
        parts = message.get_payload()
        for part in parts:
            if isinstance(part, str):
                continue

            filename = html = None
            content_type = part.get_content_type()
            if content_type == 'text/html':
                filename = part.get_filename()
                if filename is None:
                    filename = gen_filename(subject, count)
                html = extract_html_from_text_html(part)
                print "Extracted {} file: {}".format(content_type, filename)
                count += 1
            elif content_type == 'application/ms-tnef':
                filename = gen_filename(subject, count)
                html = extract_html_from_application_ms_tnef(message, part)
                print "Extracted {} file: {}".format(content_type, filename)
                count += 1
            else:
                if content_type != 'text/plain' and content_type != 'multipart/alternative':
                    print "Skipping: {}".format(content_type)

            if html is not None:
                full_path = os.path.join('data-files', filename)
                with open(full_path, 'w') as f:
                    f.write(html)

        if count == 0:
            print "ERROR: Couldn't extract data from {}".format(subject)
        else:
            print "Extracted {} data file(s) from {}".format(count, subject)
            
if __name__ == '__main__':
    main()
