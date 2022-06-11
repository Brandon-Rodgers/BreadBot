import discord
import os
import sys
from discord.ext import commands
import yaml
import asyncio
sys.path.append('/home/BreadLoaf/breadbot/cogs/extras/')
from .extras.checks import is_bread, is_admin, is_mod, is_member, is_ezay

class Mod(commands.Cog):
	def __init__(self, client):
		self.client = client

	# Commands
	@commands.command()
	@is_mod()
	async def mute(self, ctx, member : discord.Member, *, reason=None):
		if ctx.author.guild_permissions.manage_roles:
			embed = discord.Embed(
			title = "Muted",
			description = f"{member} has been sent to the corner.\nReason: {reason}"
			)

			await member.add_roles(discord.utils.get(ctx.guild.roles, name='muted'))
			#await member.remove_roles(discord.utils.get(ctx.guild.roles, name='BreadSlice'))
			await ctx.send(embed=embed)

	@commands.command()
	@is_mod()
	async def tempmute(self, ctx, time, member : discord.Member, *, reason=None):
		if ctx.author.guild_permissions.manage_roles:
			embed = discord.Embed(
			title = "Muted",
			description = f"{member} has been sent to the corner.\nReason: {reason}\nFor {time} seconds"
			)

			await member.add_roles(discord.utils.get(ctx.guild.roles, name='muted'))
			#await member.remove_roles(discord.utils.get(ctx.guild.roles, name='BreadSlice'))
			await ctx.send(embed=embed)

			await asyncio.sleep(time)
			await member.remove_roles(discord.utils.get(ctx.guild.roles, name='muted'))


	@commands.command()
	@commands.cooldown(1,3600,commands.BucketType.user)
	@is_ezay()
	async def emute(self, ctx, member : discord.Member, *, reason=None):
		embed = discord.Embed(
		title = "Ezay Mute",
		description = f"Ezay has deemed you worthy of his corner!\nReason: {reason}")

		await member.add_roles(discord.utils.get(ctx.guild.roles, name='muted'))
		#await member.remove_roles(discord.utils.get(ctx.guild.roles, name='BreadSlice'))
		await ctx.send(embed=embed)

	@commands.command()
	@is_ezay()
	async def eunmute(self, ctx, member : discord.Member, *, reason=None):
		embed = discord.Embed(
		title = "Ezay UnMute",
		description = f"Ezay has deemed you unworthy of his corner!")

		await member.remove_roles(discord.utils.get(ctx.guild.roles, name='muted'))
		#await member.remove_roles(discord.utils.get(ctx.guild.roles, name='BreadSlice'))
		await ctx.send(embed=embed)

	@commands.command()
	@is_mod()
	async def unmute(self, ctx, member : discord.Member, *, reason=None):
		if ctx.author.guild_permissions.manage_roles:
			embed = discord.Embed(
			title = "Unmuted",
			description = f"{member} can come out of the corner."
			)
			await member.remove_roles(discord.utils.get(ctx.guild.roles, name='muted'))
			#await member.add_roles(discord.utils.get(ctx.guild.roles, name='BreadSlice'))
			await ctx.send(embed=embed)

	@commands.command()
	@is_mod()
	async def ban(self, ctx, user : discord.User, *, reason=None):
		embed = discord.Embed(
			title = "Success",
			description = f"{user} has been banned.\nReason:{reason}"
		)
		if ctx.author.guild_permissions.ban_members:
			await ctx.send(embed=embed)
			await ctx.guild.ban(user=user, reason=reason)

	@commands.command()
	@is_mod()
	async def unban(self, ctx, *, user):
		if ctx.author.guild_permissions.ban_members:
			banned_users = await ctx.guild.bans()
			user_name, user_discriminator = user.split("#")

			for entry in banned_users:
				user = entry.user
				if (user.name, user.discriminator) == (user_name, user_discriminator):
					embed = discord.Embed(
					title = "Success",
					description = f"{user} has been unbanned."
					)
					await ctx.send(embed=embed)
					await ctx.guild.unban(user=user)

	@commands.command()
	@is_mod()
	async def clear(self, ctx, amount : int = 2, member : discord.Member = None):
		async for msg in ctx.message.channel.history(limit = amount):
			if member:
				if msg.author == member:
					await msg.delete()
				else:
					await msg.delete()

def setup(client):
	client.add_cog(Mod(client))