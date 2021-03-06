import ast
import os
import re
import subprocess
from datetime import datetime

import colorama
import discord
import requests
import sqlite3

from logbot_data import token, owner_id

# noinspection SpellCheckingInspection

client = discord.Client( )
colorama.init( )

discord_settings = f'{os.getcwd()}\\Discord Logs\\SETTINGS'
filter_disables = f"{discord_settings}\\filter_disable_list.txt"
_setting = f"{discord_settings}\\filter_setting.txt"
filter_disable_list = { }
filter_setting = { }
sql = sqlite3.connect( f"{discord_settings}\\logbot.db" )
cursor = sql.cursor( )

try:
	reader = open( filter_disables, 'r' )
	filter_disable_list = ast.literal_eval( reader.read( ) )
	reader.close( )
	del reader
	pass
except: pass

try:
	reader = open( _setting, 'r' )
	filter_setting = ast.literal_eval( reader.read( ) )
	reader.close( )
	del reader
	pass
except: pass

def sqlread ( cmd: str ):
	cursor.execute( cmd )
	return cursor.fetchall( )

def check ( *args: str ):
	"""
	Compares each string to check which one is ascii. Returns first ascii instance.
	:param args: Several string parameters.
	"""
	for item in args:
		if item is not None:
			if all( ord( c ) for c in item ):
				return item
			pass
		pass
	return "Unknown String."
	pass

def checkForSymbols ( m: str ) -> list:
	"""
	Filters disallowed symbols out of a message.
	:param m: 
	:return: An enumeration of the filtered message and the symbols. 
	"""
	symbols = [ '+', '#', '&' ]
	repl = "\{i\}"
	for i in symbols:
		m = m.replace( i, repl.replace( "i", str( symbols.index( i ) ) ) )
		pass
	return [ m, symbols ]
	pass

@client.event
async def on_message ( message ):
	prefix = sqlread( f"SELECT prefix FROM Prefixes WHERE server='{message.server.id}';" )[ 0 ][ 0 ]
	admin_role = discord.utils.find( lambda r:r.name == "LogBot Admin", message.server.roles )
	if not message.server.id in list( filter_setting.keys( ) ): filter_setting[ message.server.id ] = 1
	do_update = False
	if message.content == "":
		mcont = 'lol'
		pass
	else:
		mcont = message.content
		pass

	occs = re.findall( r'[^\x00-\x7F]+', mcont, flags=2 )
	for occ in occs:
		mcont = mcont.replace( occ, "(" + str( occs.index( occ ) ) + ")", 1 )
		pass

	# mcont = re.sub(r'[^\x00-\x7F]+','[emoji]', mcont, flags=2)
	print( mcont )

	mentions_tmp = [ ]
	mentions = [ ]
	[ mentions_tmp.append( mid.mention ) for mid in message.mentions ]
	mentions_tmp.sort( )
	[ (mentions.append( m ) if not m in mentions else mentions.append( None )) for m in mentions_tmp ]
	while None in mentions:
		mentions.remove( None )
		pass

	for m in message.mentions:
		mcont = mcont.replace( m.mention, "[{}]".format( mentions.index( m.mention ) ) )
		pass

	role_mentions_tmp = [ ]
	role_mentions = [ ]
	[ role_mentions_tmp.append( rid.mention ) for rid in message.role_mentions ]
	role_mentions_tmp.sort( )
	[ (role_mentions.append( r ) if not r in role_mentions else role_mentions.append( None )) for r in role_mentions_tmp ]
	while None in role_mentions:
		role_mentions.remove( None )
		pass

	for r in message.role_mentions:
		mcont = mcont.replace( r.mention, f"`{role_mentions.index(r.mention)}`" )
		pass

	tmp = checkForSymbols( mcont )
	mcont = tmp[ 0 ]

	url = "http://www.purgomalum.com/service/plain?text=" + mcont
	url2 = "http://www.purgomalum.com/service/containsprofanity?text=" + mcont
	r = requests.get( url2 ).text.lower( )
	response = requests.get( url )
	repl = (response.text.replace( "*", "\\*" ) if not r == "false" else mcont)
	if not mcont == repl and not message.server.id in filter_disable_list and not message.author.bot == True and not message.content == "":
		for i in range( 0, len( mentions ) ):
			repl = repl.replace( "[{}]".format( i ), mentions[ i ] )
			pass
		for i in range( 0, len( occs ) ):
			repl = repl.replace( "(" + str( i ) + ")", occs[ i ] )
			pass
		for i in range( 0, len( tmp[ 1 ] ) ):
			repl = repl.replace( "\{" + str( i ) + "\}", tmp[ 1 ][ i ] )
			pass
		for i in range( 0, len( role_mentions ) ):
			repl = repl.replace( f"`{i}`", role_mentions[ i ] )
			pass
		await client.delete_message( message )
		if filter_setting[ message.server.id ] == 1:
			await client.send_message( message.channel, "[{}] ".format( message.author.mention ) + repl )
			pass

		identifier = str( message.author )
		print( f"{colorama.Fore.LIGHTMAGENTA_EX}{identifier} just swore!{colorama.Fore.RESET}" )
		pass
	def startswith ( *msgs, val=message.content ):
		for m in msgs:
			if val.startswith( m ): return True
			pass
		return False
	if startswith( f"{prefix}filter settype " ):
		if admin_role in message.author.roles or message.author.id == owner_id:
			cnt = message.content.replace( f"{prefix}filter settype ", "" )
			if startswith( "d", val=cnt ): filter_setting[ message.server.id ] = 0
			elif startswith( "e", val=cnt ): filter_setting[ message.server.id ] = 1
			await client.send_message( message.channel, f"```Set the filter type!```" )
			pass
		else:
			await client.send_message( message.channel, f"```You do not have permission to use this command.```" )
			pass
		pass
	elif startswith( f"{prefix}filter" ):
		_stng = f'Type: {str(filter_setting[message.server.id]).replace("0", "Delete").replace("1", "Edit and Replace")}'
		await client.send_message( message.channel, _stng )
		pass
	elif startswith( f"$update", "logbot.filter.update" ):
		if message.author.id == "239500860336373761":
			do_update = True
			pass
		pass
	elif startswith( "logbot.settings exit", "logbot.filter.exit" ):
		if message.author.id == "239500860336373761":
			exit( 0 )
			pass
		else:
			await client.send_message( message.channel, "```You do not have permission to use this command.```" )
			print( "{Fore.LIGHTGREEN_EX}{message.author.name} attempted to turn off the swearing filter!{Fore.RESET}" )
			pass
		pass
	elif startswith( f"{prefix}ping" ):
		tm = datetime.now( ) - message.timestamp
		await client.send_message( message.channel, f"```LogBot Swearing Filter Online ~ {round(tm.microseconds / 1000)}```" )
		pass
	elif startswith( f"f{prefix}disabled" ):
		if admin_role in message.author.roles or message.author.id == owner_id:
			await client.send_message( message.channel, str( message.server.id in filter_disable_list ) )
			pass
		else:
			await client.send_message( message.channel, f"```You do not have permission to use this command.```" )
			pass
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

	writer = open( _setting, 'w' )
	writer.write( str( filter_setting ) )
	writer.close( )
	del writer
	if do_update:
		print( colorama.Fore.LIGHTCYAN_EX + "Updating..." + colorama.Fore.RESET )
		await client.close( )
		subprocess.Popen( "python " + os.getcwd( ) + "\\swearing_filter.py", False )
		exit( 0 )
		pass
	pass

