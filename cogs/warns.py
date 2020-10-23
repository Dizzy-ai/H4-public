import discord
from discord.ext import commands
import json
import atexit
import uuid


warns = {}

try:
    with open("data/utility/warn/warns.json") as file:
        warns = json.load(file)
except (FileNotFoundError, json.JSONDecodeError) as ex:
    with open("data/warn/warns.json", "w") as file:
        json.dump({}, file)


@atexit.register
def store_warns():
    with open("data/utility/warn/warns.json", "w") as file:
        json.dump(warns, file)


class Warnnings(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.has_permissions(manage_channels=True)
    @commands.command()
    async def warntestidkyet(
        self, ctx, emote, role: discord.Role, channel: discord.TextChannel, title, *, message,
    ):
        embed = discord.Embed(title=title, description=message)
        msg = await channel.send(embed=embed)
        await msg.add_reaction(emote)
        self.add_reaction(ctx.guild.id, emote, role.id, channel.id, msg.id)

    @commands.has_permissions(manage_channels=True)
    @commands.command()
    async def warn(
        self, ctx, member: discord.Member, *, reason = None
    ):
        self.add_warn(ctx.guild.id, member.id, reason)
        await ctx.send("Done.")

    @commands.has_permissions(manage_channels=True)
    @commands.command()
    async def warns(self, ctx, member: discord.Member):
        member = ctx.author if not member else member
        guild_id = str(ctx.guild.id)
        member_id = str(member.id)
        data = f"{warns[guild_id][member_id]}"
        embed = discord.Embed(title=f"Warns - {member}")
        if data is None:
            embed.description = "There are no warns for this user."
        else:
            for index, rr in enumerate(warns[guild_id][member_id]):
                reason = rr.get("reason")
                embed.add_field(name=index, value=f"{reason}", inline=False)
        await ctx.send(embed=embed)

    @commands.has_permissions(manage_channels=True)
    @commands.command()
    async def warn_remove(self, ctx, index: int):
        guild_id = ctx.guild.id
        data = warns.get(str(guild_id), None)
        embed = discord.Embed(title=f"Remove Reaction Role {index}")
        rr = None
        if data is None:
            embed.description = "Given Reaction Role was not found."
        else:
            embed.description = (
                "Do you wish to remove the reaction role below? Please react with 🗑️."
            )
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
                value=f"{emote} - @{role} - [message](https://www.discordapp.com/channels/{guild_id}/{channel_id}/{message_id})",
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
            warns[str(guild_id)] = data
            store_warns()

    def add_warn(self, guild_id, member, reason):
        if not str(guild_id) in warns:
            warns[str(guild_id)] = []
        warns[str(guild_id)].append(
            {
                str(member): str(member),
                "reason": reason,
                "id": str(uuid.uuid4())
            }
        )
        store_warns()


def setup(client):
    client.add_cog(Warnnings(client))
