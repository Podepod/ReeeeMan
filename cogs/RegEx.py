import discord
from discord.ext import tasks, commands
import datetime
import asyncio
import re
import random
import apiRequests as api

config = api.readConfig()
regexSearchWords = api.getRegexSearchWordData()
regexReactions = api.getRegexReactionData()
regexBans = api.getRegexBansData()

bot = commands.Bot(command_prefix=config["basic"]["prefix"], description=config["basic"]["description"])

# REGEX COG
class RegEx(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.config = config
        self.regexSearchWords = regexSearchWords
        self.regexReactions = regexReactions
        self.regexBans = regexBans

        self.configLoop.start()

    def cog_unload(self):
        self.configLoop.cancel()

    @bot.listen()
    async def on_message(message):
        if message.author == self.bot.user:
            return

        for searchWord in self.regexSearchWords:
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

        for searchWord in self.regexReactions:
            if re.search(rf'{searchWord["regex"]}', message.content) and searchWord["enabled"]:
                try:
                    if (searchWord["reaction"] == ""):
                        reaction = ":sweat_smile:"
                    else:
                        reaction = searchWord["reaction"]

                    await message.add_reaction(reaction)

                except Exception as e:
                    print("Couldn't react to the message: ", e)

        for searchWord in self.regexBans:
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


    # file settings file command check
    @tasks.loop(seconds=5.0)
    async def configLoop(self):

        self.config = api.readConfig()
        self.regexSearchWords = api.getRegexSearchWordData()
        self.regexReactions = api.getRegexReactionData()
        self.regexBans = api.getRegexBansData()

    @configLoop.before_loop
    async def beforeConfigLoop(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(RegEx(bot))