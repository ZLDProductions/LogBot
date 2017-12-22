import os
import random
import sqlite3
import subprocess
import traceback
from datetime import datetime

import discord
from colorama import Fore, init

from sql import SQL
from logbot_data import token

# noinspection SpellCheckingInspection
client = discord.Client( )
init( )
exiting = False
sql = sqlite3.connect( "logbot.db" )
cursor = sql.cursor( )

ret = ""
left = ""

logs = f'{os.getcwd()}\\Discord Logs'
settings = f"{logs}\\SETTINGS"
db = SQL( )
_sql = sqlite3.connect( f"{settings}\\logbot.db" )
_cursor = sql.cursor( )

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
	writer.write( f"{datetime.now()} (games.py) - {error_text}\n\n{prev_text}" )
	writer.close( )
	if "SystemExit" in error_text: exit( 0 )
	del writer
	pass

def getprefix ( server: str ) -> str:
	# _cursor.execute( f"SELECT prefix FROM Prefixes WHERE server='{server}';" )
	# return _cursor.fetchall( )[ 0 ][ 0 ]
	return db.read( "Prefixes", server )

challenges = [
	"Type no capital letters.",
	"Type no lower-case letters.",
	"Use one word sentences"
]

def _read ( cmd: str ):
	cursor.execute( cmd )
	return cursor.fetchall( )

def _execute ( cmd: str ):
	cursor.execute( cmd )
	sql.commit( )
	pass

def format_message ( msg: str ): return [ f"```{msg[n:n+1993]}```" for n in range( 0, len( msg ), 1993 ) ]

