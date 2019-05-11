

import smtplib
import time
import imaplib
import email

# -------------------------------------------------
#
# Utility to read email from Gmail Using Python
#
# ------------------------------------------------

def read_email_from_gmail():

    ORG_EMAIL   = "@gmail.com"
    FROM_EMAIL  = "xx" + ORG_EMAIL
    FROM_PWD    = "xx"
    IMAP_SERVER = "imap.gmail.com"
    IMAP_PORT   = 993
    SMTP_SERVER = "imap.gmail.com"
    SMTP_PORT   = 993


    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL, FROM_PWD)
        mail.select('Drafts')

        type, data = mail.search(None, 'ALL')
        mail_ids = data[0]

        id_list = mail_ids.split()

        for i in reversed(id_list):
            typ, data = mail.fetch(i, '(RFC822)')

            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1].decode('utf-8'))
                    email_subject = msg['subject']
                    email_from = msg['from']
                    print('From : ' + email_from)
                    print('Subject : ' + email_subject + '\n')

    except Exception as e:
        print(str(e))


read_email_from_gmail()

