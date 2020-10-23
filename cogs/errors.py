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

class errors(commands.Cog):
    # The constructor method
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed=discord.Embed(title="Cool down!", description=f"Try again in **{round(error.retry_after)} seconds**.", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        if isinstance(error, commands.CommandNotFound):
            embed=discord.Embed(title="Not a command?", description=f"That command is not a command.", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        if isinstance(error, commands.BadArgument):
            embed=discord.Embed(title="Bad Argument!", description="You may have used an inncorrect argument, try a real `member`, `role`, or `channel`.", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        if isinstance(error, commands.MissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            embed=discord.Embed(title="Permission Denied.", description=f"You don't have permission to use this command. You are missing the `{fmt}` permission.", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        else:
            raise error


def setup(client):
    client.add_cog(errors(client))
