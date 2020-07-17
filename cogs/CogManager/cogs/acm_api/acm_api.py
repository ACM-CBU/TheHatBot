from redbot.core import commands
from redbot.core import Config
import os
import requests


class AcmApi(commands.Cog):
    @commands.command()
    async def msg(self, ctx, map):
        await ctx.send(map)

    @commands.command()
    async def post(self, ctx, msg):
        url = '10.147.19.177'
        myobj = {"Discord": msg}
        headers = {'Content-type': 'application/json'}
        x = requests.post(url, data = myobj, headers=headers)
        await ctx.send("Message posted")