@client.event
async def on_message ( message ):
	global ret, left
	try:
		prefix = getprefix( message.server.id )

		do_update = False
		def startswith ( *msgs, val=message.content ):
			for m in msgs:
				if val.startswith( m ): return True
				pass
			return False
		def replace ( *stuffs, repl="", val=message.content ):
			for s in stuffs: val = val.replace( s, repl )
			return val
			pass
		if startswith( f"{prefix}guess " ):
			try:
				content = message.content.replace( f"{prefix}guess ", "" )
				if content == _read( f"""SELECT * FROM scrambles WHERE sid='{message.server.id}'""" )[ 0 ][ 0 ]:
					await client.send_message( message.channel, "You are correct!" )
					_execute( f"""DELETE FROM scrambles WHERE sid='{message.server.id}' AND word='{content}'""" )
					pass
				else:
					tmp = _read( f"""SELECT * FROM scrambles WHERE sid='{message.server.id}'""" )[ 0 ]
					word = list( tmp[ 0 ] )
					guessed = list( content )
					overall = list( )
					length = len( word ) if len( word ) >= len( guessed ) else len( guessed )
					for i in range( 0, length ):
						if word[ i ].lower( ) == guessed[ i ].lower( ): overall.append( word[ i ] )
						else: overall.append( "_" )
						pass
					await client.send_message( message.channel, f"Incorrect!\n{tmp[1]}\n{''.join(overall)}" )
					pass
				pass
			except: await client.send_message( message.channel, "```No scramble exists.```" )
			pass
		elif startswith( f"{prefix}scramble " ):
			content = message.content.replace( f"{prefix}scramble ", "", 1 )
			if startswith( "add", val=content ):
				content = content.replace( "add ", "", 1 )
				try:
					_execute( f"""INSERT INTO wordlist (word) VALUES ('{content}');""" )
					await client.send_message( message.channel, f"```Added \"{content}\".```" )
					pass
				except: await client.send_message( message.channel, f"```That word/phrase already exists in the database!```" )
				pass
			elif startswith( "rem", val=content ):
				content = content.replace( "rem ", "", 1 )
				try:
					_execute( f"""
					DELETE FROM wordlist
					WHERE word='{content}';
					""".replace( "\t", "" ) )
					await client.send_message( message.channel, f"```Removed \"{content}\"```" )
					pass
				except: await client.send_message( message.channel, f"```\"{content}\" is not in the database!```" )
			elif startswith( "find", val=content ):
				content = content.replace( "find ", "", 1 )
				res = _read( f"""SELECT word FROM wordlist WHERE word LIKE '%{content}%'""" )
				ret = "```Results:\n```"
				for item in res: ret += item[ 0 ]
				await client.send_message( message.channel, ret )
				pass
			elif startswith( "list", val=content ):
				res = _read( f"""SELECT * FROM wordlist ORDER BY word DESC;""" )
				res = [ item[ 0 ] for item in res ]
				for msg in format_message( ', '.join( res ) ): await client.send_message( message.channel, msg )
				pass
			pass
		elif startswith( f"{prefix}scramble" ):
			try:
				res = _read( f"""SELECT * FROM wordlist;""" )
				word = random.choice( res )[ 0 ]
				shuffle = ""
				for item in word.split( " " ):
					shuff = list( item )
					random.shuffle( shuff )
					shuffle += " " + "".join( shuff )
					pass
				shuffle = shuffle[ 1: ]
				_execute( f"""
				INSERT INTO scrambles (word, scramble, sid)
				VALUES ('{word}', '{shuffle}', '{message.server.id}');
				""".replace( "\t", "" ) )
				ret = ""
				left = ""
				print( f"{Fore.CYAN}Started word scramble: {word}, {shuffle}{Fore.RESET}" )
				await client.send_message( message.channel, f"```Started a word scramble:\n{shuffle}```" )
				pass
			except: await client.send_message( message.channel, "```A scramble already exists!```" )
			pass
		elif startswith( f"{prefix}giveup" ):
			try:
				await client.send_message( message.channel, "```The word was: \"" + _read( f"SELECT word FROM scrambles WHERE sid='{message.server.id}'" )[ 0 ][ 0 ] + "\"```" )
				_execute( f"""DELETE FROM scrambles WHERE sid='{message.server.id}'""" )
				pass
			except: await client.send_message( message.channel, "```No scramble exists.```" )
			pass
		elif startswith( f"g{prefix}rps " ):
			_choices = [ "rock", "paper", "scissors" ]
			_content = message.content.replace( f"g{prefix}rps ", "" )
			_choice = random.choice( _choices )
			def _check_winner ( c1: str, c2: str ) -> str:
				if c1 == c2:
					return "No one"
					pass
				elif c1 == "rock": return c2 if c2 == "paper" else c1
				elif c1 == "paper": return c2 if c2 == "scissors" else c1
				elif c1 == "scissors": return c2 if c2 == "rock" else c1
				pass
			await client.send_message( message.channel, f"I chose {_choice}, you chose {_content}. {_check_winner(_choice, _content)} won!" )
			del _choices
			del _content
			del _choice
			pass
		elif startswith( f"g{prefix}rpsls " ):
			_choices = [ "rock", "paper", "scissors", "lizard", "Spock" ]
			_content = message.content.replace( f"g{prefix}rpsls ", "" ).replace( "spock", "Spock" )
			_choice = random.choice( _choices )
			_winner = ""
			if _choice == _content: _winner = "No one"
			elif _choice == "rock":
				if _content == "Spock" or _content == "paper": _winner = _content
				elif _content == "scissors" or _content == "lizard": _winner = _choice
				pass
			elif _choice == "paper":
				if _content == "lizard" or _content == "scissors": _winner = _content
				elif _content == "Spock" or _content == "rock": _winner = _choice
				pass
			elif _choice == "scissors":
				if _content == "Spock" or _content == "rock": _winner = _content
				elif _content == "lizard" or _content == "paper": _winner = _choice
				pass
			elif _choice == "lizard":
				if _content == "scissors" or _content == "rock": _winner = _content
				elif _content == "Spock" or _content == "paper": _winner = _choice
				pass
			elif _choice == "Spock":
				if _content == "lizard" or _content == "paper": _winner = _content
				elif _content == "rock" or _content == "scissors": _winner = _choice
				pass

			await client.send_message( message.channel, f"I chose {_choice}, you chose {_content}. {_winner} wins!" )
			pass
		elif startswith( f"g{prefix}rules " ):
			content = message.content.replace( f"g{prefix}rules ", "" )
			if content == "rps":
				ret = """**rock** smashes **scissors**\n**paper** covers **rock**\n**scissors** cut **paper**"""
				await client.send_message( message.channel, ret )
				pass
			elif content == "rpsls":
				ret = """**rock** smashes **scissors** and crushes **lizard**\n**paper** covers **rock** and blinds **Spock**\n**scissors** cut **paper** and decapitate **lizard**\n**lizard** eats **paper** and poisons **Spock**\n**Spock** destroys **rock** and disintegrates **scissors**"""
				await client.send_message( message.channel, ret )
				pass
			elif content == "scramble":
				ret = """The bot will scramble a word.
				You have to find the original word.""".replace( "\t", "" )
				await client.send_message( message.channel, ret )
				pass
			pass
		elif startswith( "$exit", "logbot.games.exit" ):
			if message.author.id == "239500860336373761":
				exiting = True
				await client.logout( )
				pass
			pass
		elif startswith( f"$update", "logbot.games.update" ):
			if message.author.id == "239500860336373761":
				do_update = True
				pass
			pass
		elif startswith( f"{prefix}ping" ):
			tm = datetime.now( ) - message.timestamp
			await client.send_message( message.channel, f"```LogBot Games Online ~ {round(tm.microseconds / 1000)}```" )
			pass
		elif startswith( f"g{prefix}get\n", "```sql\n--games\n--get" ):
			if message.author.id == "239500860336373761":
				try:
					msg = "```Execution Successful. Result:\n" + str( _read( replace( "{uid}", repl=message.author.id, val=replace( "{sid}", repl=message.server.id, val=replace( f"g{prefix}get\n", "```sql", "```", repl="" ) ) ) ) ) + "```"
					for _msg in format_message( msg ): await client.send_message( message.channel, _msg )
					pass
				except: await client.send_message( message.channel, f"```Execution Failed.\n{traceback.format_exc()}```" )
				pass
			pass
		elif startswith( f"g{prefix}execute\n", "```sql\n--games\n--execute" ):
			if message.author.id == "239500860336373761":
				try:
					_execute( replace( f"g{prefix}execute\n", "```sql", "```", repl="" ).replace( "{sid}", message.server.id ).replace( "{uid}", message.author.id ) )
					await client.send_message( message.channel, f"```Execution Successful.```" )
					pass
				except: await client.send_message( message.channel, f"```Execution Failed.\n{traceback.format_exc()}```" )
				pass
			pass
		elif startswith( "g{prefix}challenge" ):
			await client.send_message( message.channel, random.choice( challenges ) )
			pass

		if do_update:
			print( Fore.LIGHTCYAN_EX + "Updating..." + Fore.RESET )
			await client.close( )
			subprocess.Popen( "python " + os.getcwd( ) + "\\games.py", False )
			exit( 0 )
			pass
		pass
	except: log_error( traceback.format_exc( ) )

@client.event
async def on_ready ( ):
	await client.change_presence( )
	# os.system( "cls" )
	print( f"{Fore.MAGENTA}Games Ready!{Fore.RESET}" )
	try: _execute( f"""CREATE TABLE wordlist (word VARCHAR(1000) UNIQUE);""" )
	except: pass
	try: _execute( f"""CREATE INDEX wordlist_index ON wordlist (word);""" )
	except: pass
	try: _execute( f"""CREATE TABLE scrambles (word VARCHAR(1000), scramble VARCHAR(1000), sid VARCHAR(50) UNIQUE);""" )
	except: pass
	try: _execute( f"""CREATE INDEX scrambles_index ON scrambles (word, scramble, sid);""" )
	except: pass
	pass

client.run( token )

if exiting == False:
	subprocess.Popen( f"python {os.getcwd()}\\games.py" )
	exit( 0 )
	pass
