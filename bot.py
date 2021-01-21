#!/usr/bin/python3.7

import discord
from discord.ext import tasks, commands
import datetime
import asyncio
import re
import apiRequests as api

config = api.readConfig()
cogList = api.getCogs()

bot = commands.Bot(command_prefix=config["basic"]["prefix"], description=config["basic"]["description"])

# ADD COGS
if __name__ == '__main__':
    for extension in cogList:
        if extension["enabled"]:
            try:
                bot.load_extension(f"cogs.{extension['name']}")
            except Exception as e:
                print(f'Failed to load extension {extension["name"]}.', e)

async def checkConfig(old_config):
    global config
    log_channel = bot.get_channel(int(config["log"]["channelID"]))

    # BASIC config
    if (old_config["basic"]["prefix"] != config["basic"]["prefix"]):
        bot.command_prefix = config["basic"]["prefix"]
        await log_channel.send(f"Changed the prefix from '{old_config['basic']['prefix']}' to '{config['basic']['prefix']}'")

    if (old_config["basic"]["name"] != config["basic"]["name"]):
        await bot.user.edit(username=config["basic"]["name"])
        await log_channel.send(f"Changed the bot's username from '{old_config['basic']['name']}' to '{config['basic']['name']}'")

    if (old_config["basic"]["description"] != config["basic"]["description"]):
        bot.description = config["basic"]["description"]
        await log_channel.send(f"Changed the bot's description from '{old_config['basic']['description']}' to '{config['basic']['description']}'")

    # ACTIVITY config
    if (old_config["activity"]["status"] != config["activity"]["status"]):
        # opties: online, offline, idle, do_no_disturb, invisible
        await bot.change_presence(status=config["activity"]["status"])
        await log_channel.send(f"Changed the activity status from '{old_config['activity']['status']}' to '{config['activity']['status']}'")

    if (old_config["activity"]["text"] != config["activity"]["text"]):
        await bot.change_presence(activity=discord.Game(name=config["activity"]["text"]))
        await log_channel.send(f"Changed the activity text from '{old_config['activity']['text']}' to '{config['activity']['text']}'")

async def checkCogs():
    global cogList
    log_channel = bot.get_channel(int(config["log"]["channelID"]))

    botCogFound = False
    apiCogFound = False

    for botCog in list(bot.cogs):
        botCogFound = False
        for cog in cogList:
            if (cog["name"] == botCog):
                botCogFound = True
                if not cog["enabled"]:
                    bot.unload_extension(f"cogs.{botCog}")
                break

        if not botCogFound:
            bot.unload_extension(f"cogs.{botCog}")

    for apiCog in cogList:
        apiCogFound = False
        for cog in list(bot.cogs):
            if (cog == apiCog["name"]):
                apiCogFound = True
                break

        if (not apiCogFound) and (apiCog["enabled"]):
            try:
                bot.load_extension(f"cogs.{apiCog['name']}")
            except discord.ext.commands.errors.ExtensionNotFound:
                pass

# COGS
# load cog command
@bot.command(
    hidden = True,
    name = "loadCog",
    aliases = ["load"],
    help = "Loads the given cog if this cog exists and is unloaded",
    brief = "Loads cogs"
)
@commands.is_owner()
async def loadCog(ctx, cog: str):
    global cogList

    cogList = api.getCogs()
    for cogName in cogList:
        if (cogName["name"] == cog):
            try:
                response = api.changeCog(cog, "load")
                bot.load_extension(f"cogs.{cogName['name']}")
            except Exception as e:
                response = f"{e}"
            finally:
                embed = discord.Embed(title=f"Load {cog}", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
                embed.add_field(
                    name = "Response",
                    value = response,
                    inline = False
                )

                return await ctx.send(embed=embed)
    
    response = f"Could not find the Cog '{cog}'"

    embed = discord.Embed(title=f"Load {cog}", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
    embed.add_field(
        name = "Response",
        value = response,
        inline = False
    )
    return await ctx.send(embed=embed)

# reload cog command
@bot.command(
    hidden = True,
    name = "reloadCog",
    aliases = ["reload"],
    help = "Reloads the given cog if this cog exists and is loaded",
    brief = "Reloads cogs"
)
@commands.is_owner()
async def reloadCog(ctx, cog: str):
    global cogList

    cogList = api.getCogs()
    for cogName in cogList:
        if (cogName["name"] == cog):
            try:
                bot.unload_extension(f"cogs.{cogName['name']}")
                bot.load_extension(f"cogs.{cogName['name']}")
                response = f"{cogName['name']} succesfully reloaded"
            except Exception as e:
                response = f"{e}"
            finally:
                embed = discord.Embed(title=f"Load {cog}", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
                embed.add_field(
                    name = "Response",
                    value = response,
                    inline = False
                )

                return await ctx.send(embed=embed)
    
    response = f"Could not find the Cog '{cog}'"

    embed = discord.Embed(title=f"Reload {cog}", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
    embed.add_field(
        name = "Response",
        value = response,
        inline = False
    )
    return await ctx.send(embed=embed)

# unload cog command
@bot.command(
    hidden = True,
    name = "unloadCog",
    aliases = ["unload"],
    help = "Unloads the given cog if this cog exists and is loaded",
    brief = "Unloads cogs"
)
@commands.is_owner()
async def unloadCog(ctx, cog: str):
    global cogList

    cogList = api.getCogs()
    for cogName in cogList:
        if (cogName["name"] == cog):
            try:
                response = api.changeCog(cog, "unload")
                bot.unload_extension(f"cogs.{cogName['name']}")
            except Exception as e:
                response = f"{e}"
            finally:
                embed = discord.Embed(title=f"Unload {cog}", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
                embed.add_field(
                    name = "Response",
                    value = response,
                    inline = False
                )

                return await ctx.send(embed=embed)
    
    response = f"Could not find the Cog '{cog}'"

    embed = discord.Embed(title=f"Unload {cog}", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
    embed.add_field(
        name = "Response",
        value = response,
        inline = False
    )
    return await ctx.send(embed=embed)

# cog list command
@bot.command(hidden = True)
@commands.is_owner()
async def listCog(ctx):
    cogList = api.getCogs()

    embed = discord.Embed(title="Cog List (from api)", description="This is a list of all the available cogs. (name and enabled?)", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())

    for cog in cogList:
        embed.add_field(
            name = cog["name"],
            value = f"{cog['enabled']}",
            inline = False
        )

    await ctx.send(embed=embed)

    return await ctx.send(bot.cogs)

# file settings file command check
@tasks.loop(seconds=5.0)
async def checkFilesLoop():
    global config
    old_config = config
    config = api.readConfig()
    await checkConfig(old_config)

    global cogList
    cogList = api.getCogs()
    await checkCogs()

@checkFilesLoop.before_loop
async def beforeCheckFilesLoop():
    await bot.wait_until_ready()

# shutdown command
@bot.command(hidden = True)
@commands.is_owner()
async def die(ctx):
    await ctx.send("Bye")
    print("Bye")
    await bot.logout()
    await bot.close()

checkFilesLoop.start()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return await ctx.send("No such command found")
    return print(error)

bot.run(config["basic"]["token"], bot=True, reconnect=True)