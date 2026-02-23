from discord.ext import commands
from discord.ui import View, Button
import discord
import json
import random

async def get_random(_type):
	with open("data.json", "r") as f:
		data = json.load(f)

		question_list = data[_type]
		
		question = random.choice(question_list[:len(question_list)])
		
		data[_type].remove(question)
		data[_type].append(question)

	with open("data.json", "w") as f:
		json.dump(data, f, indent=4)

	embed = discord.Embed(
		description = question,
		color = discord.Color.green()
	)
	return embed

class Game(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.hybrid_command(
		name = "truth",
		description = "Play a game of Truth and Dare! Get a random truth question to answer.",
		with_app_command = True
	)
	async def truth(self, ctx: commands.Context):
		embed = await get_random("truth")
		embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.display_avatar.url if ctx.author.display_avatar else None)

		await ctx.reply(embed=embed, view=GameView())

	@commands.hybrid_command(
		name = "dare",
		description = "Play a game of Truth and Dare! Get a random dare to complete.",
		with_app_command = True
	)
	async def dare(self, ctx: commands.Context):
		embed = await get_random("dare")
		embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.display_avatar.url if ctx.author.display_avatar else None)

		await ctx.reply(embed=embed, view=GameView())


class GameView(View):
	def __init__(self):
		super().__init__()

	@discord.ui.button(label="Truth", style=discord.ButtonStyle.success, custom_id="truth_button")
	async def truth_button(self, interaction: discord.Interaction, button: Button):
		embed = await get_random("truth")
		embed.set_author(name = interaction.user.display_name, icon_url = interaction.user.display_avatar.url if interaction.user.display_avatar else None)
		await interaction.response.send_message(embed=embed, view=GameView())

	@discord.ui.button(label="Dare", style=discord.ButtonStyle.success, custom_id="dare_button")
	async def dare_button(self, interaction: discord.Interaction, button: Button):
		embed = await get_random("dare")
		embed.set_author(name = interaction.user.display_name, icon_url = interaction.user.display_avatar.url if interaction.user.display_avatar else None)
		await interaction.response.send_message(embed=embed, view=GameView())

async def setup(bot):
	await bot.add_cog(Game(bot))