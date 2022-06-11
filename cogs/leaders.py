import discord
import os
import sys
from discord.ext import commands
import yaml
sys.path.append('/home/BreadLoaf/breadbot/cogs/extras/')
from .extras.checks import is_bread, is_admin, is_mod, is_member, is_leader

class Leader(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command()
  async def print_guild(self, ctx):
    with open(os.path.join(os.path.dirname(__file__), 'data/discord_guilds.yaml'), 'r') as file:
      guilds = yaml.safe_load(file)['guilds']

    print(guilds)

  @commands.command(aliases=['agr'])
  @is_leader()
  async def addguildrole(self, ctx, *args):

    user = ""
    for arg in args:
      user = f"{user}{arg} "
    user = user[:-1]

    user = discord.utils.get(ctx.guild.members, name=user)

    with open(os.path.join(os.path.dirname(__file__), 'data/discord_guilds.yaml'), 'r') as file:
      guilds = yaml.safe_load(file)['guilds']

    if ctx.message.channel.id == guilds['legion']['channel']: # Legion
      await user.add_roles(discord.utils.get(ctx.guild.roles, id=guilds['legion']['role']))
      await ctx.send(f'{user} has been given the Legion role')

    elif ctx.message.channel.id == guilds['legion unsullied']['channel']: # Legion Unsullied
      await user.add_roles(discord.utils.get(ctx.guild.roles, id=guilds['legion unsullied']['role']))
      await ctx.send(f'{user} has been given the Legion Unsullied role')

    elif ctx.message.channel.id == guilds['legion of alpacas']['channel']: # Legion Of Alpacas
      await user.add_roles(discord.utils.get(ctx.guild.roles, id=guilds['legion of alpacas']['role']))
      await ctx.send(f'{user} has been given the Legion Of Alpacas role')

    elif ctx.message.channel.id == guilds['legion of anarchy']['channel']: # Legion Of Anarchy
      await user.add_roles(discord.utils.get(ctx.guild.roles, id=guilds['legion of anarchy']['role']))
      await ctx.send(f'{user} has been given the Legion Of Anarchy role')

    elif ctx.message.channel.id == guilds['legion revenant']['channel']: # Legion Revenant
      await user.add_roles(discord.utils.get(ctx.guild.roles, id=guilds['legion revenant']['role']))
      await ctx.send(f'{user} has been given the Legion Revenant role')

    elif ctx.message.channel.id == guilds['legionaires']['channel']: # Legionaires
      await user.add_roles(discord.utils.get(ctx.guild.roles, id=guilds['legionaires']['role']))
      await ctx.send(f'{user} has been given the Legionaire role')

    elif ctx.message.channel.id == guilds['legion of titans']['channel']: # Legion Of Titans
      await user.add_roles(discord.utils.get(ctx.guild.roles, id=guilds['legion of titans']['role']))
      await ctx.send(f'{user} has been given the LegionOfTitans role')

    elif ctx.message.channel.id == guilds['legion of horizons']['channel']: # Legion Of Horizons
      await user.add_roles(discord.utils.get(ctx.guild.roles, id=guilds['legion of horizons']['role']))
      await ctx.send(f'{user} has been given the Legion Of Horizons role')

    elif ctx.message.channel.id == guilds['antilegion']['channel']: # AntiLegion
      await user.add_roles(discord.utils.get(ctx.guild.roles, id=guilds['antilegion']['role']))
      await ctx.send(f'{user} has been given the AntiLegion role')

    elif ctx.message.channel.id == 912200234896076821: # Test room
      await user.add_roles(discord.utils.get(ctx.guild.roles, id=912201757394886666))
      await ctx.send(f'{user} has been given the Test role')

    else:
      await ctx.send(f'I was unable to give {user} a role, make sure you are in a Guild channel.')

  @commands.command(aliases=['rgr'])
  @is_leader()
  async def removeguildrole(self, ctx, user: discord.Member):

    with open(os.path.join(os.path.dirname(__file__), 'data/discord_guilds.yaml'), 'r') as file:
      guilds = yaml.safe_load(file)['guilds']

    if ctx.message.channel.id == guilds['legion']['channel']: # Legion
      await user.remove_roles(discord.utils.get(ctx.guild.roles, id=guilds['legion']['role']))
      await ctx.send(f'Removed Legion role from {user}')

    elif ctx.message.channel.id == guilds['legion unsullied']['channel']: # Legion Unsullied
      await user.remove_roles(discord.utils.get(ctx.guild.roles, id=guilds['legion unsullied']['role']))
      await ctx.send(f'Removed Legion Unsullied role from {user}')

    elif ctx.message.channel.id == guilds['legion of alpacas']['channel']: # Legion Of Alpacas
      await user.remove_roles(discord.utils.get(ctx.guild.roles, id=guilds['legion of alpacas']['role']))
      await ctx.send(f'Removed Legion Of Alpacas role from {user}')

    elif ctx.message.channel.id == guilds['legion of anarchy']['channel']: # Legion Of Anarchy
      await user.remove_roles(discord.utils.get(ctx.guild.roles, id=guilds['legion of anarchy']['role']))
      await ctx.send(f'Removed Legion Of Anarchy role from {user}')

    elif ctx.message.channel.id == guilds['legion revenant']['channel']: # Legion Revenant
      await user.remove_roles(discord.utils.get(ctx.guild.roles, id=guilds['legion revenant']['role']))
      await ctx.send(f'Removed Legion Revenant role from {user}')

    elif ctx.message.channel.id == guilds['legionaires']['channel']: # Legionaires
      await user.remove_roles(discord.utils.get(ctx.guild.roles, id=guilds['legionaires']['role']))
      await ctx.send(f'Removed Legionaires role from {user}')

    elif ctx.message.channel.id == guilds['legion of titans']['channel']: # Legion Of Titans
      await user.remove_roles(discord.utils.get(ctx.guild.roles, id=guilds['legion of titans']['role']))
      await ctx.send(f'Removed LegionOfTitans role from {user}')

    elif ctx.message.channel.id == guilds['legion of horizons']['channel']: # Legion of horizons
      await user.remove_roles(discord.utils.get(ctx.guild.roles, id=guilds['legion of horizons']['role']))
      await ctx.send(f'Removed LegionOfHorizons role from {user}')

    elif ctx.message.channel.id == guilds['antilegion']['channel']: # Anti Legion
      await user.remove_roles(discord.utils.get(ctx.guild.roles, id=guilds['antilegion']['role']))
      await ctx.send(f'Removed AntiLegion role from {user}')

    elif ctx.message.channel.id == 912200234896076821: # Test room
      await user.remove_roles(discord.utils.get(ctx.guild.roles, id=912201757394886666))
      await ctx.send(f'Removed Test role from {user}')

    else:
      await ctx.send(f'I was unable to remove a role from {user}, make sure you are in a Guild channel.')

  @commands.command()
  @is_leader()
  async def pin(self, ctx, *, message):
    if ctx.message.channel.id in [878440364380418069,898545942976954478,878443257477087242,878443456182243388,878443485114548274,879291754149478420,912200234896076821]:
      sent_message = await ctx.send(f"Author: {ctx.author}\n{message}")
      await sent_message.pin()
      await ctx.delete()

def setup(client):
  client.add_cog(Leader(client))