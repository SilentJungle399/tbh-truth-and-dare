import discord, os, traceback, logging
from aiohttp import ClientSession
from discord.ext import commands
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# setup_logging()

logging.basicConfig(
    level = logging.INFO,
    format = '[%(asctime)s] [%(levelname)s] %(name)s: %(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S'
)

class Client(commands.Bot):
	def __init__(self):
		super().__init__(
			command_prefix = ">>",
			intents = intents, 
			enable_debug_events = True, 
			case_insensitive = True,
			strip_after_prefix = True,
			owner_ids = set(map(int, os.getenv("OWNER_IDS", "").split(",")))
		)
		# self.remove_command('help')

	async def on_ready(self):
		logging.info(f"[INFO] Bot has successfully started!")

		self.session = ClientSession(loop=self.loop)

		await self.load_modules()

		await self.change_presence(
			status=discord.Status.online, 
			activity=discord.Activity(
				type=discord.ActivityType.listening, 
				name='>>truth | >>dare'
			)
		)

	async def is_owner(self, user):
		return user.id in self.owner_ids

	async def load_modules(self):
		for path, subdirs, files in os.walk("modules"):
			for name in files:
				if name.endswith(".py"):
					name = os.path.join(name)[:-3]
					path = (os.path.join(path).replace("/", ".")).replace("\\", ".")
					filepath = path + "." + name
					try:
						await self.load_extension(filepath)
						logging.info(f"Loaded: " + filepath)
					except:
						logging.info(f"Error: {filepath}\n" + traceback.format_exc())
				else:
					continue

	def embedify(self, color, content):
		embed = discord.Embed(
			description = content,
			color = color,
			timestamp = datetime.now()
		)
		return embed


Client().run(os.getenv("BOT_TOKEN"))