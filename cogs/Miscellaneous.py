import discord
from discord.ext import tasks, commands
import datetime
import asyncio
import requests
import json
import re



# MISC COG
class Miscellaneous(commands.Cogs):
    def __init__(self, bot):
        sefl.bot = bot

    # CLEANUP
    # command
    @bot.command(
        name="cleanup",
        help="Removes an amount of user messages. Use this function as follows \"<prefix>cleanup <numberOfMessages>\". Where numberOfMessages is the number of messages you want to remove.",
        brief="Removes an amount of user messages",
    )
    async def cleanup(self, ctx, amount = 10):
        if type(amount) != int:
            ctx.send("The second argument should be a number.")
            return

        channel = ctx.message.channel
        messages = await channel.history(limit=1000).flatten()
        removed = 0

        for message in messages:
            if message.author.id == ctx.message.author.id:
                await message.delete()
                removed += 1
            if removed == amount:
                break
        
        dmChannel = ctx.message.author.dm_channel
        if dmChannel == None:
            await ctx.message.author.create_dm()
            dmChannel = ctx.message.author.dm_channel
        
        await dmChannel.send(f"Removed {removed} messages from the {ctx.message.channel.name} channel.")

def setup(bot):
    bot.add_cog(Miscellaneous(bot))