"""
Games module.
"""
import os
import random
import sqlite3
import subprocess
import traceback
from datetime import datetime

import discord
from colorama import Fore, init

from logbot_data import token, owner_id
import sql

# noinspection SpellCheckingInspection
CLIENT = discord.Client( )
init( )
EXITING = False
SQL = sqlite3.connect( "logbot.db" )
CURSOR = SQL.cursor( )

RET = ""
LEFT = ""

LOGS_PATH = f'{os.getcwd()}\\Discord Logs'
SETTINGS_PATH = f"{LOGS_PATH}\\SETTINGS"
DB = sql.SQL( )
_SQL = sqlite3.connect( f"{SETTINGS_PATH}\\logbot.db" )
_CURSOR = SQL.cursor( )

def log_error ( error_text: str ):
	"""
	Logs the bot's errors.
	:param error_text:
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
	writer.write( f"{datetime.now()} (games.py) - {error_text}\n\n{prev_text}" )
	writer.close( )
	if "SystemExit" in error_text:
		exit( 0 )
	del writer
	del file
	del prev_text

def getprefix ( server: str ) -> str:
	"""
	Fetches a server's prefix.
	:param server: A discord.Server object.
	:return: The prefix.
	"""
	return DB.read( "Prefixes", server )

CHALLENGES = [
	"Type no capital letters.",
	"Type no lower-case letters.",
	"Use one word sentences"
]

def _read ( cmd: str ):
	CURSOR.execute( cmd )
	return CURSOR.fetchall( )

def _execute ( cmd: str ):
	CURSOR.execute( cmd )
	SQL.commit( )

def format_message ( msg: str ):
	"""
	Formats the strings.
	:param msg: The message.
	:return: The new messages.
	"""
	return [
		f"```{msg[n:n+1993]}```"
		for n in range( 0, len( msg ), 1993 )
	]

@CLIENT.event
async def on_message ( message ):
	"""
	Occurs when the bot receives a message.
	:param message: A discord.Message object.
	"""
	global RET, LEFT, EXITING
	try:
		prefix = getprefix( message.server.id )

		do_update = False

		def startswith ( *msgs, val=message.content ):
			"""
			Checks if a string starts with several other substrings.
			:param msgs: The strings to check for.
			:param val: The string to check.
			:return: True or False
			"""
			for _msg_ in msgs:
				if val.startswith( _msg_ ):
					return True
			return False
		# noinspection SpellCheckingInspection
		def replace ( *stuffs, repl="", val=message.content ):
			"""
			Replaces several different substrings within a string.
			:param stuffs: The substrings.
			:param repl: The replacement substrings.
			:param val: The string to replace within.
			"""
			for strng in stuffs:
				val = val.replace( strng, repl )
			return val
		if startswith( f"{prefix}guess " ):
			try:
				content = message.content.replace( f"{prefix}guess ", "" )
				if content == _read( f"""SELECT * FROM scrambles WHERE sid='{message.server.id}'""" )[ 0 ][ 0 ]:
					await CLIENT.send_message( message.channel, "You are correct!" )
					_execute( f"""DELETE FROM scrambles WHERE sid='{message.server.id}' AND word='{content}'""" )
				else:
					tmp = _read( f"""SELECT * FROM scrambles WHERE sid='{message.server.id}'""" )[ 0 ]
					word = list( tmp[ 0 ] )
					guessed = list( content )
					overall = list( )
					length = len( word ) \
						if len( word ) >= len( guessed ) \
						else len( guessed )
					for i in range( 0, length ):
						if word[ i ].lower( ) == guessed[ i ].lower( ):
							overall.append( word[ i ] )
						else:
							overall.append( "_" )
					await CLIENT.send_message( message.channel, f"Incorrect!\n{tmp[1]}\n{''.join(overall)}" )
					del tmp
					del word
					del guessed
					del overall
					del length
			except Exception:
				await CLIENT.send_message( message.channel, "```No scramble exists.```" )
		elif startswith( f"{prefix}scramble " ):
			content = message.content.replace( f"{prefix}scramble ", "", 1 )
			if startswith( "add", val=content ):
				content = content.replace( "add ", "", 1 )
				try:
					_execute( f"""INSERT INTO wordlist (word) VALUES ('{content}');""" )
					await CLIENT.send_message(
						message.channel,
						f"```Added \"{content}\".```"
					)
				except Exception:
					await CLIENT.send_message(
						message.channel,
						f"```That word/phrase already exists in the database!```"
					)
			elif startswith( "rem", val=content ):
				content = content.replace( "rem ", "", 1 )
				try:
					_execute( f"""
					DELETE FROM wordlist
					WHERE word='{content}';
					""".replace( "\t", "" ) )
					await CLIENT.send_message( message.channel, f"```Removed \"{content}\"```" )
				except Exception:
					await CLIENT.send_message( message.channel, f"```\"{content}\" is not in the database!```" )
			elif startswith( "find", val=content ):
				content = content.replace( "find ", "", 1 )
				res = _read( f"""SELECT word FROM wordlist WHERE word LIKE '%{content}%'""" )
				RET = "```Results:\n```"
				for item in res:
					RET += item[ 0 ]
				await CLIENT.send_message( message.channel, RET )
				del res
				del RET
			elif startswith( "list", val=content ):
				res = _read( f"""SELECT * FROM wordlist ORDER BY word DESC;""" )
				res = [
					item[ 0 ]
					for item in res
				]
				for msg in format_message( ', '.join( res ) ):
					await CLIENT.send_message( message.channel, msg )
				del res
			del content
		elif startswith( f"{prefix}scramble" ):
			try:
				res = _read( f"""SELECT * FROM wordlist;""" )
				word = random.choice( res )[ 0 ]
				shuffle = ""
				for item in word.split( " " ):
					shuff = list( item )
					random.shuffle( shuff )
					shuffle += " " + "".join( shuff )
					del shuff
				shuffle = shuffle[ 1: ]
				_execute( f"""
				INSERT INTO scrambles (word, scramble, sid)
				VALUES ('{word}', '{shuffle}', '{message.server.id}');
				""".replace( "\t", "" ) )
				RET = ""
				LEFT = ""
				print( f"{Fore.CYAN}Started word scramble: {word}, {shuffle}{Fore.RESET}" )
				await CLIENT.send_message( message.channel, f"```Started a word scramble:\n{shuffle}```" )
				del res
				del word
				del shuffle
				del RET
				del LEFT
			except Exception:
				await CLIENT.send_message( message.channel, "```A scramble already exists!```" )
		elif startswith( f"{prefix}giveup" ):
			try:
				await CLIENT.send_message(
					message.channel,
					"```The word was: \"" + _read(
						f"SELECT word FROM scrambles WHERE sid='{message.server.id}'"
					)[ 0 ][ 0 ] + "\"```"
				)
				_execute( f"""DELETE FROM scrambles WHERE sid='{message.server.id}'""" )
			except Exception:
				await CLIENT.send_message( message.channel, "```No scramble exists.```" )
		elif startswith( f"g{prefix}rps " ):
			_choices = [ "rock", "paper", "scissors" ]
			_content = message.content.replace( f"g{prefix}rps ", "" )
			_choice = random.choice( _choices )
			def _check_winner ( choice_one: str, choice_2: str ) -> str:
				if choice_one == choice_2:
					return "No one"
				elif choice_one == "rock":
					return choice_2 if choice_2 == "paper" else choice_one
				elif choice_one == "paper":
					return choice_2 if choice_2 == "scissors" else choice_one
				elif choice_one == "scissors":
					return choice_2 if choice_2 == "rock" else choice_one
			await CLIENT.send_message(
				message.channel,
				f"I chose {_choice}, you chose {_content}. {_check_winner(_choice, _content)} won!"
			)
			del _choices
			del _content
			del _choice
		elif startswith( f"g{prefix}rpsls " ):
			_choices = [ "rock", "paper", "scissors", "lizard", "Spock" ]
			_content = message.content.replace( f"g{prefix}rpsls ", "" ).replace( "spock", "Spock" )
			_choice = random.choice( _choices )
			_winner = ""
			if _choice == _content:
				_winner = "No one"
			elif _choice == "rock":
				if _content == "Spock" or _content == "paper":
					_winner = _content
				elif _content == "scissors" or _content == "lizard":
					_winner = _choice
			elif _choice == "paper":
				if _content == "lizard" or _content == "scissors":
					_winner = _content
				elif _content == "Spock" or _content == "rock":
					_winner = _choice
			elif _choice == "scissors":
				if _content == "Spock" or _content == "rock":
					_winner = _content
				elif _content == "lizard" or _content == "paper":
					_winner = _choice
			elif _choice == "lizard":
				if _content == "scissors" or _content == "rock":
					_winner = _content
				elif _content == "Spock" or _content == "paper":
					_winner = _choice
			elif _choice == "Spock":
				if _content == "lizard" or _content == "paper":
					_winner = _content
				elif _content == "rock" or _content == "scissors":
					_winner = _choice

			await CLIENT.send_message(
				message.channel,
				f"I chose {_choice}, you chose {_content}. {_winner} wins!"
			)
			del _choices
			del _content
			del _choice
			del _winner
		elif startswith( f"g{prefix}rules " ):
			content = message.content.replace( f"g{prefix}rules ", "" )
			if content == "rps":
				RET = """**rock** smashes **scissors**\n**paper** covers **rock**\n**scissors** cut **paper**"""
				await CLIENT.send_message( message.channel, RET )
				del RET
			elif content == "rpsls":
				RET = """**rock** smashes **scissors** and crushes **lizard**
				**paper** covers **rock** and blinds **Spock**
				**scissors** cut **paper** and decapitate **lizard**
				**lizard** eats **paper** and poisons **Spock**
				**Spock** destroys **rock** and disintegrates **scissors**""" \
					.replace( "\t", "" )
				await CLIENT.send_message( message.channel, RET )
				del RET
			elif content == "scramble":
				RET = """The bot will scramble a word.
				You have to find the original word.""".replace( "\t", "" )
				await CLIENT.send_message( message.channel, RET )
				del RET
		elif startswith( "$exit", "logbot.games.exit" ):
			if message.author.id == owner_id:
				EXITING = True
				await CLIENT.logout( )
		elif startswith( f"$update", "logbot.games.update" ):
			if message.author.id == owner_id:
				do_update = True
		elif startswith( f"{prefix}ping" ):
			timestamp = datetime.now( ) - message.timestamp
			await CLIENT.send_message(
				message.channel,
				f"```LogBot Games Online ~ {round(timestamp.microseconds / 1000)}```"
			)
			del timestamp
		elif startswith( f"g{prefix}get\n", "```sql\n--games\n--get" ):
			if message.author.id == owner_id:
				try:
					msg = "```Execution Successful. Result:\n" + str(
						_read(
							replace(
								"{uid}",
								repl=message.author.id,
								val=replace(
									"{sid}",
									repl=message.server.id,
									val=replace(
										f"g{prefix}get\n",
										"```sql",
										"```",
										repl=""
									)
								)
							)
						)
					) + "```"
					for _msg in format_message( msg ):
						await CLIENT.send_message( message.channel, _msg )
					del msg
				except Exception:
					await CLIENT.send_message(
						message.channel,
						f"```Execution Failed.\n{traceback.format_exc()}```"
					)
		elif startswith( f"g{prefix}execute\n", "```sql\n--games\n--execute" ):
			if message.author.id == owner_id:
				try:
					_execute(
						replace(
							f"g{prefix}execute\n",
							"```sql",
							"```",
							repl=""
						).replace(
							"{sid}",
							message.server.id
						).replace(
							"{uid}",
							message.author.id
						)
					)
					await CLIENT.send_message( message.channel, f"```Execution Successful.```" )
				except Exception:
					await CLIENT.send_message(
						message.channel,
						f"```Execution Failed.\n{traceback.format_exc()}```" )
		elif startswith( "g{prefix}challenge" ):
			await CLIENT.send_message( message.channel, random.choice( CHALLENGES ) )

		if do_update:
			print( Fore.LIGHTCYAN_EX + "Updating..." + Fore.RESET )
			await CLIENT.close( )
			subprocess.Popen( "python " + os.getcwd( ) + "\\games.py", False )
			exit( 0 )
	except Exception:
		log_error( traceback.format_exc( ) )

@CLIENT.event
async def on_ready ( ):
	"""
	Occurs when the bot logs in.
	"""
	await CLIENT.change_presence( )
	# os.system( "cls" )
	print( f"{Fore.MAGENTA}Games Ready!{Fore.RESET}" )
	try:
		_execute( f"""CREATE TABLE wordlist (word VARCHAR(1000) UNIQUE);""" )
	except Exception:
		pass
	try:
		_execute( f"""CREATE INDEX wordlist_index ON wordlist (word);""" )
	except Exception:
		pass
	try:
		_execute(
			"CREATE TABLE scrambles (word VARCHAR(1000), scramble VARCHAR(1000), sid VARCHAR(50) UNIQUE);"
		)
	except Exception:
		pass
	try:
		_execute( f"""CREATE INDEX scrambles_index ON scrambles (word, scramble, sid);""" )
	except Exception:
		pass

CLIENT.run( token )

if not EXITING:
	subprocess.Popen( f"python {os.getcwd()}\\games.py" )
	exit( 0 )
