import io
import base64
from google_api_utils import create_service
from googleapiclient.http import MediaIoBaseUpload

def construct_service(api_service):
    CLIENT_SERVICE_FILE = '../credentials/gg-gmail-automation.json'
    
    try:
        if api_service == 'drive':
            API_NAME = 'drive'
            API_VERSION = 'v3'
            SCOPES = ['https://www.googleapis.com/auth/drive']
            return create_service(CLIENT_SERVICE_FILE, API_NAME, API_VERSION, SCOPES)
        
        elif api_service == 'gmail':
            API_NAME = 'gmail'
            API_VERSION = 'v1'
            SCOPES = ['https://mail.google.com/']
            return create_service(CLIENT_SERVICE_FILE, API_NAME, API_VERSION, SCOPES)
            
    except Exception as error:
        print(error)
        return None
    
def search_email(service, query_string, label_ids=[]):
    try:
        message_list_response = service.users().messages().list(
            userId='me',
            labelIds=label_ids,
            q=query_string
        ).execute()
        
        message_items = message_list_response.get('messages')
        nextPagetoken = message_list_response.get('nextPagetoken')
        
        while nextPagetoken:
            message_list_response = service.users().messages().list(
                userId='me',
                labelIds=label_ids,
                q=query_string,
                pageToken=nextPagetoken
            ).execute()
            
            message_items.extend(message_list_response.response.get('messages'))
            nextPagetoken = message_items.get('nextPagetoken')
        
        return message_items
            
    except Exception as error:
        return None
    
def get_message_detail(service, message_id, format='metadata', metadata_headers=[]):
    try:
        message_detail = service.users().messages().get(
            userId='me',
            id=message_id,
            format=format,
            metadataHeaders=metadata_headers
        ).execute()
        
        return message_detail
    
    except Exception as error:
        return None
    
def create_foler_in_drive(service, folder_name, parent_folder=[]):
    file_metadata = {
        'name': folder_name,
        'parents': parent_folder,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    
    file = service.files().create(body=file_metadata, fields='id').execute()
    
    return file

"""
Step 1: Create Google Service Instance
"""
gmail_service = construct_service('gmail')
drive_service = construct_service('drive')

"""
Step 2: Search email with attachments
"""
# query_string = 'has:attachment'
# query_string = 'has:attachment From:'       # if you want to search email with attachments from specific people
query_string = 'has:attachment Subject: You got files'    # if you want to search email with attachments from specific email subjects

email_messages = search_email(gmail_service, query_string=query_string, label_ids=['INBOX'])

"""
Step 3: Download emails and create drive folder
"""
for email_message in email_messages:
    messageId = email_message['threadId']
    messageSubject = '(No subject) ({0})'.format(messageId)
    messageDetails = get_message_detail(
        service=gmail_service,
        message_id=email_message['id'],
        format='full',
        metadata_headers=['parts']
    )
    messageDetailPayload = messageDetails.get('payload')

    for item in messageDetailPayload['headers']:
        if item['name'] == 'Subjec: ':
            if item['value']:
                messageSubject = '{0} ({1})'.format(item['value'], messageId)
            else:
                messageSubject = '(No subject) ({0})'.format(messageId)
                
    # create drive folder
    folder_id = create_foler_in_drive(service=drive_service, folder_name=messageSubject)['id']
    
    if 'parts' in messageDetailPayload:
        for msgPayload in messageDetailPayload['parts']:
            mime_type = msgPayload['mimeType']
            file_name = msgPayload['filename']
            body = msgPayload['body']
            
            if 'attachmentId' in body:
                attachment_id = body['attachmentId']
                
                response = gmail_service.users().messages().attachments().get(
                    userId='me',
                    messageId=email_message['id'],
                    id=attachment_id
                ).execute()
                
                file_data = base64.urlsafe_b64decode(response.get('data').encode('UTF-8'))
                                
                fh = io.BytesIO(file_data)
                
                file_metadata = {
                    'name': file_name,
                    'parents': [folder_id]
                }
                
                media_body = MediaIoBaseUpload(fh, mimetype=mime_type, chunksize=1024 * 1024, resumable=True)
                
                file = drive_service.files().create(
                    body=file_metadata,
                    media_body=media_body,
                    fields='id'
                ).execute()