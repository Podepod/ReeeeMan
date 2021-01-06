import discord
from discord.ext import tasks, commands
import datetime
import asyncio
import re
import random
import apiRequests as api

config = api.readConfig()

bot = commands.Bot(command_prefix=config["basic"]["prefix"], description=config["basic"]["description"])

# COGNAME COG
class COGNAME(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.configLoop.start()

    def cog_unload(self):
        self.configLoop.cancel()

    @tasks.loop(seconds=5.0)
    async def configLoop(self):
        pass

    @configLoop.before_loop
    async def beforeConfigLoop(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(COGNAME(bot))