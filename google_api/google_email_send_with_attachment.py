from google_api_utils import create_service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import mimetypes
import os

CLIENT_SECRET_FILE = '../credentials/gg-gmail-automation.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

file_attachments = [
    '../attachments/airtravel.csv',
    '../attachments/dummy.pdf',
    '../attachments/foobar.docx',
    '../attachments/heritage_tembusu.jpeg'
]

emailMsg = '4 files attached'

# create email message
mimeMessage = MIMEMultipart()
mimeMessage['to'] = 'galvangjx@gmail.com'
mimeMessage['subject'] = 'You got files'
mimeMessage.attach(MIMEText(emailMsg, 'plain'))

# attach files
for attachment in file_attachments:
    content_type, encoding = mimetypes.guess_type(attachment)
    main_type, sub_type = content_type.split('/', 1)
    file_name = os.path.basename(attachment)
    
    with open(attachment, 'rb') as f:        
        myFile = MIMEBase(main_type, sub_type)
        myFile.set_payload(f.read())
    
    myFile.add_header('Content-Disposition', 'attachment', filename=file_name)
    
    encoders.encode_base64(myFile)
    
    mimeMessage.attach(myFile)
    
raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

message = service.users().messages().send(userId='me', body={'raw':raw_string}).execute()
print(message)

