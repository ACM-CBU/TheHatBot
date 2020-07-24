from redbot.core import commands
from redbot.core import config
import os


class Discipleship(commands.Cog):
	
	@commands.command()
    async def mycom(self, ctx):
        """This does stuff!"""
        # Your code will go here
        await ctx.send("I can do stuff!")


    @commands.command()
    async def sayhi(self, ctx):
        await ctx.send("Hello There")