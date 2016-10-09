# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------------
#
#    Copyright (C) 2016  jeo Software  (http://www.jeo-soft.com.ar)
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#-----------------------------------------------------------------------------------
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'
MAKE_CALENDAR = '8csvojcqhf1ve1kvf3bcq5jupk@group.calendar.google.com'

def make_event(start_time,end_time,class_content):
    event = {
      'summary': class_content,
#      'location': 'Makeover Lab - Escuela de maquillaje, Avenida Rivadavia, Buenos Aires, Argentina',
      'description': 'A chance to hear more about Google\'s developer products.',
      'start': {
        'dateTime': start_time.isoformat(),
        'timeZone': 'America/Argentina/Buenos_Aires',
      },
      'end': {
        'dateTime': end_time.isoformat(),
        'timeZone': 'America/Argentina/Buenos_Aires',
      },
#      'recurrence': [
#        'RRULE:FREQ=DAILY;COUNT=2'
#      ],
#      'attendees': [
#        {'email': 'lpage@example.com'},
#        {'email': 'sbrin@example.com'},
#      ],
#      'reminders': {
#        'useDefault': False,
#        'overrides': [
#          {'method': 'email', 'minutes': 24 * 60},
#          {'method': 'popup', 'minutes': 10},
#        ],
#      },
    }
    return event

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    # crea un evento en el calendario
    ######################################################################################
    start_time = datetime.datetime.strptime('2016-10-09 17:00', '%Y-%m-%d %H:%M')
    end_time = datetime.datetime.strptime('2016-10-09 18:00', '%Y-%m-%d %H:%M')
    class_content = 'clase de maquillaje'
    event = make_event(start_time,end_time,class_content)
    event = service.events().insert(calendarId=MAKE_CALENDAR, body=event).execute()

    # lista los eventos del calendario
    now = datetime.datetime.now().isoformat() + 'Z' # 'Z' indicates UTC time
    list = service.events().list(calendarId=MAKE_CALENDAR).execute()
    events = list.get('items')
    for event in events:
        print (event['summary'])

    # elimina todos los eventos del calendario
    service.calendars().clear('MAKE_CALENDAR').execute();

    exit()


    # lista los calendarios que tengo
    page_token = None
    while True:
      calendar_list = service.calendarList().list(pageToken=page_token).execute()
      for calendar_list_entry in calendar_list['items']:
        print (calendar_list_entry['summary'])
      page_token = calendar_list.get('nextPageToken')
      if not page_token:
        break
    exit()


    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


if __name__ == '__main__':
    main()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
