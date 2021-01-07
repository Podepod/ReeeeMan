import discord
from discord.ext import tasks, commands
import datetime
import asyncio
import re
import random
import apiRequests as api

config = api.readConfig()

bot = commands.Bot(command_prefix=config["basic"]["prefix"], description=config["basic"]["description"])

# Vibes COG
class Vibes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.cofig = api.readConfig()

        self.configLoop.start()

    def cog_unload(self):
        self.configLoop.cancel()

    @bot.command(
        name="Vibe",
        aliases=["vibe", "VibeCheck", "Vibecheck", "vibecheck"],
        help=f"Vibe - sends a random vibe (aliases: vibe, VibeCheck, Vibecheck, vibecheck)",
        brief="sends the vibe",
    )
    async def Vibe(self, ctx):
        vibe = api.getRandomVibe()

        return await ctx.send(vibe["text"])

    @bot.command(
        name="SuggestVibe",
        aliases=["suggestVibe", "suggestvibe", "suggest", "svibe", "vibesug"],
        help=f"SuggestVibe x - suggest a vibe to be added to the vibelist (aliases: suggestVibe, suggestvibe, suggest, svibe, vibesug)",
        brief="Suggest a new vibe",
    )
    async def SuggestVibe(self, ctx, *, text):
        print(ctx.message.author.nick)
        print(ctx.guild.name)

        reply = api.suggestVibe(text, ctx.message.author.nick, ctx.guild.name)

        return await ctx.send(reply)

    @tasks.loop(seconds=5.0)
    async def configLoop(self):
        self.cofig = api.readConfig()

    @configLoop.before_loop
    async def beforeConfigLoop(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Vibes(bot))