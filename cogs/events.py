import discord
import os
import sys
from discord.ext import commands
import yaml
sys.path.append('/home/BreadLoaf/breadbot/cogs/extras/')
from .extras.checks import is_bread, is_admin, is_mod, is_member

class Events(commands.Cog):
  def __init__(self, client):
    self.client = client

  # Events
  @commands.Cog.listener()
  async def on_ready(self):
    print(f"We have logged in as {self.client.user}")

  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    emoji = str(payload.emoji)
    guild = discord.utils.find(lambda g : g.id == payload.guild_id, self.client.guilds)
    member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
    if member != self.client.user:
      try:
        with open(os.path.join(os.path.dirname(__file__), 'data/reaction_roles.yaml'), 'r') as file:
          reaction_roles = yaml.safe_load(file)
        role = discord.utils.get(guild.roles, name=reaction_roles[emoji]['role'])
        msg = reaction_roles[emoji]['msg id']
        if str(payload.message_id) == str(msg):
          await member.add_roles(role)
          print(f"Added role {role} to user {member}")
      except:
        return
    else:
      return

  @commands.Cog.listener()
  async def on_raw_reaction_remove(self, payload):
    emoji = str(payload.emoji)
    guild = discord.utils.find(lambda g : g.id == payload.guild_id, self.client.guilds)
    member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
    if member != self.client.user:
      try:
        with open(os.path.join(os.path.dirname(__file__), 'data/reaction_roles.yaml'), 'r') as file:
          reaction_roles = yaml.safe_load(file)
        role = discord.utils.get(guild.roles, name=reaction_roles[emoji]['role'])
        msg = reaction_roles[emoji]['msg id']
        if str(payload.message_id) == str(msg):
          await member.remove_roles(role)
          print(f"Removed role {role} from user {member}")
      except:
        return
    else:
      return

  @commands.Cog.listener()
  async def on_message(self, message):
    if str(message.channel.id) not in ("915009261329862696", "914165344631918622"):
      msg = message.content
      auth = str(message.author)
      print(f'Message from {auth}: {msg}')
      #await self.client.process_commands(message)

  @commands.Cog.listener()
  async def on_member_join(self, member):
    print(f"{member} has joined the server")
    #role = discord.utils.get(member.guild.roles, name = 'BreadSlice')
    #await member.add_roles(role)
    #print(f'{member} was given {role}')

  @commands.Cog.listener()
  async def on_member_remove(self, member):
    print(f"{member} has left the server")

  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    if isinstance(error, discord.ext.commands.errors.CheckFailure): # checking which type of error it is
        await ctx.send("You do not have permission to run that command", delete_after=5)
    else:
        print(f"Error: {error}")
        #await ctx.send(error)

def setup(client):
  client.add_cog(Events(client))