from redbot.core import commands
from redbot.core import Config
import os


class Maintenance(commands.Cog):

    @commands.command()
    async def gitpull(self, ctx):
        os.system('cd ~/TheHatBot/ && git pull')
        await ctx.send("I pulled the code!")

    @commands.command()
    async def gitreset(self, ctx):
        os.system('git rev-parse HEAD | git reset --hard')
        await ctx.send("I reset to the latest local git hash.")

    @commands.command()
    async def updateRed(self, ctx):
        os.system('pyenv shell ACM_BOT && python -m pip install --upgrade Red-DiscordBot')
        os.system("find /home/pi/.pyenv/versions/ACM_BOT/lib/python3.8/site-packages/redbot/ -type f -name \"*.py\" -print0 | xargs -0 sed -i '' -e 's/.is_owner/.admin_or_permissions/g'")
        await ctx.send("The redbot python package has been updated and the necessary changes to the packages has been made.")
