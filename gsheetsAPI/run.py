from pprint import pprint

import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE = 'creds.json'
spreadsheet_id = '1HtUXsOeRbGEy9r-FyMl1ahNAtbDRwPufKhAcQiEK5FA'

creds = ServiceAccountCredentials.from_json_keyfile_name(
    filename=CREDENTIALS_FILE,
    scopes=['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])

service = googleapiclient.discovery.build('sheets', 'v4', credentials=creds)


if __name__ == "__main__":
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='C2:J17',
        majorDimension='ROWS'
    ).execute()

    pprint(values)


