import ast
import os
import sqlite3
import subprocess
from datetime import datetime

from colorama import Fore, init
from discord import Client, Message
from discord.utils import find

from logbot_data import *

client = Client( )
init( )

dict_words = [ ]
filter_disable_list = [ ]
filter_settings = { }

discord_settings = f"{os.getcwd()}\\Discord Logs\\SETTINGS"
dictionary = f"{discord_settings}\\censored_words.txt"
filter_disables = f"{discord_settings}\\filter_disable_list.txt"
_settings = f"{discord_settings}\\filter_setting.txt"

sql = sqlite3.connect( f"{discord_settings}\\logbot.db" )
cursor = sql.cursor( )

try:
	reader = open( filter_disables, 'r' )
	filter_disable_list = ast.literal_eval( reader.read( ) )
	if isinstance( filter_disable_list, dict ): filter_disable_list = list( )
	reader.close( )
	del reader
	pass
except: pass

try:
	reader = open( _settings, 'r' )
	filter_settings = ast.literal_eval( reader.read( ) )
	reader.close( )
	del reader
	pass
except: pass

try:
	reader = open( dictionary, 'r' )
	dict_words = reader.read( ).split( "\n" )
	reader.close( )
	del reader
	pass
except: pass

def sqlread ( cmd: str ):
	cursor.execute( cmd )
	return cursor.fetchall( )

@client.event
async def on_message ( message: Message ):
	if not message.server.id in list( filter_settings.keys( ) ): filter_settings[ message.server.id ] = 1
	words = message.content.replace( ".", "" ).replace( ",", "" ).replace( "!", "" ).replace( "?", "" ).split( " " )
	for word in words:
		if word.lower( ) in dict_words:
			words[ words.index( word ) ] = "\\*" * len( word )
			pass
		pass
	if not ' '.join( words ) == message.content.replace( ".", "" ).replace( ",", "" ).replace( "!", "" ).replace( "?", "" ) and not message.server.id in filter_disable_list:
		await client.delete_message( message )
		if filter_settings[ message.server.id ] == 1:
			await client.send_message( message.channel, f"[{message.author.mention}] {' '.join(words)}" )
			pass
		print( f"{Fore.LIGHTMAGENTA_EX}{str(message.author)} just swore!{Fore.RESET}" )
		pass

	do_update = False
	prefix = sqlread( f"SELECT prefix FROM Prefixes WHERE server='{message.server.id}';" )[ 0 ][ 0 ]
	admin_role = find( lambda r:r.name == "LogBot Admin", message.server.roles )
	def startswith ( *msgs, val=message.content ):
		for msg in msgs:
			if val.startswith( msg ):
				return True
			pass
		return False
	if startswith( f"{prefix}filter settype " ):
		if admin_role in message.author.roles or message.author.id == owner_id:
			cnt = message.content.replace( f"{prefix}filter settype ", "" )
			if startswith( "d", val=cnt ): filter_settings[ message.server.id ] = 0
			elif startswith( "e", val=cnt ): filter_settings[ message.server.id ] = 1
			await client.send_message( message.channel, f"```Set the filter type!```" )
			pass
		else:
			await client.send_message( message.channel, f"```You do not have permission to use this command.```" )
			pass
		pass
	elif startswith( f"{prefix}filter" ):
		_stng = f"Type: {str(filter_settings[message.server.id]).replace('0', 'Delete').replace('1', 'Edit and Replace')}"
		await client.send_message( message.channel, _stng )
		pass
	elif startswith( "$update", "logbot.filter.update" ):
		if message.author.id == owner_id:
			do_update = True
			pass
		pass
	elif startswith( "$exit", "logbot.filter.exit" ):
		if message.author.id == owner_id:
			exit( 0 )
			pass
		pass
	elif startswith( f"{prefix}ping" ):
		tm = datetime.now( ) - message.timestamp
		await client.send_message( message.channel, f"```LogBot Swearing Filter Online ~ {round(tm.microseconds / 1000)}```" )
		pass
	elif startswith( f"f{prefix}disabled" ):
		await client.send_message( message.channel, str( message.server.id in filter_disable_list ) )
		pass
	elif startswith( f"f{prefix}disable" ):
		if admin_role in message.author.roles or message.author.id == owner_id:
			filter_disable_list.append( message.server.id )
			await client.send_message( message.channel, f"Disabled filter..." )
			pass
		else:
			await client.send_message( message.channel, f"```You do not have permission to use this command.```" )
			pass
		pass
	elif startswith( f"f{prefix}enable" ):
		if admin_role in message.author.roles or message.author.id == owner_id:
			filter_disable_list.remove( message.server.id )
			await client.send_message( message.channel, f"Enabled filter..." )
			pass
		else:
			await client.send_message( message.channel, f"```You do not have permission to use this command.```" )
			pass
		pass

	writer = open( _settings, 'w' )
	writer.write( str( filter_settings ) )
	writer.close( )
	writer = open( filter_disables, 'w' )
	writer.write( str( filter_disable_list ) )
	writer.close( )
	del writer
	if do_update:
		print( f"{Fore.LIGHTCYAN_EX}Updating...{Fore.RESET}" )
		await client.close( )
		subprocess.Popen( f"python {os.getcwd()}\\swearing_filter_v2.py", False )
		exit( 0 )
		pass
	pass

# noinspection PyUnusedLocal
@client.event
async def on_message_edit ( before: Message, after: Message ):
	if not after.server.id in list( filter_settings.keys( ) ): filter_settings[ after.server.id ] = 1
	words = after.content.replace( ",", "" ).replace( ".", "" ).split( " " )
	for word in words:
		if word.lower( ) in dict_words:
			words[ words.index( word ) ] = "\\*" * len( word )
			pass
		pass
	if not ' '.join( words ) == after.content.replace( ",", "" ).replace( ".", "" ) and not before.server.id in filter_disable_list:
		await client.delete_message( after )
		if filter_settings[ after.server.id ] == 1:
			await client.send_message( after.channel, f"[{after.author.mention}] {' '.join(words)}" )
			pass
		print( f"{Fore.LIGHTMAGENTA_EX}{str(after.author)} just swore!{Fore.RESET}" )
		pass
	pass

@client.event
async def on_ready ( ):
	os.system( "cls" )
	print( f"{Fore.MAGENTA}Ready!!!{Fore.RESET}" )
	pass

client.run( token )
