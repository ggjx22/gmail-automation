import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

CLIENT_FILE = '../credentials/gg-gmail-automation.json'
SCOPES = ['https://mail.google.com/']

credentials = None

# create token.json if user is authorizing the first time
# token.json stores the user's access and refresh tokens
if os.path.exists('../credentials/token.json'):
    credentials = Credentials.from_authorized_user_file(filename='../credentials/token.json', scopes=SCOPES)

# when there is no credentials or credentials expired
if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file=CLIENT_FILE, scopes=SCOPES)
        credentials = flow.run_local_server(port=0)
    # save token.json for the next run
    with open('../credentials/token.json', 'w') as token:
        token.write(credentials.to_json())

try:
    # call the gmail api
    service_gmail = build('gmail', 'v1', credentials=credentials)
    results = service_gmail.users().labels().list(userId='me').execute()
    labels = results.get('lables', [])
    
    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])

except HttpError as error:
    print(f'An error occured: {error}')