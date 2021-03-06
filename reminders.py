import asyncio
import os
import sqlite3
import subprocess
import traceback
from datetime import datetime

from colorama import Fore, init
from discord import Client, Message

from logbot_data import owner_id, token

CLIENT = Client( )
init( )

SQL = sqlite3.connect( f"{os.getcwd()}\\Discord Logs\\SETTINGS\\logbot.db" )

EXITING = False
REMINDERS = { }

class Timer:
	def __init__ ( self, timeout, callback, args ):
		self._timeout = timeout
		self._callback = callback
		self._task = asyncio.ensure_future( self._job( ) )
		self._args = args
	async def _job ( self ):
		await asyncio.sleep( self._timeout )
		await self._callback( self._args )
	def cancel ( self ):
		self._task.cancel( )

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
	writer.write( f"{datetime.now()} (reminders.py) - {error_text}\n\n{prev_text}" )
	writer.close( )
	if "SystemExit" in error_text:
		exit( 0 )
	del writer
	del file
	del prev_text

def get_prefix ( server: str ):
	cursor = SQL.cursor( )
	cmd = f"""SELECT prefix
	FROM Prefixes
	WHERE server='{server}';"""
	cursor.execute( cmd )
	return cursor.fetchall( )[ 0 ][ 0 ]

def calculate_time ( time: str ):
	"""
	f"%x %X" - MM/DD/YYYY HH:MM:SS
	f"%c" - WeekDayAbbr MonthNameAbbr DD HH:MM:SS YYYY `(current format)`
	:param time: The time, as a string.
	:return: A datetime object or a str object (only on error will str be returned).
	"""
	try:
		dt_tmp = datetime.strptime( time, "%c" )
		return dt_tmp
	except Exception:
		return "Incorrectly formatted time."

def parse_time ( time: str ):
	parts = time.split( " " )
	time = 0
	for part in parts:
		if "d" in part:
			time += 86400 * int( part.replace( "d", "" ) )
		elif "h" in part:
			time += 3600 * int( part.replace( "h", "" ) )
		elif "m" in part:
			time += 60 * int( part.replace( "m", "" ) )
		elif "s" in part:
			time += int( part.replace( "s", "" ) )
	return time

async def do_task ( args ) -> None:
	"""
	Sends a reminder message.
	"""
	await CLIENT.send_message( args[ 1 ], args[ 0 ] )
	tmp = REMINDERS[ args[ 2 ] ]
	for item in tmp:
		if item[ 0 ] == args[ 3 ][ 0 ] and item[ 1 ] == args[ 3 ][ 1 ]:
			REMINDERS[ args[ 2 ] ].remove( item )

@CLIENT.event
async def on_message ( message: Message ):
	global REMINDERS, EXITING
	try:
		def begins ( *args, val=message.content ):
			for arg in args:
				if val.startswith( arg ):
					return True
			return False
		prefix = get_prefix( message.server.id )
		do_update = False

		# <editor-fold desc="Check for server membership">
		if REMINDERS.get( message.author.id ) is None:
			REMINDERS[ message.author.id ] = [ ]
		# </editor-fold>
		# <editor-fold desc="Commands">
		if begins( f"r{prefix}reminder " ):
			# Create, remove, or edit a reminder
			cnt = message.content.split( " " )
			cnt.remove( cnt[ 0 ] )
			switch = cnt[ 0 ]
			cnt.remove( cnt[ 0 ] )
			options = ' '.join( cnt ).split( "||" )
			if switch == "add":
				# Create a new reminder
				server = message.author.id
				if "in " in options[ 0 ]:
					time = parse_time( options[ 0 ].replace( "in ", "" ) )
				else:
					time = calculate_time( options[ 0 ] )
				msg = options[ 1 ]
				try:
					t_tmp = float( (time - datetime.now( )).total_seconds( ) )
				except Exception:
					t_tmp = time
				timer = Timer( t_tmp, CLIENT.async_event( do_task ), [ msg, message.author, message.author.id, (time, msg) ] )
				REMINDERS[ server ].append( (time, msg, timer) )
				await CLIENT.send_message( message.channel, f"Created a new reminder:\n{time}\n{msg}" )
			elif switch == "remove":
				# Remove a reminder
				index = int( options[ 0 ] )
				try:
					REMINDERS[ message.author.id ][ index ][ 2 ].cancel( )
					REMINDERS[ message.author.id ].remove( REMINDERS[ message.server.id ][ index ] )
					await CLIENT.send_message( message.channel, f"Removed the timer." )
				except Exception:
					await CLIENT.send_message( message.channel, f"Could not remove the timer." )
		elif begins( f"r{prefix}reminders" ):
			# Show the reminders
			ret = '\n'.join( [ f"{time} - {msg}" for time, msg, t in REMINDERS[ message.author.id ] ] )
			await CLIENT.send_message( message.channel, ret )
		elif begins( f"logbot.reminders.update", f"$update" ):
			# Update the module
			if message.author.id == owner_id:
				do_update = True
		elif begins( f"logbot.reminders.exit", f"$exit" ):
			# Exit the module
			if message.author.id == owner_id:
				EXITING = True
				await CLIENT.logout( )
		# </editor-fold>
		if do_update:
			print( f"{Fore.LIGHTCYAN_EX}Updating...{Fore.RESET}" )
			await CLIENT.close( )
			subprocess.Popen( f"python {os.getcwd()}\\reminders.py", False )
			exit( 0 )
	except Exception:
		log_error( traceback.format_exc( ) )

@CLIENT.event
async def on_ready ( ):
	print( f"{Fore.MAGENTA}Ready!!!{Fore.RESET}" )

CLIENT.run( token )

if not EXITING:
	subprocess.Popen( f"python {os.getcwd()}\\reminders.py" )
	exit( 0 )
