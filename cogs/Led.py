import discord
from discord.ext import tasks, commands
import datetime
import asyncio
import re
import random
import apiRequests as api
import LEDverlichting as LEDs

config = api.readConfig()

bot = commands.Bot(command_prefix=config["basic"]["prefix"], description=config["basic"]["description"])

# COGNAME COG
class Led(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.config = api.readConfig()
        self.room = LEDs.LEDverlichting()

        self.configLoop.start()

    def cog_unload(self):
        self.configLoop.cancel()

    @bot.command(
        name="Led",
        aliases=["led"],
        help="Send commands to Podepod's LEDs",
        brief="Send commands to Podepod's LEDs",
    )
    @commands.is_owner()
    async def Led(self, ctx, *, text):
        output = self.room.commandScene(text)

        await ctx.send(output)

    @tasks.loop(seconds=5.0)
    async def configLoop(self):
        self.config = api.readConfig()

    @configLoop.before_loop
    async def beforeConfigLoop(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Led(bot))