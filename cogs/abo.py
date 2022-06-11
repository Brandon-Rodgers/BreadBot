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
import traceback

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

		self.update_last_daily_reset_date.start()

	@commands.command()
	@check.is_bread()
	async def updatedate(self, ctx):
		with open(os.path.join(os.path.dirname(__file__), 'data/abo_api.yaml'), 'r') as file:
			self.date_data = yaml.safe_load(file)

	@commands.command()
	@check.is_bread()
	async def updated(self, ctx, updated):
		if updated == "false":
			self.updated_last_reset = False
			await ctx.send("Updated last reset has been set to False")
		elif updated == "true":
			self.updated_last_reset = True
			await ctx.send("Updated last reset has been set to True")
		else:
			await ctx.send("Please use true or false as an argument")

	@tasks.loop(minutes=1)
	async def update_last_daily_reset_date(self):
		with open(os.path.join(os.path.dirname(__file__), 'data/abo_api.yaml'), 'r') as file:
			self.date_data = yaml.safe_load(file)

		date = str(datetime.utcnow())
		splt = date.split(" ")
		date = splt[0]
		hour = int(splt[1].split(":")[0])

		date_list = date.split("-")
		year, month, day = date_list[0], date_list[1], date_list[2]

		new_date = f"{date} {hour}:00:00"

		if hour == 22 and not self.updated_last_reset:
			print(f"Updated date data for last reset to {date}")

			self.date_data['last reset'] = new_date

			with open(os.path.join(os.path.dirname(__file__), 'data/abo_api.yaml'), 'w') as file:
				yaml.dump(self.date_data, file)

			self.updated_last_reset = True

		elif hour == 23 and self.updated_last_reset:
			self.updated_last_reset = False

	async def update_day(self, season, day, date):
		pass

	@commands.command()
	async def report(self, ctx, *args):
		if ctx.message.channel.id == 878800609770340402:
			await ctx.send("Commands are not allowed in this channel")
		else:
			name = ""
			for arg in args:
				name = f"{name}{arg} "
			name = name[:-1]

			with open(os.path.join(os.path.dirname(__file__), 'data/abo_api.yaml'), 'r') as file:
				self.date_data = yaml.safe_load(file)

			print(self.date_data)

			prev_date = self.date_data['last reset']
			print(prev_date)

			cur_guild_data = pull.guild_members(name)
			cur_guild_members = cur_guild_data['Guilds'][0]['Members']

			members_list = []
			longest_name = 0
			total_stones = 0

			for m in cur_guild_members:
				user_name = m['Name']

				if len(user_name) > longest_name:
					longest_name = len(user_name)

				prev_m = pull.user_info(user_name, prev_date)['Users'][0]

				if prev_m == None:
					valid = False
					stones = 0
				else:
					valid = True
					stones = m['GuildXp'] - prev_m['GuildXp']

					total_stones += stones

				members_list.append({'name':user_name, 'stones':stones, 'valid stones':valid})

			members_list = sorted(members_list, key = lambda s: s['stones'], reverse=True)

			report = "**Guild Stones**\n```"

			for m in members_list:
				user_name = m['name']
				stones = m['stones']
				valid = m['valid stones']
				if valid:
					stones, abbr = conversion.abbreviate_number(stones)
					stones = round(stones,2)
					stones = f"{stones:.2f}" + abbr
				else:
					stones = "N/A"

				spaces_needed = longest_name - len(user_name)
				for i in range(spaces_needed):
					user_name += " "

				stone_spaces = 7 - len(stones)
				stone_space = ""
				for i in range(stone_spaces):
					stone_space += " "

				report = report + f"{user_name}|{stone_space}{stones}\n"

			total_stones, abbreviation = conversion.abbreviate_number(total_stones)
			total_stones = round(total_stones, 2)
			report = report + "```"

			embed = discord.Embed(name=f"{cur_guild_data['Guilds'][0]['Name']}",title=f"{cur_guild_data['Guilds'][0]['Name']}", description=report, color=0xFF5733)
			embed.add_field(name="Total Stones Today", value=f"**{total_stones:.2f}{abbreviation}**")

			await ctx.send(embed=embed)

	@report.error
	async def report_error(self, ctx, error):
		trace = traceback.format_exception(type(error), error, error.__traceback__)
		trace = ''.join(trace)
		print(trace)

	@commands.command(aliases=['g'])
	async def guild(self, ctx, *args):
		if ctx.message.channel.id == 878800609770340402:
			await ctx.send("Commands are not allowed in this channel")
		else:
			name = ""
			for arg in args:
				name = f"{name}{arg} "
			name = name[:-1]

			cur_date = datetime.utcnow()

			guild_info = pull.guild_info(name)['Guilds'][0]

			if guild_info == None:
				await ctx.send("Sorry I was unable to find that guild!")
			else:
				guild_name = guild_info['Name']
				trophies = conversion.add_commas_to_number(guild_info['Rating'])
				position = guild_info['Position']
				leader = guild_info['LeaderName']
				members_count = guild_info['MembersCount']
				guild_seasonstones, guild_seasonabbr = conversion.abbreviate_number(guild_info['SeasonGuildXp'])
				guild_stones, guild_abbr = conversion.abbreviate_number(guild_info['GuildXp'])

				guild_members = pull.guild_members(name)['Guilds'][0]
				name = guild_members['Name']

				message = guild_members['LeaderMessage']

				description = f"\n\nLeader: {leader}\nMembers: {members_count}\n\nTrophies: {trophies}\nStones: {round(guild_seasonstones, 2)}{guild_seasonabbr} ({round(guild_stones, 2)}{guild_abbr})\n\n"

				members_list = []
				longest_name = 0
				longest_stones = 0

				for m in guild_members['Members']:
					user_name = m['Name']
					level = m['Level']
					trophies = conversion.add_commas_to_number(m['Rating'])
					seasonstones = m['SeasonGuildXp']
					stones = m['GuildXp']

					c_seasonstones, seasonabbr = conversion.abbreviate_number(seasonstones)
					c_seasonstones = round(c_seasonstones, 2)
					c_seasonstones = f"{c_seasonstones:.2f}{seasonabbr}"
					stones, abbr = conversion.abbreviate_number(stones)
					stones = round(stones, 2)
					stones = f"{c_seasonstones}({stones:.2f}{abbr})"

					if len(stones) > longest_stones:
						longest_stones = len(stones)

					last_online = m['LastUpdateTime']

					if len(user_name) > longest_name:
						longest_name = len(user_name)

					members_list.append({'name':user_name, 'level':level, 'trophies':trophies, 'season stones':seasonstones, 'stones':stones, 'last online':last_online})

				members_list = sorted(members_list, key = lambda s: s['season stones'], reverse=True)

				report = "**Members**\n```"

				for m in members_list:
					user_name = m['name']
					level = str(m['level'])
					trophies = m['trophies']
					stones = m['stones']
					last_online = datetime.timestamp(datetime.utcnow()) - m['last online']
					days, hours, minutes, seconds = conversion.seconds_to_hms(last_online)
					seconds = int(seconds)

					name_spaces = longest_name - len(user_name) + 1
					for i in range(name_spaces):
						user_name += " "

					level_spaces = 4 - len(level)
					for i in range(level_spaces):
						level += " "

					trophies_spaces = 6 - len(trophies)
					for i in range(trophies_spaces):
						trophies += " "

					stones_spaces = longest_stones - len(stones) + 1
					for i in range(stones_spaces):
						stones += " "

					if days > 0:
						days = f" {days} Days"
					else:
						days = ""

					if hours < 10:
						hours = f"0{hours}"
					if minutes < 10:
						minutes = f"0{minutes}"
					if seconds < 10:
						seconds = f"0{seconds}"

					time = f"{hours}:{minutes}:{seconds}"

					report = report + f"{user_name}| {level}| {trophies}| {stones}|{days} {time}\n"

				report += "```"
				description = description + report

				embed = discord.Embed(name=f"{ctx.author}",title=f"{name} (Rank {position})", description=description, color=0xFF5733)
				embed.set_author(name=f"{ctx.author.display_name}", icon_url=ctx.author.avatar_url)

				await ctx.send(embed=embed)

	@commands.command(aliases=['gl'])
	async def guildleaderboard(self, ctx, count=15):
		if ctx.message.channel.id not in [914936919731871785, 912200234896076821, 966503329146503170, 878440364380418069, 898545942976954478, 878443257477087242, 973828012191678505, 878443456182243388, 878443485114548274,
											973828669292314664, 954946263005155408, 973828743032340520] and ctx.author.id != 230571781490999296:
			await ctx.send("This command is not allowed in this channel")
		else:
			if count > 45:
				count = 45
			elif count == 0:
				count = 1

			if count > 30:
				extra = count % 30
				guild_leaderboard = list(pull.guild_leaderboard_range(count=count)['Guilds']) + list(pull.guild_leaderboard_range(pos=30, count=extra)['Guilds'])
			else:
				guild_leaderboard = list(pull.guild_leaderboard_range(count=count)['Guilds'])

			report = "**Guild Leaderboard**\n```"

			for g in guild_leaderboard:
				rank = g['Position'] + 1
				name = g['Name']
				stones, abbr = conversion.abbreviate_number(g['SeasonGuildXp'])
				stones = str(stones)[:5] + abbr
				trophies = conversion.add_commas_to_number(g['Rating'])

				rank_spaces = 3 - len(str(rank))
				rank_space = ""
				for i in range(rank_spaces):
					rank_space += " "

				name_spaces = 17 - len(str(name))
				name_space = ""
				for i in range(name_spaces):
					name_space += " "

				trophies_spaces = 7 - len(str(trophies))
				trophies_space = ""
				for i in range(trophies_spaces):
					trophies_space += " "

				report = report + f"#{rank}{rank_space}{name}{name_space}{stones} {trophies}{trophies_space}\n"

			report = report + "```"

			embed = discord.Embed(name=f"{ctx.author}",title=f"{ctx.author.display_name}", description=report, color=0xFF5733)

			await ctx.send(embed=embed)

	@commands.command(aliases=['pl'])
	async def playerleaderboard(self, ctx, option="trophies", count=15):
		if ctx.message.channel.id not in [914936919731871785, 912200234896076821, 966503329146503170, 878440364380418069, 898545942976954478, 878443257477087242, 973828012191678505, 878443456182243388, 878443485114548274,
											973828669292314664, 954946263005155408, 973828743032340520] and ctx.author.id != 230571781490999296:
			await ctx.send("This command is not allowed in this channel")
		else:
			if not option in self.options:
				await ctx.send("No leaderboard exists for that option.\nAvailable options are: `trophies, currentgold, totalstones, seasonxp, seasonwins, seasonstones, seasonchests, seasongold`\n*currentgold, seasonxp, seasonwins, seasonchests, seasongold are just ratings with no values*")
			else:
				if count > 45:
					count = 45
				elif count == 0:
					count = 1

				if count > 30:
					extra = count % 30
					player_leaderboard = list(pull.user_leaderboard_range(count=count, option=self.options[option])['Users']) + list(pull.user_leaderboard_range(pos=30, count=extra, option=self.options[option])['Users'])
				else:
					player_leaderboard = list(pull.user_leaderboard_range(count=count, option=self.options[option])['Users'])

				report = "```"

				longest_name = 0
				for p in player_leaderboard:
					length = len(p['Name'])

					if length > longest_name:
						longest_name = length

				for p in player_leaderboard:
					rank = p['Position'] + 1
					name = p['Name']
					level = p['Level']
					selected = ""
					selected_space = ""

					rank_spaces = 3 - len(str(rank))
					rank_space = ""
					for i in range(rank_spaces):
						rank_space += " "

					name_spaces = longest_name - len(str(name)) + 1
					name_space = ""
					for i in range(name_spaces):
						name_space += " "

					level_spaces = 4 - len(str(level))
					level_space = ""
					for i in range(level_spaces):
						level_space += " "

					# Trophies, Total Stones, Season Stones

					if option == "trophies":
						selected = conversion.add_commas_to_number(p['Rating'])

						selected_spaces = 7 - len(str(selected))
						for i in range(selected_spaces):
							selected_space += " "
					elif option == "totalstones":
						selected, abbr = conversion.abbreviate_number(p['GuildXp'])
						selected = str(selected)[:5] + abbr

						selected_spaces = 6 - len(str(selected))
						for i in range(selected_spaces):
							selected_space += " "
					elif option == "seasonstones":
						selected, abbr = conversion.abbreviate_number(p['SeasonGuildXp'])
						selected = str(selected)[:5] + abbr

						selected_spaces = 6 - len(str(selected))
						for i in range(selected_spaces):
							selected_space += " "


					report = report + f"#{rank}{rank_space}{name}{name_space}{level}{level_space}{selected}{selected_space}\n"

				report = report + "```"

				embed = discord.Embed(name=f"{ctx.author}",title="Player Leaderboard", description=report, color=0xFF5733)
				embed.set_author(name=f"{ctx.author.display_name}", icon_url=ctx.author.avatar_url)

				await ctx.send(embed=embed)

	@commands.command(aliases=['egm'])
	async def eventguildmembers(self, ctx, *args):
		if ctx.message.channel.id == 878800609770340402:
			await ctx.send("Commands are not allowed in this channel")
		else:
			guild = ""
			for arg in args:
				guild = f"{guild}{arg} "
			guild = guild[:-1]

			guild_info = pull.guild_members(guild)['Guilds'][0]
			guild = guild_info['Name']
			guild_members = guild_info['Members']

			members_list = []
			longest_name = 0

			for m in guild_members:
				name = m['Name']
				member_event_info = pull.user_worldevent_info(name)['Users'][0]

				if len(name) > longest_name:
					longest_name = len(name)

				if member_event_info == None:
					score = 0
					time = 0
				else:
					score = member_event_info['Score']
					time = member_event_info['TotalTime']

				members_list.append({'name':name, 'score':score, 'time':time})

			members_list = sorted(members_list, key = lambda s: s['score'], reverse=True)

			report = "```"

			for m in members_list:
				name = m['name']
				score = str(m['score'])
				days, hours, minutes, seconds = conversion.seconds_to_hms(m['time'])
				hours += days * 24
				seconds = int(seconds)

				if hours < 10:
					hours = f"0{hours}"
				if minutes < 10:
					minutes = f"0{minutes}"
				if seconds < 10:
					seconds = f"0{seconds}"

				time = f"{hours}:{minutes}:{seconds}"

				name_spaces = longest_name - len(name)
				for i in range(name_spaces):
					name += " "

				score_spaces = 4 - len(score)
				for i in range(score_spaces):
					score += " "

				report = report + f"{name} {score}{time}\n"

			report = report + "```"

			embed = discord.Embed(name=f"{ctx.author}",title="World Event - Guild Members", description=report, color=0xFF5733)
			embed.set_author(name=f"{guild}", icon_url=ctx.author.avatar_url)

			await ctx.send(embed=embed)

	@commands.command()
	async def ranks(self, ctx, *args):
		if ctx.message.channel.id == 878800609770340402:
			await ctx.send("Commands are not allowed in this channel")
		else:
			name = ""
			for arg in args:
				name = f"{name}{arg} "
			name = name[:-1]

			#report = "**Player Ranks**\n"
			report = ""

			options = ["trophies", "total gold", "total stones", "season xp", "season wins", "season stones", "season chests", "season gold"]
			descriptions = ["`Arena Rating  :`", "`Current Gold  :`", "`Total Stones  :`", "`Season XP     :`", "`Season Wins   :`", "`Season Stones :`", "`Season Chests :`", "`Season Gold   :`","`World Event   :`"]

			for i, o in enumerate(options):
				user_info = pull.user_leaderboard_info(name, o)['Users'][0]

				report = report + f"{descriptions[i]}**#{user_info['Position']+1}**\n"

			try:
				we_pos = f"#{pull.user_worldevent_info(name)['Users'][0]['Position']+1}"
			except:
				we_pos = 'N/A'

			report = report + f"{descriptions[-1]}**{we_pos}**\n"

			embed = discord.Embed(name=f"{ctx.author}",title=f"{user_info['Name']}'s Ranks", description=report, color=0xFF5733)
			embed.set_author(name=f"{ctx.author.display_name}", icon_url=ctx.author.avatar_url)

			await ctx.send(embed=embed)

	def cog_unload(self):
		self.update_last_daily_reset_date.stop()

def setup(client):
	client.add_cog(ABO(client))