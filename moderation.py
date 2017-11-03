import os
import sqlite3
import subprocess
import traceback

from colorama import Fore, init
from discord import Client, Message, Embed
from discord.utils import find

from logbot_data import token, owner_id

client = Client( )
init( )
exiting = False

sql = sqlite3.connect( f"{os.getcwd()}\\moderation.db" )
cursor = sql.cursor( )

_sql = sqlite3.connect( f"{os.getcwd()}\\Discord Logs\\SETTINGS\\logbot.db" )
_cursor = _sql.cursor( )

def exe ( cmd: str ):
	cursor.executescript( cmd )
	sql.commit( )
	pass

def read ( cmd: str ):
	cursor.execute( cmd )
	return cursor.fetchall( )

def getprefix ( server: str ) -> str:
	_cursor.execute( f"SELECT prefix FROM Prefixes WHERE server='{server}';" )
	return _cursor.fetchall( )[ 0 ][ 0 ]

@client.event
async def on_message ( message: Message ):
	admin_role = find( lambda r:r.name == "LogBot Admin", message.server.roles )
	begins = message.content.startswith

	prefix = getprefix( message.server.id )

	if admin_role in message.author.roles:
		if begins( f"m{prefix}strikes" ):
			if " " in message.content: user = message.mentions[ 0 ]
			else: user = message.author
			tmp = read( f"""SELECT * FROM _moderation WHERE server='{message.server.id}' AND member='{user.id}';""" )
			print( tmp )
			e = Embed( title="Strikes", description=f"For {user}" )
			for item in tmp:
				e.add_field( name=str( item[ 0 ] ), value=item[ 3 ] )
				pass
			await client.send_message( message.channel, "", embed=e )
			pass
		elif begins( f"m{prefix}strike " ):
			cnt = message.content.replace( f"m{prefix}strike ", "" )
			reason = cnt.split( "|" )[ 1 ]
			user = message.mentions[ 0 ]
			exe( f"""
			INSERT INTO _moderation (server, member, reason)
			VALUES ("{message.server.id}", "{user.id}", "{reason}");
			""".replace( "\t", "" ) )
			await client.send_message( message.channel, f"I have stricken {user}." )
			pass
		elif begins( f"m{prefix}destrike " ):
			exe( f"""
			DELETE FROM _moderation
			WHERE strike={message.content.replace(f'm{prefix}destrike ', '')}
			""".replace( "\t", "" ) )
			await client.send_message( message.channel, f"Removed strike {message.content.replace('m$destrike ', '')}." )
			pass
		pass

	if message.author.id == owner_id:
		if begins( "m$update" ) or begins( "logbot.mod.update" ):
			print( f"{Fore.CYAN}Updating...{Fore.RESET}" )
			client.close( )
			subprocess.Popen( f"{os.getcwd()}\\moderation.py" )
			pass
		elif begins( "$exit" ) or begins( "logbot.mod.exit" ):
			exiting = True
			await client.logout( )
			pass
		pass
	pass

@client.event
async def on_ready ( ):
	os.system( "cls" )
	print( f"{Fore.MAGENTA}Ready!!!{Fore.RESET}" )
	try:
		exe( f"""
		CREATE TABLE _moderation (strike INTEGER PRIMARY KEY, server VARCHAR(50), member VARCHAR(50), reason VARCHAR(100));
		""".replace( "\t", "" ) )
		pass
	except: print( traceback.format_exc( ) )
	try:
		exe( f"""
		CREATE INDEX my_mod_index
		ON _moderation (strike, server, member, reason);
		""".replace( "\t", "" ) )
		pass
	except: print( traceback.format_exc( ) )
	pass

client.run( token )

if exiting == False:
	subprocess.Popen( f"python {os.getcwd()}\\moderation.py" )
	exit( 0 )
	pass
