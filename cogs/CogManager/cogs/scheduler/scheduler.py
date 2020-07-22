from redbot.core import commands, checks
from redbot.core import Config


class Maintenance(commands.Cog):

    @checks.admin_or_permissions()
    @commands.command()
    async def testMessage(self, ctx: commands.Context, *args: str):
        if not args:
            return await ctx.send_help()
        return await ctx.send(args)
