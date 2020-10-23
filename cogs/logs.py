import io
import discord
from discord import Embed, Color, HTTPException
from discord.utils import get
from collections import deque
from datetime import datetime
from discord.ext import commands
# import discord is not necessary unless you are using it inside the code

class logs(commands.Cog):
    # The constructor method
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.guild is None: return
        if message.author.bot: return
        channel = get(message.guild.text_channels, name="logs")
        if channel is None: return
        embed=Embed(color=0x8b0000, timestamp=datetime.utcnow(),
        description=f"**User: {message.author.mention}\nChannel: <#{message.channel.id}>**\n{message.content}", title="Message deleted")
        embed.set_footer(text=f"Author: {message.author.id} | Message ID: {message.id}")
        if message.attachments:
                attachment = message.attachments[0]
                img_bytes = io.BytesIO(await attachment.read(use_cached=True))
                file = discord.File(img_bytes, filename=attachment.filename)
                embed.set_image(url=f"attachments://{file}")
                await channel.send(embed=embed, file=file)
                return
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        if message_before.guild is None: return
        channel = get(message_before.guild.text_channels, name="logs")
        if channel is None:
            return
        if message_before.author.bot is True:
            return
        if message_before.content == message_after.content:
            return
        embed=Embed(title="Message edited", description=f"**User: {message_after.author.mention}\nChannel: <#{message_after.channel.id}>** [Jump to message]({message_after.jump_url})", color=0x8b0000, timestamp=datetime.utcnow())
        try:
            embed.add_field(name="Before", value=f"{message_before.content}", inline=False)
            embed.add_field(name="After", value=f"{message_after.content}")
            embed.set_footer(text=f"Author: {message_after.author.id}")
            await channel.send(embed=embed)
        except HTTPException:
            return

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        channel = get(role.guild.text_channels, name="logs")
        if channel is None:
            return
        async for entry in channel.guild.audit_logs(limit=1):
            role_creator = entry.user
        embed=Embed(description=f"**Role created by: {role_creator.mention}** **\nName:** {role.name}", color=0x8b0000, timestamp=datetime.utcnow(), title="Role Created")
        embed.set_footer(text=f"ROLE ID: {role.id}")
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        channel = get(role.guild.text_channels, name="logs")
        if channel is None:
            return
        async for entry in channel.guild.audit_logs(limit=1):
            role_creator = entry.user
        embed=Embed(description=f"**Role deleted by: {role_creator.mention}** **\nName:** {role.name}", color=0x8b0000, timestamp=datetime.utcnow(), title="Role Deleted")
        embed.set_footer(text=f"ROLE ID: {role.id}")
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_raw_bulk_message_delete(self, payload):
        guild = self.client.get_guild(payload.guild_id)
        channel = get(guild.text_channels, name="logs")
        purge_channel = self.client.get_channel(payload.channel_id)
        if channel is None:
            return
        e = Embed(description=f"**Purged {len(payload.message_ids)} messages{'s' if len(payload.message_ids) == 1 else ''} in {purge_channel.mention}**",
        color=0x8b0000, timestamp=datetime.utcnow(), title="Message's purged")
        await channel.send(embed=e)

    @commands.Cog.listener("on_member_update")
    async def nick_logs(self, member_before, member_after):
        if member_after.nick != member_before.nick:
            channel = get(member_before.guild.text_channels, name="logs")
            if channel is None:
                return
            e = Embed(description=f"**{member_after.mention} nickname changed**", color=0x8b0000, timestamp=datetime.utcnow())
            e.add_field(name="Before", value=member_before.nick if member_before.nick else member_before.name)
            e.add_field(name="After", value=member_after.nick, inline=False)
            e.set_footer(text=f"ID: {member_after.id}")
            await channel.send(embed=e)

    @commands.Cog.listener()
    async def on_guild_role_update(self, role_before, role_after):
        channel = get(role_before.guild.text_channels, name="logs")
        if channel is None:
            return
        e = Embed(title=f"Updated role the {role_before.name}", color=0x8b0000, timestamp=datetime.utcnow())
        perms = set(role_after.permissions) - set(role_before.permissions)
        e.set_footer(text=f"ID: {role_before.id}")
        if role_before.permissions == role_after.permissions:
            return
        if role_before.name != role_after.name:
            e.add_field(name="Changed Name", value=f"Changed name from {role_before.name} to {role_after.name}")
        for name, value in perms:
            e.add_field(name=f"{name}", value=f"Set {name} to {value}", inline=False)
        await channel.send(embed=e)

    @commands.Cog.listener("on_member_update")
    async def role_logs(self, member_before, member_after):
        channel = get(member_before.guild.text_channels, name="logs")
        if channel is None:
            return
        if member_before.roles != member_after.roles:
            new_role = set(member_after.roles) - set(member_before.roles)
            removed_role = set(member_before.roles) - set(member_after.roles)
            if new_role != set():
                for role in new_role:
                    e = Embed(description=f"Added roles to {member_before.name}", color=0x8b0000, timestamp=datetime.utcnow())
                    e.add_field(name=f"Added roles:", value=f"`{role.name}`")
                    e.set_footer(text=f"ID: {member_before.id}")
                    await channel.send(embed=e)
            if removed_role != set():
                for role in removed_role:
                    e = Embed(description=f"Removed roles from {member_before.name}", color=0x8b0000, timestamp=datetime.utcnow())
                    e.add_field(name=f"Removed roles:", value=f"`{role.name}`")
                    e.set_footer(text=f"ID: {member_before.id}")
                    await channel.send(embed=e)

def setup(client):
    client.add_cog(logs(client))
