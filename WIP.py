
from apiclient import errors
import os
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

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



def gmail_labels():

    """Get a list of Labels from the user's mailbox.
    """

    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels (in account):')
        for label in labels:
            print('  '+label['name']+' [id:'+label['id']+']')

    return labels

def ListMessagesMatchingQuery(service, user_id, query=''):

  """List all Messages of the user's mailbox matching the query.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    query: String used to filter messages returned.
    Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

  Returns:
    List of Messages that match the criteria of the query. Note that the
    returned list contains Message IDs, you must use get with the
    appropriate ID to get the details of a Message.
  """
  try:
    response = service.users().messages().list(userId=user_id,
                                               q=query).execute()
    messages = []
    if 'messages' in response:
      messages.extend(response['messages'])

    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      response = service.users().messages().list(userId=user_id, q=query,
                                         pageToken=page_token).execute()
      messages.extend(response['messages'])

    return messages
  except errors.HttpError as error:
    print ('An error occurred: %s' % error)


def ListMessagesWithLabels(service, user_id, label_ids=[]):
    """List all Messages of the user's mailbox with label_ids applied.

    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      label_ids: Only return Messages with these labelIds applied.

    Returns:
      List of Messages that have all required Labels applied. Note that the
      returned list contains Message IDs, you must use get with the
      appropriate id to get the details of a Message.
    """
    try:
        response = service.users().messages().list(userId=user_id,labelIds=label_ids).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id,labelIds=label_ids,pageToken=page_token).execute()
            messages.extend(response['messages'])

            return messages

    except errors.HttpError as error:
        print ('An error occurred: %s' % error)

"""Get a list of Threads from the user's mailbox.
"""

def ListThreadsMatchingQuery(service, user_id, query=''):
  """List all Threads of the user's mailbox matching the query.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    query: String used to filter messages returned.
           Eg.- 'label:UNREAD' for unread messages only.

  Returns:
    List of threads that match the criteria of the query. Note that the returned
    list contains Thread IDs, you must use get with the appropriate
    ID to get the details for a Thread.
  """
  try:
    response = service.users().threads().list(userId=user_id, q=query).execute()
    threads = []
    if 'threads' in response:
      threads.extend(response['threads'])

    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      response = service.users().threads().list(userId=user_id, q=query,
                                        pageToken=page_token).execute()
      threads.extend(response['threads'])

    return threads
  except errors.HttpError as error:
    print ('An error occurred: %s' % error)


def ListThreadsWithLabels(service, user_id, label_ids=[]):
  """List all Threads of the user's mailbox with label_ids applied.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    label_ids: Only return Threads with these labelIds applied.

  Returns:
    List of threads that match the criteria of the query. Note that the returned
    list contains Thread IDs, you must use get with the appropriate
    ID to get the details for a Thread.
  """
  try:
    response = service.users().threads().list(userId=user_id,
                                              labelIds=label_ids).execute()
    threads = []
    if 'threads' in response:
      threads.extend(response['threads'])

    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      response = service.users().threads().list(userId=user_id,
                                                labelIds=label_ids,
                                                pageToken=page_token).execute()
      threads.extend(response['threads'])

    return threads
  except errors.HttpError as error:
    print ('An error occurred: %s' % error)


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





def GetThread(service, user_id, thread_id):
    """Get a Thread.
    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        thread_id: The ID of the Thread required.

    Returns:
        Thread with matching ID.
    """
    try:
        thread = service.users().threads().get(userId=user_id, id=thread_id).execute()
        messages = thread['messages']
        print('thread id: %s - number of messages in this thread: %d' % (thread['id'], len(messages)))
        return thread

    except errors.HttpError as error:
        print('An error occurred: %s' % error)

GetThread(service, 'me' ,'168c89f74fa17f97')

"""Get Message with given ID.
"""

import base64
import email
from apiclient import errors

def GetMessage(service, user_id, msg_id):
  """Get a Message with given ID.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.

  Returns:
    A Message.
  """
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id,format='raw').execute()

    print('Message snippet: %s' % message['snippet'])

    return message
  except errors.HttpError as error:
    print('An error occurred: %s' % error)

msg=GetMessage(service,user_id,'168c89f74fa17f97')

def GetMimeMessage(service, user_id, msg_id):
  """Get a Message and use it to create a MIME Message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.

  Returns:
    A MIME Message, consisting of data from Message.
  """
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id,
                                             format='raw').execute()

    print('Message snippet: %s' % message['snippet'])

    msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))

    # mime_msg = email.message_from_string(msg_str)

    return mime_msg
  except errors.HttpError as error:
    print('An error occurred: %s' % error)

x=GetMimeMessage(service,user_id,'168c89f74fa17f97')
msg_id='168c89f74fa17f97'





user_id='me'
thread_id='168c89f74fa17f97'



'''RUN THE FUNCTIONS ON THE GMAIL ACCOUNT
'''


service=get_service()

labels=gmail_labels()

mailwithatt=ListMessagesMatchingQuery(service, 'me', 'from:Charlotte.Cope@attwells.com ')

<<<<<<< 115240e923145d39ff598e65ca6a6a3e99022a89
=======
mailwithatt = ListMessagesMatchingQuery(service, 'me', 'from:xxx')
>>>>>>> removed mail address







<<<<<<< 115240e923145d39ff598e65ca6a6a3e99022a89
#GET THE MESSAGE IDS AND MKDIR
subject='RE:dummy subject'
store_dir='e:/gmailtest/'
path=os.path.join(store_dir,subject.replace(':','-'))
store_folder=os.mkdir(path)
=======
mailwithatt = ListMessagesMatchingQuery(service, 'me', 'from:xxx')
>>>>>>> removed mail address


for att in mailwithatt:
    GetAttachments(service, 'me', att['id'], store_folder)




# print(y)