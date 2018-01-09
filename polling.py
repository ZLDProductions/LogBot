import os
import sqlite3
import subprocess
import traceback
from datetime import datetime

import discord
from colorama import Fore, init
from discord import Client, Colour, Embed, Server
from discord.utils import find

from logbot_data import token, owner_id

client = Client( )
# noinspection SpellCheckingInspection
init( )
exiting = False

poll_path = f"{os.getcwd()}\\Discord Logs\\SETTINGS\\Polling"
_sql = sqlite3.connect( f"{poll_path}\\polling.db" )
_sql_cursor = _sql.cursor( )

__sql = sqlite3.connect( f"{os.getcwd()}\\Discord Logs\\SETTINGS\\logbot.db" )
__cursor = __sql.cursor( )

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
	writer.write( f"{datetime.now()} (polling.py) - {error_text}\n\n{prev_text}" )
	writer.close( )
	if "SystemExit" in error_text:
		exit( 0 )
		pass
	del writer
	pass

def getprefix ( server: str ) -> str:
	__cursor.execute( f"SELECT prefix FROM Prefixes WHERE server='{server}';" )
	return __cursor.fetchall( )[ 0 ][ 0 ]

def _read ( cmd ):
	_sql_cursor.execute( cmd )
	return _sql_cursor.fetchall( )
	pass

def _execute ( cmd ):
	_sql_cursor.execute( cmd )
	_sql.commit( )
	pass

def parse_num ( num ) -> str:
	_num = str( num )
	_num = _num[ ::-1 ]
	_num = ",".join( [
		_num[ i:i + 3 ]
		for i in range( 0, len( _num ), 3 )
	] )[ ::-1 ]
	return str( _num )
	pass

async def sendNoPerm ( message: discord.Message ):
	"""
	Sends a `NO PERMISSION` message to a user.
	:param message: The message object from on_message
	"""
	await client.send_message( message.channel, "```You do not have permission to use this command.```" )
	print( f"{Fore.LIGHTGREEN_EX}{str(message.author)} attempted to use a command.{Fore.RESET}" )
	pass

