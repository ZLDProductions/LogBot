"""
Music launcher.
"""
from discord.ext import commands
from colorama import Fore, init

from logbot_data import token

init( )
BOT = commands.Bot( "mu$" )
STARTUP_EXTENSIONS = [ "Music" ]

@BOT.event
async def on_ready ( ):
	"""
	Called when the bot logs in.
	"""
	print( f"{Fore.MAGENTA}Music Ready!!!{Fore.RESET}" )

for extension in STARTUP_EXTENSIONS:
	try:
		BOT.load_extension( extension )
	except Exception as ex:
		print( "Error loading extension!" )

BOT.run( token )
