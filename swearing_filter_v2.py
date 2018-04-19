import ast
import sqlite3
import subprocess
import traceback
from datetime import datetime

import os

from colorama import Fore, init
from discord import Client, Message
from discord.utils import find

from logbot_data import owner_id, token

CLIENT = Client( )
init( )
EXITING = False

DICT_WORDS = [ ]
FILTER_DISABLE_LIST = [ ]
FILTER_SETTINGS = { }

DISCORD_SETTINGS_PATH = f"{os.getcwd()}\\Discord Logs\\SETTINGS"
DICTIONARY_PATH = f"{DISCORD_SETTINGS_PATH}\\censored_words.txt"
FILTER_DISABLES = f"{DISCORD_SETTINGS_PATH}\\filter_disable_list.txt"
SETTINGS_PATH = f"{DISCORD_SETTINGS_PATH}\\filter_setting.txt"

SQL = sqlite3.connect( f"{DISCORD_SETTINGS_PATH}\\logbot.db" )
CURSOR = SQL.cursor( )

try:
	READER = open( FILTER_DISABLES, 'r' )
	FILTER_DISABLE_LIST = ast.literal_eval( READER.read( ) )
	if isinstance( FILTER_DISABLE_LIST, dict ):
		FILTER_DISABLE_LIST = list( )
	READER.close( )
	del READER
except Exception:
	pass

try:
	READER = open( SETTINGS_PATH, 'r' )
	FILTER_SETTINGS = ast.literal_eval( READER.read( ) )
	READER.close( )
	del READER
except Exception:
	pass

try:
	READER = open( DICTIONARY_PATH, 'r' )
	DICT_WORDS = READER.read( ).split( "\n" )
	READER.close( )
	del READER
except Exception:
	pass

# noinspection PyShadowingNames
def log_error ( error_text: str ):
	file = f"{os.getcwd()}\\error_log.txt"
	prev_text = ""
	try:
		reader_obj = open( file, 'r' )
		prev_text = reader_obj.read( )
		reader_obj.close( )
		del reader_obj
	except Exception:
		pass
	writer = open( file, 'w' )
	writer.write( f"{datetime.now()} (swearing_filter_v2.py) - {error_text}\n\n{prev_text}" )
	writer.close( )
	del writer
	del file
	del prev_text

def sqlread ( cmd: str ):
	CURSOR.execute( cmd )
	return CURSOR.fetchall( )

