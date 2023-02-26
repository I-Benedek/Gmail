from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


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


def get_messages(service, db, gmail_from, gmail_date, gmail_subject):
    results = service.users().messages().list(userId='me').execute()
    messages_ids = []
    for msg in results['messages']:
        messages_ids.append(msg['id'])
    for index in range(db):
        message = service.users().messages().get(userId='me', id=messages_ids[index], format='metadata').execute()
        headers = message['payload']['headers']
        for header in headers:
            if gmail_from == 'igen' or gmail_from == 'Igen':
                if header['name'] == 'From':
                    print(f'From: {header["value"]}')
            if gmail_subject == 'igen' or gmail_subject == 'Igen':
                if header['name'] == 'Subject':
                    print(f'Subject: {header["value"]}')
            if gmail_date == 'igen' or gmail_date == 'Igen':
                if header['name'] == 'Date':
                    print(f'Date: {header["value"]}')
        print('----------------------------------------------------------')


def main():
    db = int(input('Add meg, hogy hány db levélről szertnél információt kapni! '))
    print('--------------------------------------------------------------------------')
    gmail_from = input('Add meg hogy meg szeretnéd e kapni a levelek feladóinak címét! Igen vagy nem? ')
    gmail_date = input('Add meg hogy meg szeretnéd e kapni a levelek dátumát! Igen vagy nem? ')
    gmail_subject = input('Add meg hogy meg szeretnéd e kapni a levelek tárgyát! Igen vagy nem? ')
    print('--------------------------------------------------------------------------')
    service = get_service()
    get_messages(service, db, gmail_from, gmail_date, gmail_subject)


main()
