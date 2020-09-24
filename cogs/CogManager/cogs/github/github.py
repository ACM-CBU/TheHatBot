from pathlib import Path

import requests
from git import Repo
from redbot.core import checks
from redbot.core.commands import commands, Context

from .github_helper import GitHubHelper


class GitHub(commands.Cog):
    USER = 'bot'
    REPO_NAME = 'TestBot1'
    REPO_PATH = Path(f'/home/{USER}/.local/share/Red-DiscordBot/data/{REPO_NAME}/')
    TEST_REPO_DIR = REPO_PATH.joinpath('Test_Cogs')
    PARENT_REPO = Repo(str(REPO_PATH))

    @checks.admin_or_permissions()
    @commands.command()
    async def gitPull(self, ctx: Context):
        await ctx.send(self.PARENT_REPO.git.pull())

    @checks.admin_or_permissions()
    @commands.command()
    async def gitReset(self, ctx: Context):
        await ctx.send(self.PARENT_REPO.git.reset('HEAD', '--hard'))

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

    @checks.admin_or_permissions()
    @commands.command()
    async def cloneTestRepo(self, ctx: Context, github_repo_url: str):
        if not github_repo_url:
            await ctx.send_help()
        if 'github.com/ACM-CBU/' in github_repo_url and len(github_repo_url.split('/')) > 4:
            sub_name = github_repo_url.split('/')[-1]
            new_sub = self.PARENT_REPO.create_submodule(name=sub_name, path=str(self.TEST_REPO_DIR),
                                                        url=github_repo_url)
            new_sub.set_parent_commit(None)
            self.PARENT_REPO.git.commit(message=f"Added new Submodule: {sub_name}")
            self.PARENT_REPO.git.push()
        else:
            await ctx.send("The repository must be within the ACM GitHub Organization")