class Commands:
	class Member:
		@staticmethod
		async def p_status ( message: discord.Message, prefix: str ):
			content = message.content.replace( f"p{prefix}status ", "" )
			dat = _read( f"""
					SELECT *
					FROM polls
					WHERE server = "{message.server.id}"
					AND topic_index = "{content}";
					""".replace( "\t", "" ) )
			e = Embed( title=dat[ 0 ][ 2 ], description=f"Poll status for poll [{dat[0][1]}].", colour=Colour.dark_purple( ) )
			for item in dat:
				e.add_field( name=f"{item[4]} ({item[3]})", value=str( item[ 5 ] ) )
				pass
			_sum = 0
			for item in dat:
				_sum += item[ 5 ]
				pass
			if _sum is None:
				_sum = "No"
				pass
			else:
				_sum = parse_num( _sum )
				pass
			word = 'votes' if not _sum == "1" else 'vote'
			e.set_footer( text=f"{_sum} {word} so far..." )
			await client.send_message( message.channel, "Poll status...", embed=e )
			pass
		@staticmethod
		async def p_vote ( message: discord.Message ):
			msgs = [ ]
			tmp1 = await client.send_message( message.channel, f"```What is the index for your poll?```" )
			pindex = await client.wait_for_message( author=message.author, channel=message.channel )
			msgs.append( tmp1 )
			msgs.append( pindex )
			tmp2 = await client.send_message( message.channel, f"```What is the index for your choice?```" )
			cindex = await client.wait_for_message( author=message.author, channel=message.channel )
			msgs.append( tmp2 )
			msgs.append( cindex )

			res = _read( f"""
			SELECT voted
			FROM polls
			WHERE server="{message.server.id}"
			AND topic_index={pindex.content};
			""".replace( "\t", "" ) )

			v = res[ 0 ][ 0 ]
			if v is None:
				v = ""
				pass
			if not message.author.id in v.split( " " ):
				_execute( f"""
				UPDATE polls
				SET result = result + 1
				WHERE server= "{message.server.id}"
				AND topic_index = {pindex.content}
				AND choice_index = {cindex.content};
				""".replace( "\t", "" ) )
				_execute( f"""
				UPDATE polls
				SET voted="{f"{v}{message.author.id} "}"
				WHERE server="{message.server.id}"
				AND topic_index={pindex.content};
				""".replace( "\t", "" ) )
				await client.send_message( message.channel, f"Voted! :white_check_mark:" )
				pass
			else:
				await client.send_message( message.channel, f"```You have already voted!```" )
				pass
			await client.delete_messages( msgs )

			# vote = message.content.replace( f"p{prefix}vote ", "", 1 ).split( " " )
			# res = _read( f"""
			# SELECT voted
			# FROM polls
			# WHERE server = "{message.server.id}"
			# AND topic_index = {vote[0]};
			# """.replace( "\t", "" ) )
			# v = res[ 0 ][ 0 ]
			# if v is None: v = ""
			# if not message.author.id in v.split( " " ):
			# 	_execute( f"""
			# 	UPDATE polls
			# 	SET result = result + 1
			# 	WHERE server = "{message.server.id}"
			# 	AND topic_index = {vote[0]}
			# 	AND choice_index = {vote[1]};
			# 	""".replace( "\t", "" ) )
			# 	_execute( f"""
			# 	UPDATE polls
			# 	SET voted = "{f"{v}{message.author.id} "}"
			# 	WHERE server = "{message.server.id}"
			# 	AND topic_index = {vote[0]};
			# 	""".replace( "\t", "" ) )
			# 	await client.send_message( message.channel, f"Voted! :white_check_mark:" )
			# 	pass
			# else: await client.send_message( message.channel, f"```You have already voted!```" )
			pass
		@staticmethod
		async def p_polls ( message: discord.Message ):
			res = _read( f"""
			SELECT topic_index, topic
			FROM polls
			WHERE server = "{message.server.id}";
			""".replace( "\t", "" ) )
			stuffs = [ ]
			append = stuffs.append
			for item in res:
				if not f"{item[0]} : {item[1]}" in stuffs:
					append( f"{item[0]} : {item[1]}" )
					pass
				pass
			ret = [ ]
			for index, item in enumerate( stuffs ):
				if index % 5 == 0:
					ret.append( f"{item}\n" )
					pass
				else:
					ret[ -1 ] += f"{item}\n"
					pass
				pass
			for item in ret:
				await client.send_message( message.channel, f"```{item}```" )
				pass
			if len( ret ) == 0:
				await client.send_message( message.channel, "```There are no polls so far...```" )
				pass
			pass
		pass
	# noinspection PyUnusedLocal
	class Admin:
		@staticmethod
		async def p_saved ( message: discord.Message ):
			res = _read( f"""
			SELECT topic_index, topic
			FROM old_polls
			WHERE server="{message.server.id}";
			""".replace( "\t", "" ) )
			stuffs = [
				f"{item[0]} : {item[1]}"
				for item in res
			]
			ret = [ ]
			append = ret.append
			for index, item in enumerate( stuffs ):
				if index % 5 == 0:
					append( f"{item}\n" )
					pass
				else:
					ret[ -1 ] += f"{item}\n"
					pass
				pass
			for item in ret:
				await client.send_message( message.channel, f"```{item}```" )
				pass
			if len( ret ) == 0:
				await client.send_message( message.channel, f"```There are no saved polls so far...```" )
				pass
			pass
		@staticmethod
		async def p_remove ( message: discord.Message, prefix: str ):
			_execute( f"""
			DELETE FROM old_polls
			WHERE server="{message.server.id}"
			AND topic_index="{message.content.replace(f"p{prefix}remove ", "")}";
			""".replace( "\t", "" ) )
			await client.send_message( message.channel, f"```Removed \"{message.content.replace(f'p{prefix}remove ', '')}\"```" )
			pass
		@staticmethod
		async def p_view ( message: discord.Message, prefix: str ):
			dat = _read( f"""
			SELECT *
			FROM old_polls
			WHERE server="{message.server.id}"
			AND topic_index="{message.content.replace(f"p{prefix}view ", "")}";
			""".replace( "\t", "" ) )
			e = Embed( title=dat[ 0 ][ 2 ], description=f"Poll status for poll [{dat[0][1]}].", colour=Colour.dark_purple( ) )
			for item in dat:
				e.add_field( name=f"{item[4]} ({item[3]})", value=str( item[ 5 ] ) )
				pass
			_sum = 0
			for item in dat:
				_sum += item[ 5 ]
				pass
			if _sum is None:
				_sum = "No"
				pass
			else:
				_sum = parse_num( _sum )
				pass
			word = 'votes' if not _sum == '1' else 'vote'
			e.set_footer( text=f"{_sum} {word}..." )
			await client.send_message( message.channel, "Poll status... :clipboard:", embed=e )
			pass
		@staticmethod
		async def p_save ( message: discord.Message, prefix: str ):
			content = message.content.replace( f"p{prefix}save ", "" )
			res = _read( f"""
			SELECT topic_index
			FROM old_polls
			WHERE server="{message.server.id}"
			ORDER BY topic_index DESC;
			""".replace( "\t", "" ) )
			if len( res ) < 1:
				res = 0
				pass
			else:
				res = res[ 0 ]
				pass
			print( res )
			_execute( f"""
			INSERT INTO old_polls
			SELECT server, {res+1}, topic, choice_index, choice, result, voted
			FROM polls
			WHERE polls.server="{message.server.id}"
			AND polls.topic_index="{content}";
			""".replace( "\t", "" ) )
			await client.send_message( message.channel, ":floppy_disk: Saved the poll!" )
			pass
		@staticmethod
		async def p_start ( message: discord.Message, prefix: str ):
			content = message.content.replace( f"p{prefix}start ", "" ).split( "|" )
			topic = content[ 0 ]
			content.remove( content[ 0 ] )
			choices = content
			try:
				res = _read( f"""
			SELECT COUNT(*)
			WHERE server = "{message.server.id}"
			AND topic = "{topic}";
			""".replace( "\t", "" ) )
				pass
			except:
				res = 0
				pass
			if res == 0:
				topic_index = _read( f"""
				SELECT MAX(topic_index)
				FROM polls
				WHERE server = "{message.server.id}"
				ORDER BY topic_index DESC;
				""".replace( "\t", "" ) )[ 0 ][ 0 ]
				e = discord.Embed( title=topic, colour=discord.Colour.orange( ) )
				for index, item in enumerate( choices ):
					if topic_index is None:
						topic_index = 0
						pass
					e.add_field( name=f"{item} ({index+1})", value="0" )
					_execute( f"""
					INSERT INTO polls (server, topic_index, topic, choice_index, choice, result)
					VALUES ("{message.server.id}", {topic_index+1}, "{topic}", {index+1}, "{item}", 0);
					""".replace( "\t", "" ) )
					pass
				tmp = '\n'.join( [ f"{item}: {ind + 1}" for ind, item in enumerate( choices ) ] )
				await client.send_message( message.channel, f":hourglass_flowing_sand: Started a poll with an index of {topic_index+1}!", embed=e )
			else:
				await client.send_message( message.channel, "```That poll already exists!```" )
				pass
			pass
		@staticmethod
		async def p_end ( message: discord.Message, prefix: str ):
			content = message.content.replace( f"p{prefix}end ", "" )
			dat = _read( f"""
			SELECT *
			FROM polls
			WHERE server = "{message.server.id}"
			AND topic_index = "{content}"
			ORDER BY result DESC;
			""".replace( "\t", "" ) )
			e = Embed( title=dat[ 0 ][ 2 ], description=f"Poll results for poll {dat[0][1]}.", colour=Colour.dark_purple( ) )
			for item in dat:
				e.add_field( name=f"{item[4]} ({item[3]})", value=str( item[ 5 ] ) )
				pass
			_sum = 0
			for item in dat:
				_sum += item[ 5 ]
				pass
			if _sum is None:
				_sum = "No"
				pass
			else:
				_sum = parse_num( _sum )
				pass
			word = "votes" if not _sum == "1" else "vote"
			e.set_footer( text=f"{_sum} total {word}." )
			await client.send_message( message.channel, "Poll results... :clipboard:", embed=e )
			_execute( f"""
			DELETE FROM polls
			WHERE server = "{message.server.id}"
			AND topic_index = "{content}";
			""".replace( "\t", "" ) )
			pass
		pass
	class Owner:
		pass
	pass

