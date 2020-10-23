import io
import discord
import asyncio
import os
import random
from collections import deque, Counter
from discord import Embed, Color, HTTPException
from discord.utils import get
from collections import deque
from datetime import datetime
from discord.ext import commands
# import discord is not necessary unless you are using it inside the code

class actions(commands.Cog):
    # The constructor method
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def hug(self, ctx, *, member: discord.Member=None):
            author = ctx.message.author
            responses = ["https://media.discordyui.net/reactions/hug/S5rnKCF.gif",
                    "https://media.discordyui.net/reactions/hug/WgdUyyJ.gif",
                    "https://media.discordyui.net/reactions/hug/kpMgkn1.gif",
                    "https://media.discordyui.net/reactions/hug/6bJxUOb.gif",
                    "https://media.discordyui.net/reactions/hug/vcQm1YL.gif",
                    "https://media.discordyui.net/reactions/hug/JwU3EPy.gif",
                    "https://media.discordyui.net/reactions/hug/6bJxUOb.gif",
                    "https://media.discordyui.net/reactions/hug/fP0FnXi.gif",
                    "https://media.discordyui.net/reactions/hug/f4BRs7v.gif"]
            hugs = random.choice(responses)
            if author == member:
                    embed=discord.Embed(title="They do huggin themselves!", description="**{0}** hugs themselves...".format(author.mention), color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_image(url="{}".format(hugs))
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
            if not member:
               embed=discord.Embed(title="You didn't ping anyone?", description="Ping someone you dummy.", color=0x8b0000, timestamp=ctx.message.created_at)
               embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
               await ctx.send(embed=embed)
            else:
               embed=discord.Embed(title="They do be huggin!", description="**{0}** hugs **{1}**".format(author.mention, member.mention), color=0x8b0000, timestamp=ctx.message.created_at)
               embed.set_image(url="{}".format(hugs))
               embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
               await ctx.send(embed=embed)

    @commands.command()
    async def slap(self, ctx, *, member: discord.Member=None):
            author = ctx.message.author
            responses = ["https://media.discordyui.net/reactions/slap/6ySfvg5.gif",
                    "https://media.discordyui.net/reactions/slap/aVDQEfA.gif",
                    "https://media.discordyui.net/reactions/slap/HGxqG1N.gif",
                    "https://media.discordyui.net/reactions/slap/4CZe0Jb.gif",
                    "https://media.discordyui.net/reactions/slap/32TM2xW.gif",
                    "https://media.discordyui.net/reactions/slap/RJHjyv3.gif",
                    "https://media.discordyui.net/reactions/slap/6QLFD1m.gif"]
            slaps = random.choice(responses)
            if author == member:
                    embed=discord.Embed(title="But why?", description="**{0}** slaps themselves...".format(author.mention), color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_image(url="{}".format(slaps))
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
            if not member:
               embed=discord.Embed(title="You didn't ping anyone?", description="Ping someone you dummy.", color=0x8b0000, timestamp=ctx.message.created_at)
               embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
               await ctx.send(embed=embed)
            else:
               embed=discord.Embed(title="That had to hurt.", description="**{0}** slaps **{1}**".format(author.mention, member.mention), color=0x8b0000, timestamp=ctx.message.created_at)
               embed.set_image(url="{}".format(slaps))
               embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
               await ctx.send(embed=embed)

    @commands.command()
    async def kiss(self, ctx, *, member: discord.Member=None):
            author = ctx.message.author
            responses = ["https://media.discordyui.net/reactions/kiss/cxl66EV.gif",
                    "https://media.discordyui.net/reactions/kiss/iJMycFA.gif",
                    "https://media.discordyui.net/reactions/kiss/a2qzZ7w.gif",
                    "https://media.discordyui.net/reactions/kiss/0J0d9WU.gif",
                    "https://media.discordyui.net/reactions/kiss/IaHHwD7.gif",
                    "https://media.discordyui.net/reactions/kiss/Xrxhow8.gif",
                    "https://media.discordyui.net/reactions/kiss/yL5qOOP.gif"]
            kisses = random.choice(responses)
            if author == member:
                    embed=discord.Embed(title="It's not that sweet.", description="**{0}** kisses themselves...".format(author.mention), color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_image(url="{}".format(kisses))
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
            if not member:
               embed=discord.Embed(title="You didn't ping anyone?", description="Ping someone you dummy.", color=0x8b0000, timestamp=ctx.message.created_at)
               embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
               await ctx.send(embed=embed)
            else:
               embed=discord.Embed(title="Isn't that sweet.", description="**{0}** kisses **{1}**".format(author.mention, member.mention), color=0x8b0000, timestamp=ctx.message.created_at)
               embed.set_image(url="{}".format(kisses))
               embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
               await ctx.send(embed=embed)


def setup(client):
    client.add_cog(actions(client))
