from redbot.core import commands
from redbot.core import config
import os


class Discipleship(commands.Cog):
    @commands.command()
    async def myDevo(self, ctx):
        """This does stuff!"""
        # Your code will go here
        await ctx.send("I can do stuff!")


    @commands.command()
    async def welcome(self, ctx):
        await ctx.send("Hello There")
