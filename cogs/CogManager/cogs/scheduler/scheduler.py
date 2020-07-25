from redbot.core import commands, checks
import schedule
import time
from redbot.core import Config


class Scheduler(commands.Cog):

    @checks.admin_or_permissions()
    @commands.command()
    async def exampleCommand(self, ctx: commands.Context, *args: str):
        if not args:
            return await ctx.send_help()
        return await ctx.send(args)

    @checks.admin_or_permissions()
    @commands.command()
    async def addEvent(self, ctx: commands.Context, *args: str):
        def job():
            print("Are you bored yet")

        schedule.every().friday.at("22:34").do(job)

        while True:
            schedule.run_pending()
            time.sleep(1)
