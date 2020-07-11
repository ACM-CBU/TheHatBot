from redbot.core import commands
from redbot.core import Config
import os


class Mycog(commands.Cog):
    """My custom cog"""
    '''def __init__(self):
        self.config = Config.get_conf(self, identifier=1234567890)
        default_global = {
            "name": "Unknown"
        }
        self.config.register_global(**default_global)
    '''

    @commands.command()
    async def mycom(self, ctx):
        """This does stuff!"""
        # Your code will go here
        await ctx.send("I can do stuff!")

    @commands.command()
    async def gitpull(self, ctx):
        os.system('git pull')
        await ctx.send("I pulled the code! :smirk: test")

    @commands.command()
    async def sayhi(self, ctx):
        await ctx.send("Hello There")
