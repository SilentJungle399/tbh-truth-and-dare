from discord.ext import commands
import discord
import json
import os

class Management(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.hybrid_command(
		name = "whitelist",
		description = "Add a user to the whitelist. Only the bot owner can use this command.",
		with_app_command = True
	)
	@commands.is_owner()
	async def whitelist(self, ctx: commands.Context, user: discord.User):
		with open("data.json", "r") as f:
			data = json.load(f)

		if user.id in data["whitelist"]:
			await ctx.send(f"{user.mention} is already whitelisted.")
			return

		data["whitelist"].append(user.id)

		with open("data.json", "w") as f:
			json.dump(data, f, indent=4)

		await ctx.send(f"{user.mention} has been added to the whitelist.")

	@commands.hybrid_command(
		name = "unwhitelist",
		description = "Remove a user from the whitelist. Only the bot owner can use this command.",
		with_app_command = True
	)
	@commands.is_owner()
	async def unwhitelist(self, ctx: commands.Context, user: discord.User):
		with open("data.json", "r") as f:
			data = json.load(f)

		if user.id not in data["whitelist"]:
			await ctx.send(f"{user.mention} is not whitelisted.")
			return

		data["whitelist"].remove(user.id)

		with open("data.json", "w") as f:
			json.dump(data, f, indent=4)

		await ctx.send(f"{user.mention} has been removed from the whitelist.")

	@commands.hybrid_command(
		name = "whitelistlist",
		description = "List all whitelisted users. Only the bot owner can use this command.",
		with_app_command = True
	)
	@commands.is_owner()
	async def whitelistlist(self, ctx: commands.Context):
		with open("data.json", "r") as f:
			data = json.load(f)

		if not data["whitelist"]:
			await ctx.send("The whitelist is currently empty.")
			return

		embed = discord.Embed(
			title = "Whitelisted Users",
			description = "\n".join([f"<@{user_id}>" for user_id in data["whitelist"]]),
			color = discord.Color.green()
		)

		await ctx.send(embed=embed)

	@commands.hybrid_command(
		name = "add",
		description = "Add a truth or dare question to the database.",
		with_app_command = True
	)
	@commands.check_any(
		commands.has_any_role(
			os.getenv("MODERATOR_ROLE"), 
			os.getenv("ADMIN_ROLE"), 
			os.getenv("MANAGEMENT_ROLE")
		),
		commands.is_owner()
	)
	async def add(self, ctx: commands.Context, _type: str, *, question: str):
		if _type not in ["truth", "dare"]:
			await ctx.send("Invalid type. Please specify 'truth' or 'dare'.")
			return

		with open("data.json", "r") as f:
			data = json.load(f)

		data[_type].append(question)

		with open("data.json", "w") as f:
			json.dump(data, f, indent=4)

		await ctx.send(f"Added a new {_type} question to the database.")

	@commands.hybrid_command(
		name = "remove",
		description = "Remove a truth or dare question from the database.",
		with_app_command = True
	)
	@commands.check_any(
		commands.has_any_role(
			os.getenv("MODERATOR_ROLE"), 
			os.getenv("ADMIN_ROLE"), 
			os.getenv("MANAGEMENT_ROLE")
		),
		commands.is_owner()
	)
	async def remove(self, ctx: commands.Context, _type: str, *, question: str):
		if _type not in ["truth", "dare"]:
			await ctx.send("Invalid type. Please specify 'truth' or 'dare'.")
			return

		with open("data.json", "r") as f:
			data = json.load(f)

		if question not in data[_type]:
			await ctx.send(f"The specified question was not found in the {_type} database.")
			return

		data[_type].remove(question)

		with open("data.json", "w") as f:
			json.dump(data, f, indent=4)

		await ctx.send(f"Removed the specified {_type} question from the database.")

async def setup(bot):
	await bot.add_cog(Management(bot))