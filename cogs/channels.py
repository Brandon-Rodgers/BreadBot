import discord
import os
import sys
from discord.ext import commands
import yaml
sys.path.append('/home/BreadLoaf/breadbot/cogs/extras/')
from .extras.checks import is_bread, is_admin, is_mod, is_member

class Channels(commands.Cog):
  def __init__(self, client):
    self.client = client

  # Commands
  @commands.command()
  async def channels(self, ctx):
    await ctx.send("Pong!")


def setup(client):
  client.add_cog(Channels(client))