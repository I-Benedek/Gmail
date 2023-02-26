from __future__ import print_function

import os.path
from pprint import pprint

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    return service

def get_messages(service):
    results = service.users().messages().list(userId='me').execute()
    '''first_message_id = results['messages'][0]['id']
    first_message = service.users().messages().get(userId='me', id=first_message_id, format='raw').execute()
    pprint(first_message)'''
    messages_ids = []
    for msg in results['messages']:
        messages_ids.append(msg['id'])
    for index in range(10):
        message = service.users().messages().get(userId='me', id=messages_ids[index], format='metadata' ).execute()
        headers = message['payload']['headers']
        for header in headers:
            if header['name'] == 'From':
                print(f'From: {header["value"]}')
            elif header['name'] == 'Subject':
                print(f'Subject: {header["value"]}')
            elif header['name'] == 'Date':
                print(f'\n  Date: {header["value"]}')

def main():
    service = get_service()
    get_messages(service)







main()
