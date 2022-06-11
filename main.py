#Add Bot URL: https://discord.com/api/oauth2/authorize?client_id=911274069503148043&permissions=8&scope=bot
import os
import sys
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import yaml
sys.path.append('/home/BreadLoaf/breadbot/cogs/')
import cogs.extras.checks as check
from dotenv import load_dotenv
project_folder = os.path.expanduser('~/breadbot')
load_dotenv(os.path.join(project_folder, '.env'))
#raise Exception

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix = ".", intents=intents, help_command=None, case_insensitive=True)

exception_cogs = ['__init__.py', 'boss.py', 'dungeon.py', 'events.py']

@client.command()
@check.is_bread()
async def load(ctx, extension):
  client.load_extension(f'cogs.{extension}')
  await ctx.message.delete()

@client.command()
@check.is_bread()
async def unload(ctx, extension):
  client.unload_extension(f'cogs.{extension}')
  await ctx.message.delete()

@client.command()
@check.is_bread()
async def reload(ctx, extension=None):
  if extension:
    try:
      client.unload_extension(f'cogs.{extension}')
    except:
      pass
    client.load_extension(f'cogs.{extension}')
  else:
    for filename in os.listdir('/home/BreadLoaf/breadbot/cogs'):
      if filename.endswith('.py') and filename not in exception_cogs:
        try:
          client.unload_extension(f'cogs.{filename[:-3]}')
          client.load_extension(f'cogs.{filename[:-3]}')
        except:
          continue
  print("Cogs have been reloaded")
  await ctx.message.delete()

for filename in os.listdir('/home/BreadLoaf/breadbot/cogs'):
  if filename.endswith('.py') and filename not in exception_cogs:
    client.load_extension(f'cogs.{filename[:-3]}')

#start_webhost()
#client.run(os.environ['token'])
client.run(os.getenv("TOKEN"))