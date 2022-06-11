import discord
import os
import sys
from asyncio import sleep
import time
import random
from discord.ext import commands
import random
import yaml
sys.path.append('/home/BreadLoaf/breadbot/cogs/extras/')
from .extras.checks import is_bread, is_admin, is_mod, is_member

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.ligma_stop = False

    @commands.command()
    async def darkness(self, ctx):
        await ctx.message.delete()
        await ctx.send(file=discord.File("/home/BreadLoaf/breadbot/cogs/images/darkness.png"), delete_after=5)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg = f'**Still on cooldown**, please try again in {round(error.retry_after)}s'
            await ctx.send(msg)

    @commands.command()
    @commands.cooldown(1,3600,commands.BucketType.user)
    async def ligma(self, ctx):
        images = ['gay','lima.png','ligma1.png','ligma2.png','ligma3.png','ligma4.png','ligma5.png','longestdrive.gif','ha.gif']
        image = random.choice(images)
        if ctx.author.id == 508163321099190272:
            image = 'gay'
        if ctx.author.id == 230571781490999296:
            image = random.choice(['lima.png','ligma1.png','ligma2.png','ligma3.png','ligma4.png','ligma5.png','longestdrive.gif','ha.gif'])
        if image == 'gay':
            await ctx.send(f'Ha! {ctx.author.display_name} is GAAAY!!')
        else:
            await ctx.send(file=discord.File(f"/home/BreadLoaf/breadbot/cogs/images/{image}"))

    @commands.command(aliases=['🍞'])
    async def bread(self, ctx, number : int = 5):
        if number < 10 or ctx.author.id == 230571781490999296:
            await ctx.message.delete()
            async for msg in ctx.message.channel.history(limit = number):
                await msg.add_reaction('🍞')
        else:
            await ctx.send("The limit of bread is 10", delete_after=3)

    @commands.command()
    @is_bread()
    async def draw(self, ctx, msg_id: int, emoji, count=1):
        try:
            await ctx.message.delete()
            msg = await ctx.fetch_message(msg_id)
            reaction = discord.utils.get(msg.reactions, emoji=emoji)
            users = [i.id async for i in reaction.users()]

            if count > 1:
                winner_message = "**The winners are**\n"
                for i in range(count):
                    winner = users.pop(random.randint(0, len(users)-1))
                    winner_message += f"{i+1}: <@{winner}>\n"
            elif count <= 1:
                winner_message = f"The winner is <@{users.pop(random.randint(0, len(users)-1))}>"

            await ctx.send(winner_message)
        except Exception as e:
            await ctx.send(e)

    @commands.command()
    @is_bread()
    async def draw2(self, ctx, msg_id: int, emoji, count=1):
        try:
            await ctx.message.delete()
            msg = await ctx.fetch_message(msg_id)
            reaction = discord.utils.get(msg.reactions, emoji=emoji)
            users = [i.id async for i in reaction.users()]

            if count > 1:
                winner_message = "**The winners are**\n"
                for i in range(count):
                    winner = users.pop(random.randint(0, len(users)-1))
                    winner_message += f"{i+1}: <@230571781490999296>\n"
            elif count <= 1:
                winner_message = f"The winner is <@230571781490999296>"

            await ctx.send(winner_message)
        except Exception as e:
            await ctx.send(e)


def setup(client):
    client.add_cog(Fun(client))