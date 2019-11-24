# EXAMPLES OF PYTHON AND GMAIL INTERACTION
# NEED TO GIVE AUTHOURIZATION TO GMAIL FOR THE APPLICATION TO ACCESS AND INTERACT

# RETREIVE MAIL
from googleapiclient.discovery import build
import httplib2
import oauth2client
from oauth2client import file, client, tools
import os
from apiclient import errors, discovery

# If modifying these scopes, delete the file token.json.
#SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'credentials.json'
APPLICATION_NAME = 'Gmail API Python Send Email'


def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,CLIENT_SECRET_FILE)
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()

    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
        print ('Storing credentials to ') + credential_path
    return credentials

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    # store = file.Storage('token.json')
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])

if __name__ == '__main__':
    main()
