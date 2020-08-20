import os
import subprocess
from datetime import datetime
from pathlib import Path
import redbot.core.utils.chat_formatting as chat_formatting
from jsonseq.decode import JSONSeqDecoder
from redbot.core import commands, checks

from .maintenance_helper import MaintenanceHelper


class Maintenance(commands.Cog):
    BASH_COMMAND_TO_MAKE_PERMISSION_CHANGES = "sed -r -i'' -e 's/@checks\.is_owner\(\)/@checks.admin_or_permissions()/g' /home/pi/.pyenv/versions/ACM_BOT/lib/python3.8/site-packages/redbot/core/core_commands.py"
    BASH_COMMAND_TO_RESTART_BOT = "sudo systemctl restart red@TheHatBot"
    RED_DISCORD_PIP_PACKAGE = "Red-DiscordBot"

    @checks.admin_or_permissions()
    @commands.command()
    async def updateRed(self, ctx: commands.Context):
        MaintenanceHelper.upgrade_package(self.RED_DISCORD_PIP_PACKAGE)
        os.system(self.BASH_COMMAND_TO_MAKE_PERMISSION_CHANGES)
        # sed -i '' -e 's/\.is_owner/.admin_or_permissions/g' s/regex/replacement/
        await ctx.send(
            "The redbot python package has been updated and the necessary changes to the packages has been made.")

    @checks.admin_or_permissions()
    @commands.command()
    async def reinstallRed(self, ctx: commands.Context):
        await ctx.send(
            "I have started to reinstall the Red-DiscordBot python package. I will restart when the changes have been made.")
        MaintenanceHelper.force_reinstall_package(self.RED_DISCORD_PIP_PACKAGE)
        os.system(self.BASH_COMMAND_TO_MAKE_PERMISSION_CHANGES)
        await ctx.send(
            "The redbot python package has been reinstalled and the necessary changes to the packages has been made. "
            "Restarting...")
        await self.restartBot(ctx)

    @checks.admin_or_permissions()
    @commands.command()
    async def restartBot(self, ctx: commands.Context):
        os.system(self.BASH_COMMAND_TO_RESTART_BOT)
        await ctx.send("I will be back.")

    @checks.admin_or_permissions()
    @commands.command()
    async def viewLogs(self, ctx: commands.Context, *args: str):
        if not args:
            return await ctx.send_help()

        kwargs = ["journalctl", *args, "-u", "red@TheHatBot", "-o", "json", "--no-pager"]

        json_file_path = Path(__file__).absolute().parent.parent.parent.parent.parent.joinpath("test.json").absolute()

        json_file = open(json_file_path, 'w')
        subprocess.call(kwargs, stdout=json_file)

        json_file.close()
        result_string = ''

        with open(json_file_path.absolute()) as f:
            # "MESSAGE" : "Started TheHatBot redbot.",
            # "__REALTIME_TIMESTAMP" : "1595382054920981",
            for obj in JSONSeqDecoder().decode(f):
                num = int(obj.get("__REALTIME_TIMESTAMP")) // 1000000
                time_stamp = datetime.fromtimestamp(num).strftime("%Y-%m-%d %I:%M:%S")
                result_string += f'{time_stamp} -- {obj.get("MESSAGE")}\n'
        if not result_string:
            result_string = "There was no logs for specified time"

        for partial_result in chat_formatting.pagify(result_string, shorten_by=20):
            await ctx.send(chat_formatting.box(partial_result, lang='python'))

    @checks.admin_or_permissions()
    @commands.command()
    async def pipInstallRequirements(self, ctx: commands.Context):
        MaintenanceHelper.install_requirements()
        await ctx.send("I have installed all the requirements in requirements.txt")

    @checks.admin_or_permissions()
    @commands.command()
    async def pipInstall(self, ctx: commands.Context, package: str):
        if not package:
            await ctx.send_help()
        MaintenanceHelper.install_package(package)
        await ctx.send(f"I have installed the package: {package}")
