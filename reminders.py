import sqlite3
import subprocess
from datetime import datetime
from threading import Timer

from colorama import Fore, init
from discord import Client, Message

from logbot_data import *

CLIENT = Client( )
init( )

SQL = sqlite3.connect( f"{os.getcwd()}\\Discord Logs\\SETTINGS\logbot.db" )
CURSOR = SQL.cursor( )

EXITING = False
REMINDERS = { }

def get_prefix ( server: str ):
	cmd = f"""SELECT prefix
	FROM Prefixes
	WHERE server='{server}';"""
	CURSOR.execute( cmd )
	return CURSOR.fetchall( )[ 0 ][ 0 ]

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

def do_task ( arg: str, channel ) -> None:
	"""
	Sends a reminder message.
	:param arg: The message.
	:param channel: The channel.
	"""
	yield from CLIENT.send_message( channel, arg )

@CLIENT.event
async def on_message ( message: Message ):
	global REMINDERS, EXITING
	def begins ( *args, val=message.content ):
		for arg in args:
			if val.startswith( arg ):
				return True
		return False
	prefix = get_prefix( message.server.id )
	do_update = False

	# <editor-fold desc="Check for server membership">
	if REMINDERS.get( message.server.id ) is None:
		REMINDERS[ message.server.id ] = [ ]
	# </editor-fold>
	# <editor-fold desc="Commands">
	if begins( f"r{prefix}reminder " ):
		# Create, remove, or edit a reminder
		cnt = message.content.split( " " )
		cnt.remove( cnt[ 0 ] )
		switch = cnt[ 0 ]
		cnt.remove( cnt[ 0 ] )
		options = ' '.join( cnt ).split( "||" )
		if switch is "add":
			# Create a new reminder
			server = message.server.id
			time = calculate_time( options[ 0 ] )
			msg = options[ 1 ]
			t_tmp = float( (time - datetime.now( )).total_seconds( ) )
			t = Timer( t_tmp, do_task, [ msg, message.author ] )
			t.start( )
			REMINDERS[ server ].append( (time, msg, t) )
			await CLIENT.send_message( message.channel, f"Created a new reminder:\n{time}\n{msg}" )
		elif switch is "remove":
			# Remove a reminder
			index = int( options[ 0 ] )
			try:
				REMINDERS[ message.server.id ][ index ][ 2 ].cancel( )
				REMINDERS[ message.server.id ].remove( REMINDERS[ message.server.id ][ index ] )
				await CLIENT.send_message( message.channel, f"Removed the timer." )
			except Exception:
				await CLIENT.send_message( message.channel, f"Could not remove the timer." )
	elif begins( f"r{prefix}reminders" ):
		# Show the reminders
		ret = ""
		for time, msg, t in REMINDERS:
			ret += f"{time} - {msg}"
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

@CLIENT.event
async def on_ready ( ):
	print( f"{Fore.MAGENTA}Ready!!!{Fore.RESET}" )

CLIENT.run( token )

if not EXITING:
	subprocess.Popen( f"python {os.getcwd()}\\reminders.py" )
	exit( 0 )
