import io
import discord
import asyncio
import os
import json
from typing import Union
from .utils.dataIO import fileIO
from discord.utils import find
from collections import deque, Counter
from discord import Embed, Color, HTTPException
from discord.utils import get
from collections import deque
from datetime import datetime
from discord.ext import commands
# import discord is not necessary unless you are using it inside the code

class MemberNotFound(Exception):
    pass

async def resolve_member(guild, member_id):
    member = guild.get_member(member_id)
    if member is None:
        if guild.chunked:
            raise MemberNotFound()
        try:
            member = await guild.fetch_member(member_id)
        except discord.NotFound:
            raise MemberNotFound() from None
    return member

class MemberID(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            m = await commands.MemberConverter().convert(ctx, argument)
        except commands.BadArgument:
            try:
                member_id = int(argument, base=10)
                m = await resolve_member(ctx.guild, member_id)
            except ValueError:
                raise commands.BadArgument(f"{argument} is not a valid member or member ID.") from None
            except MemberNotFound:
                # hackban case
                return type('_Hackban', (), {'id': member_id, '__str__': lambda s: f'<@{s.id}>'})()

        if not can_execute_action(ctx, ctx.author, m):
            raise commands.BadArgument('You cannot do this action on this user due to role hierarchy.')
        return m

class FetchedUser(commands.Converter):
    async def convert(self, ctx, argument):
        if not argument.isdigit():
            return await ctx.send('Wrong ID.')
        try:
            return await ctx.bot.fetch_user(argument)
        except discord.NotFound:
            return  await ctx.send('User is not found.')
        except discord.HTTPException:
            return await ctx.send('An error has occurred, try again.')

class utilitys(commands.Cog):
    # The constructor method
    def __init__(self, client):
        self.client = client
        self.roles = fileIO("data/roles/roles.json", "load")
        self.botroles = fileIO("data/roles/botroles.json", "load")
        self.prefixe = fileIO("data/utility/prefix/prefix.json", "load")



    def role_get(client, message):
        with open('data/roles/roles.json', 'r') as f:
            try:
                roles = json.load(f)

                return roles[str(message.guild.id)]
            except:
                pass

    def botrole_get(client, message):
        with open('data/roles/botroles.json', 'r') as f:
            try:
                botroles = json.load(f)

                return botroles[str(message.guild.id)]
            except:
                pass

    @commands.command()
    async def info(self, ctx, member : Union[discord.Member, FetchedUser]= None):
        member = ctx.author if not member else member

        embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at)

        embed.set_author(name=f"User Info - {member}")
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        embed.add_field(name="ID:", value=member.id)
        try:
            embed.add_field(name="Server name:", value=member.display_name)
        except:
            pass

        embed.add_field(name="Created at:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        try:
            roles = [role for role in member.roles]
            embed.add_field(name="Joined at:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

            embed.add_field(name=f"Roles({len(roles)})", value=" ".join([role.mention for role in roles]))
            embed.add_field(name="Top role:", value=member.top_role.mention)
        except:
            pass

        embed.add_field(name="Bot?", value=member.bot)

        await ctx.send(embed=embed)

    @commands.command(aliases=['guildinfo'], usage='')
    @commands.guild_only()
    async def serverinfo(self, ctx, *, guild_id: int = None):
        """Shows info about the current server."""

        if guild_id is not None and await self.client.is_owner(ctx.author):
            guild = self.client.get_guild(guild_id)
            if guild is None:
                return await ctx.send(f'Invalid Guild ID given.')
        else:
            guild = ctx.guild

        roles = [role.name.replace('@', '@\u200b') for role in guild.roles]

        # we're going to duck type our way here
        class Secret:
            pass

        secret_member = Secret()
        secret_member.id = 0
        secret_member.roles = [guild.default_role]

        # figure out what channels are 'secret'
        secret = Counter()
        totals = Counter()
        for channel in guild.channels:
            perms = channel.permissions_for(secret_member)
            channel_type = type(channel)
            totals[channel_type] += 1
            if not perms.read_messages:
                secret[channel_type] += 1
            elif isinstance(channel, discord.VoiceChannel) and (not perms.connect or not perms.speak):
                secret[channel_type] += 1

        member_by_status = Counter(str(m.status) for m in guild.members)

        e = discord.Embed(color=0x8b0000)
        e.title = guild.name
        e.add_field(name='ID', value=guild.id)
        e.add_field(name='Owner', value=guild.owner)
        if guild.icon:
            e.set_thumbnail(url=guild.icon_url)

        channel_info = []
        key_to_emoji = {
            discord.TextChannel: '<:channel:765967557274239007>',
            discord.VoiceChannel: '<:voice:765967566983135234>',
        }
        for key, total in totals.items():
            secrets = secret[key]
            try:
                emoji = key_to_emoji[key]
            except KeyError:
                continue

            if secrets:
                channel_info.append(f'{emoji} {total} ({secrets} locked)')
            else:
                channel_info.append(f'{emoji} {total}')

        e.add_field(name='Channels', value='\n'.join(channel_info))

        bot_count = len(([member for member in guild.members if member.bot]))

        fmt = f'<:online:765967576245207078> {member_by_status["online"]} ' \
              f'<:idle:765967585421688842> {member_by_status["idle"]} ' \
              f'<:dnd:765967594766336020> {member_by_status["dnd"]} ' \
              f'<:offline:765967602534187039> {member_by_status["offline"]}\n' \
              f'Total: {guild.member_count} ({bot_count} bots)'

        e.add_field(name='Members', value=fmt)

        # TODO: maybe chunk and stuff for top role members
        # requires max-concurrency d.py check to work though.
        e.add_field(name='Roles', value=', '.join(roles) if len(roles) < 10 else f'{len(roles)} roles')
        e.add_field(name="Region", value=guild.region)
        e.add_field(name="Verification", value=guild.verification_level)
        e.set_footer(text='Guild Created At').timestamp = guild.created_at
        await ctx.send(embed=e)

    @commands.command(aliases=['av'])
    async def avatar(self, ctx, member : Union[discord.Member, FetchedUser]= None):
        member = ctx.author if not member else member
        embed=discord.Embed(title=f"{member}", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_image(url=f"{member.avatar_url}")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['purge'])
    async def clear(self, ctx, amount = 0):
        if ctx.message.author.guild_permissions.manage_messages or ctx.message.author.id == 740253555658719344:
            if not ctx.guild.me.guild_permissions.manage_messages:
                embed=discord.Embed(title="Permission Denied.", description="I don't have permission to use this command. I am missing the `manage messages permission`.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            if amount is 0:
                embed=discord.Embed(title="No amount?", description="You didn't specify an amount, please do that.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            await ctx.channel.purge(limit = amount + 1)
        else:
            embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command. You are missing the `manage message` permission.", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    @commands.command(pass_context = True)
    async def mute(self, ctx, member: discord.Member=None, amount=None, *, reason=None):
        guild = ctx.guild
        channel = get(guild.text_channels, name="logs")
        author = ctx.message.author
        if ctx.message.author.guild_permissions.kick_members or ctx.message.author.id == 740253555658719344:
            if not ctx.guild.me.guild_permissions.manage_roles:
                embed=discord.Embed(title="Permission Denied.", description="I don't have permission to use this command. I am missing the `manage roles permission`.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            if member == ctx.author:
                embed=discord.Embed(title="Mute yourself????", description="Are you dumb or something, cause like you can't mute yourself.".format(member, ctx.message.author), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            if member == None:
                embed=discord.Embed(title="No user?", description="Please specify a member!", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            if ctx.author.top_role < member.top_role:
                embed=discord.Embed(title="You can't do that.", description="You can't mute {0} because they're a higher role than you.".format(member.mention), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            role = discord.utils.get(member.guild.roles, name='Muted')
            if role in member.roles:
                embed=discord.Embed(title="Already muted?", description="**{0}** is already muted!".format(member.mention), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            if amount is None:
                role = discord.utils.get(member.guild.roles, name='Muted')
                await member.add_roles(role)
                embed4=discord.Embed(title="User Muted!", description="**{0}** was muted by **{1}** for **forever**!".format(member.mention, ctx.message.author.mention), color=0x8b0000, timestamp=ctx.message.created_at)
                embed4.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed4)
                return
            if reason:
                if len(reason) > 512:
                    embed=discord.Embed(title="Too Long.", description="Reason too long, try something shorter.", color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                Amo,unt=amount[:-1]if amount is not None else 10, amount
                embed2=discord.Embed(title="Invalid time.", description="The unit \"{0}\" on the amount \"{1}\" is invalid, use unit from `s, m, h, d, y`.".format(amount[-1], unt), color=0x8b0000, timestamp=ctx.message.created_at)
                embed2.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                if amount[-1] == 's': amount, long=int(amount[:-1]), "second" if int(amount[:-1])<=1 else "seconds"
                elif amount[-1] == 'm': amount, long=int(amount[:-1]) * 60, "minute" if int(amount[:-1])<=1 else "minutes"
                elif amount[-1] == 'h': amount, long=int(amount[:-1]) * 60 * 60, "hour" if int(amount[:-1])<=1 else "hours"
                elif amount[-1] == 'd': amount, long=int(amount[:-1]) * 86400, "day" if int(amount[:-1])<=1 else "days"
                elif amount[-1] == 'y': amount, long=int(amount[:-1]) * 31536000, "year" if int(amount[:-1])<=1 else "years"
                else: return await ctx.send(embed=embed2)
                role = discord.utils.get(member.guild.roles, name='Muted')
                await member.add_roles(role)
                embed=discord.Embed(title="User Muted!", description="**{0}** was muted by **{1}** for **{2} {3}** with the reason **{4}**!".format(member.mention, ctx.message.author.mention, Amo, long, reason), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                try:
                    if channel == None:
                        await asyncio.sleep(amount)
                        if role not in member.roles:
                            return
                        await member.remove_roles(role)
                        return
                    if channel and role in member.roles:
                        await asyncio.sleep(amount)
                        if role not in member.roles:
                            return
                        await member.remove_roles(role)
                        embed=discord.Embed(title="User UnMuted!", description=f"{member.mention} was auto unmuted, because their time has expired.", color=0x8b0000, timestamp=ctx.message.created_at)
                        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                        await channel.send(embed=embed)
                        return
                except:pass
                return
            if reason == None:
                Amo,unt=amount[:-1]if amount is not None else 10, amount
                embed2=discord.Embed(title="Invalid time.", description="The unit \"{0}\" on the amount \"{1}\" is invalid, use unit from `s, m, h, d, y`.".format(amount[-1], unt), color=0x8b0000, timestamp=ctx.message.created_at)
                embed2.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                if amount[-1] == 's': amount, long=int(amount[:-1]), "second" if int(amount[:-1])<=1 else "seconds"
                elif amount[-1] == 'm': amount, long=int(amount[:-1]) * 60, "minute" if int(amount[:-1])<=1 else "minutes"
                elif amount[-1] == 'h': amount, long=int(amount[:-1]) * 60 * 60, "hour" if int(amount[:-1])<=1 else "hours"
                elif amount[-1] == 'd': amount, long=int(amount[:-1]) * 86400, "day" if int(amount[:-1])<=1 else "days"
                elif amount[-1] == 'y': amount, long=int(amount[:-1]) * 31536000, "year" if int(amount[:-1])<=1 else "years"
                else: return await ctx.send(embed=embed2)
                role = discord.utils.get(member.guild.roles, name='Muted')
                await member.add_roles(role)
                embed=discord.Embed(title="User Muted!", description="**{0}** was muted by **{1}** for **{2} {3}**!".format(member.mention, ctx.message.author.mention, Amo, long, reason), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                try:
                    if channel == None:
                        await asyncio.sleep(amount)
                        if role not in member.roles:
                            return
                        await member.remove_roles(role)
                        return
                    if channel and role in member.roles:
                        await asyncio.sleep(amount)
                        if role not in member.roles:
                            return
                        await member.remove_roles(role)
                        embed=discord.Embed(title="User UnMuted!", description=f"{member.mention} was auto unmuted, because their time has expired.", color=0x8b0000, timestamp=ctx.message.created_at)
                        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                        await channel.send(embed=embed)
                        return
                except:pass
        else:
            embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command. You are missing the `kick permission`.", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    @commands.command(pass_context = True)
    async def unmute(self, ctx, member: discord.Member=None):
        if ctx.message.author.guild_permissions.kick_members or ctx.message.author.id == 740253555658719344:
            if not ctx.guild.me.guild_permissions.manage_roles:
                embed=discord.Embed(title="Permission Denied.", description="I don't have permission to use this command. I am missing the `manage roles permission`.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            if member == None:
                embed=discord.Embed(title="No user?", description="Please specify a member!".format(member, ctx.message.author), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            role = discord.utils.get(member.guild.roles, name='Muted')
            if role not in member.roles:
                embed=discord.Embed(title="Isn't muted?", description="**{0}** isn't muted!".format(member.mention), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            role = discord.utils.get(member.guild.roles, name='Muted')
            await member.remove_roles(role)
            embed=discord.Embed(title="User UnMuted!", description="**{0}** was unmuted by **{1}**!".format(member.mention, ctx.message.author.mention), color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command. You are missing the `kick permission`.", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    @commands.command(pass_context = True)
    async def ban(self, ctx, member : Union[discord.Member, MemberID]=None, *, reason=None):
        if ctx.message.author.guild_permissions.ban_members or ctx.message.author.id == 740253555658719344:
            if not ctx.guild.me.guild_permissions.ban_members:
                embed=discord.Embed(title="Permission Denied.", description="I don't have permission to use this command. I am missing the `ban permission`.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            if member == ctx.author:
                embed=discord.Embed(title="Ban yourself????", description="Are you dumb or something, cause like you can't ban yourself.".format(member, ctx.message.author), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            if member == None:
                embed=discord.Embed(title="No user?", description="Please specify a member!".format(member, ctx.message.author), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            try:
                if ctx.author.top_role == member.top_role:
                    embed=discord.Embed(title="You can't do that.", description="You can't ban {0} because you have the same top role as them.".format(member.mention), color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                if ctx.author.top_role < member.top_role:
                    embed=discord.Embed(title="You can't do that.", description="You can't ban {0} because they're a higher role than you.".format(member.mention), color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
            except:
                pass
            try:
                if reason == None:
                    embed2=discord.Embed(title="You have been banned!", description="You were banned by **{0}** in the guild **{1}**!".format(ctx.message.author.mention, ctx.guild), color=0x8b0000, timestamp=ctx.message.created_at)
                    embed2.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    try:
                        await member.send(embed=embed2)
                        await member.ban(reason="no reason at all")
                    except:
                        pass
                    await ctx.guild.ban(member, reason="no reason at all")
                    embed=discord.Embed(title="User banned!", description="**<@{0}>** was banned by **{1}**!".format(member.id, ctx.message.author.mention, reason), color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
            except discord.Forbidden:
                embed=discord.Embed(title="Forbidden!", description="I do not have permission's to do this, please move my higher role above this member.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            if len(reason) > 512:
                embed=discord.Embed(title="Too Long.", description="Reason too long, try something shorter.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            else:
                embed2=discord.Embed(title="You have been banned!", description="You were banned by **{0}** in the guild **{1}** for the reason **{2}**!".format(ctx.message.author.mention, ctx.guild, reason), color=0x8b0000, timestamp=ctx.message.created_at)
                embed2.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                try:
                    await member.send(embed=embed2)
                    await member.ban(reason=reason)
                except:
                    pass
                await ctx.guild.ban(member, reason=reason)
                embed=discord.Embed(title="User banned!", description="**<@{0}>** was banned by **{1}** with the reason **{2}**!".format(member.id, ctx.message.author.mention, reason), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command. You are missing the `ban permission`.", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    @commands.command(pass_context = True)
    async def kick(self, ctx, member: discord.Member=None, *, reason=None):
        if ctx.message.author.guild_permissions.kick_members or ctx.message.author.id == 740253555658719344:
            if not ctx.guild.me.guild_permissions.kick_members:
                embed=discord.Embed(title="Permission Denied.", description="I don't have permission to use this command. I am missing the `kick permission`.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            if member == ctx.author:
                embed=discord.Embed(title="kick yourself????", description="Are you dumb or something, cause like you can't kick yourself.".format(member, ctx.message.author), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            if not member:
                embed=discord.Embed(title="No user?", description="Please specify a member!".format(member, ctx.message.author), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            if ctx.author.top_role == member.top_role:
                embed=discord.Embed(title="You can't do that.", description="You can't kick {0} because you have the same top role as them.".format(member.mention), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            if ctx.author.top_role < member.top_role:
                embed=discord.Embed(title="You can't do that.", description="You can't kick {0} because they're a higher role than you.".format(member.mention), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            try:
                if reason == None:
                    embed2=discord.Embed(title="You have been kicked!", description="You were kicked by **{0}** in the guild **{1}**!".format(ctx.message.author.mention, ctx.guild), color=0x8b0000, timestamp=ctx.message.created_at)
                    embed2.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    try:
                        await member.send(embed=embed2)
                    except:
                        pass
                    await member.kick(reason="no reason at all")
                    embed=discord.Embed(title="User kicked!", description="**{0}** was kicked by **{1}**!".format(member.mention, ctx.message.author.mention, reason), color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
            except discord.Forbidden:
                embed=discord.Embed(title="Forbidden!", description="I do not have permission's to do this, please move my higher role above this member.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            if len(reason) > 512:
                embed=discord.Embed(title="Too Long.", description="Reason too long, try something shorter.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            if reason:
                embed2=discord.Embed(title="You have been kicked!", description="You were kicked by **{0}** in the guild **{1}** for the reason **{2}**!".format(ctx.message.author.mention, ctx.guild, reason), color=0x8b0000, timestamp=ctx.message.created_at)
                embed2.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                try:
                    await member.send(embed=embed2)
                except:
                    pass
                await member.kick(reason=reason)
                embed=discord.Embed(title="User kicked!", description="**{0}** was kicked by **{1}** with the reason **{2}**!".format(member.mention, ctx.message.author.mention, reason), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command. You are missing the `kick permission`.", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    @commands.command(aliases=['setup-logs'])
    async def _setup(self, ctx):
        if ctx.message.author.guild_permissions.manage_channels:
            if not ctx.guild.me.guild_permissions.manage_channels:
                embed=discord.Embed(title="Permission Denied.", description="I don't have permission to use this command. I am missing the `manage channels permission`.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            guild = ctx.message.guild
            overwrites = {
                        guild.default_role: discord.PermissionOverwrite(read_messages=False),
                        guild.me: discord.PermissionOverwrite(read_messages=True),
                        guild.me: discord.PermissionOverwrite(send_messages=True)
                        }
            await guild.create_text_channel('logs', overwrites=overwrites)
            embed=discord.Embed(title="Logs created!", description="The channel logs has been created, you may move it to wherever you want. Make sure I get to keep permission's to it.", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command. You are missing the `manage channels permission`.", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    @commands.command()
    async def role(self, ctx,  var=None, *, role: discord.Role=None):
        guild = ctx.guild
        members = guild.members
        if ctx.message.author.guild_permissions.manage_roles:
            if not ctx.guild.me.guild_permissions.manage_roles:
                embed=discord.Embed(title="Permission Denied.", description="I don't have permission to use this command. I am missing the `manage roles permission`.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            if var == None:
                embed=discord.Embed(title="Nothing givin.", description="Please use, `all, removeall, allhumans, removeallhumans, allbots, and removeallbots` instead.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            if var != "all" and var != "removeall" and var != "allhumans" and var != "removeallhumans" and var != "allbots" and var != "removeallbots":
                embed=discord.Embed(title="Incorrect Value.", description="Please use, `all, removeall, allhumans, removeallhumans, allbots, and removeallbots` instead.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
        else:
            embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command. You are missing the `manage roles` permission.", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        if var == "all":
            if ctx.message.author.guild_permissions.manage_roles:
                if not ctx.guild.me.guild_permissions.manage_roles:
                    embed=discord.Embed(title="Permission Denied.", description="I don't have permission to use this command. I am missing the `manage roles permission`.", color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                if role is None:
                    embed=discord.Embed(title="No role?", description="You didn't put a role, dummy head.".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                if ctx.author.top_role < role:
                    embed=discord.Embed(title="You can't do that.", description="I'm sorry but i'm afriad I can't give every human the role `{0}`, your top role is lower than that role, try getting someone to move you higher.".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                if ctx.guild.me.top_role < role:
                    embed=discord.Embed(title="Not allowed.", description="Sadly I can't give everyone this role, because it is higher than mine, if you wish to use this role put mine above this one.".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                embed=discord.Embed(title="Adding Roles.", description="Giving everyone the role, `{0}`, this may take awhile.".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                count = 0
                for member in members:
                    try:
                        await member.add_roles(role, reason="role all")
                    except discord.HTTPException:
                        pass
                    else:
                        count += 1
                embed=discord.Embed(title="Completed!", description="Finished adding the role `{0}` to everyone.".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command. You are missing the `manage roles` permission.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
        if var == "removeall":
            if ctx.message.author.guild_permissions.manage_roles:
                if not ctx.guild.me.guild_permissions.manage_roles:
                    embed=discord.Embed(title="Permission Denied.", description="I don't have permission to use this command. I am missing the `manage roles permission`.", color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                if role is None:
                    embed=discord.Embed(title="No role?", description="You didn't put a role, dummy head.".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                if ctx.author.top_role < role:
                        embed=discord.Embed(title="You can't do that.", description="I'm sorry but i'm afriad I can't remove the role `{0}` from everyone, your top role is lower than that role, try getting someone to move you higher.".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
                        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                        await ctx.send(embed=embed)
                        return
                if ctx.guild.me.top_role < role:
                    embed=discord.Embed(title="Not allowed.", description="Sadly I can't remove this role from everyone, because it is higher than mine, if you wish to remove this role put mine above that one.".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                embed=discord.Embed(title="Removing Roles.", description="Removing the role, `{0}` from everyone, this may take awhile".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                count = 0
                for member in members:
                    try:
                        await member.remove_roles(role, reason="role all")
                    except discord.HTTPException:
                        pass
                    else:
                        count += 1
                embed=discord.Embed(title="Completed!", description="Finished removing the role `{0}` from everyone.".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command. You are missing the `manage roles` permission.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
        if var == "allhumans":
            if ctx.message.author.guild_permissions.manage_roles:
                if not ctx.guild.me.guild_permissions.manage_roles:
                    embed=discord.Embed(title="Permission Denied.", description="I don't have permission to use this command. I am missing the `manage roles permission`.", color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                if role is None:
                    embed=discord.Embed(title="No role?", description="You didn't put a role, dummy head.".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                if ctx.author.top_role < role:
                    embed=discord.Embed(title="You can't do that.", description="I'm sorry but i'm afriad I can't give every human the role `{0}`, your top role is lower than that role, try getting someone to move you higher.".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                if ctx.guild.me.top_role < role:
                    embed=discord.Embed(title="Not allowed.", description="Sadly I can't add this role to everyone, because it is higher than mine, if you wish to remove this role put mine above that one.".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                embed=discord.Embed(title="Adding Roles.", description="Adding the role, `{0}` to all humans, this may take awhile".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                count = 0
                for member in members:
                    try:
                        if member.bot == True:
                            pass
                        else:
                            await member.add_roles(role, reason="role all humans")
                    except discord.HTTPException:
                        pass
                    else:
                        count += 1
                embed=discord.Embed(title="Completed!", description="Finished adding the role `{0}` to all humans.".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command. You are missing the `manage roles` permission.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
        if var == "removeallhumans":
            if ctx.message.author.guild_permissions.manage_roles:
                if not ctx.guild.me.guild_permissions.manage_roles:
                    embed=discord.Embed(title="Permission Denied.", description="I don't have permission to use this command. I am missing the `manage roles permission`.", color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                if role is None:
                    embed=discord.Embed(title="No role?", description="You didn't put a role, dummy head.".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                if ctx.author.top_role < role:
                        embed=discord.Embed(title="You can't do that.", description="I'm sorry but i'm afriad I can't remove the role `{0}` from every human, your top role is lower than that role, try getting someone to move you higher.".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
                        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                        await ctx.send(embed=embed)
                        return
                if ctx.guild.me.top_role < role:
                    embed=discord.Embed(title="Not allowed.", description="Sadly I can't remove this role from everyone, because it is higher than mine, if you wish to remove this role put mine above that one.".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                embed=discord.Embed(title="Removing Roles.", description="Removing the role, `{0}` from all humans, this may take awhile".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                count = 0
                for member in members:
                    try:
                        if member.bot == True:
                            pass
                        else:
                            await member.remove_roles(role, reason="role remove all humans")
                    except discord.HTTPException:
                        pass
                    else:
                        count += 1
                embed=discord.Embed(title="Completed!", description="Finished removing the role `{0}` from all humans.".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command. You are missing the `manage roles` permission.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
        if var == "allbots":
            if ctx.message.author.guild_permissions.manage_roles:
                if not ctx.guild.me.guild_permissions.manage_roles:
                    embed=discord.Embed(title="Permission Denied.", description="I don't have permission to use this command. I am missing the `manage roles permission`.", color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                if role is None:
                    embed=discord.Embed(title="No role?", description="You didn't put a role, dummy head.".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                if ctx.author.top_role < role:
                    embed=discord.Embed(title="You can't do that.", description="I'm sorry but i'm afriad I can't give every bot the role `{0}`, your top role is lower than that role, try getting someone to move you higher.".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                if ctx.guild.me.top_role < role:
                    embed=discord.Embed(title="Not allowed.", description="Sadly I can't add this role to everyone, because it is higher than mine, if you wish to remove this role put mine above that one.".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                embed=discord.Embed(title="Adding Roles.", description="Adding the role, `{0}` to all bots, this may take awhile".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                count = 0
                for member in members:
                    try:
                        if member.bot == False:
                            pass
                        else:
                            await member.add_roles(role, reason="role all bots")
                    except discord.HTTPException:
                        pass
                    else:
                        count += 1
                embed=discord.Embed(title="Completed!", description="Finished adding the role `{0}` to all bots.".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command. You are missing the `manage roles` permission.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
        if var == "removeallbots":
            if ctx.message.author.guild_permissions.manage_roles:
                if not ctx.guild.me.guild_permissions.manage_roles:
                    embed=discord.Embed(title="Permission Denied.", description="I don't have permission to use this command. I am missing the `manage roles permission`.", color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                if role is None:
                    embed=discord.Embed(title="No role?", description="You didn't put a role, dummy head.".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                if ctx.author.top_role < role:
                    embed=discord.Embed(title="You can't do that.", description="I'm sorry but i'm afriad I can't remove the role `{0}` from every bot, your top role is lower than that role, try getting someone to move you higher.".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                if ctx.guild.me.top_role < role:
                    embed=discord.Embed(title="Not allowed.", description="Sadly I can't remove this role from everyone, because it is higher than mine, if you wish to remove this role put mine above that one.".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                embed=discord.Embed(title="Removing Roles.", description="Removing the role, `{0}` from all bots, this may take awhile".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                count = 0
                for member in members:
                    try:
                        if member.bot == False:
                            pass
                        else:
                            await member.remove_roles(role, reason="role remove all bots")
                    except discord.HTTPException:
                        pass
                    else:
                        count += 1
                embed=discord.Embed(title="Completed!", description="Finished removing the role `{0}` from all bots.".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command. You are missing the `manage roles` permission.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)

    @commands.command()
    async def addrole(self, ctx, member: discord.Member=None, *, role: discord.Role=None):
        guild = ctx.guild
        bot = discord.utils.get(guild.roles, name="biteki")
        if ctx.message.author.guild_permissions.manage_roles:
            if not ctx.guild.me.guild_permissions.manage_roles:
                embed=discord.Embed(title="Permission Denied.", description="I don't have permission to use this command. I am missing the `manage roles permission`.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            if not member:
                embed=discord.Embed(title="No user?", description="Please specify a member!".format(member, ctx.message.author), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            if role is None:
                embed=discord.Embed(title="No role?", description="You didn't put a role, dummy head.".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            if member == ctx.message.author and role in ctx.author.roles:
                embed=discord.Embed(title="Already has role?", description="You already have the role `{0}`.".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            if role in member.roles:
                embed=discord.Embed(title="Already has role?", description="{0} already has the role `{1}`.".format(member.mention, role), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            if ctx.author.top_role < role:
                embed=discord.Embed(title="You can't do that.", description="I'm sorry but i'm afriad I can't give **{0}** the role `{1}`, your top role is lower than that role, try getting someone to move you higher.".format(member.mention, role), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            if ctx.guild.me.top_role < role:
                embed=discord.Embed(title="Not allowed.", description="Sadly I can't give the role `{0}` to **{1}**, because it is higher than mine, if you wish to use this role put mine above this one.".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            try:
                await member.add_roles(role, reason="add role")
                embed=discord.Embed(title="Adding Role.", description="Giving **{0}** the role, `{1}`.".format(member.mention, role), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            except discord.HTTPException:
                embed=discord.Embed(title="I can't do that.", description="I'm sorry but i'm afriad I can't give **{0}** the role `{1}`, try checking my permissions, an then do it again.".format(member.mention, role), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command. You are missing the `manage roles` permission.", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    @commands.command()
    async def removerole(self, ctx, member: discord.Member=None, *, role: discord.Role=None):
        guild = ctx.guild
        bot = discord.utils.get(guild.roles, name="biteki")
        if ctx.message.author.guild_permissions.manage_roles:
            if not ctx.guild.me.guild_permissions.manage_roles:
                embed=discord.Embed(title="Permission Denied.", description="I don't have permission to use this command. I am missing the `manage roles permission`.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            if not member:
                embed=discord.Embed(title="No user?", description="Please specify a member!".format(member, ctx.message.author), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            if role is None:
                embed=discord.Embed(title="No role?", description="You didn't put a role, dummy head.".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            if member == ctx.message.author and role not in ctx.author.roles:
                embed=discord.Embed(title="Doesn't have role?", description="You don't have the role `{0}`.".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            if role not in member.roles:
                embed=discord.Embed(title="Doesn't have role?", description="{0} doesn't have the role `{1}`.".format(member.mention, role), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            if ctx.author.top_role == role:
                embed=discord.Embed(title="You can't do that.", description="I'm sorry but i'm afriad I can't remove the role `{0}` from **{1}**, your top role is equal to the role you tried removing.".format(role, member.mention), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            if ctx.author.top_role < role:
                embed=discord.Embed(title="You can't do that.", description="I'm sorry but i'm afriad I can't remove the role `{0}` from **{1}**, your top role is lower than that one, try getting someone to move you higher.".format(role, member.mention), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            if ctx.guild.me.top_role < role:
                embed=discord.Embed(title="Not allowed.", description="Sadly I can't remove the role `{0}` from **{1}**, because it is higher than mine, if you wish to use this role put mine above this one.".format(role, member.mention), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            try:
                await member.remove_roles(role, reason="remove role")
                embed=discord.Embed(title="Removing Role.", description="Removing the role `{0}` from **{1}**.".format(role, member.mention), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            except discord.HTTPException:
                embed=discord.Embed(title="I can't do that.", description="I'm sorry but i'm afriad I can't remove the role `{0}` remove **{1}**, try checking my permissions, an then do it again.".format(role, member.mention), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command. You are missing the `manage roles` permission.", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)


    @commands.command()
    async def nick(self, ctx, nick=None, member: discord.Member=None):
        author = ctx.message.author
        if not member:
            if ctx.message.author.guild_permissions.change_nickname:
                if not ctx.guild.me.guild_permissions.manage_nicknames:
                    embed=discord.Embed(title="Permission Denied.", description="I don't have permission to use this command. I am missing the `manage nicknames permission`.", color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                if nick == None:
                    embed=discord.Embed(title="No name?", description="You didn't put a nickname, you dummy head.", color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                if ctx.guild.me.top_role < author.top_role:
                    embed=discord.Embed(title="Not allowed.", description="Sadly I can't nickname you because you're a higher role than me.".format(member.mention), color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                if len(nick) > 32:
                    embed=discord.Embed(title="Too Long.", description="Nickname is too long, try something shorter.", color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                if nick:
                    embed=discord.Embed(title="Setting nickname.", description=f"Changing your nickname({ctx.message.author.mention}) to the nickname `{nick}`.", color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    await ctx.message.author.edit(nick=nick)
                    return
            else:
                embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command. You are missing the `change nickname` permission.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
        if member:
            if ctx.message.author.guild_permissions.manage_nicknames:
                if not ctx.guild.me.guild_permissions.manage_nicknames:
                    embed=discord.Embed(title="Permission Denied.", description="I don't have permission to use this command. I am missing the `manage nicknames permission`.", color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                if nick == None:
                    embed=discord.Embed(title="No name?", description="You didn't put a nickname, you dummy head.", color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                if ctx.guild.me.top_role < member.top_role:
                    embed=discord.Embed(title="Not allowed.", description="Sadly I can't nickname {0} because they are a higher role than me.".format(member.mention), color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                if ctx.author.top_role < member.top_role:
                    embed=discord.Embed(title="You can't do that.", description="You can't nickname {0} because they're a higher role than you.".format(member.mention), color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                if len(nick) > 32:
                    embed=discord.Embed(title="Too Long.", description="Nickname is too long, try something shorter.", color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                if nick:
                    embed=discord.Embed(title="Setting nickname.", description=f"Changing {member.mention} nickname to `{nick}`.", color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    await member.edit(nick=nick)
            else:
                embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command. You are missing the `manage nicknames` permission.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)

    @commands.command()
    async def resetnick(self, ctx, member: discord.Member=None):
        if not member:
            if ctx.message.author.guild_permissions.change_nickname:
                if not ctx.guild.me.guild_permissions.manage_nicknames:
                    embed=discord.Embed(title="Permission Denied.", description="I don't have permission to use this command. I am missing the `manage nicknames permission`.", color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                if ctx.guild.me.top_role < author.top_role:
                    embed=discord.Embed(title="Not allowed.", description="Sadly I can't nickname you because you're a higher role than me.".format(member.mention), color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                embed=discord.Embed(title="ReSetting nickname.", description=f"ReSetting your nickname.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                await ctx.message.author.edit(nick=ctx.message.author.name)
            else:
                embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command. You are missing the `change nickname` permission.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
        if member:
            if ctx.message.author.guild_permissions.manage_nicknames:
                if not ctx.guild.me.guild_permissions.manage_nicknames:
                    embed=discord.Embed(title="Permission Denied.", description="I don't have permission to use this command. I am missing the `manage nicknames permission`.", color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                if ctx.guild.me.top_role < member.top_role:
                    embed=discord.Embed(title="Not allowed.", description="Sadly I can't nickname {0} because they are a higher role than me.".format(member.mention), color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                if ctx.author.top_role < member.top_role:
                    embed=discord.Embed(title="You can't do that.", description="You can't reset {0} nickanme because they're a higher role than you.".format(member.mention), color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                embed=discord.Embed(title="ReSetting nickname.", description=f"ReSetting {member.mention}'s nickname.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                await member.edit(nick=member.name)
            else:
                embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command. You are missing the `manage nicknames` permission.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)

    @commands.command()
    async def nickall(self, ctx, *, nick=None):
        guild = ctx.guild
        members = guild.members
        if ctx.message.author.guild_permissions.manage_guild:
            if not ctx.guild.me.guild_permissions.manage_nicknames:
                embed=discord.Embed(title="Permission Denied.", description="I don't have permission to use this command. I am missing the `manage nicknames permission`.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            if nick == None:
                embed=discord.Embed(title="No name?", description="You didn't put a nickname, you dummy head.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            if len(nick) > 32:
                embed=discord.Embed(title="Too Long.", description="Nickname is too long, try something shorter.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            embed=discord.Embed(title="Setting nicknames.", description=f"Changing everyone's nickname to `{nick}`, This might take awhile.", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            count = 0
            for member in members:
                try:
                    await member.edit(nick=nick)
                except discord.HTTPException:
                    pass
                else:
                    count += 1
        else:
            embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command. You are missing the `manage server` permission.", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    @commands.command()
    async def nickresetall(self, ctx):
        guild = ctx.guild
        members = guild.members
        if ctx.message.author.guild_permissions.manage_guild:
            if not ctx.guild.me.guild_permissions.manage_nicknames:
                embed=discord.Embed(title="Permission Denied.", description="I don't have permission to use this command. I am missing the `manage nicknames permission`.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            embed=discord.Embed(title="ReSetting nicknames.", description=f"ReSetting everyone's nicknames.", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            count = 0
            for member in members:
                try:
                    await member.edit(nick=member.name)
                except discord.HTTPException:
                    pass
                else:
                    count += 1
        else:
            embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command. You are missing the `manage server` permission.", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        role = discord.utils.get(channel.guild.roles, name='Muted')
        await channel.set_permissions(role, send_messages=False,
                                            add_reactions=False,
                                            speak=False)

    @commands.command()
    async def update_mute(self, ctx):
        guild = ctx.guild
        reason = "Auto perms update"
        role = discord.utils.get(guild.roles, name='Muted')
        for channel in guild.channels:
            perms = channel.permissions_for(guild.me)
            if perms.manage_roles:
                overwrite = channel.overwrites_for(role)
                overwrite.send_messages = False
                overwrite.add_reactions = False
                overwrite.speak = False
                try:
                    await channel.set_permissions(role, overwrite=overwrite, reason=reason)
                except:
                    pass

    @commands.command()
    async def autorole(self, ctx, var=None, *, role: discord.Role=None):
        guild = ctx.guild
        bot = discord.utils.get(guild.roles, name="biteki")
        if ctx.message.author.guild_permissions.manage_roles:
            if not ctx.guild.me.guild_permissions.manage_roles:
                embed=discord.Embed(title="Permission Denied.", description="I don't have permission to use this command. I am missing the `manage roles permission`.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            if var == None:
                embed=discord.Embed(title="Nothing givin.", description="Please use, `user, and bot` instead.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            if var != "user" and var != "bot":
                embed=discord.Embed(title="Incorrect Value.", description="Please use, `user, and bot` instead.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
        else:
            embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command. You are missing the `manage roles` permission.", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        if var == "user":
            if ctx.message.author.guild_permissions.manage_roles:
                if not ctx.guild.me.guild_permissions.manage_roles:
                    embed=discord.Embed(title="Permission Denied.", description="I don't have permission to use this command. I am missing the `manage roles permission`.", color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                if role is None:
                    embed=discord.Embed(title="No role?", description="You didn't put a role, dummy head.".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                if ctx.author.top_role < role:
                    embed=discord.Embed(title="You can't do that.", description="You can't set this role because it is a higher role than your current role.", color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                if ctx.guild.me.top_role < role:
                    embed=discord.Embed(title="Not allowed.", description="Sadly I can't set this role, because it is higher than mine, if you wish to use this role put mine above this one.".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                with open('data/roles/roles.json', 'r') as f:
                    roles = json.load(f)

                    roles[str(ctx.guild.id)] = f"{role}"

                    self.roles = roles

                with open('data/roles/roles.json', 'w') as f:
                    json.dump(roles, f, indent=4)

                embed=discord.Embed(title="Autorole set", description="Role set too `{0}`.".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command. You are missing the `manage roles` permission.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
        if var == "bot":
            if ctx.message.author.guild_permissions.manage_roles:
                if not ctx.guild.me.guild_permissions.manage_roles:
                    embed=discord.Embed(title="Permission Denied.", description="I don't have permission to use this command. I am missing the `manage roles permission`.", color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                if role is None:
                    embed=discord.Embed(title="No role?", description="You didn't put a role, dummy head.".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                if ctx.author.top_role < role:
                    embed=discord.Embed(title="You can't do that.", description="You can't set this role because it is a higher role than your current role.", color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                if ctx.guild.me.top_role < role:
                    embed=discord.Embed(title="Not allowed.", description="Sadly I can't set this role, because it is higher than mine, if you wish to use this role put mine above this one.".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                with open('data/roles/botroles.json', 'r') as f:
                    botroles = json.load(f)

                    botroles[str(ctx.guild.id)] = f"{role}"

                    self.botroles = botroles

                with open('data/roles/botroles.json', 'w') as f:
                    json.dump(botroles, f, indent=4)

                embed=discord.Embed(title="Autorole set", description="Role set too `{0}`, for bots.".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command. You are missing the `manage roles` permission.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)


    @commands.command(aliases=['autorole-disable'])
    async def _autorole2(self, ctx, var=None):
        if ctx.message.author.guild_permissions.manage_roles:
            if not ctx.guild.me.guild_permissions.manage_roles:
                embed=discord.Embed(title="Permission Denied.", description="I don't have permission to use this command. I am missing the `manage roles permission`.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            if var == None:
                embed=discord.Embed(title="Nothing givin.", description="Please use, `user, and bot` instead.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            if var != "user" and var != "bot":
                embed=discord.Embed(title="Incorrect Value.", description="Please use, `user, and bot` instead.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
        else:
            embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command. You are missing the `manage roles` permission.", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        if var == "user":
            if ctx.message.author.guild_permissions.manage_roles:
                if not ctx.guild.me.guild_permissions.manage_roles:
                    embed=discord.Embed(title="Permission Denied.", description="I don't have permission to use this command. I am missing the `manage roles permission`.", color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                with open('data/roles/roles.json', 'r') as f:
                    roles = json.load(f)

                    roles.pop(str(ctx.guild.id))

                    self.roles = roles


                with open('data/roles/roles.json', 'w') as f:
                    json.dump(roles, f, indent=4)

                embed=discord.Embed(title="Autorole disabled", description="Autorole has been disabled, to re enabled just use the autorole command again, along with your role.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command. You are missing the `manage roles` permission.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
        if var == "bot":
            if ctx.message.author.guild_permissions.manage_roles:
                if not ctx.guild.me.guild_permissions.manage_roles:
                    embed=discord.Embed(title="Permission Denied.", description="I don't have permission to use this command. I am missing the `manage roles permission`.", color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
                with open('data/roles/botroles.json', 'r') as f:
                    botroles = json.load(f)

                    botroles.pop(str(ctx.guild.id))

                    self.botroles = botroles

                with open('data/roles/botroles.json', 'w') as f:
                    json.dump(botroles, f, indent=4)

                embed=discord.Embed(title="Autorole disabled", description="Autorole has been disabled, to re enabled just use the autorole command again, along with your role.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command. You are missing the `manage roles` permission.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
            await guild.create_role(name='Muted')
            await guild.create_role(name='DJ')
            general = find(lambda x: x.name == 'general',  guild.text_channels)
            if general and general.permissions_for(guild.me).send_messages:
                    embed=discord.Embed(title="Hello there!", description="Hey, thanks for adding me to your server, if you need any help use $help. That will you give you a list of commands you can preform, and once again thank you, for adding me!!", color=0x8b0000)
                    await general.send(embed=embed)
            for channel in guild.channels:
                reason = "Auto perms update"
                role = discord.utils.get(guild.roles, name='Muted')
                perms = channel.permissions_for(guild.me)
                if perms.manage_roles:
                    overwrite = channel.overwrites_for(role)
                    overwrite.send_messages = False
                    overwrite.add_reactions = False
                    overwrite.speak = False
                    try:
                        await channel.set_permissions(role, overwrite=overwrite, reason=reason)
                    except:
                        pass

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        guild_id = str(guild.id)
        if guild_id in self.roles.keys():
            try:
                with open('data/roles/roles.json', 'r') as f:
                    roles = json.load(f)

                    roles.pop(str(guild.id))

                    self.roles = roles


                with open('data/roles/roles.json', 'w') as f:
                    json.dump(roles, f, indent=4)
            except:
                pass
        if guild_id in self.roles.keys():
            try:
                with open('data/roles/botroles.json', 'r') as f:
                    botroles = json.load(f)

                    botroles.pop(str(guild.id))

                    self.botroles = botroles

                with open('data/roles/botroles.json', 'w') as f:
                    json.dump(botroles, f, indent=4)
            except:
                pass

    @commands.Cog.listener()
    async def on_member_join(self, member):
        role3 = self.botrole_get(member)
        role4 = discord.utils.get(member.guild.roles, name = role3)
        role2 = self.role_get(member)
        role = discord.utils.get(member.guild.roles, name = role2)
        if member.bot == True:
            try:
                await member.add_roles(role4, reason="bot autorole")
            except:
                pass
        if member.bot == False:
            try:
                await member.add_roles(role, reason="autorole")
            except:
                pass

    @commands.Cog.listener()
    async def on_message(self, message):
        guild_id = str(message.guild.id)
        if guild_id in self.prefixe.keys():
            return
        if guild_id not in self.prefixe.keys():
            with open('data/utility/prefix/prefix.json', 'r') as f:
                prefixes = json.load(f)

                prefixes[str(message.guild.id)] = '$'
            with open('data/utility/prefix/prefix.json', 'w') as f:
                json.dump(prefixes, f, indent=4)

    #@commands.command()
    #async def warn(self, ctx, member: discord.Member, reason=None):
    #    if ctx.message.author.guild_permissions.kick_members:
    #        with open('warns.json', 'r') as f:
    #            warns = json.load(f)
    #            warns[ctx.guild.id] = {}
    #            warns[ctx.guild.id][member.id] = {}
    #            warns[ctx.guild.id]["reason"] = f"{reason}"
    #
    #        with open('warns.json', 'w') as f:
    #            json.dump(warns, f, indent=4)
    #        await ctx.send("Done")

def setup(client):
    client.add_cog(utilitys(client))
