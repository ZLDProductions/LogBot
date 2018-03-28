"""
Moderation module.
"""
import os
import sqlite3
import subprocess
import traceback
from datetime import datetime

from colorama import Fore, init
from discord import Client, Message, Embed
from discord.utils import find

from logbot_data import token, owner_id

CLIENT = Client( )
init( )
EXITING = False

SQLA = sqlite3.connect( f"{os.getcwd()}\\moderation.db" )
CURSORA = SQLA.cursor( )

SQLB = sqlite3.connect( f"{os.getcwd()}\\Discord Logs\\SETTINGS\\logbot.db" )
CURSORB = SQLB.cursor( )

def log_error ( error_text: str ):
	"""
	Logs the bot's errors.
	:param error_text: The error message.
	"""
	file = f"{os.getcwd()}\\error_log.txt"
	prev_text = ""
	try:
		reader = open( file, 'r' )
		prev_text = reader.read( )
		reader.close( )
		del reader
	except Exception:
		pass
	writer = open( file, 'w' )
	writer.write( f"{datetime.now()} (moderation.py) - {error_text}\n\n{prev_text}" )
	writer.close( )
	if "SystemExit" in error_text:
		exit( 0 )
	del writer
	del file
	del prev_text

def exe ( cmd: str ):
	"""
	Executes an SQL command.
	:param cmd: The command.
	"""
	CURSORA.executescript( cmd )
	SQLA.commit( )

def read ( cmd: str ):
	"""
	Reads from the DB.
	:param cmd: The SQL Read command.
	:return: The data fetched.
	"""
	CURSORA.execute( cmd )
	return CURSORA.fetchall( )

def getprefix ( server: str ) -> str:
	"""
	Gets the server's prefix.
	:param server: The server ID.
	:return: The prefix.
	"""
	CURSORB.execute( f"SELECT prefix FROM Prefixes WHERE server='{server}';" )
	return CURSORB.fetchall( )[ 0 ][ 0 ]

@CLIENT.event
async def on_message ( message: Message ):
	"""
	Called when the bot receives a message.
	:param message: A discord.Message object.
	"""
	global EXITING
	try:
		admin_role = find( lambda r:r.name == "LogBot Admin", message.server.roles )
		begins = message.content.startswith

		prefix = getprefix( message.server.id )

		if admin_role in message.author.roles:
			if begins( f"m{prefix}strikes" ):
				if " " in message.content:
					user = message.mentions[ 0 ]
				else:
					user = message.author
				tmp = read( f"""SELECT * FROM _moderation WHERE server='{message.server.id}' AND member='{user.id}';""" )
				print( tmp )
				embed_obj = Embed( title="Strikes", description=f"For {user}" )
				for item in tmp:
					embed_obj.add_field( name=str( item[ 0 ] ), value=item[ 3 ] )
				await CLIENT.send_message( message.channel, "", embed=embed_obj )
				del tmp
				del embed_obj
				del user
			elif begins( f"m{prefix}strike " ):
				cnt = message.content.replace( f"m{prefix}strike ", "" )
				reason = cnt.split( "|" )[ 1 ]
				user = message.mentions[ 0 ]
				exe( f"""
				INSERT INTO _moderation (server, member, reason)
				VALUES ("{message.server.id}", "{user.id}", "{reason}");
				""".replace( "\t", "" ) )
				await CLIENT.send_message( message.channel, f"I have stricken {user}." )
				del cnt
				del reason
				del user
			elif begins( f"m{prefix}destrike " ):
				exe( f"""
				DELETE FROM _moderation
				WHERE strike={message.content.replace(f'm{prefix}destrike ', '')}
				""".replace( "\t", "" ) )
				await CLIENT.send_message( message.channel, f"Removed strike {message.content.replace('m$destrike ', '')}." )

		if message.author.id == owner_id:
			if begins( "m$update" ) or begins( "logbot.mod.update" ):
				print( f"{Fore.CYAN}Updating...{Fore.RESET}" )
				CLIENT.close( )
				subprocess.Popen( f"{os.getcwd()}\\moderation.py" )
			elif begins( "$exit" ) or begins( "logbot.mod.exit" ):
				EXITING = True
				await CLIENT.logout( )
		del admin_role
		del begins
		del prefix
	except Exception:
		log_error( traceback.format_exc( ) )

@CLIENT.event
async def on_ready ( ):
	"""
	Called when the bot logs in.
	"""
	# os.system( "cls" )
	print( f"{Fore.MAGENTA}Mod Ready!!!{Fore.RESET}" )
	try:
		exe( f"""
		CREATE TABLE _moderation (strike INTEGER PRIMARY KEY, server VARCHAR(50), member VARCHAR(50), reason VARCHAR(100));
		""".replace( "\t", "" ) )
	except Exception:
		pass
	try:
		exe( f"""
		CREATE INDEX my_mod_index
		ON _moderation (strike, server, member, reason);
		""".replace( "\t", "" ) )
	except Exception:
		pass

CLIENT.run( token )

if not EXITING:
	subprocess.Popen( f"python {os.getcwd()}\\moderation.py" )
	exit( 0 )
