import base64
from typing import List
import time
import os
from google_api_utils import create_service

class GmailException(Exception):
    """gmail exception base class"""
    
class NoEmailFound(GmailException):
    """no email found exception error"""
    
def search_emails(query_string: str, label_ids: List=None):
    try:
        message_list_response = service.users().messages().list(
            userId='me',
            labelIds=label_ids,
            q=query_string
        ).execute()
        
        message_items = message_list_response.get('messages')
        next_page_token = message_list_response.get('nextPagetoken')
        
        while next_page_token:
            message_list_response = service.users().messages().list(
                userId='me',
                labelIds=label_ids,
                q=query_string,
                page=next_page_token
            ).execute()
            
            message_items.extend(message_list_response.get('messages'))
            next_page_token = message_list_response.get('nextPagetoken')
            
        return message_items
        
    except Exception as error:
        return None
    
def get_file_data(message_id, attachment_id, file_name, save_location):
    response = service.users().messages().attachments().get(
        userId='me',
        messageId=message_id,
        id=attachment_id
    ).execute()
    
    file_data = base64.urlsafe_b64decode(response.get('data').encode('Utf-8'))

    return file_data

def get_message_detail(message_id, message_format='metadata', metadata_header: List=None):
    message_detail = service.users().messages().get(
        userId='me',
        id=message_id,
        format=message_format,
        metadataHeaders=metadata_header
    ).execute()

    return message_detail
    
if __name__ == '__main__':
    CLIENT_FILE = '../credentials/gg-gmail-automation.json'
    API_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']
    
    service = create_service(CLIENT_FILE, API_NAME, API_VERSION, SCOPES)

    query_string = 'has:attachment Subject: You got files'
    
    save_location = '../attachments/local'
    email_messages = search_emails(query_string)
    
    for email_message in email_messages:
        messageDetail = get_message_detail(email_message['id'], message_format='full', metadata_header=['parts'])
        messageDetailPayload = messageDetail.get('payload')
        if 'parts' in messageDetailPayload:
            for message_payload in messageDetailPayload['parts']:
                file_name = message_payload['filename']
                body = message_payload['body']
                if 'attachmentId' in body:
                    attachment_id = body['attachmentId']
                    attachment_content = get_file_data(email_message['id'], attachment_id=attachment_id, file_name=file_name, save_location=save_location)
                    
                    with open(os.path.join(save_location, file_name), 'wb') as _f:
                        _f.write(attachment_content)
                        print(f'File {file_name} is saved at {save_location}')
        time.sleep(0.5)