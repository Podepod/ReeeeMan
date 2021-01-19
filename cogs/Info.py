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

        self.config = api.readConfig()

        self.configLoop.start()

    def cog_unload(self):
        self.configLoop.cancel()

    # BOTINFO
    # command
    @bot.command(
        name="botInfo",
        aliases=["info", "Botinfo", "BotInfo", "botinfo", "bInfo", "binfo"],
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
            value=self.config["basic"]["prefix"],
            inline=False
        )
        embed.add_field(
            name="Name",
            value=self.config["basic"]["name"],
            inline=False
        )
        embed.add_field(
            name="Description",
            value=self.config["basic"]["description"],
            inline=False
        )
        embed.add_field(
            name="Version",
            value=self.config["basic"]["version"],
            inline=False
        )

        embed.add_field(
            name="Activity status",
            value=self.config["activity"]["status"],
            inline=False
        )
        embed.add_field(
            name="Activity text",
            value=self.config["activity"]["text"],
            inline=False
        )

        embed.add_field(
            name="Stalking enabled?",
            value=self.config["log"]["stalkingEnabled"],
            inline=False
        )

        return await ctx.channel.send(embed=embed)

    # COGINFO
    # command


    # GUILDINFO
    # command
    @bot.command(
        name="ServerInfo",
        aliases=["serverinfo", "sinfo", "serverInfo", "Sinfo", "sInfo", "guildInfo", "GuildInfo", "guildinfo"],
        help="Gives you some info about the server you're in",
        brief="Gives you some info about the server"
    )
    async def ServerInfo(self, ctx):
        embed = discord.Embed(
            title=f"{ctx.guild.name}", 
            description=f"Description: {ctx.guild.description}\nCreated at: {ctx.guild.created_at}\nRegion: {ctx.guild.region}\nMember Count: {ctx.guild.member_count}\nRole Count: {len(ctx.guild.roles)}\nText Channels: {len(ctx.guild.text_channels)}\nVoice Channels: {len(ctx.guild.voice_channels)}\nAFK Channel: {ctx.guild.afk_channel.name  if (ctx.guild.afk_channel != None) else 'None'}\nAFK Timeout: {ctx.guild.afk_timeout  if (ctx.guild.afk_channel != None) else 'None'}", 
            timestamp=datetime.datetime.utcnow(), 
            color=discord.Color.red()
        )
        embed.set_thumbnail(url=ctx.guild.icon_url)

        for channel in ctx.guild.text_channels:
            embed.add_field(
                name=channel.name,
                value=f"Channel ID: {channel.id}\nCategory: {channel.category.name}\nCategory ID: {channel.category_id}\nNSFW Channel: {channel.is_nsfw()}\nNews Channel: {channel.is_news()}\nChannel Type: Text",
                inline=False
            )

        for channel in ctx.guild.voice_channels:
            embed.add_field(
                name=channel.name,
                value=f"Channel ID: {channel.id}\nCategory: {channel.category.name}\nCategory ID: {channel.category_id}\nChannel bitrate: {channel.bitrate}\nUser limit: {channel.user_limit}\nChannel Type: Voice",
                inline=False
            )
        
        await ctx.send(embed=embed)

    # MEMBER INFO
    # command
    @bot.command(
        name="MemberInfo",
        aliases=["serverinfo", "sinfo", "serverInfo", "Sinfo", "sInfo", "guildInfo", "GuildInfo", "guildinfo"],
        help="Gives you some info about a member or all members of the server",
        brief="Gives you some info about a member"
    )
    async def ServerInfo(self, ctx, member : discord.Member = None):
        pass

    
    # PING
    # command
    @bot.command(
        name="Ping",
        aliases=["ping"],
        help="Gives you some info about this bot and its settings",
        brief="Gives you some info about this bot",
    )
    async def Ping(self, ctx):
        await ctx.send(self.bot.latency)

    # Custom help?
    # command

    @tasks.loop(seconds=5.0)
    async def configLoop(self):
        self.config = api.readConfig()

    @configLoop.before_loop
    async def beforeConfigLoop(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Info(bot))