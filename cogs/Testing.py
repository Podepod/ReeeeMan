import discord
from discord.ext import tasks, commands
import datetime
import asyncio
import re
import random
import apiRequests as api
import emojiList as em

config = api.readConfig()

bot = commands.Bot(command_prefix=config["basic"]["prefix"], description=config["basic"]["description"])

# TESTING COG
class Testing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #self.testLoop.start()

    def cog_unload(self):
        self.testLoop.cancel()

    @bot.command(hidden = True)
    @commands.is_owner()
    async def emoji(self, ctx):
        for emojinaam in em.emojiList:
            reaction = em.emojiList[emojinaam]
            await ctx.message.add_reaction(reaction)

    @bot.command(hidden = True)
    @commands.is_owner()
    async def checkLoop(self, ctx):
        await ctx.send(f"Failed? {testLoop.failed()}")

    # file settings file command check
    @tasks.loop(seconds=5.0)
    async def testLoop(self):
        print("TEST LOOP")

    @testLoop.before_loop
    async def beforeTestLoop(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(Testing(bot))