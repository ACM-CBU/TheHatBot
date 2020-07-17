from redbot.core import commands
from redbot.core import Config
import os
import requests


class AcmApi(commands.Cog):
    @commands.command()
    async def msg(self, ctx, msg1, msg2):
        await ctx.send(msg1)
        await ctx.send(msg2)

    async def post(self, ctx, username, msg):
    	await ctx.send("Message posted successfully!")
