from redbot.core import commands
from redbot.core import Config
import os


class AcmApi(commands.Cog):
    @commands.command()
    async def msg(self, ctx, msg):
        await ctx.send(msg)
