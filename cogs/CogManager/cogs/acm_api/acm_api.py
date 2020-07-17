from redbot.core import commands
from redbot.core import Config
import os
import requests
import json


class AcmApi(commands.Cog):
    @commands.command()
    async def msg(self, ctx, map):
        await ctx.send(map)

    @commands.command()
    async def post(self, ctx, msg):
        url = 'http://10.147.19.177/posts'
        myobj = {"Discord": msg}
        headers = {'Content-type': 'application/json'}
        x = requests.post(url, data = json.dumps(myobj), headers=headers)
        await ctx.send("Message posted")