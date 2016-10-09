# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------------
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
# -----------------------------------------------------------------------------------
import os

import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client.file import Storage


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'
MAKE_CALENDAR = '8csvojcqhf1ve1kvf3bcq5jupk@group.calendar.google.com'


class google():
    def _get_credentials(self):
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
        credential_path = os.path.join(credential_dir, 'calendar-python-quickstart.json')
        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            print('Storing credentials to ' + credential_path)
        return credentials

    def connect(self):
        # Creates a Google Calendar API service object
        credentials = self._get_credentials()
        http = credentials.authorize(httplib2.Http())
        self._service = discovery.build('calendar', 'v3', http=http)
        print 'connectado a google'
        return self

    def clear(self):
        # Traer los eventos del calendario make
        list = self._service.events().list(
            calendarId=MAKE_CALENDAR,
            maxResults=2000).execute()
        events = list.get('items')
        for event in events:
            print 'eliminando', event['summary']
            self._service.events().delete(
                calendarId=MAKE_CALENDAR, eventId=event['id']).execute()

    def _make_event(self, start, end, summary):
        event = {
            'summary': summary,
            'description': 'una clase de makeover.',
            'start': {
                'dateTime': start.isoformat() + 'Z',  # 'Z' indicates UTC time,
                'timeZone': 'America/Argentina/Buenos_Aires',
            },
            'end': {
                'dateTime': end.isoformat() + 'Z',  # 'Z' indicates UTC time,
                'timeZone': 'America/Argentina/Buenos_Aires',
            },
        }
        return event

    def insert(self, ge):
        print 'inserting event', ge.date_start(), ge.summary()
        event = self._make_event(ge.date_start(), ge.date_end(), ge.summary())
        event = self._service.events().insert(calendarId=MAKE_CALENDAR,
                                              body=event).execute()


class google_event():
    def __init__(self, lecture):
        self._lecture = lecture

    def date_start(self):
        return self._lecture.date_start

    def date_end(self):
        return self._lecture.date_stop

    def summary(self):
        return u'[{}] {}-{}'.format(
            self._lecture.curso_id.product.default_code,
            self._lecture.seq,
            self._lecture.name)
