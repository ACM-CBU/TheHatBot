from datetime import datetime
from pathlib import Path

from jsonseq.decode import JSONSeqDecoder
from redbot.core import commands, checks
from redbot.core import Config
import os
import jsonseq



class Maintenance(commands.Cog):
    BASH_COMMAND_TO_MAKE_PERMISSION_CHANGES = "sed -r -i'' -e 's/@checks\.is_owner\(\)/@checks.admin_or_permissions()/g' /home/pi/.pyenv/versions/ACM_BOT/lib/python3.8/site-packages/redbot/core/core_commands.py"
    BASH_COMMAND_TO_RESTART_BOT = "sudo systemctl restart red@TheHatBot"
    BASH_COMMAND_TO_CD_TO_BOT_DIR = "cd ~/TheHatBot/"
    BASH_COMMAND_TO_PULL_FROM_GIT = "git pull"
    BASH_COMMAND_TO_RESET_LOCAL_REPO = "git reset HEAD --hard"
    BASH_COMMAND_TO_USE_PYENV_SHELL = "pyenv shell ACM_BOT"
    PIP_FLAG_TO_REINSTALL = "--force-reinstall"
    PIP_FLAG_TO_UPGRADE = "--upgrade"
    BASH_COMMAND_TO_PIP_INSTALL = "pip install"
    RED_DISCORD_PIP_PACKAGE = "Red-DiscordBot"

    @checks.admin_or_permissions()
    @commands.command()
    async def gitPull(self, ctx: commands.Context):
        os.system('cd ~/TheHatBot/ && git pull')
        await ctx.send("I pulled the code!")

    @checks.admin_or_permissions()
    @commands.command()
    async def gitReset(self, ctx: commands.Context):
        os.system('cd ~/TheHatBot/ && git reset HEAD --hard')
        await ctx.send("I reset to the latest local git hash.")

    @checks.admin_or_permissions()
    @commands.command()
    async def updateRed(self, ctx: commands.Context):
        os.system(
            f'{self.BASH_COMMAND_TO_USE_PYENV_SHELL} -m {self.BASH_COMMAND_TO_PIP_INSTALL} {self.PIP_FLAG_TO_UPGRADE} {self.RED_DISCORD_PIP_PACKAGE} && {self.BASH_COMMAND_TO_MAKE_PERMISSION_CHANGES}')
        # sed -i '' -e 's/\.is_owner/.admin_or_permissions/g' s/regex/replacement/
        await ctx.send(
            "The redbot python package has been updated and the necessary changes to the packages has been made.")

    @checks.admin_or_permissions()
    @commands.command()
    async def reinstallRed(self, ctx: commands.Context):
        await ctx.send(
            "I have started to reinstall the Red-DiscordBot python package. I will restart when the changes have been made.")
        os.system(
            f"{self.BASH_COMMAND_TO_USE_PYENV_SHELL} && {self.BASH_COMMAND_TO_PIP_INSTALL} {self.PIP_FLAG_TO_REINSTALL} {self.RED_DISCORD_PIP_PACKAGE} && {self.BASH_COMMAND_TO_MAKE_PERMISSION_CHANGES} && {self.BASH_COMMAND_TO_RESTART_BOT}")
        await ctx.send(
            "The redbot python package has been reinstalled and the necessary changes to the packages has been made.")

    @checks.admin_or_permissions()
    @commands.command()
    async def restartBot(self, ctx: commands.Context):
        os.system(f'{self.BASH_COMMAND_TO_RESTART_BOT}')
        await ctx.send("I will be back.")

    @checks.admin_or_permissions()
    @commands.command()
    async def viewLogs(self, ctx: commands.Context, *args: str):
        global BASH_COMMAND_TO_CD_TO_BOT_DIR
        if not args:
            return await ctx.send_help()
        arguments = ''
        for arg in args:
            arguments += arg + ' '
        print(arguments)
        os.system(f'{BASH_COMMAND_TO_CD_TO_BOT_DIR} && journalctl {arguments} -u red@TheHatBot -o --no-pager > test.json')
        # "MESSAGE" : "Started TheHatBot redbot.",
        # "__REALTIME_TIMESTAMP" : "1595382054920981",
        result_string = ''
        json_file_path = Path(__file__).parent.parent.parent.parent.parent.joinpath("test.json")

        with open(json_file_path) as f:
            for obj in JSONSeqDecoder().decode(f):
                num = int(obj.get("__REALTIME_TIMESTAMP")) // 1000000
                time_stamp = datetime.fromtimestamp(num).strftime("%Y-%m-%d %I:%M:%S")
                result_string += f'{time_stamp} -- {obj.get("MESSAGE")}\n'
        await ctx.send(result_string)

    @checks.admin_or_permissions()
    @commands.command()
    async def pipInstallRequirements(self, ctx: commands.Context, *args: str):
        if not args:
            return await ctx.send_help()
        os.system(
            f'{self.BASH_COMMAND_TO_CD_TO_BOT_DIR} && {self.BASH_COMMAND_TO_USE_PYENV_SHELL} && {self.BASH_COMMAND_TO_PIP_INSTALL} -r requirements.txt')
        await ctx.send("I have installed the python dependencies in requirements.txt")

    @checks.admin_or_permissions()
    @commands.command
    async def testMessage(self, ctx: commands.Context, *args: str):
        if not args:
            return await ctx.send_help()
        return await ctx.send(args)
