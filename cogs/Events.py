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
        config = self.config

        print("#############################################")
        print(f"joined a new guild:\nname: {guild.name}\ncreated at: {guild.created_at}\nregion: {guild.region}\nowner: {guild.owner}\nicon url: {guild.icon_url}\nchannels:")
        for channel in guild.text_channels:
            print(f"- channelname: {channel.name}\n * id: {channel.id}\n * nsfw: {channel.is_nsfw()}\n * news: {channel.is_news()}")
        print("roles:")
        for role in guild.roles:
            print(f"- Rolename: {role.name}\n * ID: {role.id}")
        print(f"members ({guild.member_count}):")
        for member in guild.members:
            print(f"- membername: {member.name}\n * id: {member.id}\n * discriminator: {member.discriminator}\n * nickname: {member.nick}\n * bot: {member.bot}")
        print("#############################################")

    # on ready
    @commands.Cog.listener()
    async def on_ready(self):   
        config = self.config
        logchannel = self.bot.get_channel(int(self.config["log"]["channelID"]))
        print(f"{config['basic']['name']} is up and running...")

        await self.bot.change_presence(activity=discord.Game(name=config["activity"]["text"]))

        print("#############################################")
        print(f"Active in {len(bot.guilds)} guilds:")
        for guild in self.bot.guilds:
            print(f"name: {guild.name}\ncreated at: {guild.created_at}\nregion: {guild.region}\nowner: {guild.owner}\nicon url: {guild.icon_url}\nchannels:")
            for channel in guild.text_channels:
                print(f"- channelname: {channel.name}\n * id: {channel.id}\n * nsfw: {channel.is_nsfw()}\n * news: {channel.is_news()}")
            print("roles:")
            for role in guild.roles:
                print(f"- Rolename: {role.name}\n * ID: {role.id}")
            print(f"members ({guild.member_count}):")
            for member in guild.members:
                print(f"- membername: {member.name}\n * id: {member.id}\n * discriminator: {member.discriminator}\n * nickname: {member.nick}\n * bot: {member.bot}")
        print("#############################################")

        embed = discord.Embed(title=f"{self.config['basic']['name']} is up and running...", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
        embed.add_field(name="Active Guilds", value=len(self.bot.guilds), inline=False)
        embed.add_field(name="Activity text", value=self.config["activity"]["text"], inline=False)
        await logchannel.send(embed=embed)

        for guild in self.bot.guilds:
            embed = discord.Embed(title=f"{guild.name}", description=f"Created at: {guild.created_at}\n Region: {guild.region}\n Owner: {guild.owner}", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
            embed.set_image(url=guild.icon_url)
            for channel in guild.text_channels:
                embed.add_field(
                    name=channel.name,
                    value=f"ID: {channel.id}\nNSFW: {channel.is_nsfw()}\nNews: {channel.is_news()}",
                    inline=False
                )
            await logchannel.send(embed=embed)


    @tasks.loop(seconds=5.0)
    async def configLoop(self):
        self.config = api.readConfig()

    @configLoop.before_loop
    async def beforeConfigLoop(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Events(bot))