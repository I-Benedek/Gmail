from __future__ import print_function
import os.path
from pprint import pprint
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64
from email.message import EmailMessage
import google.auth
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']


def get_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    return service


def informations():
    fro = 'f', ''''input('Add meg a feladó email címét! ')'''
    to = input('Add meg az email címét, akinek szeretnéd küldeni ezt az emailt! ')
    subject = input('Add meg az email tárgyát! ')
    message = input('Add meg az üzenet szövegét! ')
    return fro, to, subject, message


def send_message(service, fro, to, subject, message_):
    message = EmailMessage()

    message.set_content(message_)

    message['To'] = to
    message['From'] = fro
    message['Subject'] = subject

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {
        'raw': encoded_message
    }

    send_message = (service.users().messages().send
                    (userId="me", body=create_message).execute())
    print(F'Message Id: {send_message["id"]}')


def main():
    inform = informations()
    fro = inform[0]
    to = inform[1]
    subject = inform[2]
    message = inform[3]
    service = get_service()
    send_message(service, fro, to, subject, message)


main()
