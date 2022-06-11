import discord
import os
import sys
from discord.ext import commands, tasks
import yaml
import importlib
sys.path.append('/home/BreadLoaf/breadbot/cogs/extras/')
import extras.checks as check
from .extras import pull
from .extras import pull2
from .extras import conversion
from datetime import datetime

custom_modules = [pull, conversion, pull2]

for m in custom_modules:
    importlib.reload(m)

class ABO(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.options = {"trophies":"trophies", "currentgold":"total gold", "totalstones":"total stones", "seasonxp":"season xp", "seasonwins":"season wins",
						"seasonstones":"season stones", "seasonchests":"season chests", "seasongold":"season gold"}
		with open(os.path.join(os.path.dirname(__file__), 'data/abo_api.yaml'), 'r') as file:
			self.date_data = yaml.safe_load(file)
		self.updated_last_reset = True

	@commands.command()
	async def lastseason(self, ctx):
		self.date_data['last season'] = {'start':datetime.utcnow(), 'end':str(datetime.utcnow())}

		with open(os.path.join(os.path.dirname(__file__), 'data/abo_api.yaml'), 'w') as file:
			yaml.dump(self.date_data, file)



def setup(client):
	client.add_cog(ABO(client))