from __future__ import print_function

import datetime
from datetime import timedelta

import discord
from discord.ext import commands
from googleapiclient.discovery import build
from httplib2 import Http
import oauth2client

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'


client = discord.Client()

class Scheduler(commands.Cog):

    @checks.admin_or_permissions()
    @commands.command()
    async def events(self, ctx: commands.Context, *args: str):
        print("Upcoming")
        now = datetime.datetime.now()
        run_at = now + timedelta(hours=3)
        delay = (run_at - now).total_seconds()
        #Begin Google Calander API
        store = oauth2client.file.Storage('cogs/CogManager/cogs/scheduler/creds.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = oauth2client.client.flow_from_clientsecrets('credentials.json', SCOPES)
            creds = oauth2client.tools.run_flow(flow, store)
        service = build('calendar', 'v3', http=creds.authorize(Http()))
        now = datetime.datetime.utcnow().isoformat() + 'Z'
            #Retrieve all Events
        events_result = service.events().list(calendarId='CENSORED', timeMin=now,maxResults=250, singleEvents=True,orderBy='startTime').execute()
        events = events_result.get('items', [])

            #Currentmode stores if searching for tommorow, the week, or other (1,2,3)
        Currentmode = 0
        UMode=1
        none = True
            #Gets end of week
        dt = datetime.datetime.now()
        startweek = dt - timedelta(days=dt.weekday())
        endweek = startweek + timedelta(days=6)
        dtstring = str(dt.date())
        TheMessages = "**" + dtstring + " Report**"
        ctx.channel.send(TheMessages)
        if not events:
            ctx.channel.send('No upcoming events')
        for event in events:

            if Currentmode == 0:
                ctx.channel.send('Tommorow')
                Currentmode = 1

            thestr = event['start'].get('dateTime')

            count = 0
            count2 = 0
            for x in thestr:
                count += 1
                if x == "-":
                    count2 +=1
                    if count2 == 3:
                        break
            count = count - 1
            thestr = thestr[0:count]


            start = datetime.datetime.strptime(thestr, "%Y-%m-%dT%H:%M:%S")

            if (start - dt).days <= 7 and Currentmode == 1:
                if UMode == 1:
                    ctx.channel.send('None')
                    ctx.channel.send('in the next 7 days')
                UMode = 2
                Currentmode = 2
            elif (start - dt).days >= 7 and (Currentmode == 1 or Currentmode == 2):
                if UMode == 1:
                    ctx.channel.send('None')
                    ctx.channel.send('in the next 7 days')
                    ctx.channel.send('None')
                ctx.channel.send('Longterm')
                Currentmode = 3
                UMode = 3
            FirstMessage = str(start.date())
            SecondMessage = event['summary']
            ThirdMessage= FirstMessage + " " + SecondMessage
            ctx.channel.send(ThirdMessage)