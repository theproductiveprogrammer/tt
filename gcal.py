import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def toEvent(tm):
    return {
        'summary': tm.txt,
        'start': {
            'dateTime': tm.toISOstart(),
            'timeZone': 'Australia/Melbourne',
        },
        'end': {
            'dateTime': tm.toISOend(),
            'timeZone': 'Australia/Melbourne',
        },
    }

def addToGoogleCalendar(tm):
    creds = authorize()
    service = build("calendar", "v3", credentials=creds)
    event = toEvent(tm)
    event_res = service.events().insert(calendarId='primary', body=event).execute()
    print(f"Event created: {event_res.get('htmlLink')}")

def authorize():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds
