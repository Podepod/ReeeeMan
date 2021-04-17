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

        self.config = api.readConfig()
        self.regexSearchWords = api.getRegexSearchWordData()
        self.regexReactions = api.getRegexReactionData()
        self.regexBans = api.getRegexBansData()

        self.configLoop.start()

    def cog_unload(self):
        self.configLoop.cancel()

    @bot.command(
        name="getRegex",
        aliases=["getregex", "regexlist", "listregex"],
        help=f"Gives an embed with all regex searchwords and there reactions",
        brief="Lists all regex searchwords",
    )
    async def getRegex(self, ctx):
        # SEARCHWORDS
        embed = discord.Embed(
            title="Basic answers",
            timestamp=datetime.datetime.utcnow(),
            color=discord.Color.red()
        )

        embed.set_thumbnail(url=self.bot.user.avatar_url)

        for regexData in self.regexSearchWords:
            embed.add_field(
                name=f"{regexData['regex']}",
                value=f"Regex string: {regexData['regex']}\nAnswer: {regexData['response']}\nTTS enabled: {regexData['tts']}\nEnabled: {regexData['enabled']}\nRemove message: {regexData['removeMessage']}",
                inline=False
            )

        await ctx.send(embed=embed)

        # REACTIONS
        embed = discord.Embed(
            title="Reactions",
            timestamp=datetime.datetime.utcnow(),
            color=discord.Color.red()
        )

        embed.set_thumbnail(url=self.bot.user.avatar_url)

        for regexData in self.regexReactions:
            embed.add_field(
                name=f"{regexData['regex']}",
                value=f"Regex string: {regexData['regex']}\nReaction: {regexData['reaction']}\nEnabled: {regexData['enabled']}",
                inline=False
            )

        await ctx.send(embed=embed)

        #BANS
        embed = discord.Embed(
            title="Bans",
            timestamp=datetime.datetime.utcnow(),
            color=discord.Color.red()
        )

        embed.set_thumbnail(url=self.bot.user.avatar_url)

        for regexData in self.regexBans:
            embed.add_field(
                name=f"{regexData['regex']}",
                value=f"Regex string: {regexData['regex']}\nOwner Answer: {regexData['ownerAnswer']}\nNormal Answer: {regexData['answer']}\nEnabled: {regexData['enabled']}",
                inline=False
            )

        await ctx.send(embed=embed)


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or message.author.bot:
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

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.author == self.bot.user:
            return

        for searchWord in self.regexSearchWords:
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
                    await after.remove_reaction(emoji, self.bot.user)

                except Exception as e:
                    print("Couldn't remove previous reaction: ", e)

        for searchWord in self.regexReactions:
            if re.search(rf'{searchWord["regex"]}', after.content) and searchWord["enabled"]:            
                try:
                    if (searchWord["reaction"] == ""):
                        reaction = ":sweat_smile:"
                    else:
                        reaction = searchWord["reaction"]

                    await after.add_reaction(reaction)

                except Exception as e:
                    print("Couldn't react to the message: ", e)

        for searchWord in self.regexBans:
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