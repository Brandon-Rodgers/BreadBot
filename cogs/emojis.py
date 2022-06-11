import discord
import os
import sys
from discord.ext import commands
import yaml
sys.path.append('/home/BreadLoaf/breadbot/cogs/extras/')
from .extras.checks import is_bread, is_admin, is_mod, is_member

class Emojis(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command("adde")
  @is_mod()
  async def addemoji(self, ctx, msg_id: int, emoji):
    print(emoji)
    msg = await ctx.fetch_message(msg_id)
    await msg.add_reaction(emoji)
    await ctx.message.delete()

  @commands.command(aliases=["reme", "removeemoji"])
  @is_mod()
  async def rememoji(self, ctx, msg_id: int, emoji):
    msg = await ctx.fetch_message(msg_id)
    await msg.remove_reaction(emoji, self.client.user)
    await ctx.message.delete()

def setup(client):
  client.add_cog(Emojis(client))