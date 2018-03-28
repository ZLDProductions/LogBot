"""
Polling Module
"""
import os
import sqlite3
import subprocess
import traceback
from datetime import datetime

import discord
from colorama import Fore, init
from discord import Client, Colour, Embed, Server, utils

from logbot_data import token, owner_id

CLIENT = Client( )
# noinspection SpellCheckingInspection
init( )
EXITING = False

POLL_PATH = f"{os.getcwd()}\\Discord Logs\\SETTINGS\\Polling"
SQLA = sqlite3.connect( f"{POLL_PATH}\\polling.db" )
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
	writer.write( f"{datetime.now()} (polling.py) - {error_text}\n\n{prev_text}" )
	writer.close( )
	if "SystemExit" in error_text:
		exit( 0 )
	del writer
	del file
	del prev_text

def getprefix ( server: str ) -> str:
	"""
	Gets a server's prefix.
	:param server: A server ID.
	:return: The server's prefix.
	"""
	CURSORB.execute( f"SELECT prefix FROM Prefixes WHERE server='{server}';" )
	return CURSORB.fetchall( )[ 0 ][ 0 ]

def _read ( cmd ):
	"""
	Reads from the DB.
	:param cmd: The SQL Read command.
	:return: The data retrieved.
	"""
	CURSORA.execute( cmd )
	return CURSORA.fetchall( )

def _execute ( cmd ):
	"""
	Executes an SQL command.
	:param cmd: The command.
	"""
	CURSORA.execute( cmd )
	SQLA.commit( )

def parse_num ( num ) -> str:
	"""
	Parses a number so it is more readable.
	:param num: The unparsed number.
	:return: The parsed number.
	"""
	_num = str( num )
	_num = _num[ ::-1 ]
	_num = ",".join( [
		_num[ i:i + 3 ]
		for i in range( 0, len( _num ), 3 )
	] )[ ::-1 ]
	return str( _num )

async def send_no_perm ( message: discord.Message ):
	"""
	Sends a `NO PERMISSION` message to a user.
	:param message: The message object from on_message
	"""
	await CLIENT.send_message( message.channel, "```You do not have permission to use this command.```" )
	print( f"{Fore.LIGHTGREEN_EX}{str(message.author)} attempted to use a command.{Fore.RESET}" )

