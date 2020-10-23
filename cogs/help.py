import io
import discord
import asyncio
import os
from collections import deque, Counter
from discord import Embed, Color, HTTPException
from discord.utils import get
from collections import deque
from datetime import datetime
from discord.ext import commands
# import discord is not necessary unless you are using it inside the code

class help(commands.Cog):
    # The constructor method
    def __init__(self, client):
        self.client = client


    @commands.command(pass_context=True)
    async def help(self, ctx):
        author = ctx.message.author

        embed=discord.Embed(title="Help!", description="looks like you need some help.", color=0x8b0000, timestamp=ctx.message.created_at)

        embed.add_field(name=f"⚙️ {ctx.prefix}core", value="Shows all the core commands.")
        embed.add_field(name=f"🛠 {ctx.prefix}utility", value="Shows moderation commands and other useful tools.")
        embed.add_field(name=f"😄 {ctx.prefix}fun", value="Shows some fun commands you can do.")
        embed.add_field(name=f"👏 {ctx.prefix}actions", value="Shows commands for actions such as slap, kiss, and hug.")
        embed.add_field(name=f"<:reddit:766325395074973767> {ctx.prefix}reddit", value="Shows commands such as memes, and cursed comments.")
        embed.add_field(name=f"🐶 {ctx.prefix}animals", value="Shows commands for looking at animals.")
        embed.add_field(name=f"😏 {ctx.prefix}nsfw", value="Shows commands for weird things.")
        embed.add_field(name=f"🎵 {ctx.prefix}music", value="Shows commands for playing music.")
        embed.add_field(name=f"‍🤷‍♂️ {ctx.prefix}other", value="Shows some extra commands.")

        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.group(name="core")
    async def _core(self, ctx):
        if ctx.invoked_subcommand is None:
            author = ctx.message.author

            embed=discord.Embed(title="Core commands!", description=f"{ctx.prefix}core `<command name>` - Use this to get help with certain commands.\n\n`{ctx.prefix}help`, `{ctx.prefix}invite`, `{ctx.prefix}sever`, `{ctx.prefix}vote`, `{ctx.prefix}updates`, `{ctx.prefix}about`", color=0x8b0000, timestamp=ctx.message.created_at)

            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

            await ctx.send(embed=embed)

    @_core.command(aliases=['help'])
    async def help2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}help`", description="Show's the help menu.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_core.command(aliases=['invite'])
    async def invite2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}invite`", description="Give's you an invite for the bot.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_core.command(aliases=['server'])
    async def server2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}server`", description="Give's you an invite to the help server.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_core.command(aliases=['vote'])
    async def vote2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}server`", description="Give's you an a link so you can vote for the bot.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_core.command(aliases=['updates'])
    async def updates2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}updates`", description="Show's you the latest bot updates.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_core.command(aliases=['about'])
    async def about2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}updates`", description="Show's you the latest bot updates.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.group(name="fun")
    async def _fun(self, ctx):
        if ctx.invoked_subcommand is None:
            author = ctx.message.author

            embed=discord.Embed(title="Fun commands!", description=f"{ctx.prefix}fun `<command name>` - Use this to get help with certain commands.\n\n`{ctx.prefix}gay`, `{ctx.prefix}straight`, `{ctx.prefix}iq`, `{ctx.prefix}dice`, `{ctx.prefix}fakesnake`, `{ctx.prefix}bruh`, `{ctx.prefix}say`, `emsay`, `{ctx.prefix}pp`, `{ctx.prefix}rapist`, `{ctx.prefix}funfact`, `{ctx.prefix}rps`, `{ctx.prefix}8ball`, `{ctx.prefix}kill`, `{ctx.prefix}love`, `{ctx.prefix}ship`, `{ctx.prefix}snipe`, `{ctx.prefix}editsnipe`", color=0x8b0000, timestamp=ctx.message.created_at)

            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

            await ctx.send(embed=embed)

    @_fun.command(aliases=['gay'])
    async def gay2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}gay <optinal @user>`", description="Tell's you how gay you are, or how gay someone else is.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_fun.command(aliases=['straight'])
    async def straight2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}straight <optinal @user>`", description="Tell's you how straight you are, or how gay someone else is.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_fun.command(aliases=['iq'])
    async def iq2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}iq <optinal @user>`", description="Tell's you what your iq is, or someone else's iq.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_fun.command(aliases=['dice'])
    async def dice2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}dice`", description="Allow's you to roll a dice 1-6.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_fun.command(aliases=['fakesnake'])
    async def fakesnake2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}fakesnake`", description="Shows a slithery small green snake.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_fun.command(aliases=['bruh'])
    async def bruh2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}bruh`", description="Send's five bruh's, no seriously try it.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_fun.command(aliases=['say'])
    async def say2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}say <content>`", description="Allow's you to make the bot say whatever you want.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_fun.command(aliases=['emsay'])
    async def emsay2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}say <content>`", description="Allow's you to make the bot say whatever you want, but it's in an embed.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_fun.command(aliases=['pp'])
    async def pp2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}pp <optional @user>`", description="Tell's you your pp size or, someone else's pp size.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_fun.command(aliases=['rapist'])
    async def rapist2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}rapist <optional @user>`", description="Tell's you if your a rapist, or if someone else is a rapist.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_fun.command(aliases=['funfact'])
    async def funfact2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}funfact <optional @user>`", description="Tell's you a random funfact.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_fun.command(aliases=['rps'])
    async def rps2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}rps <rock/paper/scissors>`", description="Allow's you to play rock, paper, scissors with the bot.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_fun.command(aliases=['8ball'])
    async def ball2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}8ball <question>`", description="Ask the bot a question and it will give you your fortune.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_fun.command(aliases=['kill'])
    async def kill2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}kill <@user>`", description="Allow's you to kill another user.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_fun.command(aliases=['love'])
    async def love2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}love <@user> <optional @user>`", description="How much do they love you, or how much do they love another user?", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_fun.command(aliases=['ship'])
    async def ship2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}ship <@user> <optional @user>`", description="Are you guys a ship, or are they a ship?", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_fun.command(aliases=['snipe'])
    async def snipe2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}snipe`", description="Get a recently deleted message in the channel you are currently in.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_fun.command(aliases=['editsnipe'])
    async def editsnipe2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}editsnipe`", description="Get a recently edited message in the channel you are currently in.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)



    @commands.group(name="actions")
    async def _actions(self, ctx):
        if ctx.invoked_subcommand is None:

            author = ctx.message.author

            embed=discord.Embed(title="Actions commands!", description=f"{ctx.prefix}fun `<command name>` - Use this to get help with certain commands.\n\n`{ctx.prefix}hug`, `{ctx.prefix}kiss`, `{ctx.prefix}slap`", color=0x8b0000, timestamp=ctx.message.created_at)

            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

            await ctx.send(embed=embed)

    @_actions.command(aliases=['hug'])
    async def hug2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}hug <@user>`", description="Hugs the person you ping.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_actions.command(aliases=['kiss'])
    async def kiss2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}kiss <@user>`", description="Kisses the person you ping.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_actions.command(aliases=['slap'])
    async def slap2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}slap <@user>`", description="Slaps the person you ping.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.group(name="reddit")
    async def _reddit(self, ctx):
        if ctx.invoked_subcommand is None:
            author = ctx.message.author

            embed=discord.Embed(title="Reddit commands!", description=f"{ctx.prefix}reddit `<command name>` - Use this to get help with certain commands.\n\n`{ctx.prefix}meme`, `{ctx.prefix}dankmeme`, `{ctx.prefix}cursedcomments`, `{ctx.prefix}blacktwitter`", color=0x8b0000)

            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

            await ctx.send(embed=embed)

    @_reddit.command(aliases=['meme'])
    async def meme2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}meme`", description="Show's you a funny meme, maybe it depends the day.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_reddit.command(aliases=['dankmeme'])
    async def dankmeme2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}dankmeme`", description="Show's you a dank meme.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_reddit.command(aliases=['cursedcomments'])
    async def cursedcomments2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}cursedcomments`", description="Shows a cursed comments.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_reddit.command(aliases=['blacktwitter'])
    async def blacktwitter2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}blacktwitter`", description="Shows you how black twitter is.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.group(name="nsfw")
    async def _nsfw(self, ctx):
        if ctx.invoked_subcommand is None:
            author = ctx.message.author

            embed=discord.Embed(title="NSFW commands!", description=f"{ctx.prefix}nsfw `<command name>` - Use this to get help with certain commands.\n\n`{ctx.prefix}nsfw`, `{ctx.prefix}boobs`, `{ctx.prefix}ass`,  `{ctx.prefix}pussy`", color=0x8b0000)

            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

            await ctx.send(embed=embed)

    @_nsfw.command(aliases=['nsfw2'])
    async def nsfw3(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}nsfw2`", description="Show's a nsfw photo, from the nsfw2 subreddit.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_nsfw.command(aliases=['boobs'])
    async def boobs2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}boobs`", description="Show's pictures of boobs.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_nsfw.command(aliases=['ass'])
    async def ass2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}ass`", description="Show's a picture of some ass.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_nsfw.command(aliases=['pussy'])
    async def pussy2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}pussy`", description="Show's a picture of some pussy.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.group(name="animals")
    async def _animals(self, ctx):
        if ctx.invoked_subcommand is None:
            author = ctx.message.author

            embed=discord.Embed(title="Animal commands!", description=f"{ctx.prefix}animals `<command name>` - Use this to get help with certain commands.\n\n`{ctx.prefix}animal`, `{ctx.prefix}cat`, `{ctx.prefix}dog`, `{ctx.prefix}snake`, `{ctx.prefix}lizard`", color=0x8b0000)

            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

            await ctx.send(embed=embed)

    @_animals.command(aliases=['animal'])
    async def animal2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}animal`", description="Show's you a random picture of a animal.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_animals.command(aliases=['cat'])
    async def cat2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}cat`", description="Show's you a random picture of a cat.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_animals.command(aliases=['dog'])
    async def dog2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}dog`", description="Show's you a random pic of a dog.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_animals.command(aliases=['snake'])
    async def snake2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}snake`", description="Show's you a random pic of a snake.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_animals.command(aliases=['lizard'])
    async def lizard2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}lizard`", description=" Shows you a random pic of a lizard.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


    @commands.group(name="utility")
    async def _utility(self, ctx):
        if ctx.invoked_subcommand is None:
            author = ctx.message.author

            embed=discord.Embed(title="Utility commands!", description=f"{ctx.prefix}utility `<command name>` - Use this to get help with certain commands.", color=0x8b0000, timestamp=ctx.message.created_at)

            embed.add_field(name="Basic moderation", value=f"`{ctx.prefix}clear`, `{ctx.prefix}mute`, `{ctx.prefix}unmute`, `{ctx.prefix}kick`, `{ctx.prefix}ban`, `{ctx.prefix}setup-logs`", inline=False)
            embed.add_field(name="Information", value=f"`{ctx.prefix}info`, `{ctx.prefix}serverinfo`, `{ctx.prefix}avatar`", inline=False)
            embed.add_field(name="Automation", value=f"`{ctx.prefix}autorole`, `{ctx.prefix}autorole-disable`", inline=False)
            embed.add_field(name="Role", value=f"`{ctx.prefix}addrole`, `{ctx.prefix}removerole`, `{ctx.prefix}role`, `{ctx.prefix}`", inline=False)
            embed.add_field(name="Nickname", value=f"`{ctx.prefix}nick`, `{ctx.prefix}nickreset`, `{ctx.prefix}nickall`, `{ctx.prefix}nickresetall`", inline=False)

            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

            await ctx.send(embed=embed)

    @_utility.command(aliases=['clear'])
    async def clear2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}clear <amount>`", description="Allow's you to clear the amount of message's you put.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_utility.command(aliases=['mute'])
    async def mute2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}mute <@user> <time> <optional reason>`", description="Allow's you to mute someone for a certain amount of time, you don't need to put a time.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_utility.command(aliases=['unmute'])
    async def unmute2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}unmute <@user>`", description="Allow's you to unmute a user that is muted.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_utility.command(aliases=['kick'])
    async def kick2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}kick <@user> <optinal reason>`", description="Allow's you to kick a user.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_utility.command(aliases=['ban'])
    async def ban2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}ban <@user> <optinal reason>`", description="Allow's you to ban a user.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_utility.command(aliases=['setup-logs'])
    async def setuplogs2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}setup-logs`", description="Create's a channel that the bot will put logs in.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_utility.command(aliases=['autorole'])
    async def autorole2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}autorole <user/bot> <@role>`", description="Set's autorole for users, or bots.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_utility.command(aliases=['autorole-disable'])
    async def autodisable2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}autorole-disable <user/bot>`", description="Disable's autorole for users, or bots.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_utility.command(aliases=['addrole'])
    async def addrole2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}addrole <@user> <@role>`", description="Give's a user a role.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_utility.command(aliases=['removerole'])
    async def removerole2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}removerole <@user> <@role>`", description="Remove's a role from a user.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_utility.command(aliases=['role'])
    async def role2(self, ctx):
        embed=discord.Embed(title=f"Usage:\n`{ctx.prefix}role <all/removeall> <@role>`\n`{ctx.prefix}role <allhumans/removeallhumans> <@role>`\n`{ctx.prefix}role <allbots/removeallbots> <@role>`", description="Allow's you to give everyone a role, or remove one.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_utility.command(aliases=['nick'])
    async def nick2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}nick <'name'> <@optinal user>`", description="Nicknames you, or another user. If your nickname has spaces in it you need to put quotes around it.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_utility.command(aliases=['nickreset'])
    async def nickreset2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}nickreset <@optinal user>`", description="Resets your nickname, or another users nickname.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_utility.command(aliases=['nickall'])
    async def nickall2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}nickall <name>`", description="Give's everyone a nickname you choose.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_utility.command(aliases=['nickresetall'])
    async def nickresetall2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}nickresetall`", description="Reset's everyone's nickname.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_utility.command(aliases=['info'])
    async def info2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}info <optinal @user>`", description="See your or someone else's info.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_utility.command(aliases=['serverinfo'])
    async def serverinfo2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}serverinfo <optional 'server id'>`", description="See the current server info, or another guilds info.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_utility.command(aliases=['avatar'])
    async def avatar2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}avatar <optional @user>`", description="Show's you your avatar or someone else's avatar.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.group(name="music")
    async def _music(self, ctx):
        if ctx.invoked_subcommand is None:

            author = ctx.message.author

            embed=discord.Embed(title="Music commands!", description=f"{ctx.prefix}music `<command name>` - Use this to get help with certain commands.\n\n`{ctx.prefix}play`, `{ctx.prefix}skip`, `{ctx.prefix}pause`, `{ctx.prefix}resume`, `{ctx.prefix}queue`, `{ctx.prefix}now`, `{ctx.prefix}volume`, `{ctx.prefix}stop`, `{ctx.prefix}summon`, `{ctx.prefix}join`, `{ctx.prefix}leave`", color=0x8b0000, timestamp=ctx.message.created_at)

            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

            await ctx.send(embed=embed)

    @_music.command(aliases=['play'])
    async def play2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}play <keyterm/url>`", description="Make's the bot play a song.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_music.command(aliases=['skip'])
    async def skip2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}skip`", description="Skip's the current song playing.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_music.command(aliases=['pause'])
    async def pause2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}pause`", description="Pause's the current song playing.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_music.command(aliases=['resume'])
    async def resume2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}resume`", description="Resume's the song that was paused.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_music.command(aliases=['queue'])
    async def queue2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}queue <page #>`", description="Show's what's currently in queue.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_music.command(aliases=['now'])
    async def now2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}now`", description="Show's what's currently playing.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_music.command(aliases=['volume'])
    async def volume2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}volume <number 1-100>`", description="Allow's you to change how loud the bot is.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_music.command(aliases=['stop'])
    async def stop2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}stop`", description="Stop's the bot from playing music, and clears the queue.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_music.command(aliases=['summon'])
    async def summon2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}summon`", description="Summons the bot to the channel that you are currently in.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_music.command(aliases=['join'])
    async def join2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}join <channel>`", description="Makes the bot join a channel that you specify.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    @_music.command(aliases=['leave'])
    async def leave2(self, ctx):
        embed=discord.Embed(title=f"Usage: `{ctx.prefix}leave`", description="Make's the bot leave the channel that you are currently in.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


    @commands.group(name="other")
    async def _other(self, ctx):
        if ctx.invoked_subcommand is None:
            author = ctx.message.author

            embed=discord.Embed(title="Some extra commands!", description=f"{ctx.prefix}other `<command name>` - Use this to get help with certain commands.\n\nCurrently no commands.", color=0x8b0000, timestamp=ctx.message.created_at)

            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

            await ctx.send(embed=embed)

    @commands.command()
    async def economy(self, ctx):
        author = ctx.message.author

        embed=discord.Embed(title="Economy commands!", description="Economy commands so you can play with fake money.", color=0x8b0000, timestamp=ctx.message.created_at)

        embed.add_field(name="Job commands‏‏‎", value=f"`{ctx.prefix}jobs` - Show's all current jobs that you have available.\n`{ctx.prefix}job` - Show's your current job.\n`{ctx.prefix}job register <job name>` - Allow's you to register for any of the jobs you currently have available.\n`{ctx.prefix}job change <job name>` - Allow'ss you to change to another job.\n`{ctx.prefix}work` - Allow's you to work for the job you currently have.", inline=False)

        embed.add_field(name="Bank commands‏‏‎", value=f"`{ctx.prefix}balance` - Show's how much money you have.\n`{ctx.prefix}transfer <@user> <amount>` - Allow's you to give people money.", inline=False)

        embed.add_field(name="Make money commands‏‏‎", value=f"`{ctx.prefix}beg` - Make's you beg for money.\n`{ctx.prefix}rob <@user>` - Make's you rob somebody.\n`{ctx.prefix}slot <amount>` - You gamble in this gamemode, so much fun.\n`{ctx.prefix}payouts` - Allow's you to see what kind of money you can make from playing slot.\n`{ctx.prefix}payday <@user> <amount>` - Allow's you to get free money for the day.\n`{ctx.prefix}payweek <@user> <amount>` - Allow's you to get free money for the week.", inline=False)

        embed.add_field(name="Shop commands‏‏‎", value=f"`{ctx.prefix}shop <page#>` - Allow's you to see all items you can buy.\n`{ctx.prefix}buy <item>` - Allow's you to buy the item you choose from the shop.\n`{ctx.prefix}use <item>` - Allow's you to use the item you chose.\n", inline=False)

        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(help(client))
