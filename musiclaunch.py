from discord.ext import commands
from discord.voice_client import VoiceClient
from colorama import Fore, init

from logbot_data import token

init()
bot = commands.Bot("mu$")
startup_extensions = ["Music"]

@bot.event
async def on_ready():
	print(f"{Fore.MAGENTA}Music Ready!!!{Fore.RESET}")
	pass

for extension in startup_extensions:
	try:
		bot.load_extension(extension)
		pass
	except Exception as ex:
		print("Error loading extension!")
		pass
	pass

bot.run(token)