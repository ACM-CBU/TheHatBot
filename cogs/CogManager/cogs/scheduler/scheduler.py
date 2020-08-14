from __future__ import print_function

import os
import pickle
import datetime
from pathlib import Path

import discord
from google_auth_httplib2 import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from redbot.core import commands

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'

client = discord.Client()


class Scheduler(commands.Cog):

    @staticmethod
    def build_google_calendar_service():
        SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    Path(__file__).absolute().parent.joinpath("credentials.json").absolute(), SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        return build('calendar', 'v3', credentials=creds)

    @commands.command()
    async def getEvents(self, ctx: commands.Context):
        # Call the Calendar API
        service = self.build_google_calendar_service()
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        await ctx.send('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            await ctx.send('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            await ctx.send(str((start, event['summary'])))