#!/usr/bin/env python

import mailbox
import quopri
import tnefparse

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

            content_type = part.get_content_type()
            if content_type == 'text/html':
                html = extract_html_from_text_html(part)
                extracted_html = True
                count += 1
            elif content_type == 'application/ms-tnef':
                html = extract_html_from_application_ms_tnef(message, part)
                extracted_html = True
                count += 1
            else:
                print "Skipping: {}".format(content_type)

        if count == 0:
            print "ERROR: Couldn't extract data from {}".format(subject)
        else:
            print "Extracted {} data file(s) from {}".format(count, subject)
            
if __name__ == '__main__':
    main()
