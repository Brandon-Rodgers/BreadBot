import discord
import os
import sys
from discord.ext import commands
import yaml
sys.path.append('/home/BreadLoaf/breadbot/cogs/extras/')
from .extras.checks import is_bread, is_admin, is_mod, is_member

class Boss(commands.Cog):
  def __init__(self, client):
    self.client = client

  # Commands
  @commands.command(aliases=['bf'])
  async def bossformations(self, ctx, form: int = None):
    if form == 1:
      embed1 = discord.Embed(name=f"{ctx.author}",title="Boss Formations", description="These formations are for keeping the mages from walking up on the boss. From testing about 5 out of 7 fights the mages will stay far enough back", color=0xFF5733)
      embed1.set_author(name=f"{ctx.author.display_name}", icon_url=ctx.author.avatar_url)
      embed1.set_thumbnail(url="https://imgur.com/ya1qCfH.jpg")

      embed1.add_field(name="1 Warrior Team", value="From top to bottom: Archer, Mage, Warrior, Mage, Mage.\nThe first archer and mage should be able to be swapped, but this has not been tested.")
      embed1.set_image(url="https://imgur.com/GHWxm2C.jpg")

      embed = embed1

    if form == 2:
      embed2 = discord.Embed(name=f"{ctx.author}",title="Boss Formations", description="These formations are for keeping the mages from walking up on the boss. From testing about 5 out of 7 fights the mages will stay far enough back", color=0xFF5733)
      embed2.set_author(name=f"{ctx.author.display_name}", icon_url=ctx.author.avatar_url)
      embed2.set_thumbnail(url="https://imgur.com/MlHlZ4B.jpg")

      embed2.add_field(name="2 Warrior Team", value="From top to bottom: Mage, Warrior, Warrior, Mage.\nArcher can go behind either mage, but make sure the mages are as far in the corners as possible.")
      embed2.set_image(url="https://imgur.com/s8CyTC1.jpg")

      embed = embed2

    if ctx.channel.id == 914936919731871785 and form != None:
      await ctx.send(embed=embed)
    elif ctx.channel.id == 914936919731871785 and form == None:
      await ctx.send("Please use 1 or 2 to select how many warriors are going to be in your formation.\n*Example: `.bf 1`*")
    else:
      await ctx.send("Please use the #breadbot-stuff channel!", delete_after=10)
      await ctx.message.delete()

  @commands.command(aliases=["bt"])
  async def bossteams(self, ctx, team=None):
    embed = discord.Embed(name=f"{ctx.author}",title="Possible Boss Teams", description="These are tested to be some of the best teams, but can always be improved on and will not work for everyone.", color=0xFF5733)
    embed.set_author(name=f"{ctx.author.display_name}", icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url="https://imgur.com/MlHlZ4B.jpg")

    if team in ("max","Max", None):
      embed.add_field(name="Max DPS Teams", value="These teams are for the most damage output if your Front Line does not die.\nGrouch will do the most damage if he can survive. Replace Guan in team 1, or leo in team 2 for the best lineup.", inline = False)

      embed.add_field(name="Max Damage 1", value="Edward - Giant slayer, power 3, smite, repulsion\nGuan - giant slayer, power 3, smite\nKronos - giant slayer, power 3, smite\nRiddle - second wind, power 3, smite\nElfa - giant slayer, power 3, smite", inline=True)
      embed.add_field(name="Max Damage 2", value="Leo - Giant slayer, power 3, smite\nGuan - giant slayer, power 3, smite\nKronos - giant slayer, power 3, smite\nRiddle - second wind, power 3, smite\nElfa - giant slayer, power 3, smite", inline=True)

    if team in ("high","High","h",None):
      embed.add_field(name="High Damage Teams", value="These teams are for more survivability if your front line keeps getting killed before 60s is up.", inline = False)

      embed.add_field(name="High Damage 1", value="Leo - Giant slayer, power 3, smite\nHerc - giant slayer, power 3, smite\nKronos - giant slayer, power 3, smite\nRiddle - second wind, power 3, smite\nElfa - giant slayer, power 3, smite", inline=True)
      embed.add_field(name="High Damage 2", value="Leo - Giant slayer, power 3, smite\nEdward - second wind, physical resist, vamp, repulsion\nKronos - giant slayer, power 3, smite\nRiddle - second wind, power 3, smite\nElfa - giant slayer, power 3, smite", inline=True)

    if team in ("mid","Mid", None):
      embed.add_field(name="Mid Damage Teams", value="These teams add Mary to allow front line to survive the full 60s.", inline = False)

      embed.add_field(name="Mid Damage 1", value="Guan - Giant slayer, power 3, smite\nMary - giant slayer, power 3, smite\nKronos - giant slayer, power 3, smite\nRiddle - second wind, power 3, smite\nElfa - giant slayer, power 3, smite", inline=True)
      embed.add_field(name="Mid Damage 2", value="Leo - Giant slayer, power 3, smite\nMary - giant slayer, power 3, smite\nKronos - giant slayer, power 3, smite\nRiddle - second wind, power 3, smite\nElfa - giant slayer, power 3, smite", inline=True)

    if team in ("low","Low","l", None):
      embed.add_field(name="Low Damage Teams", value="These teams switch to survivability enchant to get through the 60s.", inline = False)

      embed.add_field(name="Low Damage 1", value="Leo - second wind, physical resist, smite\nMary - giant slayer, power 3, smite\nKronos - giant slayer, power 3, smite\nRiddle - second wind, power 3, smite\nElfa - giant slayer, power 3, smite", inline=True)
      embed.add_field(name="Low Damage 2", value="Herc - second wind, physical resist, smite\nMary - giant slayer, power 3, smite\nKronos - giant slayer, power 3, smite\nRiddle - second wind, power 3, smite\nElfa - giant slayer, power 3, smite", inline=True)

    embed.add_field(name="Extra Info", value="- For stronger bosses Giant Slayer can be replaced by Sword Breaker.\n- If the hero has 4 enchants they are running sword and dagger.", inline = False)

    embed.set_footer(text="*These are not guaranteed the best squads to use, but will give a good amount of kills.\nIf you have a better team, post the formation and enchants in the boss tips room and @BreadLoaf.*")

    if ctx.channel.id == 914936919731871785:
      await ctx.send(embed=embed)
    else:
      await ctx.send("Please use the #breadbot-stuff channel!", delete_after=10)
      await ctx.message.delete()

def setup(client):
  client.add_cog(Boss(client))