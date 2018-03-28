"""
Security Module.
"""
import subprocess
import traceback
from datetime import datetime

import os
from colorama import init, Fore
from discord import Client, Message, Permissions
from discord.utils import find

from logbot_data import token, owner_id, bot_id

CLIENT = Client( )
init( )
EXITING = False

def log_error ( error_text: str ):
	"""
	Logs the bot's errors.
	:param error_text: The error message.
	"""
	file = f"{os.getcwd()}\\error_log.txt"
	prev_text = ""
	try:
		reader_obj = open( file, 'r' )
		prev_text = reader_obj.read( )
		reader_obj.close( )
		del reader_obj
	except Exception:
		pass
	writer_obj = open( file, 'w' )
	writer_obj.write( f"{datetime.now()} (security.py) - {error_text}\n\n{prev_text}" )
	writer_obj.close( )
	if "SystemExit" in error_text:
		exit( 0 )
	del writer_obj
	del file
	del prev_text

# noinspection PyUnresolvedReferences
@CLIENT.event
async def on_message ( message: Message ):
	"""
	Called when the bot receives a message.
	:param message: A discord.Message object.
	"""
	global EXITING
	try:
		if not message.server is None:
			# <editor-fold desc="Local Variables">
			owner = find( lambda m:m.id == owner_id, message.server.members )
			bot = find( lambda m:m.id == bot_id, message.server.members )
			muted = find( lambda r:r.name == "LogBot Muted", message.server.roles )
			admin = find( lambda r:r.name == "LogBot Admin", message.server.roles )
			member = find( lambda r:r.name == "LogBot Member", message.server.roles )
			# </editor-fold>
			# <editor-fold desc="Insurance that Roles are Created">
			if muted is None:
				perms = Permissions( send_messages=False )
				muted = await CLIENT.create_role( message.server, name="LogBot Muted", permissions=perms )
				print( "Created LogBot Muted" )
				del perms
			if admin is None:
				admin = await CLIENT.create_role( message.server, name="LogBot Admin" )
				print( "Created LogBot Admin" )
			if not member is None:
				await CLIENT.delete_role( message.server, member )
				print( "Removed LogBot Member" )
			await CLIENT.move_role( message.server, muted, bot.top_role.position - 1 )
			# </editor-fold>
			# <editor-fold desc="Add Roles">
			await CLIENT.add_roles( message.server.owner, admin )
			await CLIENT.add_roles( bot, admin )
			try:
				await CLIENT.add_roles( owner, admin )
			except Exception:
				pass
			# </editor-fold>
			# <editor-fold desc="Remove Roles">
			await CLIENT.remove_roles( message.server.owner, muted )
			try:
				await CLIENT.remove_roles( owner, muted )
			except Exception:
				pass
			await CLIENT.remove_roles( bot, muted )
			# </editor-fold>

			if message.content.startswith( "$exit" ) or message.content.startswith( "logbot.security.exit" ):
				if message.author.id == owner_id:
					EXITING = True
					await CLIENT.logout( )
			del owner
			del bot
			del muted
			del admin
			del member
	except Exception:
		log_error( traceback.format_exc( ) )

@CLIENT.event
async def on_ready ( ):
	"""
	Called when the bot logs in.
	"""
	print( f"{Fore.MAGENTA}Security Ready!!!{Fore.RESET}" )

CLIENT.run( token )

if not EXITING:
	subprocess.Popen( f"python {os.getcwd()}\\security.py" )
	exit( 0 )
