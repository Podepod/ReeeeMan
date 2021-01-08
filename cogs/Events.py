import discord
from discord.ext import tasks, commands
import datetime
import asyncio
import re
import random
import apiRequests as api

config = api.readConfig()

bot = commands.Bot(command_prefix=config["basic"]["prefix"], description=config["basic"]["description"])

# EVENTS COG
class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.config = api.readConfig()

        self.configLoop.start()

    def cog_unload(self):
        self.configLoop.cancel()

    # on bot joins guild
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        logchannel = self.bot.get_channel(int(self.config["log"]["channelID"]))
        print(f"{self.config['basic']['name']} joined a new server")

        embed = discord.Embed(
            title=f"{guild.name}",
            description=f"Created at: {guild.created_at}\nRegion: {guild.region}\nMember Count: {guild.member_count}\nRole Count: {len(guild.roles)}\nText Channels: {len(guild.text_channels)}\nVoice Channels: {len(guild.voice_channels)}",
            timestamp=datetime.datetime.utcnow(),
            color=discord.Color.red()
        )
        for channel in guild.text_channels:
            embed.add_field(
                name=channel.name,
                value=f"Channel ID: {channel.id}\nNSFW Channel: {channel.is_nsfw()}\nNews Channel: {channel.is_news()}",
                inline=False
            )
        await logchannel.send(embed=embed)


    # on ready
    @commands.Cog.listener()
    async def on_ready(self):   
        logchannel = self.bot.get_channel(int(self.config["log"]["channelID"]))
        print(f"{self.config['basic']['name']} is up and running...")

        await self.bot.change_presence(activity=discord.Game(name=self.config["activity"]["text"]))

        embed = discord.Embed(title=f"{self.config['basic']['name']} is up and running...", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
        embed.add_field(name="Active Guilds", value=len(self.bot.guilds), inline=False)
        embed.add_field(name="Activity text", value=self.config["activity"]["text"], inline=False)
        await logchannel.send(embed=embed)

        for guild in self.bot.guilds:
            embed = discord.Embed(
                title=f"{guild.name}", 
                description=f"Created at: {guild.created_at}\nRegion: {guild.region}\nMember Count: {guild.member_count}\nRole Count: {len(guild.roles)}\nText Channels: {len(guild.text_channels)}\nVoice Channels: {len(guild.voice_channels)}", 
                timestamp=datetime.datetime.utcnow(), 
                color=discord.Color.red()
            )
            embed.set_thumbnail(url=guild.icon_url)
            for channel in guild.text_channels:
                embed.add_field(
                    name=channel.name,
                    value=f"Channel ID: {channel.id}\nNSFW Channel: {channel.is_nsfw()}\nNews Channel: {channel.is_news()}",
                    inline=False
                )
            await logchannel.send(embed=embed)

    # on message, log in chat log channel
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if self.config["log"]["stalkingEnabled"]:
            logchannel = self.bot.get_channel(int(self.config["log"]["stalkChannelID"]))

            embed = discord.Embed(
                title=f"{message.author.nick} has sent a message in {message.guild.name}", 
                timestamp=datetime.datetime.utcnow(), 
                color=discord.Color.red()
            )

            embed.add_field(
                name="User",
                value=f"Nickname: {message.author.nick}\nUsername: {message.author.name}\nID: {message.author.id}",
                inline=False
            )
            embed.add_field(
                name="Channel",
                value=f"Name: {message.channel.name}\nID: {message.channel.id}\nguild: {message.guild.name}",
                inline=False
            )
            embed.add_field(
                name="Message",
                value=f"{message.content}",
                inline=False
            )

            await logchannel.send(embed=embed)

        return


    # on message, log in chat log channel
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author == self.bot.user:
            return

    # on message, log in chat log channel
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if message.author == self.bot.user:
            return

    @tasks.loop(seconds=5.0)
    async def configLoop(self):
        self.config = api.readConfig()

    @configLoop.before_loop
    async def beforeConfigLoop(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Events(bot))