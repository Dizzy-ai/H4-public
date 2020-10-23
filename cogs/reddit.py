import asyncio
import praw
import discord
import random
from discord.ext import commands


class reddit(commands.Cog):
    # The constructor method
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
    async def meme(self, ctx):
        reddit = praw.Reddit(client_id='agYWlvIPuzdLfQ',
                             client_secret='cvGBAczkf706jqIjtUyQGI2j0So',
                             user_agent='u/mrbutter1234567')
        memes_submissions = reddit.subreddit('memes').hot()
        post_to_pick = random.randint(1, 50)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)
        embed=discord.Embed(title="Its the funny me me", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_image(url="{}".format(submission.url))
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
    async def dankmeme(self, ctx):
        reddit = praw.Reddit(client_id='agYWlvIPuzdLfQ',
                             client_secret='cvGBAczkf706jqIjtUyQGI2j0So',
                             user_agent='u/mrbutter1234567')
        dankmemes_submissions = reddit.subreddit('dankmemes').hot()
        post_to_pick = random.randint(1, 50)
        for i in range(0, post_to_pick):
            submission = next(x for x in dankmemes_submissions if not x.stickied)
        embed=discord.Embed(title="Its the dank me me", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_image(url="{}".format(submission.url))
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
    async def cursedcomments(self, ctx):
        reddit = praw.Reddit(client_id='agYWlvIPuzdLfQ',
                             client_secret='cvGBAczkf706jqIjtUyQGI2j0So',
                             user_agent='u/mrbutter1234567')
        cursedcomments_submissions = reddit.subreddit('cursedcomments').hot()
        post_to_pick = random.randint(1, 50)
        for i in range(0, post_to_pick):
            submission = next(x for x in cursedcomments_submissions if not x.stickied)
        embed=discord.Embed(title="Thats pretty cursed, maybe.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_image(url="{}".format(submission.url))
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
    async def blacktwitter(self, ctx):
        reddit = praw.Reddit(client_id='agYWlvIPuzdLfQ',
                             client_secret='cvGBAczkf706jqIjtUyQGI2j0So',
                             user_agent='u/mrbutter1234567')
        blacktwitterpics_submissions = reddit.subreddit('blacktwitterpics').hot()
        post_to_pick = random.randint(1, 50)
        for i in range(0, post_to_pick):
            submission = next(x for x in blacktwitterpics_submissions if not x.stickied)
        embed=discord.Embed(title="black twitter, its black I know.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_image(url="{}".format(submission.url))
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
    async def cat(self, ctx):
        reddit = praw.Reddit(client_id='agYWlvIPuzdLfQ',
                             client_secret='cvGBAczkf706jqIjtUyQGI2j0So',
                             user_agent='u/mrbutter1234567')
        cats_submissions = reddit.subreddit('cats').hot()
        post_to_pick = random.randint(1, 50)
        for i in range(0, post_to_pick):
            submission = next(x for x in cats_submissions if not x.stickied)
        embed=discord.Embed(title="Here is a random cat", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_image(url="{}".format(submission.url))
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
    async def dog(self, ctx):
        reddit = praw.Reddit(client_id='agYWlvIPuzdLfQ',
                             client_secret='cvGBAczkf706jqIjtUyQGI2j0So',
                             user_agent='u/mrbutter1234567')
        lookatmydog_submissions = reddit.subreddit('lookatmydog').hot()
        post_to_pick = random.randint(1, 50)
        for i in range(0, post_to_pick):
            submission = next(x for x in lookatmydog_submissions if not x.stickied)
        embed=discord.Embed(title="Here is a random dog", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_image(url="{}".format(submission.url))
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
    async def animal(self, ctx):
        reddit = praw.Reddit(client_id='agYWlvIPuzdLfQ',
                             client_secret='cvGBAczkf706jqIjtUyQGI2j0So',
                             user_agent='u/mrbutter1234567')
        aww_submissions = reddit.subreddit('aww').hot()
        post_to_pick = random.randint(1, 50)
        for i in range(0, post_to_pick):
            submission = next(x for x in aww_submissions if not x.stickied)
        embed=discord.Embed(title="An random animal, thing.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_image(url="{}".format(submission.url))
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
    async def snake(self, ctx):
        reddit = praw.Reddit(client_id='agYWlvIPuzdLfQ',
                             client_secret='cvGBAczkf706jqIjtUyQGI2j0So',
                             user_agent='u/mrbutter1234567')
        snakes_submissions = reddit.subreddit('snakes').hot()
        post_to_pick = random.randint(1, 50)
        for i in range(0, post_to_pick):
            submission = next(x for x in snakes_submissions if not x.stickied)
        embed=discord.Embed(title="Here is an random snake.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_image(url="{}".format(submission.url))
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
    async def lizard(self, ctx):
        reddit = praw.Reddit(client_id='agYWlvIPuzdLfQ',
                             client_secret='cvGBAczkf706jqIjtUyQGI2j0So',
                             user_agent='u/mrbutter1234567')
        BeardedDragons_submissions = reddit.subreddit('BeardedDragons').hot()
        post_to_pick = random.randint(1, 50)
        for i in range(0, post_to_pick):
            submission = next(x for x in BeardedDragons_submissions if not x.stickied)
        embed=discord.Embed(title="Here is an random lizard.", color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_image(url="{}".format(submission.url))
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
    async def nsfw2(self, ctx):
        reddit = praw.Reddit(client_id='agYWlvIPuzdLfQ',
                             client_secret='cvGBAczkf706jqIjtUyQGI2j0So',
                             user_agent='u/mrbutter1234567')
        nsfw = ctx.channel.is_nsfw()
        nsfw2_submissions = reddit.subreddit('nsfw2').hot()
        post_to_pick = random.randint(1, 50)
        for i in range(0, post_to_pick):
            submission = next(x for x in nsfw2_submissions if not x.stickied)
        if nsfw:
            embed=discord.Embed(title="That's uh a nsfw photo.", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_image(url="{}".format(submission.url))
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        else:
            embed=discord.Embed(title="No nsfw here.", description="Looks like this channel isn't labeled as nsfw, so I can't post it.", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
    async def boobs(self, ctx):
        reddit = praw.Reddit(client_id='agYWlvIPuzdLfQ',
                             client_secret='cvGBAczkf706jqIjtUyQGI2j0So',
                             user_agent='u/mrbutter1234567')
        nsfw = ctx.channel.is_nsfw()
        boobs_submissions = reddit.subreddit('boobs').hot()
        post_to_pick = random.randint(1, 50)
        for i in range(0, post_to_pick):
            submission = next(x for x in boobs_submissions if not x.stickied)
        if nsfw:
            embed=discord.Embed(title="Here's some tittes.", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_image(url="{}".format(submission.url))
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        else:
            embed=discord.Embed(title="No nsfw here.", description="Looks like this channel isn't labeled as nsfw, so I can't post it.", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
    async def ass(self, ctx):
        reddit = praw.Reddit(client_id='agYWlvIPuzdLfQ',
                             client_secret='cvGBAczkf706jqIjtUyQGI2j0So',
                             user_agent='u/mrbutter1234567')
        nsfw = ctx.channel.is_nsfw()
        ass_submissions = reddit.subreddit('ass').hot()
        post_to_pick = random.randint(1, 50)
        for i in range(0, post_to_pick):
            submission = next(x for x in ass_submissions if not x.stickied)
        if nsfw:
            embed=discord.Embed(title="Here's some ass.", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_image(url="{}".format(submission.url))
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        else:
            embed=discord.Embed(title="No nsfw here.", description="Looks like this channel isn't labeled as nsfw, so I can't post it.", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
    async def pussy(self, ctx):
        reddit = praw.Reddit(client_id='agYWlvIPuzdLfQ',
                             client_secret='cvGBAczkf706jqIjtUyQGI2j0So',
                             user_agent='u/mrbutter1234567')
        nsfw = ctx.channel.is_nsfw()
        vagina_submissions = reddit.subreddit('vagina').hot()
        post_to_pick = random.randint(1, 50)
        for i in range(0, post_to_pick):
            submission = next(x for x in vagina_submissions if not x.stickied)
        if nsfw:
            embed=discord.Embed(title="Here's some pussy.", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_image(url="{}".format(submission.url))
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        else:
            embed=discord.Embed(title="No nsfw here.", description="Looks like this channel isn't labeled as nsfw, so I can't post it.", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(reddit(client))
