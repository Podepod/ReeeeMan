import discord
from discord.ext import tasks, commands
import datetime
import asyncio
import re
import random
import apiRequests as api
import wavelink

config = api.readConfig()

bot = commands.Bot(command_prefix=config["basic"]["prefix"], description=config["basic"]["description"])

# Music COG
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.config = api.readConfig()
        self.tracks = list()

        self.configLoop.start()

        if not hasattr(bot, 'wavelink'):
            self.bot.wavelink = wavelink.Client(bot=self.bot)

        self.bot.loop.create_task(self.start_nodes())

    def cog_unload(self):
        self.configLoop.cancel()

    async def start_nodes(self):
        await self.bot.wait_until_ready()

        # Initiate our nodes. For this example we will use one server.
        # Region should be a discord.py guild.region e.g sydney or us_central (Though this is not technically required)
        await self.bot.wavelink.initiate_node(host='10.30.20.187',
                                              port=4321,
                                              rest_uri='http://10.30.20.187:4321',
                                              password='youshallnotpass',
                                              identifier='TEST',
                                              region='eu_east')

    @bot.command(
        name="Connect",
        aliases=["con", "connect", "Con"],
        help=f"Connects the bot to your current voice channel or a chosen voice channel",
        brief="Connects the bot to a voice channel"
    )
    async def connect_(self, ctx, *, channel: discord.VoiceChannel=None):
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise discord.DiscordException('No channel to join. Please either specify a valid channel or join one.')

        player = self.bot.wavelink.get_player(ctx.guild.id)
        await ctx.send(f'Connecting to **`{channel.name}`**')
        await player.connect(channel.id)

    @bot.command(
        name="Play",
        aliases=["play", "p", "P"],
        help=f"Plays a given song from probably youtube",
        brief="Plays a given song"
    )
    async def play(self, ctx, *, query: str):
        self.tracks += await self.bot.wavelink.get_tracks(f'ytsearch:{query}')

        if not self.tracks:
            return await ctx.send('Could not find any songs with that query.')

        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            await ctx.invoke(self.connect_)

        await ctx.send(f'Added {str(tracks[0])} to the queue.')
        await player.play(self.tracks[0])

    @tasks.loop(seconds=5.0)
    async def configLoop(self):
        self.config = api.readConfig()

    @configLoop.before_loop
    async def beforeConfigLoop(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Music(bot))