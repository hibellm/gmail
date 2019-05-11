
from apiclient import errors
import os
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def get_service():

    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    return service

service=get_service()


"""Retrieve an attachment from a Message.
"""

import base64
from apiclient import errors

def GetAttachments(service, user_id, msg_id, store_dir):
    """Get and store attachment from Message with given id.

    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      msg_id: ID of Message containing attachment.
      store_dir: The directory used to store attachments.
    """
    try:
      message = service.users().messages().get(userId=user_id, id=msg_id).execute()

      for part in message['payload']['parts']:
        if part['filename']:
          attachment = service.users().messages().attachments().get(userId='me', messageId=message['id'],id=part['body']['attachmentId']).execute()
          file_data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))

          path = ''.join([store_dir, part['filename']])

          f = open(path, 'wb')
          f.write(file_data)
          f.close()

    except errors.HttpError as error:
        print ('An error occurred: %s' % error)


GetAttachments(service, 'me', '15aa00f7c6ef510b', 'e:/gmailtest')

user_id='me'
msg_id='15aa00f7c6ef510b'
store_dir='e:/gmailtest'