class Commands:
	"""
	Command methods.
	"""
	class Member:
		"""
		For everyone!
		"""
		@staticmethod
		async def p_status ( message: discord.Message, prefix: str ):
			"""
			Shows the current status of a poll.
			:param message: A discord.Message object.
			:param prefix: The server's prefix.
			"""
			content = message.content.replace( f"p{prefix}status ", "" )
			dat = _read( f"""
					SELECT *
					FROM polls
					WHERE server = "{message.server.id}"
					AND topic_index = "{content}";
					""".replace( "\t", "" ) )
			embed_obj = Embed( title=dat[ 0 ][ 2 ], description=f"Poll status for poll [{dat[0][1]}].", colour=Colour.dark_purple( ) )
			for item in dat:
				embed_obj.add_field( name=f"{item[4]} ({item[3]})", value=str( item[ 5 ] ) )
			_sum = 0
			for item in dat:
				_sum += item[ 5 ]
			if _sum is None:
				_sum = "No"
			else:
				_sum = parse_num( _sum )
			word = 'votes' if not _sum == "1" else 'vote'
			embed_obj.set_footer( text=f"{_sum} {word} so far..." )
			await CLIENT.send_message( message.channel, "Poll status...", embed=embed_obj )
			del content
			del dat
			del embed_obj
			del _sum
			del word
		@staticmethod
		async def p_vote ( message: discord.Message ):
			"""
			Votes on a poll.
			:param message: A discord.Message object.
			"""
			msgs = [ ]
			tmp1 = await CLIENT.send_message( message.channel, f"```What is the index for your poll?```" )
			pindex = await CLIENT.wait_for_message( author=message.author, channel=message.channel )
			msgs.append( tmp1 )
			msgs.append( pindex )
			tmp2 = await CLIENT.send_message( message.channel, f"```What is the index for your choice?```" )
			cindex = await CLIENT.wait_for_message( author=message.author, channel=message.channel )
			msgs.append( tmp2 )
			msgs.append( cindex )

			res = _read( f"""
			SELECT voted
			FROM polls
			WHERE server="{message.server.id}"
			AND topic_index={pindex.content};
			""".replace( "\t", "" ) )

			vote = res[ 0 ][ 0 ]
			if vote is None:
				vote = ""
			if not message.author.id in vote.split( " " ):
				_execute( f"""
				UPDATE polls
				SET result = result + 1
				WHERE server= "{message.server.id}"
				AND topic_index = {pindex.content}
				AND choice_index = {cindex.content};
				""".replace( "\t", "" ) )
				_execute( f"""
				UPDATE polls
				SET voted="{f"{vote}{message.author.id} "}"
				WHERE server="{message.server.id}"
				AND topic_index={pindex.content};
				""".replace( "\t", "" ) )
				await CLIENT.send_message( message.channel, f"Voted! :white_check_mark:" )
			else:
				await CLIENT.send_message( message.channel, f"```You have already voted!```" )
			await CLIENT.delete_messages( msgs )
			del msgs
			del tmp1
			del pindex
			del cindex
			del res
			del vote
		@staticmethod
		async def p_polls ( message: discord.Message ):
			"""
			Shows a list of the current polls.
			:param message: A discord.Message object.
			"""
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
			ret = [ ]
			for index, item in enumerate( stuffs ):
				if index % 5 == 0:
					ret.append( f"{item}\n" )
				else:
					ret[ -1 ] += f"{item}\n"
			for item in ret:
				await CLIENT.send_message( message.channel, f"```{item}```" )
			if not ret:
				await CLIENT.send_message( message.channel, "```There are no polls so far...```" )
			del res
			del stuffs
			del append
			del ret
	# noinspection PyUnusedLocal
	class Admin:
		"""
		For admins only!
		"""
		@staticmethod
		async def p_saved ( message: discord.Message ):
			"""
			Views a list of all saved polls.
			:param message: A discord.Message object.
			"""
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
				else:
					ret[ -1 ] += f"{item}\n"
			for item in ret:
				await CLIENT.send_message( message.channel, f"```{item}```" )
			if not ret:
				await CLIENT.send_message( message.channel, f"```There are no saved polls so far...```" )
			del res
			del stuffs
			del ret
			del append
		@staticmethod
		async def p_remove ( message: discord.Message, prefix: str ):
			"""
			Removes a poll.
			:param message: A discord.Message object.
			:param prefix: The server's prefix.
			"""
			_execute( f"""
			DELETE FROM old_polls
			WHERE server="{message.server.id}"
			AND topic_index="{message.content.replace(f"p{prefix}remove ", "")}";
			""".replace( "\t", "" ) )
			await CLIENT.send_message( message.channel, f"```Removed \"{message.content.replace(f'p{prefix}remove ', '')}\"```" )
		@staticmethod
		async def p_view ( message: discord.Message, prefix: str ):
			"""
			Views a saved poll.
			:param message: A discord.Message object.
			:param prefix: The server's prefix.
			"""
			dat = _read( f"""
			SELECT *
			FROM old_polls
			WHERE server="{message.server.id}"
			AND topic_index="{message.content.replace(f"p{prefix}view ", "")}";
			""".replace( "\t", "" ) )
			embed_obj = Embed( title=dat[ 0 ][ 2 ], description=f"Poll status for poll [{dat[0][1]}].", colour=Colour.dark_purple( ) )
			for item in dat:
				embed_obj.add_field( name=f"{item[4]} ({item[3]})", value=str( item[ 5 ] ) )
			_sum = 0
			for item in dat:
				_sum += item[ 5 ]
			if _sum is None:
				_sum = "No"
			else:
				_sum = parse_num( _sum )
			word = 'votes' if not _sum == '1' else 'vote'
			embed_obj.set_footer( text=f"{_sum} {word}..." )
			await CLIENT.send_message( message.channel, "Poll status... :clipboard:", embed=embed_obj )
			del dat
			del embed_obj
			del _sum
			del word
		@staticmethod
		async def p_save ( message: discord.Message, prefix: str ):
			"""
			Saves a vote.
			:param message: A discord.Message object.
			:param prefix: The server's prefix.
			"""
			content = message.content.replace( f"p{prefix}save ", "" )
			res = _read( f"""
			SELECT topic_index
			FROM old_polls
			WHERE server="{message.server.id}"
			ORDER BY topic_index DESC;
			""".replace( "\t", "" ) )
			if len( res ) < 1:
				res = 0
			else:
				res = res[ 0 ]
			print( res )
			_execute( f"""
			INSERT INTO old_polls
			SELECT server, {res+1}, topic, choice_index, choice, result, voted
			FROM polls
			WHERE polls.server="{message.server.id}"
			AND polls.topic_index="{content}";
			""".replace( "\t", "" ) )
			await CLIENT.send_message( message.channel, ":floppy_disk: Saved the poll!" )
			del content
			del res
		@staticmethod
		async def p_start ( message: discord.Message, prefix: str ):
			"""
			Starts a vote.
			:param message: A discord.Message object.
			:param prefix: The server's prefix.
			"""
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
			except Exception:
				res = 0
			if res == 0:
				topic_index = _read( f"""
				SELECT MAX(topic_index)
				FROM polls
				WHERE server = "{message.server.id}"
				ORDER BY topic_index DESC;
				""".replace( "\t", "" ) )[ 0 ][ 0 ]
				embed_obj = discord.Embed( title=topic, colour=discord.Colour.orange( ) )
				for index, item in enumerate( choices ):
					if topic_index is None:
						topic_index = 0
					embed_obj.add_field( name=f"{item} ({index+1})", value="0" )
					_execute( f"""
					INSERT INTO polls (server, topic_index, topic, choice_index, choice, result)
					VALUES ("{message.server.id}", {topic_index+1}, "{topic}", {index+1}, "{item}", 0);
					""".replace( "\t", "" ) )
				tmp = '\n'.join( [ f"{item}: {ind + 1}" for ind, item in enumerate( choices ) ] )
				await CLIENT.send_message( message.channel, f":hourglass_flowing_sand: Started a poll with an index of {topic_index+1}!", embed=embed_obj )
				del topic_index
				del embed_obj
				del tmp
			else:
				await CLIENT.send_message( message.channel, "```That poll already exists!```" )
			del content
			del topic
			del choices
		@staticmethod
		async def p_end ( message: discord.Message, prefix: str ):
			"""
			Ends a vote.
			:param message: A discord.Message object.
			:param prefix: The server's prefix.
			"""
			content = message.content.replace( f"p{prefix}end ", "" )
			dat = _read( f"""
			SELECT *
			FROM polls
			WHERE server = "{message.server.id}"
			AND topic_index = "{content}"
			ORDER BY result DESC;
			""".replace( "\t", "" ) )
			embed_obj = Embed( title=dat[ 0 ][ 2 ], description=f"Poll results for poll {dat[0][1]}.", colour=Colour.dark_purple( ) )
			for item in dat:
				embed_obj.add_field( name=f"{item[4]} ({item[3]})", value=str( item[ 5 ] ) )
			_sum = 0
			for item in dat:
				_sum += item[ 5 ]
			if _sum is None:
				_sum = "No"
			else:
				_sum = parse_num( _sum )
			word = "votes" if not _sum == "1" else "vote"
			embed_obj.set_footer( text=f"{_sum} total {word}." )
			await CLIENT.send_message( message.channel, "Poll results... :clipboard:", embed=embed_obj )
			_execute( f"""
			DELETE FROM polls
			WHERE server = "{message.server.id}"
			AND topic_index = "{content}";
			""".replace( "\t", "" ) )
			del content
			del dat
			del embed_obj
			del _sum
			del word
	class Owner:
		"""
		For the developer only!
		"""

