import os

from redbot.core import checks
from redbot.core.commands import commands, Context
from .github_helper import GitHubHelper


class GitHub(commands.Cog):

    @checks.admin_or_permissions()
    @commands.command()
    async def gitPull(self, ctx: Context):
        os.system('cd ~/TheHatBot/ && git pull')
        await ctx.send("I pulled the code!")

    @checks.admin_or_permissions()
    @commands.command()
    async def gitReset(self, ctx: Context):
        os.system('cd ~/TheHatBot/ && git reset HEAD --hard')
        await ctx.send("I reset to the latest local git hash.")

    @commands.command()
    async def addToGitHubOrganization(self, ctx: Context, github_username):
        if not github_username:
            await ctx.send_help()
        driver = GitHubHelper.make_driver()
        admin_username = 'some username'  # TODO get admin username
        admin_password = 'some password'  # TODO get admin password
        GitHubHelper.login_to_github(driver=driver, username=admin_username, password=admin_password)
        try:
            GitHubHelper.add_user_to_organization(driver=driver, organization_name="ACN-CBU",
                                                  user_to_add=github_username)
            await ctx.send(f'Check your email associated with the github account: {github_username}')
        except AssertionError:
            await ctx.send(f'Could not find the github account with the username of: {github_username}')
