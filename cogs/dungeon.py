import discord
import os
import sys
from discord.ext import commands
import yaml
sys.path.append('/home/BreadLoaf/breadbot/cogs/extras/')
from .extras.checks import is_bread, is_admin, is_mod, is_member

class Dungeon(commands.Cog):
  def __init__(self, client):
    self.client = client

  # Commands
  @commands.command(aliases=["d"])
  async def dungeon(self, ctx):
    embed = discord.Embed(name=f"{ctx.author}",title="Dungeon Event", description="This information is for pushing the last of the event, a weaker and faster team can be used in the beginning.", color=0xFF5733)
    embed.set_author(name=f"{ctx.author.display_name}", icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url="https://imgur.com/8W7CKqQ.jpg")

    embed.add_field(name="Dungeon Event Team", value="Mary - giant slayer, power 3, shattering blow\nRemus - 2x physical resist, shattering blow\nHerc - second wind, physical resist, shattering blow\nSam - 3x omni resist, crit\nHeim/Grey - 3x omni resist, crit")

    embed.set_footer(text="*This is not guaranteed the best team, but it has worked for many.\nOmni resist can be replaced with Chance Resist if you get stuck. A little luck can go a long way.*")


    if ctx.channel.id == 914936919731871785 or ctx.channel.id == 912200234896076821:
      await ctx.send(embed=embed)
    else:
      await ctx.send("Please use the #breadbot-stuff channel!", delete_after=10)
      await ctx.message.delete()

def setup(client):
  client.add_cog(Dungeon(client))