@client.event
async def on_message ( message ):
	global exiting
	try:
		prefix = getprefix( message.server.id )
		admin_role = find( lambda r:r.name == "LogBot Admin", message.server.roles )
		do_update = False
		def startswith ( *msgs: str, val: str = message.content ):
			"""
			Checks if `val` startswith a value in `msgs`
			:param msgs: Several arguments, all of which are strings.
			:param val: A string that will be checked for similarities.
			:return: True if `val` starts with any `msgs`, else False.
			"""
			for msg in msgs:
				if val.startswith( msg ):
					return True
				pass
			return False
		if isinstance( message.server, Server ):
			if startswith( f"p{prefix}start " ):
				if admin_role in message.author.roles or message.author.id == owner_id:
					await Commands.Admin.p_start( message, prefix )
					pass
				else:
					sendNoPerm( message )
					pass
				pass
			elif startswith( f"p{prefix}end " ):
				if admin_role in message.author.roles or message.author.id == owner_id:
					await Commands.Admin.p_end( message, prefix )
					pass
				else:
					sendNoPerm( message )
					pass
				pass
			elif startswith( f"p{prefix}status " ):
				await Commands.Member.p_status( message, prefix )
				pass
			elif startswith( f"p{prefix}vote" ):
				await Commands.Member.p_vote( message )
				pass
			elif startswith( f"p{prefix}polls" ):
				await Commands.Member.p_polls( message )
				pass
			elif startswith( f"p{prefix}save " ):
				if admin_role in message.author.roles:
					await Commands.Admin.p_save( message, prefix )
					pass
				else:
					sendNoPerm( message )
					pass
				pass
			elif startswith( f"p{prefix}view " ):
				if admin_role in message.author.roles:
					await Commands.Admin.p_view( message, prefix )
					pass
				else:
					sendNoPerm( message )
					pass
				pass
			elif startswith( f"p{prefix}remove " ):
				if admin_role in message.author.roles:
					await Commands.Admin.p_remove( message, prefix )
					pass
				else:
					sendNoPerm( message )
					pass
				pass
			elif startswith( f"p{prefix}saved" ):
				if admin_role in message.author.roles:
					await Commands.Admin.p_saved( message )
					pass
				else:
					sendNoPerm( message )
					pass
				pass
			elif startswith( "logbot.polling.update", "p$update", "$update" ):
				if message.author.id == owner_id:
					do_update = True
					pass
				else:
					sendNoPerm( message )
					pass
				pass
			elif startswith( f"{prefix}ping" ):
				tm = datetime.now( ) - message.timestamp
				await client.send_message( message.channel, f"```LogBot Polling Online ~ {round(tm.microseconds / 1000)}```" )
				pass
			elif startswith( "$prefix", "logbot.polling.exit" ):
				if message.author.id == owner_id:
					exiting = True
					await client.logout( )
					pass
				pass
			pass

		if do_update:
			print( f"{Fore.LIGHTCYAN_EX}Updating...{Fore.RESET}" )
			await client.close( )
			subprocess.Popen( f"python {os.getcwd()}\\polling.py", False )
			exit( 0 )
			pass
		pass
	except:
		log_error( traceback.format_exc( ) )
		pass
	pass

