import discord
import json
from discord.ext import commands
from .utils.dataIO import fileIO
from random import randint
from copy import deepcopy
import os
import random
import time
import logging


class Level(commands.Cog):
    """Level system"""

    def __init__(self, client):
        self.client = client
        self._cooldown = commands.CooldownMapping.from_cooldown(1.0, 15.0, commands.BucketType.user)
        self.bank = fileIO("data/economy/bank.json", "load")
        self.settings = fileIO("data/economy/settings.json", "load")
        self.jobs = fileIO("data/economy/jobs.json", "load")
        self.levels = fileIO("data/level/levels.json", "load")
        self.lvlmessage = fileIO("data/level/levelmessage.json", "load")

    def lvl_up(self, author_id):
        cur_xp = self.levels[author_id]["exp"]
        cur_lvl = self.levels[author_id]["level"]

        if cur_xp >= round((4 * (cur_lvl ** 3)) / 5):
            self.levels[author_id]["level"] += 1
            fileIO("data/level/levels.json", "save", self.levels)
            return True
        else:
            return False

    @commands.Cog.listener()
    async def on_message(self, message):
        author = message.author
        author_id = str(message.author.id)
        guild_id = str(message.guild.id)
        author = message.author
        _bucket = self._cooldown.get_bucket(message)
        _retry_after = _bucket.update_rate_limit()

        if message.author.bot:
            return

        if not author_id in self.levels:
            self.levels[author_id] = {"level" : 1, "exp" : 0}
            fileIO("data/level/levels.json", "save", self.levels)
            return

        if self.levels[author_id]["level"] >= int(100):
            return

        if _retry_after:
            return

        self.levels[author_id]["exp"] += 1
        fileIO("data/level/levels.json", "save", self.levels)

        if self.lvl_up(author_id):
            if guild_id in self.lvlmessage.keys():
                await message.channel.send(f"{message.author.mention} is now level {self.levels[author_id]['level']}")

    @commands.command(aliases=['lvl'])
    async def level(self, ctx, member: discord.Member=None):
        member = ctx.author if not member else member
        member_id = str(member.id)

        if not member_id in self.levels:
            await ctx.send("member doesn't have a level")
        else:
            embed=discord.Embed(color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_author(name=f"Level - {member}", icon_url=member.avatar_url)
            embed.add_field(name="Level", value=self.levels[member_id]['level'])
            embed.add_field(name="Exp", value=self.levels[member_id]['exp'])
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    @commands.command(aliases=['level-messages'])
    async def _enable(self, ctx, var=None):
        if var == None:
            embed=discord.Embed(title="Nothing givin.", description="Please use, `enable, and disable`.", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        if var != "enable" and var != "disable":
            embed=discord.Embed(title="Incorrect Value.", description="Please use, `enable, and disable` instead.", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        if var == "enable":
            if ctx.message.author.guild_permissions.manage_guild:
                with open('data/level/levelmessage.json', 'r') as f:
                    lvlmess = json.load(f)

                    lvlmess[str(ctx.guild.id)] = "enabled"

                    self.lvlmessage = lvlmess

                with open('data/level/levelmessage.json', 'w') as f:
                    json.dump(lvlmess, f, indent=4)

                embed=discord.Embed(title="Level message enabled", description="Level messages has been enabled in your server.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command. You are missing the `manage guild` permission.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
        if var == "disable":
            if ctx.message.author.guild_permissions.manage_guild:
                with open('data/level/levelmessage.json', 'r') as f:
                    lvlmess = json.load(f)

                    lvlmess.pop(str(ctx.guild.id))

                    self.lvlmessage = lvlmess

                with open('data/level/levelmessage.json', 'w') as f:
                    json.dump(lvlmess, f, indent=4)

                embed=discord.Embed(title="Level message disabled", description="Level messages has been disabled in your server.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command. You are missing the `manage server` permission.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Level(client))
