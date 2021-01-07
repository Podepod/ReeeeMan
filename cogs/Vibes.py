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

        self.cofig = api.readConfig()

        self.configLoop.start()

    def cog_unload(self):
        self.configLoop.cancel()

    @bot.command(
        name="Vibe",
        aliases=["vibe", "VibeCheck", "Vibecheck", "vibecheck"],
        help=f"{self.config["basic"]["prefix"]}Vibe - sends a random vibe (aliases: vibe, VibeCheck, Vibecheck, vibecheck)",
        brief="sends the vibe",
    )
    async def Vibe(self, ctx):
        #vibe = api.getRandomVibe() 
        pass

    @bot.command(
        name="SuggestVibe",
        aliases=["suggestVibe", "suggestvibe", "suggest", "svibe", "vibesug"],
        help=f"{self.config["basic"]["prefix"]}SuggestVibe x - suggest a vibe to be added to the vibelist (aliases: suggestVibe, suggestvibe, suggest, svibe, vibesug)",
        brief="Suggest a new vibe",
    )
    async def SuggestVibe(self, ctx):
        # api.suggestVibe(text, author, guildname)
        # log ook in logkanaal dat er een nieuwe sugestion is
        pass

    @tasks.loop(seconds=5.0)
    async def configLoop(self):
        self.cofig = api.readConfig()

    @configLoop.before_loop
    async def beforeConfigLoop(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(COGNAME(bot))