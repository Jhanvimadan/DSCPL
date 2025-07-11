# utils/calendar_utils.py

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle
import datetime

SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google_calendar():
    creds = None
    if os.path.exists('token.pkl'):
        with open('token.pkl', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pkl', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service

def create_event(service, summary, description, start_datetime, duration_minutes=30):
    end_datetime = start_datetime + datetime.timedelta(minutes=duration_minutes)

    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_datetime.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end_datetime.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
    }

    created_event = service.events().insert(calendarId='primary', body=event).execute()
    return created_event.get('htmlLink')
