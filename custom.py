"""
Custom Commands module.
"""
import ast
import os
import sqlite3
import subprocess
import traceback
from datetime import datetime

from colorama import Fore, init
from discord import Client, Message

from logbot_data import token, owner_id

CLIENT = Client( )
init( )
EXITING = False

COMMANDS = { }
SETTINGS_PATH = f"{os.getcwd()}\\Discord Logs\\SETTINGS"
COMMANDS_PATH = f"{SETTINGS_PATH}\\custom_commands.txt"

SQL = sqlite3.connect( f"{SETTINGS_PATH}\\logbot.db" )
CURSOR = SQL.cursor( )

try:
	READER = open(
		COMMANDS_PATH,
		'r'
	)
	COMMANDS = ast.literal_eval( READER.read( ) )
	READER.close( )
	del READER
except Exception:
	WRITER = open(
		COMMANDS_PATH,
		'w'
	)
	WRITER.write( "" )
	WRITER.close( )
	del WRITER

# noinspection PyShadowingNames
def log_error ( error_text: str ):
	"""
	Log the bot's errors.
	:param error_text: The error message.
	"""
	file = f"{os.getcwd()}\\error_log.txt"
	prev_text = ""
	try:
		reader_obj = open(
			file,
			'r'
		)
		prev_text = reader_obj.read( )
		reader_obj.close( )
		del reader_obj
	except Exception:
		pass
	writer_obj = open(
		file,
		'w'
	)
	writer_obj.write( f"{datetime.now()} (custom.py) - {error_text}\n\n{prev_text}" )
	writer_obj.close( )
	if "SystemExit" in error_text:
		exit( 0 )
	del writer_obj
	del file
	del prev_text

def sqlread ( cmd: str ):
	"""
	Read from the DB.
	:param cmd: The SQL Read command.
	:return: The data retrieved.
	"""
	CURSOR.execute( cmd )
	return CURSOR.fetchall( )

@CLIENT.event
async def on_ready ( ):
	"""
	Occurs when the bot logs in.
	"""
	# os.system( "cls" )
	print( f"{Fore.MAGENTA}Custom Ready!!!{Fore.RESET}" )

@CLIENT.event
async def on_message ( message: Message ):
	"""
	Occurs when the bot receives a message.
	:param message: A discord.Message object.
	"""
	global EXITING
	try:
		prefix = sqlread(
			f"SELECT prefix FROM Prefixes WHERE server='{message.server.id}';"
		)[ 0 ][ 0 ]
		begins = message.content.startswith
		if not message.server.id in COMMANDS.keys( ):
			COMMANDS[ message.server.id ] = dict( )

		if begins( f"c{prefix}add " ):
			cmd = message.content.replace(
				f'c{prefix}add ',
				''
			).split( '||' )
			if not cmd[ 0 ] == "":
				COMMANDS[ message.server.id ][ cmd[ 0 ] ] = cmd[ 1 ]
				await CLIENT.send_message(
					message.channel,
					f"```Created the command.```"
				)
				print( f"{Fore.LIGHTMAGENTA_EX}Command {cmd[0]}:{cmd[1]} was created.{Fore.RESET}" )
			else:
				await CLIENT.send_message(
					message.channel,
					f"```A command cannot be triggered like that!```"
				)
			del cmd
		elif begins( f"c{prefix}remove " ):
			cmd = message.content.replace(
				f"c{prefix}remove ",
				""
			)
			data = {
				cmd:COMMANDS[
					message.server.id
				][
					cmd
				]
			}
			del COMMANDS[ message.server.id ][ cmd ]
			await CLIENT.send_message(
				message.channel,
				"```Deleted the command.```"
			)
			print( f"{Fore.LIGHTMAGENTA_EX}Command {cmd}:{data[cmd]} was deleted.{Fore.RESET}" )
			del data
			del cmd
		elif begins( f"c{prefix}show" ):
			tmp = '\n'.join(
				list(
					COMMANDS[
						message.server.id
					].keys( )
				)
			)
			await CLIENT.send_message(
				message.channel,
				f"```Commands:\n{tmp}```"
			)
			del tmp
		elif begins( f"logbot.custom.exit" ):
			if message.author.id == owner_id:
				EXITING = True
				await CLIENT.logout( )

		for key, value in COMMANDS[ message.server.id ].items( ):
			if begins( key ):
				await CLIENT.send_message(
					message.channel,
					value
				)
		del prefix
		del begins
	except Exception:
		log_error( traceback.format_exc( ) )

CLIENT.run( token )

if not EXITING:
	subprocess.Popen( f"python {os.getcwd()}\\custom.py" )
	exit( 0 )
