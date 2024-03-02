import pickle
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
import datetime
import logging


def create_service(client_secret_file, api_name, api_version, *scopes):
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    
    print('INFO: Initializing service creation.')

    cred = None

    pickle_file = os.path.abspath(f'credentials/token_{API_SERVICE_NAME}_{API_VERSION}.pickle')
    
    # print(pickle_file)

    print('INFO: Searching for any existing token file.')
    if os.path.exists(pickle_file):
        print('INFO: Found existing token file.')
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        print('INFO: Credentials not found or invalid. Obtaining new credentials.')
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            print('INFO: Running local server flow to obtain new credentials.')
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            print('INFO: Saving new credentials to token file.')
            pickle.dump(cred, token)

    try:
        print('INFO: Building service.')
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print('INFO: Service created successfully.')
        return service
    except Exception as error:
        print(f'ERROR: Unable to connect to service. Error occured: {error}')
        return None

def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt