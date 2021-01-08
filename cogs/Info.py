import discord
from discord.ext import tasks, commands
import datetime
import asyncio
import re
import random
import apiRequests as api

config = api.readConfig()

bot = commands.Bot(command_prefix=config["basic"]["prefix"], description=config["basic"]["description"])

# Info COG
class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.cofig = api.readConfig()

        self.configLoop.start()

    def cog_unload(self):
        self.configLoop.cancel()

    # BOTINFO
    # command
    @bot.command(
        name="botInfo",
        aliases=["info", "Botinfo", "BotInfo", "bInfo", "binfo"],
        help="Gives you some info about this bot and its settings",
        brief="Gives you some info about this bot",
    )
    async def botInfo(self, ctx):
        embed = discord.Embed(
            title="Bot info",
            timestamp=datetime.datetime.utcnow(),
            color=discord.Color.red()
        )

        embed.set_thumbnail(url=self.bot.user.avatar_url)

        embed.add_field(
            name="Prefix",
            value=self.config.basic.prefix,
            inline=False
        )
        embed.add_field(
            name="Name",
            value=self.config.basic.name,
            inline=False
        )
        embed.add_field(
            name="Description",
            value=self.config.basic.description,
            inline=False
        )
        embed.add_field(
            name="Version",
            value=self.config.basic.version,
            inline=False
        )

        embed.add_field(
            name="Activity status",
            value=self.config.activity.status,
            inline=False
        )
        embed.add_field(
            name="Activity text",
            value=self.config.activity.text,
            inline=False
        )

        embed.add_field(
            name="Stalking enabled?",
            value=self.config.log.stalkingEnabled,
            inline=False
        )

        return await ctx.channel.send(embed=embed)

    @tasks.loop(seconds=5.0)
    async def configLoop(self):
        self.cofig = api.readConfig()

    @configLoop.before_loop
    async def beforeConfigLoop(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Info(bot))