@CLIENT.event
async def on_message ( message ):
	"""
	Called when the bot receives a message.
	:param message: A discord.Message object.
	"""
	global EXITING
	try:
		prefix = getprefix( message.server.id )
		admin_role = utils.find( lambda r:r.name == "LogBot Admin", message.server.roles )
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
			return False
		if isinstance( message.server, Server ):
			if startswith( f"p{prefix}start " ):
				if admin_role in message.author.roles or message.author.id == owner_id:
					await Commands.Admin.p_start( message, prefix )
				else:
					send_no_perm( message )
			elif startswith( f"p{prefix}end " ):
				if admin_role in message.author.roles or message.author.id == owner_id:
					await Commands.Admin.p_end( message, prefix )
				else:
					send_no_perm( message )
			elif startswith( f"p{prefix}status " ):
				await Commands.Member.p_status( message, prefix )
			elif startswith( f"p{prefix}vote" ):
				await Commands.Member.p_vote( message )
			elif startswith( f"p{prefix}polls" ):
				await Commands.Member.p_polls( message )
			elif startswith( f"p{prefix}save " ):
				if admin_role in message.author.roles:
					await Commands.Admin.p_save( message, prefix )
				else:
					send_no_perm( message )
			elif startswith( f"p{prefix}view " ):
				if admin_role in message.author.roles:
					await Commands.Admin.p_view( message, prefix )
				else:
					send_no_perm( message )
			elif startswith( f"p{prefix}remove " ):
				if admin_role in message.author.roles:
					await Commands.Admin.p_remove( message, prefix )
				else:
					send_no_perm( message )
			elif startswith( f"p{prefix}saved" ):
				if admin_role in message.author.roles:
					await Commands.Admin.p_saved( message )
				else:
					send_no_perm( message )
			elif startswith( "logbot.polling.update", "p$update", "$update" ):
				if message.author.id == owner_id:
					do_update = True
				else:
					send_no_perm( message )
			elif startswith( f"{prefix}ping" ):
				timestamp = datetime.now( ) - message.timestamp
				await CLIENT.send_message( message.channel, f"```LogBot Polling Online ~ {round(timestamp.microseconds / 1000)}```" )
				del timestamp
			elif startswith( "$prefix", "logbot.polling.exit" ):
				if message.author.id == owner_id:
					EXITING = True
					await CLIENT.logout( )

		if do_update:
			print( f"{Fore.LIGHTCYAN_EX}Updating...{Fore.RESET}" )
			await CLIENT.close( )
			subprocess.Popen( f"python {os.getcwd()}\\polling.py", False )
			exit( 0 )
		del prefix
		del admin_role
		del do_update
	except Exception:
		log_error( traceback.format_exc( ) )

