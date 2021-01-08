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

    # MESSAGES
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

            embed.set_thumbnail(url=message.author.avatar_url)

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


    # on message delete, log in chat log channel
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author == self.bot.user:
            return

        if self.config["log"]["stalkingEnabled"]:
            logchannel = self.bot.get_channel(int(self.config["log"]["stalkChannelID"]))

            embed = discord.Embed(
                title=f"{message.author.nick}'s message has been deleted in {message.guild.name}", 
                timestamp=datetime.datetime.utcnow(), 
                color=discord.Color.red()
            )

            embed.set_thumbnail(url=message.author.avatar_url)

            embed.add_field(
                name="Author",
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

    # on message edit, log in chat log channel
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author == self.bot.user:
            return

        if self.config["log"]["stalkingEnabled"]:
            logchannel = self.bot.get_channel(int(self.config["log"]["stalkChannelID"]))

            embed = discord.Embed(
                title=f"{before.author.nick} has edited a message in {before.guild.name}", 
                timestamp=datetime.datetime.utcnow(), 
                color=discord.Color.red()
            )

            embed.set_thumbnail(url=message.author.avatar_url)

            embed.add_field(
                name="User",
                value=f"Nickname: {before.author.nick}\nUsername: {before.author.name}\nID: {before.author.id}",
                inline=False
            )
            embed.add_field(
                name="Channel",
                value=f"Name: {before.channel.name}\nID: {before.channel.id}\nguild: {before.guild.name}",
                inline=False
            )
            embed.add_field(
                name="Message before",
                value=f"{before.content}",
                inline=False
            )
            embed.add_field(
                name="Message after",
                value=f"{after.content}",
                inline=False
            )

            await logchannel.send(embed=embed)

        return

    # REACTIONS
    # on reaction added, log in chat log channel
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        pass

    # on reaction removed, log in chat log channel
    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        pass

    # on reactions cleared, log in chat log channel
    @commands.Cog.listener()
    async def on_reaction_clear(self, message, reactions):
        pass

    # on reaction emoji cleared, log in chat log channel
    @commands.Cog.listener()
    async def on_reaction_clear_emoji(self, reaction):
        pass

    # PRIVATE CHANNELS
    # on_private_channel_create(self, channel)
    # on_private_channel_delete(self, channel)
    # on_private_channel_update(self, before, after)
    # on_private_channel_pins_update(self, channel, last_pin)

    # GUILD CHANNELS
    # on_guild_channel_create(self, channel)
    # on_guild_channel_delete(self, channel)
    # on_guild_channel_update(self, before, after)
    # on_guild_channel_pins_update(self, channel, last_pin)
    # on_guild_integrations_update(self, guild)
    # on_webhooks_update(self, channel)
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

    # on_guild_remove(self, guild)
    # on_guild_update(self, before, after)
    # on_guild_role_create(self, role)
    # on_guild_role_delete(self, role)
    # on_guild_role_update(self, before, after)
    # on_guild_emojis_update(self, guild, before, after)
    # on_guild_available(self, guild)
    # on_guild_unavailable(sefl, guild)

    # MEMBERS
    # on_member_join(self, member)
    # on_member_remove(self, member)
    # on_member_update(self, before, after)
    # on_user_update(self, before, after)
    # on_voice_state_update(self, member, before, after)
    # on_member_ban(self, guild, user)
    # on_member_unban(self, guild, user)

    # INVITES
    # on_invite_create(self, invite)
    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        logchannel = self.bot.get_channel(int(self.config["log"]["channelID"]))

        embed = discord.Embed(
            title=f"New invite created for {invite.guild.name}",
            timestamp=datetime.datetime.utcnow(),
            color=discord.Color.red()
        )

        embed.add_field(
            name="Invite Details",
            value=f"Created at: {invite.created_at}\nCreated By: {invite.inviter.name}\nTemporary: {invite.temporary}\nURL: {invite.url}\nMax Age: {invite.max_age}\nMax Uses: {invite.max_uses}\nID: {invite.id}",
            inline=False
        )

        embed.add_field(
            name="Guild Details",
            value=f"Created at: {invite.guild.created_at}\nRegion: {invite.guild.region}\nMember Count: {intivite.guild.member_count}\nRole Count: {len(invite.guild.roles)}\nText Channels: {len(invite.guild.text_channels)}\nVoice Channels: {len(invite.guild.voice_channels)}",
            inline=False
        )

    # on_invite_delete(self, invite)

    # BOT
    # on_group_join(self, channel, user)
    # on_group_remove(self, channel, user)
    # on_relationship_add(self, relationship)
    # on_relationship_remove(self, relationship)
    # on_relationship_update(self, before, after)

    @tasks.loop(seconds=5.0)
    async def configLoop(self):
        self.config = api.readConfig()

    @configLoop.before_loop
    async def beforeConfigLoop(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Events(bot))