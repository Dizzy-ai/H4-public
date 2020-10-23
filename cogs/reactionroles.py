import discord
import asyncio
from discord.ext import commands
import json
import atexit
import uuid


reaction_roles_data = {}

try:
    with open("data/utility/reaction_roles/reaction_roles.json") as file:
        reaction_roles_data = json.load(file)
except (FileNotFoundError, json.JSONDecodeError) as ex:
    with open("data/reaction_roles/reaction_roles.json", "w") as file:
        json.dump({}, file)


@atexit.register
def store_reaction_roles():
    with open("data/utility/reaction_roles/reaction_roles.json", "w") as file:
        json.dump(reaction_roles_data, file)


class ReactionRoles(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        role, user = self.parse_reaction_payload(payload)
        if role is not None and user is not None and user.bot == False:
            await user.add_roles(role, reason="ReactionRole")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        role, user = self.parse_reaction_payload(payload)
        if role is not None and user is not None and user.bot == False:
            await user.remove_roles(role, reason="ReactionRole")

    @commands.has_permissions(manage_channels=True)
    @commands.command()
    async def emreaction(self, ctx, emote=None, role: discord.Role=None, channel: discord.TextChannel=None, title=None, *, message=None):
        if not ctx.guild.me.guild_permissions.administrator:
            embed=discord.Embed(title="Permission Denied.", description="I don't have permission to use this command. I am missing the `administrator permission`.", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        if not emote:
            embed=discord.Embed(title="No emote?", description="Please put a emote!", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        if not role:
            embed=discord.Embed(title="No role?", description="Please put a role!", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        if ctx.author.top_role < role:
            embed=discord.Embed(title="You can't do that.", description=f"Your role is lower than the role you tried to set for the reaction role, try to get someone to move you above {role.mention}.".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        if ctx.guild.me.top_role < role:
            embed=discord.Embed(title="Not allowed.", description=f"My role is lower than the role you tried to set for the reaction role, try moving me above {role.mention}.".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        if not channel:
            embed=discord.Embed(title="No channel?", description="Please put a channel!", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        if not title:
            embed=discord.Embed(title="No title?", description="Please put a title!", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        if not message:
            embed=discord.Embed(title="No message?", description="Please put a message!", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        embed = discord.Embed(title=title, description=message)
        msg = await channel.send(embed=embed)
        await msg.add_reaction(emote)
        self.add_reaction(ctx.guild.id, emote, role.id, channel.id, msg.id)
        embed=discord.Embed(title="Emote added!", description=f"{emote} - {role.mention} - [message](https://www.discordapp.com/channels/{ctx.guild.id}/{channel.id}/{msg.id})\nIf this is wrong you can always remove it!", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        msg2 = await ctx.send(embed=embed)
        await asyncio.sleep(5)
        await msg2.delete()

    @commands.has_permissions(manage_channels=True)
    @commands.command()
    async def reaction_add(self, ctx, emote=None, role: discord.Role=None, channel: discord.TextChannel=None, message_id: int=None):
        if not ctx.guild.me.guild_permissions.administrator:
            embed=discord.Embed(title="Permission Denied.", description="I don't have permission to use this command. I am missing the `administrator permission`.", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        if not emote:
            embed=discord.Embed(title="No emote?", description="Please put a emote!", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        if not role:
            embed=discord.Embed(title="No role?", description="Please put a role!", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        if ctx.author.top_role < role:
            embed=discord.Embed(title="You can't do that.", description=f"Your role is lower than the role you tried to set for the reaction role, try to get someone to move you above {role.mention}.".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        if ctx.guild.me.top_role < role:
            embed=discord.Embed(title="Not allowed.", description=f"My role is lower than the role you tried to set for the reaction role, try moving me above {role.mention}.".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        if not channel:
            embed=discord.Embed(title="No channel?", description="Please put a channel!", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        if not message_id:
            embed=discord.Embed(title="No message id?", description="Please put a message id!", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        message = await channel.fetch_message(message_id)
        await message.add_reaction(emote)
        self.add_reaction(ctx.guild.id, emote, role.id, channel.id, message_id)
        embed=discord.Embed(title="Emote added!", description=f"{emote} - {role.mention} - [message](https://www.discordapp.com/channels/{ctx.guild.id}/{channel.id}/{message_id})\nIf this is wrong you can always remove it!", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.has_permissions(manage_channels=True)
    @commands.command()
    async def reactions(self, ctx):
        guild_id = ctx.guild.id
        data = reaction_roles_data.get(str(guild_id), None)
        embed = discord.Embed(title="Reaction Roles")
        if data is None:
            embed.description = "There are no reaction roles set up right now."
            embed.color = 0x8b0000
        else:
            for index, rr in enumerate(data):
                emote = rr.get("emote")
                role_id = rr.get("roleID")
                role = ctx.guild.get_role(role_id)
                channel_id = rr.get("channelID")
                message_id = rr.get("messageID")
                embed.color = 0x8b0000
                embed.add_field(
                    name=index,
                    value=f"{emote} - {role.mention} - [message](https://www.discordapp.com/channels/{guild_id}/{channel_id}/{message_id})",
                    inline=False,
                )
        await ctx.send(embed=embed)

    @commands.has_permissions(manage_channels=True)
    @commands.command()
    async def reaction_remove(self, ctx, index: int):
        guild_id = ctx.guild.id
        data = reaction_roles_data.get(str(guild_id), None)
        embed = discord.Embed(title=f"Remove Reaction Role {index}")
        rr = None
        if data is None:
            embed.description = "Given Reaction Role was not found."
            embed.color = 0x8b0000
            return
        role_id = rr.get("roleID")
        role = ctx.guild.get_role(role_id)
        if ctx.author.top_role < role:
            embed=discord.Embed(title="You can't do that.", description=f"Your role is lower than the role you tried to remove for the reaction role, try to get someone to move you above {role.mention}.".format(role), color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        if data:
            embed.description = (
                "Do you wish to remove the reaction role below? Please react with 🗑️."
            )
            embed.color = 0x8b0000
            rr = data[index]
            emote = rr.get("emote")
            role_id = rr.get("roleID")
            role = ctx.guild.get_role(role_id)
            channel_id = rr.get("channelID")
            message_id = rr.get("messageID")
            _id = rr.get("id")
            embed.set_footer(text=_id)
            embed.add_field(
                name=index,
                value=f"{emote} - {role.mention} - [message](https://www.discordapp.com/channels/{guild_id}/{channel_id}/{message_id})",
                inline=False,
            )
        msg = await ctx.send(embed=embed)
        if rr is not None:
            await msg.add_reaction("🗑️")

            def check(reaction, user):
                return (
                    reaction.message.id == msg.id
                    and user == ctx.message.author
                    and str(reaction.emoji) == "🗑️"
                )

            reaction, user = await self.client.wait_for("reaction_add", check=check)
            data.remove(rr)
            reaction_roles_data[str(guild_id)] = data
            store_reaction_roles()

    def add_reaction(self, guild_id, emote, role_id, channel_id, message_id):
        if not str(guild_id) in reaction_roles_data:
            reaction_roles_data[str(guild_id)] = []
        reaction_roles_data[str(guild_id)].append(
            {
                "id": str(uuid.uuid4()),
                "emote": emote,
                "roleID": role_id,
                "channelID": channel_id,
                "messageID": message_id,
            }
        )
        store_reaction_roles()

    def parse_reaction_payload(self, payload: discord.RawReactionActionEvent):
        guild_id = payload.guild_id
        data = reaction_roles_data.get(str(guild_id), None)
        if data is not None:
            for rr in data:
                emote = rr.get("emote")
                if payload.message_id == rr.get("messageID"):
                    if payload.channel_id == rr.get("channelID"):
                        if str(payload.emoji) == emote:
                            guild = self.client.get_guild(guild_id)
                            role = guild.get_role(rr.get("roleID"))
                            user = guild.get_member(payload.user_id)
                            return role, user
        return None, None


def setup(client):
    client.add_cog(ReactionRoles(client))
