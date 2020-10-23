import discord, datetime, time
import praw
import os
import asyncio
from cogs.utils.dataIO import fileIO
import json
import random
import io
from discord.utils import find
from discord.ext import commands
from discord import Embed, Color, HTTPException
from discord.utils import get
from collections import deque, Counter
from datetime import datetime
from discord.ext import commands, tasks
from itertools import cycle

def prefix_get(client, message):
    with open('data/utility/prefix/prefix.json', 'r') as f:
        try:
            prefixes = json.load(f)

            return prefixes[str(message.guild.id)]
        except:
            pass

def get_prefix(client, message):

    prefixes = [f'{prefix_get}']

    return commands.when_mentioned_or(*prefixes)(client, message)

client = commands.Bot(command_prefix = prefix_get)

@client.event
async def on_ready():
    change_status.start()
    print('Ready to roll')

client.remove_command('help')

@tasks.loop(seconds=15)
async def change_status():
    await client.wait_until_ready()
    status = cycle([f"$help | {(str(len(set(client.get_all_members()))))} Members", f"$help | {(str(len(client.guilds)))} Guilds", f"{(str(len(set(client.get_all_members()))))} Members | {(str(len(client.guilds)))} Guilds"])
    while not client.is_closed():
        await client.change_presence(status=discord.Status.online, activity=discord.Game(next(status)))
        await asyncio.sleep(15)

#dev commands
@client.command()
async def load(ctx, extension):
    if ctx.message.author.id == 740253555658719344:
        client.load_extension(f'cogs.{extension}')
        embed=discord.Embed(title="Cog loaded.", description=f"The cog **{extension}** has been loaded, what more do you want.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="Bruh.", description="You can't do that.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

@client.command()
async def unload(ctx, extension):
    if ctx.message.author.id == 740253555658719344:
        client.unload_extension(f'cogs.{extension}')
        embed=discord.Embed(title="Cog unloaded.", description=f"The cog **{extension}** has been unloaded, what more do you want.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="Bruh.", description="You can't do that.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

@client.command()
async def reload(ctx, extension):
    if ctx.message.author.id == 740253555658719344:
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
        embed=discord.Embed(title="Cogs reloaded.", description=f"The cog **{extension}** is reloaded, what more do you want.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="Bruh.", description="You can't do that.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@client.command()
async def shutdown(ctx):
        if ctx.message.author.id == 740253555658719344:
                embed=discord.Embed(title="Shutting down.", description="Peace dummy.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                await ctx.bot.logout()
        else:
                embed=discord.Embed(title="Bruh.", description="You can't do that.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)

@client.command()
async def restart(ctx):
        if ctx.message.author.id == 740253555658719344:
                embed=discord.Embed(title="Restarting...", description="hol up im finna restart.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                try:
                    await bot.logout()
                except:
                    pass
                finally:
                    os.system("python3 slaytter.py")
        else:
            embed=discord.Embed(title="Bruh.", description="You can't do that.", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

@client.event
async def on_guild_join(guild):
    with open('data/utility/prefix/prefix.json', 'r') as f:
        prefixes = json.load(f)

        prefixes[str(guild.id)] = '$'

    with open('data/utility/prefix/prefix.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):
    with open('data/utility/prefix/prefix.json', 'r') as f:
        prefixes = json.load(f)

        prefixes.pop[str(guild.id)]

    with open('data/utility/prefix/prefix.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@commands.has_permissions(manage_guild=True)
@client.command()
async def changeprefix(ctx, prefix=None):
    guild = ctx.guild
    if not prefix:
        embed=discord.Embed(title="No prefix?", description=f"You didn't put a prefix.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        return
    if len(prefix) > 2:
        embed=discord.Embed(title="Too Long.", description="Prefix can only be 2 characters.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        return
    with open('data/utility/prefix/prefix.json', 'r') as f:
        prefixes = json.load(f)

        prefixes[str(guild.id)] = prefix

    with open('data/utility/prefix/prefix.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    embed=discord.Embed(title="Prefix changed!", description=f"Prefix has been set too `{prefix}`.", color=0x8b0000, timestamp=ctx.message.created_at)
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

client.run("")
