import os.path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from parser import create_json, Event

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

# event = {
#   'summary': 'Google I/O 2015',
#   'location': '800 Howard St., San Francisco, CA 94103',
#   'description': 'A chance to hear more about Google\'s developer products.',
#   'start': {
#     'dateTime': '2015-05-28T09:00:00-07:00',
#     'timeZone': 'America/Los_Angeles',
#   },
#   'end': {
#     'dateTime': '2015-05-28T17:00:00-07:00',
#     'timeZone': 'America/Los_Angeles',
#   },
#   'recurrence': [
#     'RRULE:FREQ=DAILY;COUNT=2'
#   ],
#   'attendees': [
#     {'email': 'lpage@example.com'},
#     {'email': 'sbrin@example.com'},
#   ],
#   'reminders': {
#     'useDefault': False,
#     'overrides': [
#       {'method': 'email', 'minutes': 24 * 60},
#       {'method': 'popup', 'minutes': 10},
#     ],
#   },
# }

event = {
  "summary": "Calendar event for tomorrow",
  "location": "",
  "description": "",
  "start": {
    "dateTime": "2021-10-11T15:00:00-07:00",
    "timeZone": "America/Los_Angeles"
  },
  "end": {
    "dateTime": "2021-10-11T16:00:00-07:00",
    "timeZone": "America/Los_Angeles"
  },
  "recurrence": [],
  "attendees": [],
  "reminders": {
    "useDefault": True,
    "overrides": []
  }
}

def input_json():
    with open('parse.json', 'r') as openfile:
 
    # Reading from json file
        json_object = json.load(openfile)
        return json_object

def create_event(event_json):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
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

    try:
        service = build('calendar', 'v3', credentials=creds)
        event = service.events().insert(calendarId='primary', body=event_json).execute()
        print('Event created: %s' % (event.get('htmlLink')))
        return 1

    except HttpError as error:
        print('An error occurred: %s' % error)
        return 0 
item_json = input_json()
create_event(event)

# event_json = create_json("Create a calendar event for tomorrow at 3pm", Event)
# print(event_json)
    # create_event(event_json)