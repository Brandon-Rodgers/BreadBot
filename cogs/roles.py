import discord
import os
import sys
from discord.ext import commands
import yaml
sys.path.append('/home/BreadLoaf/breadbot/cogs/extras/')
from .extras.checks import is_bread, is_admin, is_mod, is_member

class Roles(commands.Cog):
  def __init__(self, client):
    self.client = client

  # Commands
  @commands.command()
  @is_mod()
  async def roles(self, ctx):
    print(ctx.guild.roles)

  @commands.command(aliases=['giver'])
  @is_mod()
  async def giverole(self, ctx, role: discord.Role, user: discord.Member):
    if ctx.author.guild_permissions.manage_roles:
      await user.add_roles(role)

  @commands.command(aliases=["removerole",'remover', 'remr', "rr"])
  @is_mod()
  async def remrole(self, ctx, role: discord.Role, user: discord.Member):
    if ctx.author.guild_permissions.manage_roles:
      await user.remove_roles(role)

  @commands.command()
  @is_mod()
  async def addrr(self, ctx, msg: discord.Message, emoji, role):
    new_rr = {'role': f'{role}',
              'msg id': f'{msg.id}',
            }

    with open(os.path.join(os.path.dirname(__file__), 'data/reaction_roles.yaml'), 'r') as file:
      reaction_roles = yaml.safe_load(file)
    reaction_roles[emoji] = new_rr
    with open(os.path.join(os.path.dirname(__file__), 'data/reaction_roles.yaml'), 'w') as file:
      yaml.dump(reaction_roles, file)

    await msg.add_reaction(emoji)
    await ctx.message.delete()

  @commands.command(aliases=['remrr'])
  @is_mod()
  async def removerr(self, ctx, msg: discord.Message, emoji: str):
    with open(os.path.join(os.path.dirname(__file__), 'data/reaction_roles.yaml'), 'r') as file:
      reaction_roles = yaml.safe_load(file)
    try:
      del reaction_roles[emoji]
    except:
      print(f"No reaction roles exist for {emoji}")
    with open(os.path.join(os.path.dirname(__file__), 'data/reaction_roles.yaml'), 'w') as file:
      yaml.dump(reaction_roles, file)

    reaction = discord.utils.get(msg.reactions, emoji=emoji)
    async for user in reaction.users():
      await reaction.remove(user)

    await ctx.message.delete()

  @commands.command()
  @is_mod()
  async def addroleall(self, ctx, role: discord.Role):
    for m in ctx.guild.members:
      await m.add_roles(role)

  @commands.command()
  @is_mod()
  async def remroleall(self, ctx, role: discord.Role):
    for m in ctx.guild.members:
      await m.remove_roles(role)

def setup(client):
  client.add_cog(Roles(client))