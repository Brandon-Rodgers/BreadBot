import discord
import os
import sys
from discord.ext import commands
import yaml
sys.path.append('/home/BreadLoaf/breadbot/cogs/extras/')
from .extras.checks import is_bread, is_admin, is_mod, is_member, is_leader

class Help(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command()
  async def help(self, ctx, info=None):
    await ctx.send("Sorry, the help command has not been setup yet.")


def setup(client):
  client.add_cog(Help(client))