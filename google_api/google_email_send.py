from google_api_utils import create_service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

CLIENT_SECRET_FILE = '../credentials/gg-gmail-automation.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

emailMessage = 'This email is sent using a Python program!'
mimeMessage = MIMEMultipart()
mimeMessage['to'] = 'galvangjx@gmail.com'
mimeMessage['subject'] = 'Delete this 2'
mimeMessage.attach(MIMEText(emailMessage, 'plain'))
raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
print(message)