# noinspection PyUnusedLocal
@client.event
async def on_message_edit ( before, after ):
	message = after
	if message.content == "":
		mcont = 'lol'
		pass
	else:
		mcont = message.content
		pass

	occs = re.findall( r'[^\x00-\x7F]+', mcont, flags=2 )
	for occ in occs:
		mcont = mcont.replace( occ, "(" + str( occs.index( occ ) ) + ")", 1 )
		pass

	# mcont = re.sub(r'[^\x00-\x7F]+','[emoji]', mcont, flags=2)
	print( mcont )

	mentions_tmp = [ ]
	mentions = [ ]
	[ mentions_tmp.append( mid.mention ) for mid in message.mentions ]
	mentions_tmp.sort( )
	[ (mentions.append( m ) if not m in mentions else mentions.append( None )) for m in mentions_tmp ]
	while None in mentions:
		mentions.remove( None )
		pass

	for m in message.mentions:
		mcont = mcont.replace( m.mention, "[{}]".format( mentions.index( m.mention ) ) )
		pass

	tmp = checkForSymbols( mcont )
	mcont = tmp[ 0 ]

	url = "http://www.purgomalum.com/service/plain?text=" + mcont
	url2 = "http://www.purgomalum.com/service/containsprofanity?text=" + mcont
	r = requests.get( url2 ).text.lower( )
	response = requests.get( url )
	repl = (response.text.replace( "*", "\\*" ) if not r == "false" else mcont)
	if not mcont == repl and not message.server.id in filter_disable_list and not message.author.bot == True and not message.content == "":
		for i in range( 0, len( mentions ) ):
			repl = repl.replace( "[{}]".format( i ), mentions[ i ] )
			pass
		for i in range( 0, len( occs ) ):
			repl = repl.replace( "(" + str( i ) + ")", occs[ i ] )
			pass
		for i in range( 0, len( tmp[ 1 ] ) ):
			repl = repl.replace( "\{" + str( i ) + "\}", tmp[ 1 ][ i ] )
			pass
		await client.delete_message( message )
		await client.send_message( message.channel, "[{}] ".format( message.author.mention ) + repl )

		identifier = check( message.author.nick, message.author.name, message.author.id )
		print( "{}{} just swore!{}".format( colorama.Fore.LIGHTMAGENTA_EX, identifier, colorama.Fore.RESET ) )
		pass
	pass

@client.event
async def on_ready ( ):
	await client.change_presence( )
	os.system( "cls" )
	print( f"{colorama.Fore.MAGENTA}Ready!!!{colorama.Fore.RESET}" )
	pass

client.run( token )
