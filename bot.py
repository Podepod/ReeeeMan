#!/usr/bin/python3.7

import discord
from discord.ext import tasks, commands
import datetime
import asyncio
import requests
import json
import re

def readConfig():
    api_page = requests.get("http://10.30.20.187:4005/api/bot/settings")
    
    return json.loads(api_page.text)["data"]

def getCustomText():
    api_page = requests.get("http://10.30.20.187:4005/api/bot/customText")
    
    return json.loads(api_page.text)["data"]

config = readConfig()

bot = commands.Bot(command_prefix=config["prefix"], description=config["description"])


# listener
@bot.listen()
async def on_message(message):
    if message.author == bot.user:
        return

    if re.search(rf'(?i)(\bree+\b)', message.content):
        await message.channel.send("Reeeeeeee")

    if re.search(r'(?i)(^\bpls\b)', message.content):
        await message.channel.send("Weeral?")


@bot.listen()
async def on_message_edit(before, after):
    if after.author == bot.user:
        return
        
    if re.search(rf'(?i)(\bre+\b)', after.content):
        await message.channel.send("Reeeeeeee")



# on bot joins guild
@bot.event
async def on_guild_join(guild):
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
@bot.event
async def on_ready():
    print(f"{config['name']} is up and running...")

    print("#############################################")
    print(f"Active in {len(bot.guilds)} guilds:")
    for guild in bot.guilds:
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

    await bot.change_presence(activity=discord.Game(name="Reeeeeeee"))

# custom text command
@bot.command(hidden = True)
async def customText(ctx):
    await ctx.send(getCustomText()["text"])

# file settings file command check
@tasks.loop(seconds=5.0)
async def checkFiles():
    global config
    old_config = config
    config = readConfig()
    if (old_config["activity"] != config["activity"]):
        await bot.change_presence(activity=discord.Game(name=config["activity"]))


# shutdown command
@bot.command(hidden = True)
@commands.is_owner()
async def die(ctx):
    await ctx.send("Bye")
    await ctx.bot.logout()

bot.run(config["token"], bot=True, reconnect=True)