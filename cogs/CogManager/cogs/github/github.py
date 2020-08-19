import os
import requests
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
        try:
            GitHubHelper.is_valid_github_user(driver=driver, user=github_username)
            requests.post(url='http://10.147.19.43:41434/api/v1/github_invite', data={"username": github_username})
            await ctx.send(f'Check your email associated with the github account: {github_username}')
        except AssertionError:
            await ctx.send(f'Could not find the github account with the username of: {github_username}')
