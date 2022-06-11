import os
import discord
from discord.ext import commands
import yaml

def read():
  with open(os.path.join(os.path.dirname(__file__), 'config.yaml'), 'r') as file:
    return yaml.safe_load(file)

def is_bread():
  async def predicate(ctx):
    file = read()
    return ctx.author.id in file['bread']
  return commands.check(predicate)

def is_ezay():
  async def predicate(ctx):
    return ctx.author.id in [282103815820410880]
  return commands.check(predicate)

def is_special():
    async def predicate(ctx):
        file = read()
        return ctx.author.id in file['special']
    return commands.check(predicate)

def is_admin():
  async def predicate(ctx):
    file = read()
    user_roles = ctx.author.roles
    valid_roles = file['roles']['admins']
    return any(item.name in valid_roles for item in user_roles) or ctx.author.id in file['users']
  return commands.check(predicate)

def is_mod():
  async def predicate(ctx):
    file = read()
    user_roles = ctx.author.roles
    valid_roles = file['roles']['mods'] + file['roles']['admins']
    return any(item.name in valid_roles for item in user_roles) or ctx.author.id in file['users']
  return commands.check(predicate)

def is_leader():
  async def predicate(ctx):
    file = read()
    user_roles = ctx.author.roles
    valid_roles = file['roles']['leaders'] + file['roles']['mods'] + file['roles']['admins']
    return any(item.name in valid_roles for item in user_roles) or ctx.author.id in file['users']
  return commands.check(predicate)

def is_member():
  async def predicate(ctx):
    file = read()
    user_roles = ctx.author.roles
    valid_roles = file['roles']['members'] + file['roles']['mods'] + file['roles']['admins']
    return any(item.name in valid_roles for item in user_roles) or ctx.author.id in file['users']
  return commands.check(predicate)

def allowed_channel():
  async def predicate(ctx):
    file = read()

    return False
  return commands.check(predicate)