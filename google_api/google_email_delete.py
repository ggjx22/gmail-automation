from typing import List
from google_api.google_api_utils import create_service
import os


CLIENT_SERVICE_FILE = os.path.abspath('credentials/gg-gmail-automation.json')
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

gmail_service = create_service(CLIENT_SERVICE_FILE, API_NAME, API_VERSION, SCOPES)

def get_label_id(label_name: str=None):
    try:
        print(f'INFO: Retrieving label ID for label: {label_name}')
        labels = gmail_service.users().labels().list(
            userId='me'
        ).execute()
        
        for label in labels['labels']:
            if label['name'] == label_name:
                print(f'INFO: Label ID found for label {label_name}: {label["id"]}')
                return label['id']
        
        print(f'WARNING: No label ID found for label: {label_name}')
        return None
    
    except Exception as error:
        print(f'ERROR: Error while retrieving label ID for {label_name}: {error}')
        return None
    
    
def search_emails(query_string: str=None, label_ids: List[str]=None):
    try:
        if query_string:
            print(f'INFO: Searching for emails by query_string.')
            print(f'DEBUG: Query string: {query_string}')
        elif label_ids:
            print(f'INFO: Searching for emails within label(s).')
            print(f'DEBUG: Label IDs: {label_ids}')
        else:
            print(f'WARNING: Neither query string nor label IDs provided for emails search.')
            
        message_list_response = gmail_service.users().messages().list(
            userId='me',
            labelIds=label_ids,
            q=query_string
        ).execute()
        
        message_items = message_list_response.get('messages')
        next_page_token = message_list_response.get('nextPagetoken')
        
        while next_page_token:
            message_list_response = gmail_service.users().messages().list(
                userId='me',
                labelIds=label_ids,
                q=query_string,
                page=next_page_token
            ).execute()
            
            message_items.extend(message_list_response.get('messages'))
            next_page_token = message_list_response.get('nextPagetoken')
        
        print(f'INFO: Found {len(message_items)} email(s).')
        return message_items
        
    except Exception as error:
        print(f'ERROR: An error occured while searching for emails: {error}')
        return None
    
def delete_emails(email_results):
    print(f'INFO: Deleting emails.')
    deleted_emails = 0
    for email_result in email_results:
        try:
            gmail_service.users().messages().trash(
                userId='me',
                id=email_result['id']
            ).execute()
            deleted_emails += 1
            
        except Exception as error:
            print(f'ERROR: An error occured while deleting email_id: {email_result["id"]}. Error: {error}')
            
    if deleted_emails == len(email_results):
        print(f'INFO: {deleted_emails} emails deleted successfully.')
    else:
        print(f'WARNING: Not all emails deleted successfully. Total emails to delete: {len(email_results)}. Deleted emails: {deleted_emails}')