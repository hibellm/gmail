'''
Reference : https://developers.google.com/sheets/api/quickstart/python


https://github.com/robin900/gspread-formatting
'''

#
# from __future__ import print_function
import pickle
import os.path
import gspread
from gspread_formatting import *     # PIP INSTALL GSPREAD_FORMATTING


from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('./sheets/gsheet-access.json', scope)

gc = gspread.authorize(credentials)


# OPENING A SPREADSHEET BY NAME
wks = gc.open("1nCyw-9KB1Ut07BNQ8_zQLVvrScOZvkKPMAorcu5Ad2U").sheet1

# WORKSHEET ACTIONS

wks.update_title("Sheet 1")

# FETCH THE DATA
cell_list = wks.range('A2:D4')

# UPDATE VALUE (ROW/COL)
wks.update_acell('D2', "TRUE")
wks.update_cell(4, 1, 'TRUE')  # TRUE AS A CHECKBOX


# UPDATE FORMAT OF CELL - SUING GSPREAD_FORMATTING MODULE


fmt = get_effective_format(wks, 'A1')

fmt = cellFormat(
    backgroundColor=color(1, 0.5, 0.5),
    textFormat=textFormat(bold=True, foregroundColor=color(0.4, 0, 1))
    )

format_cell_range(wks, 'A1:A10', fmt)






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
