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

bot = commands.Bot(command_prefix=config["basic"]["prefix"], description=config["basic"]["description"])


# listener
@bot.listen()
async def on_message(message):
    global config
    if message.author == bot.user:
        return

    if re.search(rf'(?i)(\bree+\b)', message.content) or re.search(rf'(?i)(\b^vibecheck\b)', message.content):
        await message.channel.send("Reeeeeeee")

    if re.search(r'(?i)(^\bpls\b)', message.content):
        await message.channel.send("Weeral?")


@bot.listen()
async def on_message_edit(before, after):
    if after.author == bot.user:
        return
        
    if re.search(rf'(?i)(\bre+\b)', after.content) or re.search(rf'(?i)(\b^vibecheck\b)', after.content):
        await message.channel.send("Reeeeeeee")



# on bot joins guild
@bot.event
async def on_guild_join(guild):
    global config

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
    global config
    print(f"{config['basic']['name']} is up and running...")

    await bot.change_presence(activity=discord.Game(name=config["activity"]["text"]))

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

# custom text command
@bot.command(hidden = True)
async def customText(ctx):
    global config
    await ctx.send(getCustomText()["text"])

# file settings file command check
@tasks.loop(seconds=5.0)
async def checkFilesLoop():
    global config
    log_channel = bot.get_channel(777697840464920586)

    old_config = config
    config = readConfig()

    if (old_config["basic"]["prefix"] != config["basic"]["prefix"]):
        bot.command_prefix = config["basic"]["prefix"]
        await log_channel.send(f"Changed the prefix from '{old_config['basic']['prefix']}' to '{config['basic']['prefix']}'")

    if (old_config["basic"]["name"] != config["basic"]["name"]):
        await bot.user.edit(username=config["basic"]["name"])
        await log_channel.send(f"Changed the bot's username from '{old_config['basic']['name']}' to '{config['basic']['name']}'")

    if (old_config["basic"]["description"] != config["basic"]["description"]):
        bot.description = config["basic"]["description"]
        await log_channel.send(f"Changed the bot's description from '{old_config['basic']['description']}' to '{config['basic']['description']}'")

    if (old_config["activity"]["text"] != config["activity"]["text"]):
        await bot.change_presence(activity=discord.Game(name=config["activity"]["text"]))
        await log_channel.send(f"Changed the activity from '{old_config['activity']['text']}' to '{config['activity']['text']}'")

    #await bot.user.edit(username=name)


@checkFilesLoop.before_loop
async def beforeCheckFilesLoop():
    await bot.wait_until_ready()

# shutdown command
@bot.command(hidden = True)
@commands.is_owner()
async def die(ctx):
    await ctx.send("Bye")
    await ctx.bot.logout()

checkFilesLoop.start()

bot.run(config["basic"]["token"], bot=True, reconnect=True)