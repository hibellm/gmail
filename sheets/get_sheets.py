'''
Reference : https://developers.google.com/sheets/api/quickstart/python
'''

#
# from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import gspread

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SAMPLE_RANGE_NAME = 'Class Data!A2:E'

MY_SPREADSHEET_ID = '1nCyw-9KB1Ut07BNQ8_zQLVvrScOZvkKPMAorcu5Ad2U'
MY_RANGE_NAME = 'Sheet1!A1:E'




def getservice():
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
            flow = InstalledAppFlow.from_client_secrets_file('./sheets/credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    return service


service = getservice()




wks = service.open(MY_SPREADSHEET_ID).sheet1










def readsheet(sheetid, sheetrange):

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheetid,
                                range=sheetrange).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print(f'Found data : rows {len(values)}')

    return values

x = readsheet(MY_SPREADSHEET_ID, MY_RANGE_NAME)


def updatesheet(sheetid, sheetrange, uptype='USER_DEFINED'):

    values = [
        [
            # Cell values ...
        ],
        # Additional rows ...
    ]
    body = {
        'values': values
    }
    result = service.spreadsheets().values().update(
        spreadsheetId=sheetid,
        range=sheetrange,
        valueInputOption=uptype,
        body=body).execute()

    # print(f'{result.get('updatedCells')} cells updated.')
