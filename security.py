import subprocess
import traceback
from datetime import datetime

import os
from colorama import init, Fore
from discord import Client, Message, Permissions
from discord.utils import find

from logbot_data import token, owner_id, bot_id

client = Client( )
init( )
exiting = False

def log_error ( error_text: str ):
	file = f"{os.getcwd()}\\error_log.txt"
	prev_text = ""
	try:
		reader = open( file, 'r' )
		prev_text = reader.read( )
		reader.close( )
		del reader
		pass
	except: pass
	writer = open( file, 'w' )
	writer.write( f"{datetime.now()} (security.py) - {error_text}\n\n{prev_text}" )
	writer.close( )
	if "SystemExit" in error_text: exit( 0 )
	del writer
	pass

@client.event
async def on_message ( message: Message ):
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
				muted = await client.create_role( message.server, name="LogBot Muted", permissions=perms )
				print( "Created LogBot Muted" )
				pass
			if admin is None:
				admin = await client.create_role( message.server, name="LogBot Admin" )
				print( "Created LogBot Admin" )
				pass
			if not member is None:
				await client.delete_role( message.server, member )
				print( "Removed LogBot Member" )
				pass
			await client.move_role( message.server, muted, bot.top_role.position - 1 )
			# </editor-fold>
			# <editor-fold desc="Add Roles">
			await client.add_roles( message.server.owner, admin )
			await client.add_roles( bot, admin )
			try: await client.add_roles( owner, admin )
			except: pass
			# </editor-fold>
			# <editor-fold desc="Remove Roles">
			await client.remove_roles( message.server.owner, muted )
			try: await client.remove_roles( owner, muted )
			except: pass
			await client.remove_roles( bot, muted )
			# </editor-fold>

			if message.content.startswith( "$exit" ) or message.content.startswith( "logbot.security.exit" ):
				if message.author.id == owner_id:
					exiting = True
					await client.logout( )
					pass
				pass
			pass
		pass
	except: log_error( traceback.format_exc( ) )
	pass

@client.event
async def on_ready ( ):
	print( f"{Fore.MAGENTA}Security Ready!!!{Fore.RESET}" )
	pass

client.run( token )

if not exiting:
	subprocess.Popen( f"python {os.getcwd()}\\security.py" )
	exit( 0 )
	pass
