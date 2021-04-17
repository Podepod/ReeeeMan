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
        self.activated = False

        self.configLoop.start()

    def cog_unload(self):
        self.configLoop.cancel()

    @bot.command(
        hidden=True,
        name="LedToggle",
        aliases=["ledToggle", "ledtoggle", "Ledtoggle", "Ltoggle", "lToggle", "ltoggle", "LToggle", "lt", "LT", "ledT", "ledt"],
        help="Toggles Led commands",
        brief="Toggles Led commands",
    )
    @commands.is_owner()
    async def Led(self, ctx):
        self.activated = not self.activated

        await ctx.send(f"Led commands activation is now set to {self.activated}")

    @bot.command(
        name="Led",
        aliases=["led"],
        help="Send commands to Podepod's LEDs",
        brief="Send commands to Podepod's LEDs",
    )
    async def Led(self, ctx, *, text):
        if self.activated:
            output = self.room.commandScene(text)
        else:
            output = "Led commands are disabled at this point"

        await ctx.send(output)

    @tasks.loop(seconds=5.0)
    async def configLoop(self):
        self.config = api.readConfig()

    @configLoop.before_loop
    async def beforeConfigLoop(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Led(bot))