@CLIENT.event
async def on_ready ( ):
	"""
	Called when the bot logs in.
	"""
	await CLIENT.change_presence( )
	# os.system( "cls" )
	print( f"{Fore.MAGENTA}Polling Ready!{Fore.RESET}" )
	try:
		_execute( """
			CREATE TABLE polls (server VARCHAR(50), topic_index INTEGER, topic VARCHAR(100), choice_index INTEGER, choice VARCHAR(50), result INTEGER, voted VARCHAR(19000000));
			""".replace( "\t", "" ) )
	except Exception:
		pass
	try:
		_execute( """
		CREATE INDEX poll_index
		ON polls(server, topic_index, topic, choice_index, choice, result, voted);
		""".replace( "\t", "" ) )
	except Exception:
		pass
	try:
		_execute(
			f"""
			CREATE TABLE old_polls (server VARCHAR(50), topic_index INTEGER, topic VARCHAR(100), choice_index INTEGER, choice VARCHAR(100), result INTEGER, voted VARCHAR(19000000));
			""".replace(
				"\t",
				""
			)
		)
	except Exception:
		pass
	try:
		_execute(
			f"""
			CREATE INDEX op_index
			ON old_polls (server, topic_index, topic, choice_index, choice, result, voted);
		""".replace(
				"\t",
				""
			)
		)
	except Exception:
		pass

CLIENT.run( token )

if not EXITING:
	subprocess.Popen( f"python {os.getcwd()}\\polling.py" )
	exit( 0 )