@client.event
async def on_ready ( ):
	await client.change_presence( )
	# os.system( "cls" )
	print( f"{Fore.MAGENTA}Polling Ready!{Fore.RESET}" )
	try: _execute( """
			CREATE TABLE polls (server VARCHAR(50), topic_index INTEGER, topic VARCHAR(100), choice_index INTEGER, choice VARCHAR(50), result INTEGER, voted VARCHAR(19000000));
			""".replace( "\t", "" ) )
	except: pass
	try: _execute( """
		CREATE INDEX poll_index
		ON polls(server, topic_index, topic, choice_index, choice, result, voted);
		""".replace( "\t", "" ) )
	except: pass
	try: _execute( f"""
	CREATE TABLE old_polls (server VARCHAR(50), topic_index INTEGER, topic VARCHAR(100), choice_index INTEGER, choice VARCHAR(100), result INTEGER, voted VARCHAR(19000000));
	""".replace( "\t", "" ) )
	except: pass
	try: _execute( f"""
		CREATE INDEX op_index
		ON old_polls (server, topic_index, topic, choice_index, choice, result, voted);
		""".replace( "\t", "" ) )
	except: pass
	pass

client.run( token )

if not exiting:
	subprocess.Popen( f"python {os.getcwd()}\\polling.py" )
	exit( 0 )
	pass
