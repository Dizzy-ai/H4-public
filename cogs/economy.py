import discord
import json
import asyncio
from discord.ext import commands
from .utils.dataIO import fileIO
from random import randint
from copy import deepcopy
import os
import random
import time
import logging

#
# A silly little module for users to make and loose $$$. By mrbutter#7753
# Future features include configuring a "Cost" to run commands on a per server basis.
# Use [P]economyset to configure settings.
#


class Economy(commands.Cog):
    """Economy
    Get rich and have fun with imaginary currency!"""

    def __init__(self, client):
        self.client = client
        self.bank = fileIO("data/economy/bank.json", "load")
        self.settings = fileIO("data/economy/settings.json", "load")
        self.jobs = fileIO("data/economy/jobs.json", "load")
        self.levels = fileIO("data/level/levels.json", "load")
        self.payweek_register = {}
        self.payday_register = {}
        self.slot_register = {}
        "all the items are below"
        self.guns = fileIO("data/economy/items/gun.json", "load")
        self.butter = fileIO("data/economy/items/butter.json", "load")
        self.redbutter = fileIO("data/economy/items/redbutter.json", "load")
        self.greenbutter = fileIO("data/economy/items/greenbutter.json", "load")
        self.bluebutter = fileIO("data/economy/items/bluebutter.json", "load")
        self.infinity = fileIO("data/economy/items/infinity.json", "load")
        self.travis = fileIO("data/economy/items/travis.json", "load")
        self.highstakes = fileIO("data/economy/items/highstakes.json", "load")
        self.laptop = fileIO("data/economy/items/laptop.json", "load")
        self.crate = fileIO("data/economy/items/crate.json", "load")
        self.uncomcrate = fileIO("data/economy/items/uncomcrate.json", "load")
        self.rarecrate = fileIO("data/economy/items/rarecrate.json", "load")
        self.epiccrate = fileIO("data/economy/items/epiccrate.json", "load")
        self.legcrate = fileIO("data/economy/items/legcrate.json", "load")
        "crate items"
        self.mind = fileIO("data/economy/items/mind.json", "load")
        self.power = fileIO("data/economy/items/power.json", "load")
        self.reality = fileIO("data/economy/items/reality.json", "load")
        self.soul = fileIO("data/economy/items/soul.json", "load")
        self.space = fileIO("data/economy/items/space.json", "load")
        self.time = fileIO("data/economy/items/time.json", "load")
        self.catears = fileIO("data/economy/items/catears.json", "load")
        "all buffs are below"
        self.threetimes = fileIO("data/economy/buffs/threetimes.json", "load")

    @commands.Cog.listener()
    async def on_message(self, message):
        author = message.author
        author_id = str(message.author.id)
        guild_id = str(message.guild.id)
        author = message.author

        if message.author.bot:
            return

        if author_id not in self.bank:
            self.bank[author_id] = {"name" : author.name, "balance" : 100}
            fileIO("data/economy/bank.json", "save", self.bank)
            return

    @commands.command()
    async def shop(self, ctx, page : int=1):
        if page == 1:
            embed=discord.Embed(title="Shop", description="<a:Infinitygauntlet:753359342497169610> **Infinity-Gauntlet** - __5,000,000 coins__ - Item\nRobs a whole server, pretty op in my opinion.\n\n<:butter:752943064263163954> **Butter** - __1,000,000 coins__ - Collectable\nVery rare item, only the richest people have this.\n\n<:redbutter:754825556914339840> **Red-Butter** - __500,000 coins__ - Collectable\nIt's another rich item, yum red butter.\n\n<:greenbutter:754825526786392084> **Green-Butter** - __100,000 coins__ - Collectable\nI mean it's ok, I wouldn't say you're the richest.\n\n<:bluebutter:754825491252510787> **Blue-Butter** - __50,000 coins__ - Collectable\nYeah this is for people who are kinda rich, but it's still butter.\n\n<:highstakes:754775716368744529> **Highstakes** - __500,000 coins__ - Item\nGetting one of these allows you to bid higher on the slot game.\n\n<a:pepegun:752929397408923728> **Gun** - __10,000 coins__ - Item\nShoots someone who tries to rob you.\n\n<:travis_burger:753579092074299412> **Travis-Scott-Burger** - __500 coins__ - Item\nEating the Travis Scott Burger gives you 3x luck.", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author} (Page 1/2)", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        if page == 2:
            embed=discord.Embed(title="Shop", description="<:laptop:755043503956033566> **Laptop** - __3,000 coins__ - Item\nBuying a laptop allows you to make money, or not it depends.\n\n<:commoncrate:755438685998153798> **Common-Crate** - __5,000 coins__ - Item\nDrops a random item, low chances probably not worth it.\n\n<:uncommoncrate:755438720202834050> **Uncommon-Crate** - __10,000 coins__ - Item\nDrops a random item, higher chances but probably not worth it.\n\n<:rarecrate:755438770328699001> **Rare-Crate** - __50,000 coins__ - Item\nDrops a random item, higher chances, probably worth it.\n\n<:epiccrate:755440621136904294> **Epic-Crate** - __100,000 coins__ - Item\nDrops a random item, higher chances, it's worth it.\n\n<:legcrate:755440008172798053> **Legendary-Crate** - __1,000,000 coins__ - Item\nDrops a random item, higher chances, definitely worth it.", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author} (Page 2/2)", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    @commands.group(name="buy")
    async def _buy(self, ctx):
        """buying operations"""
        if ctx.invoked_subcommand is None:
            await ctx.send(f"You forgot to put an item to buy, try doing {ctx.prefix}buy `item`.")

    @_buy.command(aliases=['Gun'])
    async def gun(self, ctx):
        user = ctx.author
        """Registers a job"""
        user_id = str(ctx.message.author.id)
        if user_id in self.guns:
            await ctx.send("You already have a gun.".format(user.mention))
            return
        if not self.enough_money(user_id, 10000):
            await ctx.send("You dont have enough money for that.")
            return
        if user_id not in self.guns:
            self.withdraw_money(user_id, 10000)
            self.guns[user_id] = {"uses" : 9, "amount" : 1}
            fileIO("data/economy/items/gun.json", "save", self.guns)
            await ctx.send("{} just bought a gun for **10,000** coins".format(user.mention))
        else:
            await ctx.send("something happened.")

    @_buy.command(aliases=['Butter'])
    async def butter(self, ctx):
        user = ctx.author
        """Registers a job"""
        user_id = str(ctx.message.author.id)
        if user_id in self.butter:
            await ctx.send("You already have butter.".format(user.mention))
            return
        if not self.enough_money(user_id, 1000000):
            await ctx.send("You dont have enough money for that.")
            return
        if user_id not in self.butter:
            self.withdraw_money(user_id, 1000000)
            self.butter[user_id] = {"uses" : 0, "amount" : 1}
            fileIO("data/economy/items/butter.json", "save", self.butter)
            await ctx.send("{} just bought butter for **1,000,000** coins".format(user.mention))
        else:
            await ctx.send("something happened.")

    @_buy.command(aliases=['Red-Butter', 'red-butter'])
    async def redbutter(self, ctx):
        user = ctx.author
        """Registers a job"""
        user_id = str(ctx.message.author.id)
        if user_id in self.redbutter:
            await ctx.send("You already have red butter.".format(user.mention))
            return
        if not self.enough_money(user_id, 500000):
            await ctx.send("You dont have enough money for that.")
            return
        if user_id not in self.redbutter:
            self.withdraw_money(user_id, 500000)
            self.redbutter[user_id] = {"uses" : 0, "amount" : 1}
            fileIO("data/economy/items/redbutter.json", "save", self.redbutter)
            await ctx.send("{} just bought red butter for **500,000** coins".format(user.mention))
        else:
            await ctx.send("something happened.")

    @_buy.command(aliases=['Green-Butter', 'green-butter'])
    async def greenbutter(self, ctx):
        user = ctx.author
        """Registers a job"""
        user_id = str(ctx.message.author.id)
        if user_id in self.greenbutter:
            await ctx.send("You already have red butter.".format(user.mention))
            return
        if not self.enough_money(user_id, 100000):
            await ctx.send("You dont have enough money for that.")
            return
        if user_id not in self.greenbutter:
            self.withdraw_money(user_id, 100000)
            self.greenbutter[user_id] = {"uses" : 0, "amount" : 1}
            fileIO("data/economy/items/greenbutter.json", "save", self.greenbutter)
            await ctx.send("{} just bought green butter for **100,000** coins".format(user.mention))
        else:
            await ctx.send("something happened.")

    @_buy.command(aliases=['Blue-Butter', 'blue-butter'])
    async def bluebutter(self, ctx):
        user = ctx.author
        """Registers a job"""
        user_id = str(ctx.message.author.id)
        if user_id in self.bluebutter:
            await ctx.send("You already have blue butter.".format(user.mention))
            return
        if not self.enough_money(user_id, 50000):
            await ctx.send("You dont have enough money for that.")
            return
        if user_id not in self.bluebutter:
            self.withdraw_money(user_id, 50000)
            self.bluebutter[user_id] = {"uses" : 0, "amount" : 1}
            fileIO("data/economy/items/bluebutter.json", "save", self.bluebutter)
            await ctx.send("{} just bought blue butter for **50,000** coins".format(user.mention))
        else:
            await ctx.send("something happened.")

    @_buy.command(aliases=['Highstakes'])
    async def highstakes(self, ctx):
        user = ctx.author
        """Registers a job"""
        user_id = str(ctx.message.author.id)
        if user_id in self.highstakes:
            await ctx.send("You already have the highstakes pass.".format(user.mention))
            return
        if not self.enough_money(user_id, 500000):
            await ctx.send("You dont have enough money for that.")
            return
        if user_id not in self.highstakes:
            self.withdraw_money(user_id, 500000)
            self.highstakes[user_id] = {"uses" : 0, "amount" : 1}
            fileIO("data/economy/items/highstakes.json", "save", self.highstakes)
            await ctx.send("{} just bought the Highstakes Pass for **500,000** coins".format(user.mention))
        else:
            await ctx.send("something happened.")

    def inf_check(self, id):
        if id in self.infinity:
            return True
        else:
            return False

    def add_inf(self, id, amount):
        if self.inf_check(id):
            self.infinity[id]["amount"] = self.infinity[id]["amount"] + int(amount)
            fileIO("data/economy/items/infinity.json", "save", self.infinity)
        else:
            return False

    @_buy.command(aliases=['Infinity-Gauntlet', 'infinity-gauntlet'])
    async def infinity(self, ctx, amount=1):
        user = ctx.author
        """Registers a job"""
        user_id = str(ctx.message.author.id)
        if not self.enough_money(user_id, 5000000*amount):
            await ctx.send("You dont have enough money for that.")
            return
        if user_id in self.infinity:
            self.withdraw_money(user_id, 5000000*amount)
            self.add_inf(user_id, amount)
            await ctx.send("{} just bought {} Infinity Gauntlets for **{}** coins".format(user.mention, amount, 5000000*amount))
            return
        if user_id not in self.infinity:
            self.withdraw_money(user_id, 5000000*amount)
            self.infinity[user_id] = {"uses" : 0, "amount" : amount}
            fileIO("data/economy/items/infinity.json", "save", self.infinity)
            await ctx.send("{} just bought {} Infinity Gauntlet for **{}** coins".format(user.mention, amount, 5000000*amount))
        else:
            await ctx.send("something happened.")

    def travis_check(self, id):
        if id in self.travis:
            return True
        else:
            return False

    def has_travis(self, id, amount):
        if self.travis_check(id):
            if self.travis[id]["amount"] >= int(amount):
                return True
            else:
                return False
        else:
            return False

    def add_travis(self, id, amount):
        if self.travis_check(id):
            self.travis[id]["amount"] = self.travis[id]["amount"] + int(amount)
            fileIO("data/economy/items/travis.json", "save", self.travis)
        else:
            return False

    def remove_travis(self, id, amount):
        if self.travis_check(id):
            if self.travis[id]["amount"] >= int(amount):
                self.travis[id]["amount"] = self.travis[id]["amount"] - int(amount)
                fileIO("data/economy/items/travis.json", "save", self.travis)
            else:
                return False
        else:
            return False

    @_buy.command(aliases=['Travis-Scott-Burger', 'travis-scott-burger', 'Travis'])
    async def travis(self, ctx, amount=1):
        user = ctx.author
        """Registers a job"""
        user_id = str(ctx.message.author.id)
        if not self.enough_money(user_id, 500*amount):
            await ctx.send("You dont have enough money for that.")
            return
        if user_id in self.travis:
            self.withdraw_money(user_id, 500*amount)
            self.add_travis(user_id, amount)
            await ctx.send("{} just bought {} Travis Scott Burgers for **{}** coins".format(user.mention, amount, 500*amount))
            return
        if user_id not in self.travis:
            self.withdraw_money(user_id, 500*amount)
            self.travis[user_id] = {"uses" : 0, "amount" : amount}
            fileIO("data/economy/items/travis.json", "save", self.travis)
            await ctx.send("{} just bought {} Travis Scott Burgers for **{}** coins".format(user.mention, amount, 500*amount))
        else:
            await ctx.send("something happened.")


    def laptop_check(self, id):
        if id in self.laptop:
            return True
        else:
            return False

    def has_laptop(self, id, amount):
        if self.laptop_check(id):
            if self.laptop[id]["amount"] >= int(amount):
                return True
            else:
                return False
        else:
            return False

    def add_laptop(self, id, amount):
        if self.laptop_check(id):
            self.laptop[id]["amount"] = self.laptop[id]["amount"] + int(amount)
            fileIO("data/economy/items/laptop.json", "save", self.laptop)
        else:
            return False

    def remove_laptop(self, id, amount):
        if self.laptop_check(id):
            if self.laptop[id]["amount"] >= int(amount):
                self.laptop[id]["amount"] = self.laptop[id]["amount"] - int(amount)
                fileIO("data/economy/items/laptop.json", "save", self.laptop)
            else:
                return False
        else:
            return False

    @_buy.command(aliases=['Laptop'])
    async def laptop(self, ctx, amount=1):
        user = ctx.author
        """Registers a job"""
        user_id = str(ctx.message.author.id)
        if not self.enough_money(user_id, 3000*amount):
            await ctx.send("You dont have enough money for that.")
            return
        if user_id in self.laptop:
            self.withdraw_money(user_id, 3000*amount)
            self.add_laptop(user_id, amount)
            await ctx.send("{} just bought {} Laptops for **{}** coins".format(user.mention, amount, 3000*amount))
            return
        if user_id not in self.laptop:
            self.withdraw_money(user_id, 3000*amount)
            self.laptop[user_id] = {"uses" : 0, "amount" : amount}
            fileIO("data/economy/items/laptop.json", "save", self.laptop)
            await ctx.send("{} just bought {} Laptops for **{}** coins".format(user.mention, amount, 3000*amount))
        else:
            await ctx.send("something happened.")

    def crate_check(self, id):
        if id in self.crate:
            return True
        else:
            return False

    def has_crate(self, id, amount):
        if self.crate_check(id):
            if self.crate[id]["amount"] >= int(amount):
                return True
            else:
                return False
        else:
            return False

    def add_crate(self, id, amount):
        if self.crate_check(id):
            self.crate[id]["amount"] = self.crate[id]["amount"] + int(amount)
            fileIO("data/economy/items/crate.json", "save", self.crate)
        else:
            return False

    def remove_crate(self, id, amount):
        if self.crate_check(id):
            if self.crate[id]["amount"] >= int(amount):
                self.crate[id]["amount"] = self.crate[id]["amount"] - int(amount)
                fileIO("data/economy/items/crate.json", "save", self.crate)
            else:
                return False
        else:
            return False

    @_buy.command(aliases=['common-crate', 'Common-Crate'])
    async def crate(self, ctx, amount=1):
        user = ctx.author
        """Registers a job"""
        user_id = str(ctx.message.author.id)
        if not self.enough_money(user_id, 5000*amount):
            await ctx.send("You dont have enough money for that.")
            return
        if user_id in self.crate:
            self.withdraw_money(user_id, 5000*amount)
            self.add_crate(user_id, amount)
            await ctx.send("{} just bought {} Common Crates for **{}** coins".format(user.mention, amount, 5000*amount))
            return
        if user_id not in self.crate:
            self.withdraw_money(user_id, 5000*amount)
            self.crate[user_id] = {"uses" : 0, "amount" : amount}
            fileIO("data/economy/items/crate.json", "save", self.crate)
            await ctx.send("{} just bought {} Common Crates for **{}** coins".format(user.mention, amount, 5000*amount))
        else:
            await ctx.send("something happened.")

    def uncomcrate_check(self, id):
        if id in self.uncomcrate:
            return True
        else:
            return False

    def has_uncomcrate(self, id, amount):
        if self.uncomcrate_check(id):
            if self.uncomcrate[id]["amount"] >= int(amount):
                return True
            else:
                return False
        else:
            return False

    def add_uncomcrate(self, id, amount):
        if self.uncomcrate_check(id):
            self.uncomcrate[id]["amount"] = self.uncomcrate[id]["amount"] + int(amount)
            fileIO("data/economy/items/uncomcrate.json", "save", self.uncomcrate)
        else:
            return False

    def remove_uncomcrate(self, id, amount):
        if self.uncomcrate_check(id):
            if self.uncomcrate[id]["amount"] >= int(amount):
                self.uncomcrate[id]["amount"] = self.uncomcrate[id]["amount"] - int(amount)
                fileIO("data/economy/items/uncomcrate.json", "save", self.uncomcrate)
            else:
                return False
        else:
            return False

    @_buy.command(aliases=['uncommon-crate', 'Uncommon-Crate'])
    async def uncomcrate(self, ctx, amount=1):
        user = ctx.author
        """Registers a job"""
        user_id = str(ctx.message.author.id)
        if not self.enough_money(user_id, 10000*amount):
            await ctx.send("You dont have enough money for that.")
            return
        if user_id in self.uncomcrate:
            self.withdraw_money(user_id, 10000*amount)
            self.add_uncomcrate(user_id, amount)
            await ctx.send("{} just bought {} Uncommon Crates for **{}** coins".format(user.mention, amount, 10000*amount))
            return
        if user_id not in self.uncomcrate:
            self.withdraw_money(user_id, 10000*amount)
            self.uncomcrate[user_id] = {"uses" : 0, "amount" : amount}
            fileIO("data/economy/items/uncomcrate.json", "save", self.uncomcrate)
            await ctx.send("{} just bought {} Uncommon Crates for **{}** coins".format(user.mention, amount, 10000*amount))
        else:
            await ctx.send("something happened.")

    def rarecrate_check(self, id):
        if id in self.rarecrate:
            return True
        else:
            return False

    def has_rarecrate(self, id, amount):
        if self.rarecrate_check(id):
            if self.rarecrate[id]["amount"] >= int(amount):
                return True
            else:
                return False
        else:
            return False

    def add_rarecrate(self, id, amount):
        if self.rarecrate_check(id):
            self.rarecrate[id]["amount"] = self.rarecrate[id]["amount"] + int(amount)
            fileIO("data/economy/items/rarecrate.json", "save", self.rarecrate)
        else:
            return False

    def remove_rarecrate(self, id, amount):
        if self.rarecrate_check(id):
            if self.rarecrate[id]["amount"] >= int(amount):
                self.rarecrate[id]["amount"] = self.rarecrate[id]["amount"] - int(amount)
                fileIO("data/economy/items/rarecrate.json", "save", self.rarecrate)
            else:
                return False
        else:
            return False

    @_buy.command(aliases=['rare-crate', 'Rare-Crate'])
    async def rarecrate(self, ctx, amount=1):
        user = ctx.author
        """Registers a job"""
        user_id = str(ctx.message.author.id)
        if not self.enough_money(user_id, 50000*amount):
            await ctx.send("You dont have enough money for that.")
            return
        if user_id in self.rarecrate:
            self.withdraw_money(user_id, 50000*amount)
            self.add_rarecrate(user_id, amount)
            await ctx.send("{} just bought {} Rare Crates for **{}** coins".format(user.mention, amount, 50000*amount))
            return
        if user_id not in self.rarecrate:
            self.withdraw_money(user_id, 50000*amount)
            self.rarecrate[user_id] = {"uses" : 0, "amount" : amount}
            fileIO("data/economy/items/rarecrate.json", "save", self.rarecrate)
            await ctx.send("{} just bought {} Rare Crates for **{}** coins".format(user.mention, amount, 50000*amount))
        else:
            await ctx.send("something happened.")

    def epiccrate_check(self, id):
        if id in self.epiccrate:
            return True
        else:
            return False

    def has_epiccrate(self, id, amount):
        if self.epiccrate_check(id):
            if self.epiccrate[id]["amount"] >= int(amount):
                return True
            else:
                return False
        else:
            return False

    def add_epiccrate(self, id, amount):
        if self.epiccrate_check(id):
            self.epiccrate[id]["amount"] = self.epiccrate[id]["amount"] + int(amount)
            fileIO("data/economy/items/epiccrate.json", "save", self.epiccrate)
        else:
            return False

    def remove_epiccrate(self, id, amount):
        if self.epiccrate_check(id):
            if self.epiccrate[id]["amount"] >= int(amount):
                self.epiccrate[id]["amount"] = self.epiccrate[id]["amount"] - int(amount)
                fileIO("data/economy/items/epiccrate.json", "save", self.epiccrate)
            else:
                return False
        else:
            return False

    @_buy.command(aliases=['epic-crate', 'Epic-Crate'])
    async def epiccrate(self, ctx, amount=1):
        user = ctx.author
        """Registers a job"""
        user_id = str(ctx.message.author.id)
        if not self.enough_money(user_id, 100000*amount):
            await ctx.send("You dont have enough money for that.")
            return
        if user_id in self.epiccrate:
            self.withdraw_money(user_id, 100000*amount)
            self.add_epiccrate(user_id, amount)
            await ctx.send("{} just bought {} Epic Crates for **{}** coins".format(user.mention, amount, 100000*amount))
            return
        if user_id not in self.epiccrate:
            self.withdraw_money(user_id, 100000*amount)
            self.epiccrate[user_id] = {"uses" : 0, "amount" : amount}
            fileIO("data/economy/items/epiccrate.json", "save", self.epiccrate)
            await ctx.send("{} just bought {} Epic Crate for **{}** coins".format(user.mention, amount, 100000*amount))
        else:
            await ctx.send("something happened.")

    def legcrate_check(self, id):
        if id in self.legcrate:
            return True
        else:
            return False

    def has_legcrate(self, id, amount):
        if self.legcrate_check(id):
            if self.legcrate[id]["amount"] >= int(amount):
                return True
            else:
                return False
        else:
            return False

    def add_legcrate(self, id, amount):
        if self.legcrate_check(id):
            self.legcrate[id]["amount"] = self.legcrate[id]["amount"] + int(amount)
            fileIO("data/economy/items/legcrate.json", "save", self.legcrate)
        else:
            return False

    def remove_legcrate(self, id, amount):
        if self.legcrate_check(id):
            if self.legcrate[id]["amount"] >= int(amount):
                self.legcrate[id]["amount"] = self.legcrate[id]["amount"] - int(amount)
                fileIO("data/economy/items/legcrate.json", "save", self.legcrate)
            else:
                return False
        else:
            return False

    @_buy.command(aliases=['legendary-crate', 'Legendary-Crate'])
    async def legcrate(self, ctx, amount=1):
        user = ctx.author
        """Registers a job"""
        user_id = str(ctx.message.author.id)
        if not self.enough_money(user_id, 1000000*amount):
            await ctx.send("You dont have enough money for that.")
            return
        if user_id in self.legcrate:
            self.withdraw_money(user_id, 1000000*amount)
            self.add_legcrate(user_id, amount)
            await ctx.send("{} just bought {} Legendary Crate for **{}** coins".format(user.mention, amount, 1000000*amount))
            return
        if user_id not in self.legcrate:
            self.withdraw_money(user_id, 1000000*amount)
            self.legcrate[user_id] = {"uses" : 0, "amount" : amount}
            fileIO("data/economy/items/legcrate.json", "save", self.legcrate)
            await ctx.send("{} just bought {} Legendary Crates for **{}** coins".format(user.mention, amount, 1000000*amount))
        else:
            await ctx.send("something happened.")

    @commands.group(name="use")
    async def _use(self, ctx):
        """buying operations"""
        if ctx.invoked_subcommand is None:
            await ctx.send(f"You forgot to put an item to use, try doing {ctx.prefix}use `item`.")

    @_use.command(aliases=['Travis-Scott-Burger', 'travis-scott-burger', 'travis', 'Travis'])
    async def travis2(self, ctx):
        user = ctx.author
        user_id = str(ctx.message.author.id)
        if user_id not in self.travis:
            await ctx.send(f"You don't have a Travis Scott Burger. Try buying one by doing {ctx.prefix}buy travis-scott-burger")
        if self.has_travis(user_id, 2):
            if user_id in self.threetimes:
                await ctx.send("3x is currently active.")
                return
            else:
                self.remove_travis(user_id, 1)
                self.threetimes[user_id] = {"enabled" : 1, "enabled2": 1}
                fileIO("data/economy/buffs/threetimes.json", "save", self.threetimes)
                await ctx.send(f"You used one Travis Scott Burger, You have now received 3x luck.")
                await asyncio.sleep(8600)
                with open('data/economy/buffs/threetimes.json', 'r') as f:
                    three = json.load(f)

                    three.pop(str(user.id))

                    self.threetimes = three

                with open('data/economy/buffs/threetimes.json', 'w') as f:
                    json.dump(three, f, indent=4)
                return
        if self.has_travis(user_id, 1):
            if user_id in self.threetimes:
                await ctx.send("3x is currently active.")
                return
            else:
                with open('data/economy/items/travis.json', 'r') as f:
                    travis = json.load(f)

                    travis.pop(str(user.id))

                    self.travis = travis

                with open('data/economy/items/travis.json', 'w') as f:
                    json.dump(travis, f, indent=4)
                self.threetimes[user_id] = {"enabled" : 1, "enabled2": 1}
                fileIO("data/economy/buffs/threetimes.json", "save", self.threetimes)
                await ctx.send(f"You have used a Travis Scott Burger, You have now received 3x luck.")
                await asyncio.sleep(8600)
                with open('data/economy/buffs/threetimes.json', 'r') as f:
                    three = json.load(f)

                    three.pop(str(user.id))

                    self.threetimes = three

                with open('data/economy/buffs/threetimes.json', 'w') as f:
                    json.dump(three, f, indent=4)
                return

    @_use.command(aliases=['laptop', 'Laptop'])
    @commands.cooldown(rate=1, per=1000.0, type=commands.BucketType.user)
    async def laptop2(self, ctx):
        user = ctx.author
        user_id = str(ctx.message.author.id)
        radint = random.randint(1, 300)
        radint2 = random.randint(1, 100)
        radint3 = random.randint(1, 500)
        if user_id not in self.laptop:
            await ctx.send(f"You don't have a laptop. Try buying one by doing {ctx.prefix}buy laptop")
        if user_id in self.threetimes:
            if self.has_laptop(user_id, 2):
                if radint >= 300:
                    self.remove_laptop(user_id, 1)
                    await ctx.send(f"Oh no one of your laptops broke")
                    return
                elif radint2 >= 75:
                    await ctx.send(f"You just did nothing, looked at porn you weirdo.")
                    return
                elif radint2 >= 0:
                    self.add_money(id, radint3)
                    await ctx.send(f"You decided to post a meme, it made **{radint3}** coins")
                    return
            if self.has_laptop(user_id, 1):
                if radint >= 300:
                    with open('data/economy/items/laptop.json', 'r') as f:
                        laptop = json.load(f)

                        laptop.pop(str(user.id))

                        self.laptop = laptop
                    with open('data/economy/items/laptop.json', 'w') as f:
                        json.dump(laptop, f, indent=4)
                    await ctx.send(f"Oh no your laptop broke")
                    return
                elif radint2 >= 75:
                    await ctx.send(f"You just did nothing, and you looked at porn you weirdo.")
                    return
                elif radint2 >= 0:
                    self.add_money(id, radint3)
                    await ctx.send(f"You decided to post a meme, it made **{radint3}** coins")
                    return
        if self.has_laptop(user_id, 2):
            if radint >= 300:
                self.remove_laptop(user_id, 1)
                await ctx.send(f"Oh no one of your laptops broke")
                return
            elif radint2 >= 60:
                self.add_money(id, radint3)
                await ctx.send(f"You decided to post a meme, it made **{radint3}** coins")
            elif radint2 >= 0:
                await ctx.send(f"You just did nothing, looked at porn you weirdo.")
                return
        if self.has_laptop(user_id, 1):
            if radint >= 300:
                with open('data/economy/items/laptop.json', 'r') as f:
                    laptop = json.load(f)

                    laptop.pop(str(user.id))

                    self.laptop = laptop

                with open('data/economy/items/laptop.json', 'w') as f:
                    json.dump(laptop, f, indent=4)
                await ctx.send(f"Oh no your laptop broke")
                return
            elif radint2 >= 60:
                self.add_money(id, radint3)
                await ctx.send(f"You decided to post a meme, it made **{radint3}** coins")
            elif radint2 >= 0:
                await ctx.send(f"You just did nothing, and you looked at porn you weirdo.")

    @_use.command(aliases=['Common-Crate', 'common-crate'])
    async def crate2(self, ctx):
        user = ctx.author
        user_id = str(ctx.message.author.id)
        radint = random.randint(0, 350)
        if user_id not in self.crate:
            await ctx.send(f"You don't have a common crate. Try buying one by doing {ctx.prefix}buy common-crate")
        if self.has_crate(user_id, 2):
            self.remove_crate(user_id, 1)
            if radint >= 350:
                if user_id in self.time:
                    self.time[user_id]["amount"] = self.time[user_id]["amount"] + int(1)
                    fileIO("data/economy/items/time.json", "save", self.time)
                    await ctx.send("You just got another Time stone.")
                    return
                if user_id not in self.time:
                    self.time[user_id] = {"uses" : 0, "amount" : 1}
                    fileIO("data/economy/items/time.json", "save", self.time)
                    await ctx.send("You just got the Time stone.")
                    return
            elif radint >= 300:
                if user_id in self.catears:
                    self.catears[user_id]["uses"] = self.catears[user_id]["uses"] + int(10)
                    fileIO("data/economy/items/catears.json", "save", self.catears)
                    await ctx.send("You just got more uses on your catears.")
                    return
                if user_id not in self.catears:
                    self.catears[user_id] = {"uses" : 10, "amount" : 1}
                    fileIO("data/economy/items/catears.json", "save", self.catears)
                    await ctx.send("You just got Cat Ears.")
                    return
            elif radint >= 250:
                return

    #@_use.command(aliases=['Uncommon-Crate', 'uncommon-crate'])
    #async def uncomcrate(self, ctx):
    #    user = ctx.author
    #    user_id = str(ctx.message.author.id)


    #@_use.command(aliases=['Rare-Crate', 'rare-crate'])
    #async def rarecrate(self, ctx):
    #    user = ctx.author
    #    user_id = str(ctx.message.author.id)

    #@_use.command(aliases=['Epic-Crate', 'epic-crate'])
    #async def epiccrate(self, ctx):
    #    user = ctx.author
    #    user_id = str(ctx.message.author.id)

    #@_use.command(aliases=['Legendary-Crate', 'legendary-crate'])
    #async def legcrate(self, ctx):
    #    user = ctx.author
    #    user_id = str(ctx.message.author.id)


    @_use.command(aliases=['Infinity-Gauntlet', 'infinity-gauntlet'])
    async def infinity(self, ctx):
        user = ctx.author
        user_id = str(ctx.message.author.id)
        if user_id not in self.infinity:
            await ctx.send(f"You do not own an Infinity Gauntlet. Buy one by doing {ctx.prefix}buy infinity-gauntlet")


    @commands.command(aliases=['inv'])
    async def inventory(self, ctx, page: int = 1, member: discord.Member=None):
        member = ctx.author if not member else member
        member_id = str(member.id)
        embed=discord.Embed(color=0x8b0000, timestamp=ctx.message.created_at)
        embed.set_author(name=f"Inventory - {member}", icon_url=member.avatar_url)

        embed2=discord.Embed(color=0x8b0000, timestamp=ctx.message.created_at)
        embed2.set_author(name=f"Inventory - {member}", icon_url=member.avatar_url)

        if member_id not in self.laptop and member_id not in self.crate and member_id not in self.uncomcrate and member_id not in self.rarecrate and member_id not in self.epiccrate and member_id not in self.legcrate:
            pages = 1
        elif member_id in self.laptop or member_id in self.crate or member_id in self.uncomcrate or member_id in self.rarecrate or member_id in self.epiccrate or member_id in self.legcrate:
            pages = 2

        if page == 1:
            if member_id in self.highstakes:
                embed.add_field(name=f"<:highstakes:754775716368744529> **Highstakes Pass -** {self.highstakes[member_id]['amount']}", value="*ID* `highstakes` - Item", inline=False)

        if page == 1:
            if member_id in self.infinity:
                embed.add_field(name=f"<a:Infinitygauntlet:753359342497169610> **Infinity Gauntlet -** {self.infinity[member_id]['amount']}", value="*ID* `infinity-gauntlet` - Item", inline=False)
            if member_id in self.mind:
                embed.add_field(name=f"<:mindstone:757288973289914440> **Mind Stone -** {self.mind[member_id]['amount']}", value="*ID* `mind-stone`")
            if member_id in self.power:
                embed.add_field(name=f"<:powerstone:757292273431085280> **Power Stone -** {self.power[member_id]['amount']}", value="*ID* `power-stone`")
            if member_id in self.reality:
                embed.add_field(name=f"<:realitystone:757289964831768667> **Reality Stone -** {self.reality[member_id]['amount']}", value="*ID* `reality-stone`")
            if member_id in self.soul:
                embed.add_field(name=f"<:soulstone:757290982717784287> **Soul Stone -** {self.soul[member_id]['amount']}", value="*ID* `soul-stone`")
            if member_id in self.space:
                embed.add_field(name=f"<:spacestone:757289311002689586> **Space Stone -** {self.space[member_id]['amount']}", value="*ID* `space-stone`")
            if member_id in self.time:
                embed.add_field(name=f"<:timestone:757292979147767929> **Time Stone -** {self.time[member_id]['amount']}", value="*ID* `time-stone`")


        if page == 1:
            if member_id in self.guns:
                embed.add_field(name=f"<a:pepegun:752929397408923728> **Gun -** {self.guns[member_id]['amount']} \n**Uses Left -** {self.guns[member_id]['uses']}", value="*ID* `gun` - Item", inline=False)

        if page == 1:
            if member_id in self.butter:
                embed.add_field(name=f"<:butter:752943064263163954> **Butter -** {self.butter[member_id]['amount']}", value="*ID* `butter` - Collectable", inline=False)

        if page == 1:
            if member_id in self.redbutter:
                embed.add_field(name=f"<:redbutter:754825556914339840> **Red Butter -** {self.redbutter[member_id]['amount']}", value="*ID* `red-butter` - Collectable", inline=False)

        if page == 1:
            if member_id in self.greenbutter:
                embed.add_field(name=f"<:greenbutter:754825526786392084> **Green Butter -** {self.greenbutter[member_id]['amount']}", value="*ID* `green-butter` - Collectable", inline=False)

        if page == 1:
            if member_id in self.bluebutter:
                embed.add_field(name=f"<:bluebutter:754825491252510787> **Blue Butter -** {self.bluebutter[member_id]['amount']}", value="*ID* `blue-butter` - Collectable", inline=False)

        if page == 1:
            if member_id in self.travis:
                embed.add_field(name=f"<:travis_burger:753579092074299412> **Travis Scott Burger -** {self.travis[member_id]['amount']}", value="*ID* `travis-scott-burger` - Item", inline=False)

        if page == 2:
            if member_id in self.laptop:
                embed2.add_field(name=f"<:laptop:755043503956033566> **Laptop -** {self.laptop[member_id]['amount']}", value="*ID* `laptop` - Item", inline=False)

        if page == 2:
            if member_id in self.crate:
                embed2.add_field(name=f"<:commoncrate:755438685998153798> **Common Crate -** {self.crate[member_id]['amount']}", value="*ID* `common-crate` - Item", inline=False)

        if page == 2:
            if member_id in self.uncomcrate:
                embed2.add_field(name=f"<:uncommoncrate:755438720202834050> **Uncommon Crate -** {self.uncomcrate[member_id]['amount']}", value="*ID* `uncommon-crate` - Item", inline=False)

        if page == 2:
            if member_id in self.rarecrate:
                embed2.add_field(name=f"<:rarecrate:755438770328699001> **Rare Crate -** {self.rarecrate[member_id]['amount']}", value="*ID* `rare-crate` - Item", inline=False)

        if page == 2:
            if member_id in self.epiccrate:
                embed2.add_field(name=f"<:epiccrate:755440621136904294> **Epic Crate -** {self.epiccrate[member_id]['amount']}", value="*ID* `epic-crate` - Item", inline=False)

        if page == 2:
            if member_id in self.legcrate:
                embed2.add_field(name=f"<:legcrate:755440008172798053> **Legendary Crate -** {self.legcrate[member_id]['amount']}", value="*ID* `legendary-crate` - Item", inline=False)


        if page == 1:
            embed.set_footer(text=f"Requested by {ctx.author} (Page 1/{pages})", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        if page == 2:
            embed2.set_footer(text=f"Requested by {ctx.author} (Page 2/{pages})", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed2)

    @commands.command()
    async def jobs(self, ctx):
        id = str(ctx.message.author.id)
        if self.lvl_check(id, 15):
            embed4=discord.Embed(title="Current Jobs", description="**Level 1 jobs:**\nyoutuber\nfastfood worker\n\n**Level 5 jobs:**\nchild careworker\nbarber\n\n**Level 10 jobs:**\nclergy\nembalmers\n\n**Level 15 jobs:**\ncosplayer\nprogrammer", color=0x8b0000, timestamp=ctx.message.created_at)
            embed4.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed4)
            return
        if self.lvl_check(id, 10):
            embed3=discord.Embed(title="Current Jobs", description="**Level 1 jobs:**\nyoutuber\nfastfood worker\n\n**Level 5 jobs:**\nchild careworker\nbarber\n\n**Level 10 jobs:**\nclergy\nembalmers", color=0x8b0000, timestamp=ctx.message.created_at)
            embed3.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed3)
            return
        if self.lvl_check(id, 5):
            embed2=discord.Embed(title="Jobs", description="**Level 1 jobs:**\nyoutuber\nfastfood worker\n\n**Level 5 jobs:**\nchild careworker\nbarber", color=0x8b0000, timestamp=ctx.message.created_at)
            embed2.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed2)
            return
        if self.lvl_check(id, 1):
            embed=discord.Embed(title="Jobs", description="**Level 1 jobs:**\nyoutuber\nfastfood worker", color=0x8b0000, timestamp=ctx.message.created_at)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    @commands.group(name="job")
    async def _job(self, ctx):
        author_id = str(ctx.message.author.id)
        author = ctx.message.author
        """Shows job of user.
        Defaults to yours."""
        if ctx.invoked_subcommand is None:
            if self.job_check(author_id):
                await ctx.send("{} Your current job is {}.".format(author.mention, str(self.check_job(author_id))))
            else:
                await ctx.send("{} You don't have an job. Type {}job register 'job name' to open one.".format(author.mention, ctx.prefix))


    @_job.command()
    async def change(self, ctx, *, job=None):
        user = ctx.author
        """Registers a job"""
        id = str(ctx.message.author.id)
        if id not in self.jobs:
            await ctx.send(f"You don't have a job, you should register for one by doing {ctx.prefix}job register 'job'")
            return
        if job == None:
            await ctx.send("You forgot to put a job")
            return
        if job != "youtuber" and job != "fastfood worker" and job != "child careworker" and job != "barber" and job != "clergy" and job != "embalmers" and job != "cosplayer" and job != "programmer":
            await ctx.send(f"That's not a job, try doing {ctx.prefix}jobs to see all the jobs.")
            return
        if self.lvl_check(id, 1) and job == "youtuber" or job == "fastfood worker":
            self.jobs[id] = {"name" : user.name, "job" : job}
            fileIO("data/economy/jobs.json", "save", self.jobs)
            await ctx.send("{} has changed their job, the job is {}".format(user.mention, job))
            return
        if self.lvl_check(id, 5) and job == "child careworker":
            self.jobs[id] = {"name" : user.name, "job" : job}
            fileIO("data/economy/jobs.json", "save", self.jobs)
            await ctx.send("{} has changed their job, the job is {}".format(user.mention, job))
            return
        if self.lvl_check(id, 5) and job == "barber":
            self.jobs[id] = {"name" : user.name, "job" : job}
            fileIO("data/economy/jobs.json", "save", self.jobs)
            await ctx.send("{} has changed their job, the job is {}".format(user.mention, job))
            return
        if self.lvl_check(id, 10) and job == "clergy":
            self.jobs[id] = {"name" : user.name, "job" : job}
            fileIO("data/economy/jobs.json", "save", self.jobs)
            await ctx.send("{} has changed their job, the job is {}".format(user.mention, job))
            return
        if self.lvl_check(id, 10) and job == "embalmers":
            self.jobs[id] = {"name" : user.name, "job" : job}
            fileIO("data/economy/jobs.json", "save", self.jobs)
            await ctx.send("{} has changed their job, the job is {}".format(user.mention, job))
            return
        if self.lvl_check(id, 15) and job == "cosplayer":
            self.jobs[id] = {"name" : user.name, "job" : job}
            fileIO("data/economy/jobs.json", "save", self.jobs)
            await ctx.send("{} has changed their job, the job is {}".format(user.mention, job))
            return
        if self.lvl_check(id, 15) and job == "programmer":
            self.jobs[id] = {"name" : user.name, "job" : job}
            fileIO("data/economy/jobs.json", "save", self.jobs)
            await ctx.send("{} has changed their job, the job is {}".format(user.mention, job))

    @_job.command()
    async def register(self, ctx, *, job=None):
        user = ctx.author
        """Registers a job"""
        id = str(ctx.message.author.id)
        if id in self.jobs:
            await ctx.send(f"You already have a job, you should try changing it by doing {ctx.prefix}job change 'job'")
            return
        if job == None:
            await ctx.send("You forgot to put a job")
            return
        if job != "youtuber" and job != "fastfood worker" and job != "child careworker" and job != "barber" and job != "clergy" and job != "embalmers" and job != "cosplayer" and job != "programmer":
            await ctx.send(f"That's not a job, try doing {ctx.prefix}jobs to see all the jobs.")
            return
        if self.lvl_check(id, 1) and job == "youtuber" or job == "fastfood worker":
            self.jobs[id] = {"name" : user.name, "job" : job}
            fileIO("data/economy/jobs.json", "save", self.jobs)
            await ctx.send("{} has gotten a job, the job is {}".format(user.mention, job))
            return
        if self.lvl_check(id, 5) and job == "child careworker":
            self.jobs[id] = {"name" : user.name, "job" : job}
            fileIO("data/economy/jobs.json", "save", self.jobs)
            await ctx.send("{} has gotten a job, the job is {}".format(user.mention, job))
            return
        if self.lvl_check(id, 5) and job == "barber":
            self.jobs[id] = {"name" : user.name, "job" : job}
            fileIO("data/economy/jobs.json", "save", self.jobs)
            await ctx.send("{} has gotten a job, the job is {}".format(user.mention, job))
            return
        if self.lvl_check(id, 10) and job == "clergy":
            self.jobs[id] = {"name" : user.name, "job" : job}
            fileIO("data/economy/jobs.json", "save", self.jobs)
            await ctx.send("{} has gotten a job, the job is {}".format(user.mention, job))
            return
        if self.lvl_check(id, 10) and job == "embalmers":
            self.jobs[id] = {"name" : user.name, "job" : job}
            fileIO("data/economy/jobs.json", "save", self.jobs)
            await ctx.send("{} has gotten a job, the job is {}".format(user.mention, job))
        if self.lvl_check(id, 15) and job == "cosplayer":
            self.jobs[id] = {"name" : user.name, "job" : job}
            fileIO("data/economy/jobs.json", "save", self.jobs)
            await ctx.send("{} has changed their job, the job is {}".format(user.mention, job))
            return
        if self.lvl_check(id, 15) and job == "programmer":
            self.jobs[id] = {"name" : user.name, "job" : job}
            fileIO("data/economy/jobs.json", "save", self.jobs)
            await ctx.send("{} has changed their job, the job is {}".format(user.mention, job))

    @commands.command()
    @commands.cooldown(rate=1, per=3600.0, type=commands.BucketType.user)
    async def work(self, ctx):
        failed_randint = random.randint(1, 10)
        successful_randint = random.randint(100, 150)
        author = ctx.message.author
        id = str(ctx.message.author.id)
        jobchoice = ["failed", "successful"]
        chance = random.choice(jobchoice)
        if id not in self.jobs:
                await ctx.send("{} You don't have a job. Type {}job register 'job name' to get one.".format(author.mention, ctx.prefix))
                return
        if self.hasjob_check(id, "youtuber"):
            if chance == "failed":
                await ctx.send(f"Yikes your video didn't do to well maybe make a better one next time, you received {failed_randint} coins.")
                self.add_money(id, failed_randint)
                return
            if chance == "successful":
                await ctx.send(f"Your video did pretty well congratz, you received {successful_randint} coins.")
                self.add_money(id, successful_randint)
                return
        if self.hasjob_check(id, "fastfood worker"):
            if chance == "failed":
                await ctx.send(f"You couldn't flip those burgers fast enough you failed, you received {failed_randint} coins.")
                self.add_money(id, failed_randint)
                return
            if chance == "successful":
                await ctx.send(f"You sure are making those good hamburgers, you received {successful_randint} coins.")
                self.add_money(id, successful_randint)
                return
        failed_randint2 = random.randint(1, 20)
        successful_randint2 = random.randint(150, 200)
        if self.hasjob_check(id, "barber"):
            if chance == "failed":
                await ctx.send(f"You messed up that mans cut, you received {failed_randint2} coins.")
                self.add_money(id, failed_randint2)
                return
            if chance == "successful":
                await ctx.send(f"You smack him in the back of the head, and say I like yuh cut g, you received {successful_randint2} coins.")
                self.add_money(id, successful_randint2)
                return
        if self.hasjob_check(id, "child careworker"):
            if chance == "failed":
                await ctx.send(f"You lost track of a child, how could you!, you received {failed_randint2} coins.")
                self.add_money(id, failed_randint2)
                return
            if chance == "successful":
                await ctx.send(f"You kept everything in order, way to go!, you received {successful_randint2} coins.")
                self.add_money(id, successful_randint2)
                return
        failed_randint3 = random.randint(1, 30)
        successful_randint3 = random.randint(200, 250)
        if self.hasjob_check(id, "clergy"):
            if chance == "failed":
                await ctx.send(f"You didn't pray good enough, you received {failed_randint3} coins.")
                self.add_money(id, failed_randint3)
                return
            if chance == "successful":
                await ctx.send(f"You keeping the praise goin, you received {successful_randint3} coins.")
                self.add_money(id, successful_randint3)
                return
        if self.hasjob_check(id, "embalmers"):
            if chance == "failed":
                await ctx.send(f"You lost a body, how???? you received {failed_randint3} coins.")
                self.add_money(id, failed_randint3)
                return
            if chance == "successful":
                await ctx.send(f"You kept the body safe, you received {successful_randint3} coins.")
                self.add_money(id, successful_randint3)
                return
        failed_randint4 = random.randint(1, 40)
        successful_randint4 = random.randint(250, 300)
        if self.hasjob_check(id, "cosplayer"):
            if chance == "failed":
                await ctx.send(f"Your cosplay sucked, you received {failed_randint4} coins.")
                self.add_money(id, failed_randint3)
                return
            if chance == "successful":
                await ctx.send(f"People wanted to kiss you, that's a bit weird but ok, you received {successful_randint4} coins.")
                self.add_money(id, successful_randint3)
                return
        if self.hasjob_check(id, "programmer"):
            if chance == "failed":
                await ctx.send(f"Your code gave everyone a virius, you received {failed_randint4} coins.")
                self.add_money(id, failed_randint3)
                return
            if chance == "successful":
                await ctx.send(f"Your code was great everyone loved it, you received {successful_randint4} coins.")
                self.add_money(id, successful_randint3)
                return

    @commands.command(aliases=['bal'])
    async def balance(self, ctx, user : discord.Member=None):
        author_id = str(ctx.message.author.id)
        author = ctx.message.author
        """Shows balance of user.
        Defaults to yours."""
        if not user:
            if self.account_check(author_id):
                await ctx.send("{} Your balance is: {}".format(author.mention, str(self.check_balance(author_id))))
            else:
                await ctx.send("{} You don't have an account at the Biteki bank. Type {}bank register to open one.".format(author.mention, ctx.prefix))
        else:
            user_id = str(user.id)
            if self.account_check(user_id):
                balance = self.check_balance(user_id)
                await ctx.send("{}'s balance is {}".format(user.name, str(balance)))
            else:
                await ctx.send("That user has no bank account.")

    @commands.command()
    async def transfer(self, ctx, user : discord.Member, sum : int):
        """Transfer credits to other users"""
        author = ctx.message.author
        id = str(ctx.message.author.id)
        id2 = str(user.id)
        if author == user:
            await ctx.send("You can't transfer money to yourself.")
            return
        if sum < 1:
            await ctx.send("You need to transfer at least 1 credit.")
            return
        if self.account_check(id2):
            if self.enough_money(id, sum):
                self.withdraw_money(id, sum)
                self.add_money(id2, sum)
                logger.info("{}({}) transferred {} credits to {}({})".format(author.name, id, str(sum), user.name, id2))
                await ctx.send("{} credits have been transferred to {}'s account.".format(str(sum), user.name))
            else:
                await ctx.send("You don't have that sum in your bank account.")
        else:
            await ctx.send("That user has no bank account.")

    @commands.command(name="set", pass_context=True)
    @commands.is_owner()
    async def _set(self, ctx, user : discord.Member, sum : int):
        """Sets money of user's bank account
        Admin/owner restricted."""
        author = ctx.message.author
        id = str(ctx.message.author.id)
        id2 = str(user.id)
        done = self.set_money(id2, sum)
        if done:
            logger.info("{}({}) set {} credits to {} ({})".format(author.name, id, str(sum), user.name, id2))
            await ctx.send("{}'s credits have been set to {}".format(user.name, str(sum)))
        else:
            await ctx.send("User has no bank account.")

    @commands.command()
    async def payday(self, ctx):
        """Get some free credits"""
        author = ctx.message.author
        id = str(ctx.message.author.id)
        if self.account_check(id):
            if id in self.payday_register:
                seconds = abs(self.payday_register[id] - int(time.perf_counter()))
                if seconds  >= self.settings["PAYDAY_TIME"]:
                    self.add_money(id, self.settings["PAYDAY_CREDITS"])
                    self.payday_register[id] = int(time.perf_counter())
                    await ctx.send("{} Here, take some credits. Enjoy! (+{} credits!)".format(author.mention, str(self.settings["PAYDAY_CREDITS"])))
                else:
                    await ctx.send("{} Too soon. For your next payday you have to wait {}.".format(author.mention, self.display_time(self.settings["PAYDAY_TIME"] - seconds)))
            else:
                self.payday_register[id] = int(time.perf_counter())
                self.add_money(id, self.settings["PAYDAY_CREDITS"])
                await ctx.send("{} Here, take some credits. Enjoy! (+{} credits!)".format(author.mention, str(self.settings["PAYDAY_CREDITS"])))
        else:
            await ctx.send("{} You need an account to receive credits.".format(author.mention))

    @commands.command(pass_context=True, no_pm=True)
    async def payweek(self, ctx):
        """Get some free credits"""
        author = ctx.message.author
        id = str(ctx.message.author.id)
        if self.account_check(id):
            if id in self.payweek_register:
                seconds = abs(self.payweek_register[id] - int(time.perf_counter()))
                if seconds  >= self.settings["PAYWEEK_TIME"]:
                    self.add_money(id, self.settings["PAYWEEK_CREDITS"])
                    self.payweek_register[id] = int(time.perf_counter())
                    await ctx.send("{} Here, take some credits. Enjoy! (+{} credits!)".format(author.mention, str(self.settings["PAYWEEK_CREDITS"])))
                else:
                    await ctx.send("{} Too soon. For your next payweek you have to wait {}.".format(author.mention, self.display_time(self.settings["PAYWEEK_TIME"] - seconds)))
            else:
                self.payweek_register[id] = int(time.perf_counter())
                self.add_money(id, self.settings["PAYWEEK_CREDITS"])
                await ctx.send("{} Here, take some credits. Enjoy! (+{} credits!)".format(author.mention, str(self.settings["PAYWEEK_CREDITS"])))
        else:
            await ctx.send("{} You need an account to receive credits.".format(author.mention))

    @commands.command()
    @commands.cooldown(rate=1, per=30.0, type=commands.BucketType.user)
    async def beg(self, ctx):
        randint = random.randint(1, 150)
        author = ctx.message.author
        id = str(ctx.message.author.id)
        choice2 = ["failed", "successful"]
        choice = random.choice(choice2)
        list = [f"**Jake Paul** has donated {randint} coins to {author.mention}.", f"**Thanos** has donated {randint} coins to {author.mention}.", f"**Billie Eyelash** has donated {randint} coins to {author.mention}.", f"**Flo from Progressive** has donated {randint} coins to {author.mention}.", f"**Dawn Keebals** has donated {randint} coins to {author.mention}.", f"**mrbutter** has donated {randint} coins to {author.mention}.", f"**Jennifer Lopez** has donated {randint} coins to {author.mention}.", f"**Pewdiepie** has donated {randint} coins to {author.mention}"]
        list2 = [f"**mrbutter**: You really thought I was gonna donate to you, you thought wrong.", f"**Jordan Peele**: No I don't think so", "**Jake Paul**: No I don't have money for you, poor person.", "**Donald Trump**: HAHAHAAH no"]
        donate = random.choice(list)
        failed_donate = random.choice(list2)
        radint2 = random.randint(1, 100)
        if id not in self.bank:
            await ctx.send("{} You don't have an account at the Biteki bank. Type {}bank register to open one.".format(author.mention, ctx.prefix))
        if id in self.threetimes:
            if self.account_check(id):
                if radint2 >= 75:
                    await ctx.send(f"{failed_donate}")
                    return
                if radint2 >= 0:
                    await ctx.send(f"{donate}")
                    self.add_money(id, randint)
                    return
        if self.account_check(id):
            if choice == "successful":
                await ctx.send(f"{donate}")
                self.add_money(id, randint)
                return
            if choice == "failed":
                await ctx.send(f"{failed_donate}")

    def gun_check(self, id):
        if id in self.guns:
            return True
        else:
            return False

    def gun_uses(self, id, amount):
        if self.gun_check(id):
            if self.guns[id]["uses"] >= int(amount):
                self.guns[id]["uses"] = self.guns[id]["uses"] - int(amount)
                fileIO("data/economy/items/gun.json", "save", self.guns)
            else:
                return False
        else:
            return False

    def gun_has(self, id, left):
        if self.gun_check(id):
            if self.guns[id]["uses"] == int(left):
                return True
            else:
                return False
        else:
            return False

    @commands.command()
    @commands.cooldown(rate=1, per=300.0, type=commands.BucketType.user)
    async def rob(self, ctx, user: discord.Member):
        choice = ["failed", "successful", "caught"]
        chance = random.choice(choice)
        user_id = str(user.id)
        author = ctx.message.author
        id = str(ctx.message.author.id)
        if id not in self.bank:
            await ctx.send("{} You don't have an account at the Biteki bank. Type {}bank register to open one.".format(author.mention, ctx.prefix))
        if user_id not in self.bank:
            await ctx.send(f"{user.mention} doesn't have an a account")
            return
        if not self.enough_money(user_id, 500):
            await ctx.send(f"{user.mention} doesn't have over 500 coins.")
            return
        if not self.enough_money(id, 500):
            await ctx.send(f"You don't have over 500 coins.")
            return
        radint = random.randint(1, 100)
        if user_id in self.guns and id in self.guns:
            if self.enough_money(user_id, 500):
                if radint >= 50:
                    await ctx.send(f"You guys had a gun fight, and You({author.mention}) won. You took **500** coins.")
                    self.withdraw_money(user_id, 500)
                    self.add_money(id, 500)
                    if self.gun_has(user_id, 0) and self.gun_has(id, 0):
                        with open('data/economy/items/gun.json', 'r') as f:
                            gun = json.load(f)

                            gun.pop(str(user.id))

                            self.guns = gun

                        with open('data/economy/items/gun.json', 'w') as f:
                            json.dump(gun, f, indent=4)

                        with open('data/economy/items/gun.json', 'r') as f:
                            gun = json.load(f)

                            gun.pop(str(author.id))

                            self.guns = gun

                        with open('data/economy/items/gun.json', 'w') as f:
                            json.dump(gun, f, indent=4)
                        return
                    if self.gun_has(id, 0):
                        self.gun_uses(user_id, 1)
                        with open('data/economy/items/gun.json', 'r') as f:
                            gun = json.load(f)

                            gun.pop(str(author.id))

                            self.guns = gun

                        with open('data/economy/items/gun.json', 'w') as f:
                            json.dump(gun, f, indent=4)
                        return
                    if self.gun_has(user_id, 0):
                        self.gun_uses(id, 1)
                        with open('data/economy/items/gun.json', 'r') as f:
                            gun = json.load(f)

                            gun.pop(str(user.id))

                            self.guns = gun

                        with open('data/economy/items/gun.json', 'w') as f:
                            json.dump(gun, f, indent=4)
                        return
                    self.gun_uses(user_id, 1)
                    self.gun_uses(id, 1)
                    return
                elif radint >= 0:
                    await ctx.send(f"You guys had a gun fight, and {user.mention} won. They took **500** coins.")
                    self.withdraw_money(id, 500)
                    self.add_money(user_id, 500)
                    if self.gun_has(user_id, 0) and self.gun_has(id, 0):
                        with open('data/economy/items/gun.json', 'r') as f:
                            gun = json.load(f)

                            gun.pop(str(user.id))

                            self.guns = gun

                        with open('data/economy/items/gun.json', 'w') as f:
                            json.dump(gun, f, indent=4)

                        with open('data/economy/items/gun.json', 'r') as f:
                            gun = json.load(f)

                            gun.pop(str(author.id))

                            self.guns = gun

                        with open('data/economy/items/gun.json', 'w') as f:
                            json.dump(gun, f, indent=4)
                        return
                    if self.gun_has(id, 0):
                        self.gun_uses(user_id, 1)
                        with open('data/economy/items/gun.json', 'r') as f:
                            gun = json.load(f)

                            gun.pop(str(author.id))

                            self.guns = gun

                        with open('data/economy/items/gun.json', 'w') as f:
                            json.dump(gun, f, indent=4)
                        return
                    if self.gun_has(user_id, 0):
                        self.gun_uses(id, 1)
                        with open('data/economy/items/gun.json', 'r') as f:
                            gun = json.load(f)

                            gun.pop(str(user.id))

                            self.guns = gun

                        with open('data/economy/items/gun.json', 'w') as f:
                            json.dump(gun, f, indent=4)
                        return
                    self.gun_uses(user_id, 1)
                    self.gun_uses(id, 1)
                    return
        if user_id in self.guns:
            if self.enough_money(user_id, 500):
                await ctx.send(f"{user.mention} shot you with a gun, and took **500** coins from you, haha lol.")
                self.withdraw_money(id, 500)
                self.add_money(user_id, 500)
                if self.gun_has(user_id, 0):
                    with open('data/economy/items/gun.json', 'r') as f:
                        gun = json.load(f)

                        gun.pop(str(user.id))

                        self.guns = gun

                    with open('data/economy/items/gun.json', 'w') as f:
                        json.dump(gun, f, indent=4)
                    return
                self.gun_uses(user_id, 1)
                return
        randint = random.randint(500, (self.check_balance(user_id)))
        if chance == "successful":
            if self.enough_money(user_id, 500):
                await ctx.send(f"You robbed {user.mention} for **{randint}** amount of coins, congratz.")
                self.add_money(id, randint)
                self.withdraw_money(user_id, randint)
                return
        if chance == "failed":
            if self.enough_money(id, 500):
                await ctx.send(f"You failed to rob {user.mention}, and got nothing.")
                return
        if chance == "caught":
            if self.enough_money(id, 500):
                await ctx.send(f"You were caught by {user.mention}, and had to pay them **500** coins")
                self.add_money(user_id, 500)
                self.withdraw_money(id, 500)

    @commands.command()
    async def leaderboard(self, ctx):
        """Prints out the leaderboard
        Defaults to top 10""" #Originally coded by Airenkun - edited by irdumb
        top = 10
        bank_sorted = sorted(self.bank.items(), key=lambda x: x[1]["balance"], reverse=True)
        if len(bank_sorted) < top:
            top = len(bank_sorted)
        topten = bank_sorted[:top]
        highscore = ""
        place = 1
        for id in topten:
            highscore += str(f"{place}. ").ljust(len(str(top))+1)
            highscore += (id[1]["name"]+" ").ljust(23-len(str(id[1]["balance"])))
            highscore += str(id[1]["balance"]) + "\n"
            place += 1
        if highscore:
            if len(highscore) < 1985:
                embed=discord.Embed(title="Leaderboard", description="**"+highscore+"**", color=0x8b0000, timestamp=ctx.message.created_at)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
            else:
                await ctx.send("The leaderboard is too big to be displayed. Try with a lower <top> parameter.")
        else:
            await ctx.send("There are no accounts in the bank.")

    @commands.command()
    async def payouts(self, ctx):
        """Shows slot machine payouts"""
        slot_payouts = """Slot machine payouts:
            :two: :two: :six: Bet * 5000
            :four_leaf_clover: :four_leaf_clover: :four_leaf_clover: +1000
            :cherries: :cherries: :cherries: +800
            :two: :six: Bet * 4
            :cherries: :cherries: Bet * 3
            Three symbols: +500
            Two symbols: Bet * 2"""
        await ctx.send(slot_payouts)

    @commands.command(pass_context=True, no_pm=True)
    async def slot(self, ctx, bid : int):
        """Play the slot machine"""
        author = ctx.message.author
        id = str(ctx.message.author.id)
        if self.enough_money(id, bid):
            if id in self.highstakes:
                if bid >= self.settings["SLOT_MIN"] and bid <= self.settings["SLOT_MAX_HIGH"]:
                    if id in self.slot_register:
                        if abs(self.slot_register[id] - int(time.perf_counter()))  >= self.settings["SLOT_TIME"]:
                            self.slot_register[id] = int(time.perf_counter())
                            await self.slot_machine(ctx.message, bid)
                            return
                        else:
                            await ctx.send("Slot machine is still cooling off! Wait {} seconds between each pull".format(self.settings["SLOT_TIME"]))
                            return
                    else:
                        self.slot_register[id] = int(time.perf_counter())
                        await self.slot_machine(ctx.message, bid)
                        return
                else:
                    await ctx.send("{0} Bid must be between {1} and {2}.".format(author.mention, self.settings["SLOT_MIN"], self.settings["SLOT_MAX_HIGH"]))
                    return
        else:
            await ctx.send("{0} You need an account with enough funds to play the slot machine.".format(author.mention))
            return
        if self.enough_money(id, bid):
            if bid >= self.settings["SLOT_MIN"] and bid <= self.settings["SLOT_MAX"]:
                if id in self.slot_register:
                    if abs(self.slot_register[id] - int(time.perf_counter()))  >= self.settings["SLOT_TIME"]:
                        self.slot_register[id] = int(time.perf_counter())
                        await self.slot_machine(ctx.message, bid)
                        return
                    else:
                        await ctx.send("Slot machine is still cooling off! Wait {} seconds between each pull".format(self.settings["SLOT_TIME"]))
                        return
                else:
                    self.slot_register[id] = int(time.perf_counter())
                    await self.slot_machine(ctx.message, bid)
                    return
            else:
                await ctx.send("{0} Bid must be between {1} and {2}.".format(author.mention, self.settings["SLOT_MIN"], self.settings["SLOT_MAX"]))
                return
        else:
            await ctx.send("{0} You need an account with enough funds to play the slot machine.".format(author.mention))

    async def slot_machine(self, message, bid):
        id = str(message.author.id)
        if id in self.threetimes:
            radint = random.randint(0, 100)
            radint2 = random.randint(1, 100)
            radint3 = random.randint(0, 500)
            pattern1 = [":cherries: :cookie: :two:", ":mushroom: :heart: :snowflake:", ":four_leaf_clover: :cyclone: :sunflower:", ":six: :mushroom: :heart:"]
            pattern2 = [":mushroom: :cookie: :two:", ":cherries: :cyclone: :snowflake:", ":four_leaf_clover: :cyclone: :sunflower:", ":heart: :six: :mushroom:"]
            pattern3 = [":two: :cyclone: :mushroom:", ":cookie: :cherries: :snowflake:", ":four_leaf_clover: :snowflake: :sunflower:", ":cyclone: :six: :mushroom:"]
            choice = [":cherries: :two: :six:", ":two: :six: :cookie:", ":two: :four_leaf_clover: :six:", ":cyclone:", ":six: :sunflower: :two:", ":two: :six: :mushroom:", ":heart: :two: :six:", ":two: :snowflake: :six:"]
            choice2 = [":cherries: :cherries: :cookie:", ":two: :cherries: :cherries:", ":cherries: :four_leaf_clover: :cherries: ", ":cyclone: :cherries: :cherries:", ":cherries: :sunflower: :cherries:", ":cherries: :cherries: :six:", ":cherries: :mushroom: :cherries:", ":heart: :cherries: :cherries:", ":cherries: :cherries: :snowflake:"]
            choice5 = [":cookie: :cookie: :two:", ":two: :cookie: :two:", ":cyclone: :four_leaf_clover: :four_leaf_clover:", ":cyclone: :cookie: :cyclone:", ":sunflower: :heart: :sunflower:", ":six: :six: :heart:", ":mushroom: :snowflake: :mushroom:", ":heart: :mushroom: :heart:", ":heart: :snowflake: :snowflake:"]
            choice7 = [":cookie: :cookie: :cookie:", ":two: :two: :two:", ":cyclone: :cyclone: :cyclone:", ":sunflower: :sunflower: :sunflower:", ":mushroom: :mushroom: :mushroom:", ":heart: :heart: :heart:", ":snowflake: :snowflake: :snowflake:"]
            patternran = random.choice(pattern1)
            patternran2 = random.choice(pattern2)
            patternran3 = random.choice(pattern3)
            choice3 = random.choice(choice)
            choice4 = random.choice(choice2)
            choice6 = random.choice(choice5)
            choice8 = random.choice(choice7)
            if radint >= 75:
                await message.channel.send(f"{patternran}\n{patternran3}\n{patternran2}\n{message.author.mention} Nothing! Lost bet.")
                self.withdraw_money(id, bid)
                await message.channel.send("Credits left: {}".format(str(self.check_balance(id))))
                return
            if radint >= 0:
                if radint3 >= 500:
                    bid = bid * 5000
                    await message.channel.send(f"{patternran}\n:two: :two: :six:\n{patternran2}\n{message.author.mention} 226! Your bet is multiplied * 5000! {str(bid)}! ")
                elif radint2 >= 80:
                    bid += 1000
                    await message.channel.send(f"{patternran}\n:four_leaf_clover: :four_leaf_clover: :four_leaf_clover:\n{patternran2}\n{message.author.mention} Three FLC! +1000! ".format(message.author.mention))
                elif radint2 >= 70:
                    bid += 800
                    await message.channel.send(f"{patternran}\n:cherries: :cherries: :cherries:\n{patternran2}\n{message.author.mention} Three cherries! +800! ")
                elif radint2 >= 60:
                    bid += 500
                    await message.channel.send(f"{patternran}\n{choice8}\n{patternran2}\n{message.author.mention} Three symbols! +500! ")
                elif radint2 >= 50:
                    bid = bid * 4
                    await message.channel.send(f"{patternran}\n{choice3}\n{patternran2}\n{message.author.mention} 26! Your bet is multiplied * 4! {str(bid)}! ")
                elif radint2 >= 20:
                    bid = bid * 3
                    await message.channel.send(f"{patternran}\n{choice4}\n{patternran2}\n{message.author.mention} Two cherries! Your bet is multiplied * 3! {str(bid)}! ")
                elif radint2 >= 0:
                    bid = bid * 2
                    await message.channel.send(f"{patternran}\n{choice6}\n{patternran2}\n{message.author.mention} Two symbols! Your bet is multiplied * 2! {str(bid)}! ")
                self.add_money(id, bid)
                await message.channel.send("Current credits: {}".format(str(self.check_balance(id))))
                return
        reel_pattern = [":cherries:", ":cookie:", ":two:", ":four_leaf_clover:", ":cyclone:", ":sunflower:", ":six:", ":mushroom:", ":heart:", ":snowflake:"]
        padding_before = [":mushroom:", ":heart:", ":snowflake:"] # padding prevents index errors
        padding_after = [":cherries:", ":cookie:", ":two:"]
        reel = padding_before + reel_pattern + padding_after
        reels = []
        for i in range(0, 3):
            n = randint(3,12)
            reels.append([reel[n - 1], reel[n], reel[n + 1]])
        line = [reels[0][1], reels[1][1], reels[2][1]]

        display_reels = "  " + reels[0][0] + " " + reels[1][0] + " " + reels[2][0] + "\n"
        display_reels += ">" + reels[0][1] + " " + reels[1][1] + " " + reels[2][1] + "\n"
        display_reels += "  " + reels[0][2] + " " + reels[1][2] + " " + reels[2][2] + "\n"

        if line[0] == ":two:" and line[1] == ":two:" and line[2] == ":six:":
            bid = bid * 5000
            await message.channel.send("{}{} 226! Your bet is multiplied * 5000! {}! ".format(display_reels, message.author.mention, str(bid)))
        elif line[0] == ":four_leaf_clover:" and line[1] == ":four_leaf_clover:" and line[2] == ":four_leaf_clover:":
            bid += 1000
            await message.channel.send("{}{} Three FLC! +1000! ".format(display_reels, message.author.mention))
        elif line[0] == ":cherries:" and line[1] == ":cherries:" and line[2] == ":cherries:":
            bid += 800
            await message.channel.send("{}{} Three cherries! +800! ".format(display_reels, message.author.mention))
        elif line[0] == line[1] == line[2]:
            bid += 500
            await message.channel.send("{}{} Three symbols! +500! ".format(display_reels, message.author.mention))
        elif line[0] == ":two:" and line[1] == ":six:" or line[1] == ":two:" and line[2] == ":six:":
            bid = bid * 4
            await message.channel.send("{}{} 26! Your bet is multiplied * 4! {}! ".format(display_reels, message.author.mention, str(bid)))
        elif line[0] == ":cherries:" and line[1] == ":cherries:" or line[1] == ":cherries:" and line[2] == ":cherries:":
            bid = bid * 3
            await message.channel.send("{}{} Two cherries! Your bet is multiplied * 3! {}! ".format(display_reels, message.author.mention, str(bid)))
        elif line[0] == line[1] or line[1] == line[2]:
            bid = bid * 2
            await message.channel.send("{}{} Two symbols! Your bet is multiplied * 2! {}! ".format(display_reels, message.author.mention, str(bid)))
        else:
            await message.channel.send("{}{} Nothing! Lost bet. ".format(display_reels, message.author.mention))
            self.withdraw_money(id, bid)
            await message.channel.send("Credits left: {}".format(str(self.check_balance(id))))
            return True
        self.add_money(id, bid)
        await message.channel.send("Current credits: {}".format(str(self.check_balance(id))))

    def job_check(self, id):
        if id in self.jobs:
            return True
        else:
            return False

    def hasjob_check(self, id, work):
        if self.account_check(id):
            if self.jobs[id]["job"] == str(work):
                return True
            else:
                return False
        else:
            return False

    def canwork_check(self, id):
        if self.job_check(id):
            return self.jobs[id]["job"]
        else:
            return False

    def account_check(self, id):
        if id in self.bank:
            return True
        else:
            return False

    def check_job(self, id):
        if self.account_check(id):
            return self.jobs[id]["job"]
        else:
            return False

    def check_balance(self, id):
        if self.account_check(id):
            return self.bank[id]["balance"]
        else:
            return False

    def add_money(self, id, amount):
        if self.account_check(id):
            self.bank[id]["balance"] = self.bank[id]["balance"] + int(amount)
            fileIO("data/economy/bank.json", "save", self.bank)
        else:
            return False

    def withdraw_money(self, id, amount):
        if self.account_check(id):
            if self.bank[id]["balance"] >= int(amount):
                self.bank[id]["balance"] = self.bank[id]["balance"] - int(amount)
                fileIO("data/economy/bank.json", "save", self.bank)
            else:
                return False
        else:
            return False

    def enough_money(self, id, amount):
        if self.account_check(id):
            if self.bank[id]["balance"] >= int(amount):
                return True
            else:
                return False
        else:
            return False

    def set_money(self, id, amount):
        if self.account_check(id):
            self.bank[id]["balance"] = amount
            fileIO("data/economy/bank.json", "save", self.bank)
            return True
        else:
            return False

    def has_lvl(self, id):
        if id in self.levels:
            return True
        else:
            return False

    def lvl_check(self, id, lvl):
        if self.has_lvl(id):
            if self.levels[id]["level"] >= int(lvl):
                return True
            else:
                return False
        else:
            return False

    def display_time(self, seconds, granularity=2): # What would I ever do without stackoverflow?
        intervals = (                               # Source: http://stackoverflow.com/a/24542445
            ('weeks', 604800),  # 60 * 60 * 24 * 7
            ('days', 86400),    # 60 * 60 * 24
            ('hours', 3600),    # 60 * 60
            ('minutes', 60),
            ('seconds', 1),
            )

        result = []

        for name, count in intervals:
            value = seconds // count
            if value:
                seconds -= value * count
                if value == 1:
                    name = name.rstrip('s')
                result.append("{} {}".format(value, name))
        return ', '.join(result[:granularity])

def setup(client):
    global logger
    logger = logging.getLogger("economy")
    if logger.level == 0: # Prevents the logger from being loaded again in case of module reload
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(filename='data/economy/economy.log', encoding='utf-8', mode='a')
        handler.setFormatter(logging.Formatter('%(asctime)s %(message)s', datefmt="[%d/%m/%Y %H:%M]"))
        logger.addHandler(handler)
    client.add_cog(Economy(client))
