#!/usr/bin/python3.7

import discord
from discord.ext import commands
import datetime
import asyncio
import requests
import json
import re

CONFIG_FILE = "./botSettings.json"

def readConfig():
    with open(CONFIG_FILE, "r") as read_file:
        data = json.load(read_file)
        read_file.close()

    return data

def getCustomText():
    api_page = requests.get("http://10.30.20.187:4005/api/bot/customText")
    
    return json.loads(api_page.text)

config = readConfig()

bot = commands.Bot(command_prefix=config["prefix"], description=config["description"])

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

# random troll command
@bot.command(hidden = True)
async def drink(ctx):
    await ctx.send("Lol das hier wel grappig gelle zyt goe weg.")
    await ctx.send("Conrad ge zyt dronken man")
    await bot.change_presence(activity=discord.Game(name="Conrad ge zyt dronken"))

# custom text command
@bot.command(hidden = True)
async def customText(ctx):
    await ctx.send(getCustomText()["data"]["text"])

# shutdown command
@bot.command(hidden = True)
@commands.is_owner()
async def die(ctx):
    await ctx.send("Bye")
    await ctx.bot.logout()

bot.run(config["token"], bot=True, reconnect=True)