@CLIENT.event
async def on_message ( message: Message ):
	global EXITING
	try:
		if not message.server.id in list( FILTER_SETTINGS.keys( ) ):
			FILTER_SETTINGS[ message.server.id ] = 1
		words = message.content.replace( ".", "" ).replace( ",", "" ).replace( "!", "" ).replace( "?", "" ).split( " " )
		for word in words:
			if word.lower( ) in DICT_WORDS:
				words[ words.index( word ) ] = "\\*" * len( word )
		if not ' '.join( words ) == message.content.replace( ".", "" ).replace( ",", "" ).replace( "!", "" ).replace( "?", "" ) and not message.server.id in FILTER_DISABLE_LIST:
			await CLIENT.delete_message( message )
			if FILTER_SETTINGS[ message.server.id ] == 1:
				await CLIENT.send_message( message.channel, f"[{message.author.mention}] {' '.join(words)}" )
			print( f"{Fore.LIGHTMAGENTA_EX}{str(message.author)} just swore!{Fore.RESET}" )

		do_update = False
		prefix = sqlread( f"SELECT prefix FROM Prefixes WHERE server='{message.server.id}';" )[ 0 ][ 0 ]
		admin_role = find( lambda r:r.name == "LogBot Admin", message.server.roles )
		def startswith ( *msgs, val=message.content ):
			for msg in msgs:
				if val.startswith( msg ):
					return True
			return False
		if startswith( f"{prefix}filter settype " ):
			if admin_role in message.author.roles or message.author.id == owner_id:
				cnt = message.content.replace( f"{prefix}filter settype ", "" )
				if startswith( "d", val=cnt ):
					FILTER_SETTINGS[ message.server.id ] = 0
				elif startswith( "e", val=cnt ):
					FILTER_SETTINGS[ message.server.id ] = 1
				await CLIENT.send_message( message.channel, f"```Set the filter type!```" )
				del cnt
			else:
				await CLIENT.send_message( message.channel, f"```You do not have permission to use this command.```" )
		elif startswith( f"{prefix}filter" ):
			_stng = f"Type: {str(FILTER_SETTINGS[message.server.id]).replace('0', 'Delete').replace('1', 'Edit and Replace')}"
			await CLIENT.send_message( message.channel, _stng )
			del _stng
		elif startswith( "$update", "logbot.filter.update" ):
			if message.author.id == owner_id:
				do_update = True
		elif startswith( "$exit", "logbot.filter.exit" ):
			if message.author.id == owner_id:
				EXITING = True
				await CLIENT.logout( )
		elif startswith( f"{prefix}ping" ):
			timestamp = datetime.now( ) - message.timestamp
			await CLIENT.send_message( message.channel, f"```LogBot Swearing Filter Online ~ {round(timestamp.microseconds / 1000)}```" )
			del timestamp
		elif startswith( f"f{prefix}disabled" ):
			await CLIENT.send_message( message.channel, str( message.server.id in FILTER_DISABLE_LIST ) )
		elif startswith( f"f{prefix}disable" ):
			if admin_role in message.author.roles or message.author.id == owner_id:
				FILTER_DISABLE_LIST.append( message.server.id )
				await CLIENT.send_message( message.channel, f"Disabled filter..." )
			else:
				await CLIENT.send_message( message.channel, f"```You do not have permission to use this command.```" )
		elif startswith( f"f{prefix}enable" ):
			if admin_role in message.author.roles or message.author.id == owner_id:
				FILTER_DISABLE_LIST.remove( message.server.id )
				await CLIENT.send_message( message.channel, f"Enabled filter..." )
			else:
				await CLIENT.send_message( message.channel, f"```You do not have permission to use this command.```" )

		writer = open( SETTINGS_PATH, 'w' )
		writer.write( str( FILTER_SETTINGS ) )
		writer.close( )
		writer = open( FILTER_DISABLES, 'w' )
		writer.write( str( FILTER_DISABLE_LIST ) )
		writer.close( )
		del writer
		if do_update:
			print( f"{Fore.LIGHTCYAN_EX}Updating...{Fore.RESET}" )
			await CLIENT.close( )
			subprocess.Popen( f"python {os.getcwd()}\\swearing_filter_v2.py", False )
			exit( 0 )
		del do_update
		del prefix
		del admin_role
		del words
	except Exception:
		log_error( traceback.format_exc( ) )

# noinspection PyUnusedLocal
@CLIENT.event
async def on_message_edit ( before: Message, after: Message ):
	if not after.server.id in list( FILTER_SETTINGS.keys( ) ):
		FILTER_SETTINGS[ after.server.id ] = 1
	words = after.content.replace( ",", "" ).replace( ".", "" ).split( " " )
	for word in words:
		if word.lower( ) in DICT_WORDS:
			words[ words.index( word ) ] = "\\*" * len( word )
	if not ' '.join( words ) == after.content.replace( ",", "" ).replace( ".", "" ) and not before.server.id in FILTER_DISABLE_LIST:
		await CLIENT.delete_message( after )
		if FILTER_SETTINGS[ after.server.id ] == 1:
			await CLIENT.send_message( after.channel, f"[{after.author.mention}] {' '.join(words)}" )
		print( f"{Fore.LIGHTMAGENTA_EX}{str(after.author)} just swore!{Fore.RESET}" )
	del words

@CLIENT.event
async def on_ready ( ):
	# os.system( "cls" )
	print( f"{Fore.MAGENTA}Filter Ready!!!{Fore.RESET}" )

CLIENT.run( token )

if not EXITING:
	subprocess.Popen( f"python {os.getcwd()}\\swearing_filter_v2.py" )
	exit( 0 )
