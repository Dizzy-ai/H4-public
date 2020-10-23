import io
import discord
import asyncio
import os
import json
import random
from .utils.dataIO import fileIO
from collections import deque, Counter
from discord import Embed, Color, HTTPException
from discord.utils import get
from collections import deque
from datetime import datetime
from discord.ext import commands
# import discord is not necessary unless you are using it inside the code

class fun(commands.Cog):
    # The constructor method
    def __init__(self, client):
        self.client = client
        self.sniped = fileIO("data/fun/sniped.json", "load")
        self.editsniped = fileIO("data/fun/editsniped.json", "load")

    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        author = str(message_after.author.id)
        channel_id = str(message_after.channel.id)
        content = message_before.content
        if not str(channel_id) in self.editsniped:
            self.editsniped[channel_id] = {"author" : author, "content" : content}
            fileIO("data/fun/editsniped.json", "save", self.editsniped)
            return
        if str(channel_id) in self.editsniped:
            with open('data/fun/editsniped.json', 'r') as f:
                editsniped = json.load(f)

                editsniped[channel_id] = {}
                editsniped[channel_id]["author"] = author
                editsniped[channel_id]["content"] = content

                self.editsniped = editsniped

            with open('data/fun/editsniped.json', 'w') as f:
                json.dump(editsniped, f, indent=4)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        author = str(message.author.id)
        channel_id = str(message.channel.id)
        content = message.content
        if not str(channel_id) in self.sniped:
            self.sniped[channel_id] = {"author" : author, "content" : content}
            fileIO("data/fun/sniped.json", "save", self.sniped)
            return
        if str(channel_id) in self.sniped:
            with open('data/fun/sniped.json', 'r') as f:
                sniped = json.load(f)

                sniped[channel_id] = {}
                sniped[channel_id]["author"] = author
                sniped[channel_id]["content"] = content

                self.sniped = sniped

            with open('data/fun/sniped.json', 'w') as f:
                json.dump(sniped, f, indent=4)

    @commands.command(aliases=['esnipe'])
    async def editsnipe(self, ctx):
        author = ctx.message.author.id
        channel_id = str(ctx.message.channel.id)
        if channel_id not in self.editsniped:
               embed=discord.Embed(title=f"Nothing to snipe?", description="There is nothing to snipe.", color=0x8b0000, timestamp=ctx.message.created_at)
               embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
               await ctx.send(embed=embed)
               return
        if channel_id in self.editsniped:
            embed = discord.Embed(title="Edit Sniped", description=f"{self.editsniped[channel_id]['content']}\n**Author:** <@{self.sniped[channel_id]['author']}>", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=embed)

    @commands.command()
    async def snipe(self, ctx):
        author = ctx.message.author.id
        channel_id = str(ctx.message.channel.id)
        if channel_id not in self.sniped:
               embed=discord.Embed(title=f"Nothing to snipe?", description="There is nothing to snipe.", color=0x8b0000, timestamp=ctx.message.created_at)
               embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
               await ctx.send(embed=embed)
               return
        if channel_id in self.sniped:
            embed = discord.Embed(title="Sniped", description=f"{self.sniped[channel_id]['content']}\n**Author:** <@{self.sniped[channel_id]['author']}>", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=embed)

    @commands.command()
    async def gay(self, ctx, member: discord.Member=None):
            radint = random.randint(0, 100)
            author = ctx.message.author
            if not member:
               embed=discord.Embed(title="How gay?", description="**{0}** is **{1}%** gay.".format(author.mention, radint), color=0x8b0000, timestamp=ctx.message.created_at)
               embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
               await ctx.send(embed=embed)
            else:
               embed=discord.Embed(title="How gay?", description="**{0}** is **{1}%** gay.".format(member.mention, radint), color=0x8b0000, timestamp=ctx.message.created_at)
               embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
               await ctx.send(embed=embed)

    @commands.command()
    async def straight(self, ctx, member: discord.Member=None):
            radint = random.randint(0, 100)
            author = ctx.message.author
            if not member:
               embed=discord.Embed(title="How straight?", description="**{0}** is **{1}%** straight.".format(author.mention, radint), color=0x8b0000, timestamp=ctx.message.created_at)
               embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
               await ctx.send(embed=embed)
            else:
               embed=discord.Embed(title="How straight?", description="**{0}** is **{1}%** straight.".format(member.mention, radint), color=0x8b0000, timestamp=ctx.message.created_at)
               embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
               await ctx.send(embed=embed)

    @commands.command()
    async def iq(self, ctx, member: discord.Member=None):
        radint = random.randint(0, 140)
        author = ctx.message.author
        if not member:
            embed=discord.Embed(title="What is your IQ?", description="**{0}** has an IQ of **{1}**.".format(author.mention, radint), color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="What is thier IQ?", description="**{0}** has an IQ of **{1}**.".format(member.mention, radint), color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    @commands.command()
    async def dice(self, ctx):
            randint = random.randint(1, 6)
            embed=discord.Embed(title="Roll some dice!", description="You rolled a **{0}**.".format(randint), color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    @commands.command()
    async def fakesnake(self, ctx):
            embed=discord.Embed(title="snake!", description="Hot snake", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_image(url="https://cdn.discordapp.com/attachments/284695295558942720/647050243715760166/image0.jpg")
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    @commands.command()
    async def bruh(self, ctx):
            await ctx.send(f"bruh")
            await ctx.send(f"bruh")
            await ctx.send(f"bruh")
            await ctx.send(f"bruh")
            await ctx.send(f"bruh")

    @commands.command()
    async def pp(self, ctx, member: discord.Member=None):
            author = ctx.message.author
            responses = ['no pp.',
                    'a small pp.',
                    'a moderate pp.',
                    'a large pp.',
                    'a mega pp.']
            pp = random.choice(responses)
            if not member:
               embed=discord.Embed(title="How big is there pp?", description="**{0}** has **{1}**".format(author.mention, pp), color=0x8b0000, timestamp=ctx.message.created_at)
               embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
               await ctx.send(embed=embed)
            else:
               embed=discord.Embed(title="How big is there pp?", description="**{0}** has **{1}**".format(member.mention, pp), color=0x8b0000, timestamp=ctx.message.created_at)
               embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
               await ctx.send(embed=embed)

    @commands.command()
    async def rapist(self, ctx, member: discord.Member=None):
            author = ctx.message.author
            responses = ['is not a rapist.',
                    'might be a rapist.',
                    'is a rapist.',
                    'has raped your whole family.']
            rape = random.choice(responses)
            if not member:
               embed=discord.Embed(title="Are they a rapist?", description="**{0}** {1}".format(author.mention, rape), color=0x8b0000, timestamp=ctx.message.created_at)
               embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
               await ctx.send(embed=embed)
            else:
               embed=discord.Embed(title="Are they a rapist?", description="**{0}** {1}".format(member.mention, rape), color=0x8b0000, timestamp=ctx.message.created_at)
               embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
               await ctx.send(embed=embed)

    @commands.command()
    async def funfact(self, ctx):
    	responses = ["Charles Darwin's personal pet tortoise didn't die until recently.",
                    "The average person will spend six months of their life waiting for red lights to turn green.",
                    "A bolt of lightning contains enough energy to toast 100,000 slices of bread.",
                    "Cherophobia is the word for the irrational fear of being happy.",
                    "You can hear a blue whale's heartbeat from two miles away.",
                    "Nearly 30,000 rubber ducks were lost a sea in 1992 and are still being discovered today.",
                    "There's a Manhattan-specific ant.",
                    "There's a bridge exclusively for squirrels.",
                    "Subway footlongs aren't a foot long.",
                    "Marie Curie's notebooks are still radioactive.",
                    "One in three divorce filings include the word 'Facebook'.",
                    "Blood banks in Sweden notify donors when blood is used.",
                    "Instead of saying 'cheese' before taking a picture, Victorians said 'prunes'.",
                    "Roosters have built-in earplugs.",
                    "The Netherlands is so safe, it imports criminals to fill jails.",
                    "One journal published a fake paper about Star Trek.",
                    "The world's largest pyramid isn't in Egypt.",
                    "Coke saved one town from the Depression.",
                    "We may have already had alien contact.",
                    "Yes, you ***can*** smell rain.",
                    "London cabbies have to memorize literally everything.",
                    "There was a secret Baseball Hall of Fame inductee.",
                    "Dolphins have actual names.",
                    "Superman helped take down the KKK.",
                    "A wild dog is the most successful predator.",
                    "Medicine bottle foil exists because of poison.",
                    "Tons and tons and tons of countries celebrate their independence from the U.K.",
                    "LBJ owned a water-surfing car.",
                    "Sears used to sell houses.",
                    "There's an encrypted monument outside the CIA.",
                    "Manhattan tap water isn't kosher.",
                    "Timothy Leary busted out of prison.",
                    "Cold water is just as cleansing as hot water.",
                    "Incan people used knots to keep records.",
                    "A U.S. Park Ranger once got hit by lightning seven times.",
                    "Bottled water expiration dates are for the bottle, not the water.",
                    "Queen Elizabeth wouldn't sit on the Iron Throne.",
                    "A hiker found and returned an ancient wallet.",
                    "South Koreans are 4cm taller than North Koreans.",
                    "Animal shelters are slammed on July 5th.",
                    "The most requested funeral song in England is by Monty Python.",
                    "The world's most successful pirate was a woman.",
                    "There may be treasure in Virginia.",
                    "A sea lion once saved a man.",
                    "Rich Russians hire fake ambulances.",
                    "Milk wagons gave us roadway lines.",
                    "Pandas fake pregnancy for better care.",
                    "Businesses once didn't see the value of diaper stations.",
                    "Beloved children's book author Roald Dahl was a spy.",
                    "NASCAR drivers can lose up to 10 pounds in sweat due to high temperatures during races.",
                    "Victorians once used leeches to predict the weather.",
                    "Indians spend more than 10 hours a week reading, more than any other country in the world.",
                    "The Aurora Borealis has a sister phenomenon in the southern hemisphere called the Aurora Australis.",
                    "Your funny bone is actually a nerve.",
                    "Pineapples were named after pine cones."
                    "A California woman tried to sue the makers of Cap'N'Crunch after she learned Crunch Berries were not real berries.",
                    "Cap'N'Crunch's full name is Horatio Magellan Crunch.",
                    "Apple briefly had its own clothing and lifestyle line in 1986.",
                    "The IKEA catalog is the most widely printed book in history.",
                    "3 Musketeers bars had three flavors until wartime rations made accessing vanilla and strawberry flavoring too difficult.",
                    "Crocodiles are one of the oldest living species, having survived for more than 200 million years.",
                    "Bacon's saltiness isn't natural—it comes from curing and brining.",
                    "Research shows that all blue-eyed people may be related.",
                    "There was a fifth Beatle named Stuart Sutcliffe.",
                    "The cracking sound your joints make is the sound of gases being released.",
                    "Your bones can multiply in density—times eight.",
                    "The largest snowflake on record was 15 inches wide.",
                    "Scotland has more than 400 words for 'snow'.",
                    "A pig was once executed for murdering a child in France.",
                    "Someone tried to sell New Zealand on eBay but was stopped once the bid reached $3,000.",
                    "A Canadian woman who lost her wedding ring while gardening found it 13 years later growing on a carrot.",
                    "The city of Boring has a sister city called Dull.",
                    "McDonald's once tried to sell bubblegum-flavored broccoli to encourage kids to eat healthier.",
                    "In the 1990s, North Korean teachers were required to play the accordion.",
                    "This punctuation mark ?! is called an interrobang.",
                    "Doritos are flammable and can be used as kindling.",
                    "It's illegal to own only one guinea pig in Switzerland.",
                    "In 2016, a Florida man was charged with assault after throwing a live alligator through a drive-thru window.",
                    "American Airlines saved a boatload by removing a single olive from meals.",
                    "Great Britain once had a Cones Hotline for people to report rogue traffic cones.",
                    "Starbucks flopped Down Under.",
                    "The first written use of 'OMG' was in a 1917 letter to Winston Churchill",
                    "Flamin' Hot Cheetos were invented by a janitor.",
                    "The largest living organism is an aspen grove in Utah called Pando.",
                    "Melting glaciers make a fizzy sound called 'bergy seltzer'.",
                    "Flipping a shark upside down renders it immobile for up to 15 minutes.",
                    "Male students at Brigham Young University in Utah need special permission to grow a beard.",
                    "When Koko the gorilla met Mr. Rogers, she took off his shoes as she had seen him do on his TV show.",
                    "If you die alone in the Netherlands, someone will write you a poem and recite it at your funeral.",
                    "In the 16th century, poets exchanged rap-battle like stylized insults in an act called 'flyting'.",
                    "Astronaut Alan Shepard Hit Two Golf Balls on the Moon's Surface.",
                    "The chief translator of the European Parliament speaks 32 languages fluently",
                    "Beauty and the Beast was written to help girls accept arranged marriages.",
                    "The first roller coaster was invented at Coney Island as a way to distract people from sinful activities",
                    "The German word 'kummerspeck' means weight gained from emotional eating.",
                    "Continental plates drift at about the same rate as fingernails grow.",
                    "Hitler's nephew wrote an essay defaming the dictator, then moved to the U.S. and served in the Navy to fight his uncle.",
                    "David Bowie helped topple the Berlin Wall.",
                    "Brunch was originally invented to cure hangovers"]
    	fun = random.choice(responses)
    	embed=discord.Embed(title="Did you know?", description="{}".format(fun), color=0x8b0000, timestamp=ctx.message.created_at)
    	embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
    	await ctx.send(embed=embed)

    @commands.command(aliases=['8ball', 'test'])
    async def _8ball(self, ctx, *, question=None):
        if question == None:
            embed=discord.Embed(title="No question?", description="You didn't ask a question.", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        responses = ["It is certain.",
                    "It is decidedly so.",
                    "Without a doubt.",
                    "Yes - definitely.",
                    "You may rely on it.",
                    "As I see it, yes.",
                    "Most likely.",
                    "Outlook good.",
                    "Yes.",
                    "Signs point to yes.",
                    "Reply hazy, try again.",
                    "Ask again later.",
                    "Better not tell you now.",
                    "Cannot predict now.",
                    "Concentrate and ask again.",
                    "Don't count on it.",
                    "My reply is no.",
                    "My sources say no.",
                    "Outlook not so good.",
                    "Very doubtful."]
        outlook = random.choice(responses)
        if question:
            embed=discord.Embed(title="The magic 8ball!", description="Question: **{0}**\nAnswer: **{1}**".format(question, outlook), color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    @commands.command()
    async def kill(self, ctx, member: discord.Member=None):
            author = ctx.message.author
            if member == None:
                embed=discord.Embed(title="You didn't ping anyone?", description="Ping someone you dummy.", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            responses = [f"You at shoot at {member.mention} killing them with 50 bullet's, nice.",
                    f"You stab {member.mention} causing them to die.",
                    f"You brought a knife to a gun fight, {member.mention} shoot's you. OUCH!",
                    f"{member.mention} takes an arrow to the knee.",
                    f"You kill {member.mention} by looking at them, are you that ugly?",
                    f"You do a drive by on {member.mention}, shooting them, ofcouse they died.",
                    f"You killed {member.mention} with a tomahawk."]
            kills = random.choice(responses)
            if author == member:
                    embed=discord.Embed(title="Don't kill yourself.", description="$uicide is never the answer.", color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
            else:
                    embed=discord.Embed(title="Killing people is the way.", description="**{0}**".format(kills), color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)

    @commands.command()
    async def love(self, ctx, member: discord.Member=None, member2: discord.Member=None):
            radint = random.randint(0, 100)
            author = ctx.message.author
            if not member:
                    embed=discord.Embed(title="You didn't ping anyone?", description="Ping someone you dummy.", color=0x8b0000, timestamp=ctx.message.created_at)
                    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
                    return
            if not member2:
               embed=discord.Embed(title="How much does that person love them?", description="**{0}** loves **{1}** with **{2}%** of their heart.".format(member.mention, author.mention, radint), color=0x8b0000, timestamp=ctx.message.created_at)
               embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
               await ctx.send(embed=embed)
            else:
               embed=discord.Embed(title="How much does that person love them?", description="**{0}** loves **{1}** with **{2}%** of their heart.".format(member.mention, member2.mention, radint), color=0x8b0000, timestamp=ctx.message.created_at)
               embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
               await ctx.send(embed=embed)

    @commands.command()
    async def ship(self, ctx, member: discord.Member=None, member2: discord.Member=None):
    	radint = random.randint(0, 100)
    	author = ctx.message.author
    	if not member:
    		embed=discord.Embed(title="You didn't ping anyone?", description="Ping someone you dummy.", color=0x8b0000, timestamp=ctx.message.created_at)
    		embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
    		await ctx.send(embed=embed)
    		return
    	if not member2:
    		embed=discord.Embed(title="Is it a match?", description="**-{0}**\n**-{1}**\n**{2}%**.".format(member.mention, author.mention, radint), color=0x8b0000, timestamp=ctx.message.created_at)
    		embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
    		await ctx.send(embed=embed)
    	else:
    		embed=discord.Embed(title="Is it a match?", description="-**{0}**\n-**{1}**\n**{2}%**.".format(member.mention, member2.mention, radint), color=0x8b0000, timestamp=ctx.message.created_at)
    		embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
    		await ctx.send(embed=embed)

    @commands.command(aliases=['rps', 'rock-paper-scissors', 'rock_paper_scissors'])
    async def rockpaperscissors(self, ctx, player=None):
        t = ["rock", "paper", "scissors"]
        computer = random.choice(t)

        tie=discord.Embed(title="TIE!", description="You got a **tie**, epic.", color=0x8b0000, timestamp=ctx.message.created_at)
        tie.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        win=discord.Embed(title="YOU WIN!", description=f"You win!, **{player}** smashes **{computer}**", color=0x8b0000, timestamp=ctx.message.created_at)
        win.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        win2=discord.Embed(title="YOU WIN!", description=f"You win!, **{player}** covers **{computer}**", color=0x8b0000, timestamp=ctx.message.created_at)
        win2.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        win3=discord.Embed(title="YOU WIN!", description=f"You win!, **{player}** cuts **{computer}**", color=0x8b0000, timestamp=ctx.message.created_at)
        win3.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        lose=discord.Embed(title="YOU LOSE!", description=f"You lose!, **{computer}** covers **{player}**", color=0x8b0000, timestamp=ctx.message.created_at)
        lose.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        lose2=discord.Embed(title="YOU LOSE!", description=f"You lose!, **{computer}** cuts **{player}**", color=0x8b0000, timestamp=ctx.message.created_at)
        lose2.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        lose3=discord.Embed(title="YOU LOSE!", description=f"You lose!, **{computer}** smashes **{player}**", color=0x8b0000, timestamp=ctx.message.created_at)
        lose3.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        if player == None:
            embed=discord.Embed(title="Nothing?", description="You didn't put anything, please use, `rock, paper, scissors`.", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        if player != "rock" and player != 'paper' and player != "scissors":
            embed=discord.Embed(title="Incorrect Value.", description="Use, `rock, paper, scissors` instead.", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        if player == "rock" or 'paper' or "scissors":
            if player == computer:
                await ctx.send(embed=tie)
            elif player == "rock":
                if computer == "paper":
                    await ctx.send(embed=lose)
                else:
                    await ctx.send(embed=win)
            elif player == "paper":
                if computer == "scissors":
                    await ctx.send(embed=lose2)
                else:
                    await ctx.send(embed=win2)
            elif player == "scissors" or 'scissor':
                if computer == "rock":
                    await ctx.send(embed=lose3)
                else:
                    await ctx.send(embed=win3)
            else:
                await ctx.send("That's not a valid play. Check your spelling!")

    @commands.command()
    async def say(self, ctx, *, content: commands.clean_content):
        await ctx.send(f"{content}")

    @commands.command()
    async def emsay(self, ctx, *, content=None):
        embed=discord.Embed(description=f"{content}", color=0x8b0000)
        await ctx.message.delete()
        await ctx.send(embed=embed)

    @commands.command()
    async def test3(self, ctx, *, content: commands.clean_content):
        user = ctx.message.author
        channel = ctx.message.channel
        if content:
            await channel.send(f"Are you sure you want to send {content}, if yes, then say yes.")

        def check(m):
            return m.content == 'yes' and m.channel == channel and m.author == user

        try:
            msg = await self.client.wait_for('message', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("User didnt respond in time")
        else:
            await ctx.send(f"{content}")

    @commands.command()
    async def ping(self, ctx, member: discord.Member=None):
        if member.id == 740253555658719344:
            await ctx.send ("no")
            return
        if ctx.message.author.guild_permissions.ban_members or ctx.message.author.id == 101300423649939456:
            await ctx.send(f"{member.mention} get on clown <:PeepoClown:764724064807419914>")
            await ctx.send(f"{member.mention} get on clown <:PeepoClown:764724064807419914>")
            await ctx.send(f"{member.mention} get on clown <:PeepoClown:764724064807419914>")
            await ctx.send(f"{member.mention} get on clown <:PeepoClown:764724064807419914>")
            await ctx.send(f"{member.mention} get on clown <:PeepoClown:764724064807419914>")
            await ctx.send(f"{member.mention} get on clown <:PeepoClown:764724064807419914>")
            await ctx.send(f"{member.mention} get on clown <:PeepoClown:764724064807419914>")
            await ctx.send(f"{member.mention} get on clown <:PeepoClown:764724064807419914>")
            await ctx.send(f"{member.mention} get on clown <:PeepoClown:764724064807419914>")
            await ctx.send(f"{member.mention} get on clown <:PeepoClown:764724064807419914>")
            await ctx.send(f"{member.mention} get on clown <:PeepoClown:764724064807419914>")
            await ctx.send(f"{member.mention} get on clown <:PeepoClown:764724064807419914>")
            await ctx.send(f"{member.mention} get on clown <:PeepoClown:764724064807419914>")
            await ctx.send(f"{member.mention} get on clown <:PeepoClown:764724064807419914>")
            await ctx.send(f"{member.mention} get on clown <:PeepoClown:764724064807419914>")
            await ctx.send(f"{member.mention} get on clown <:PeepoClown:764724064807419914>")
            await ctx.send(f"{member.mention} get on clown <:PeepoClown:764724064807419914>")
            await ctx.send(f"{member.mention} get on clown <:PeepoClown:764724064807419914>")
            await ctx.send(f"{member.mention} get on clown <:PeepoClown:764724064807419914>")
            await ctx.send(f"{member.mention} get on clown <:PeepoClown:764724064807419914>")
            await ctx.send(f"{member.mention} get on clown <:PeepoClown:764724064807419914>")
            await ctx.send(f"{member.mention} get on clown <:PeepoClown:764724064807419914>")
            await ctx.send(f"{member.mention} get on clown <:PeepoClown:764724064807419914>")
            await ctx.send(f"{member.mention} get on clown <:PeepoClown:764724064807419914>")

def setup(client):
    client.add_cog(fun(client))
