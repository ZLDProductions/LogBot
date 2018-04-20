"""
The main bot. This module contains most of the features.
"""
import ast
import codecs
import configparser
import decimal
import os
import random
import re
import subprocess
import traceback
from asyncio import sleep
from datetime import datetime, timezone
from sys import argv
from typing import List, Union

import discord
import giphy_client
import lyricwikia
import psutil
import translate
import urbandictionary
import wikipedia
import wolframalpha
from PyDictionary import PyDictionary
from PyQt5 import Qt
from colorama import Fore, init

import argparser
import sql
import tools
from logbot_data import bot_id, giphy_key, git_link, hq_link, owner_id, token, wa_token

# <editor-fold desc="Base Variables">
VERSION = '16.10.0 Python'
WHATS_NEW = [
	"• Added a magic 8 ball.",
	"• Added NIV Bible.",
	"• Code structure changes (should be more readable now).",
	"• Updated copypasta character list."
] # list of recent changes to the code.
PLANNED = [
	"There is nothing planned at the moment."
] # list of what I plan to do.
BOOTUP_TIME = datetime.now( ) # the time the bot started.
EXITING = False # determines if the bot is closing. If False, the bot automatically restarts.
EIGHTBALL_POS = [
	"It is certain",
	"Without a doubt",
	"Most likely",
	"Yes",
	"Signs point to yes"
]
EIGHTBALL_NEU = [
	"Reply hazy try again",
	"Ask again later",
	"Better not tell you now",
	"Cannot predict now",
	"Concentrate and ask again"
]
EIGHTBALL_NEG = [
	"Don't count on it",
	"My reply is no",
	"My sources say no",
	"Outlook not so good",
	"Very doubtful"
]
# </editor-fold>

# <editor-fold desc="Clients and Classes">
CLIENT = discord.Client( ) # Discord client
init( ) # Colorama client (color the console!)
WCLIENT = wolframalpha.Client( app_id=wa_token ) # Wolfram|Alpha client
PARSER = configparser.ConfigParser( ) # ConfigParser init
CHANNELPARSER = configparser.ConfigParser( ) # ConfigParser init
PYDICT = PyDictionary( ) # PyDictionary client
PURGEPARSER = argparser.ArgParser( "&&", "=" ) # ArgParser (my own class) init
GC = giphy_client.DefaultApi( ) # Giphy client
# </editor-fold>

# <editor-fold desc="Tray Icon">
SELECTED_IMAGE = f"{os.getcwd()}\\Discord Logs\\SETTINGS\\avatar5.jpg" # Bot image
APP = Qt.QApplication( argv )
STI = Qt.QSystemTrayIcon( Qt.QIcon( SELECTED_IMAGE ), APP )
ICON = Qt.QIcon( SELECTED_IMAGE )
STI.setIcon( ICON )
STI.show( )
STI.setToolTip( "LogBot" )
# </editor-fold>

# <editor-fold desc="Databases">
DB = sql.SQL( )
DB.create( "Welcomes", "server", "message" )
DB.create( "Goodbyes", "server", "message" )
DB.create( "Prefixes", "server", "prefix" )
# </editor-fold>

# <editor-fold desc="Instance Variables">
EXCLUDE_CHANNEL_LIST = [ ]
MARKLIST = [ ]
CHANNELS = [ ]
USER_NAME = ""
DISABLES = { }
CUSTOM_COMMANDS = { }
TIMES = [ ]
JOIN_ROLES = { }
LOG_CHANNEL = { }
DEFAULT_CHANNEL = { }
DICT_WORDS = [ ]
PLAYLISTS = { }
FILTER_SETTINGS = { }
# </editor-fold>

# <editor-fold desc="Paths">
DISCORD_LOGS_PATH = f"{os.getcwd()}\\Discord Logs"
DISCORD_SETTINGS_PATH = f"{DISCORD_LOGS_PATH}\\SETTINGS"
SERVER_SETTINGS_PATH = f"{DISCORD_SETTINGS_PATH}\\SERVER SETTINGS"
CHANNEL_WHITELIST_PATH = f"{DISCORD_SETTINGS_PATH}\\channel_whitelist.txt"
MARK_LIST_PATH = f"{DISCORD_SETTINGS_PATH}\\mark_list.txt"
CHANNEL_LIST_PATH = f"{DISCORD_SETTINGS_PATH}\\channels.txt"
NAME_PATH = f"{DISCORD_SETTINGS_PATH}\\name.txt"
CUSTOM_COMMANDS_PATH = f"{DISCORD_SETTINGS_PATH}\\commands.txt"
SUGGESTIONS_PATH = f"{DISCORD_SETTINGS_PATH}\\suggestions.txt"
CHANNEL_SETTINGS_PATH = f"{DISCORD_SETTINGS_PATH}\\channel_settings.ini"
JOIN_ROLES_PATH = f"{DISCORD_SETTINGS_PATH}\\join_roles.txt"
DEFAULT_CHANNELS_PATH = f"{DISCORD_SETTINGS_PATH}\\default_channels.txt"
DICTIONARY_PATH = f"{DISCORD_SETTINGS_PATH}\\censored_words.txt"
DISABLES_PATH = f"{DISCORD_SETTINGS_PATH}\\disables.txt"
PLAYLISTS_PATH = f"{DISCORD_SETTINGS_PATH}\\playlists.txt"
FILTER_SETTINGS_PATH = f"{DISCORD_SETTINGS_PATH}\\filter_settings.txt"
# </editor-fold>

if not os.path.exists( DISCORD_SETTINGS_PATH ):
	os.makedirs( DISCORD_SETTINGS_PATH )

# <editor-fold desc="data loading">
PARSER.read( f'{DISCORD_SETTINGS_PATH}\\data.ini' )

# Load the join roles.
try:
	READER = open( JOIN_ROLES_PATH, 'r' )
	JOIN_ROLES = ast.literal_eval( READER.read( ) )
	READER.close( )
	del READER
except Exception:
	pass

# Load the default channels.
try:
	READER = open( DEFAULT_CHANNELS_PATH, 'r' )
	DEFAULT_CHANNEL = ast.literal_eval( READER.read( ) )
	READER.close( )
	del READER
except Exception:
	pass

# Load the banned words.
try:
	READER = open( DICTIONARY_PATH, 'r' )
	DICT_WORDS = READER.read( ).split( "\n" )
	READER.close( )
	del READER
except Exception:
	pass

# Load the disabled features.
try:
	READER = open( DISABLES_PATH, 'r' )
	DISABLES = ast.literal_eval( READER.read( ) )
	READER.close( )
	del READER
except Exception:
	pass

# Load the playlists.
try:
	READER = open( PLAYLISTS_PATH, 'r' )
	PLAYLISTS = ast.literal_eval( READER.read( ) )
	READER.close( )
	del READER
except Exception:
	pass

# Load the Filter Settings
try:
	READER = open( FILTER_SETTINGS_PATH, 'r' )
	FILTER_SETTINGS = ast.literal_eval( READER.read( ) )
	READER.close( )
	del READER
	if FILTER_SETTINGS is None:
		FILTER_SETTINGS = { }
except Exception:
	pass

if "SETTINGS" not in PARSER.sections( ):
	PARSER[ "SETTINGS" ] = {
		"name"      :input( f"{Fore.CYAN}What is your name on Discord? {Fore.RESET}" ),
		"customcmds":str( CUSTOM_COMMANDS )
	}

if "SETTINGS" in PARSER.sections( ):
	if "name" in PARSER[ "SETTINGS" ]:
		USER_NAME = PARSER[ "SETTINGS" ][ "name" ]
	else:
		# noinspection PyUnresolvedReferences,PyUnresolvedReferences
		USER_NAME = input( f"{Fore.CYAN}What is your nickname on Discord? {Fore.RESET}" )
		PARSER[ "SETTINGS" ][ "name" ] = USER_NAME
	try:
		CUSTOM_COMMANDS = ast.literal_eval( PARSER[ "SETTINGS" ][ "customcmds" ] )
		EXCLUDE_CHANNEL_LIST = ast.literal_eval( PARSER[ "SETTINGS" ][ "channel_whitelist" ] )
		MARKLIST = ast.literal_eval( PARSER[ "SETTINGS" ][ "mark_list" ] )
		CHANNELS = ast.literal_eval( PARSER[ "SETTINGS" ][ "channel_list" ] )
	except Exception:
		pass

# </editor-fold>

# noinspection PyShadowingNames
def send ( message: str, servername: str, channel: str = "event" ):
	"""
	Sends an event to a file-stream to be written to a file.
	:param message: The string message to send to the writer.
	:param servername: The server to write to. This is a folder.
	:param channel: The channel to write to. This is the actually log file. Defaults to "event".
	"""
	# noinspection PyUnresolvedReferences,PyUnresolvedReferences
	if not os.path.exists( f"{DISCORD_LOGS_PATH}\\{servername}" ):
		os.makedirs( f"{DISCORD_LOGS_PATH}\\{servername}" )
	try:
		# logs if the channel is marked.
		MARKLIST.index( channel )
		writer = open( f"{DISCORD_LOGS_PATH}\\{servername}\\{channel}.mark.txt", 'a' )
		writer.write( f"{codecs.unicode_escape_encode(message, 'ignore')[0]}\n" )
		writer.close( )
		del writer
	except Exception:
		# logs if the channel is not marked.
		writer = open( f"{DISCORD_LOGS_PATH}\\{servername}\\{channel}.txt", 'a' )
		writer.write( f"{message if is_ascii(message) else codecs.unicode_escape_encode(message, 'ignore')[0]}\n" )
		writer.close( )
		del writer
	try:
		# converts the message to unicode, then prints to the pyconsole.
		message = u"{}".format( message )
		print( message )
		del message
	except Exception:
		print( f"{servername} ~ {Fore.LIGHTRED_EX}There was an error with the encoding of the message.{Fore.RESET}" )

def is_ascii ( string: str ) -> bool:
	"""
	Determines if a string, `s`, is non-unicode.
	:param string: The string to analyze.
	:return: True if `s` is not unicode, otherwise False.
	"""
	return all( ord( c ) < 128 for c in string ) # Returns true if the string has no unicode characters.

# Changes the time from UTC to PST (-8 hrs)
def format_time ( time_stamp: datetime ) -> datetime:
	"""
	Converts the time from UTC +0 to PST -8.
	:param time_stamp: A UTC timestamp.
	:return: A PST timestamp.
	"""
	return time_stamp.replace( tzinfo=timezone.utc ).astimezone( tz=None ) # Converts the datetime from UTC to the machine's local time.

def save ( sid: str ):
	"""
	Saves all of the data in the bot to several files.
	:param sid: The server id to save the data to.
	"""
	PARSER[ "SETTINGS" ] = {
		"name"             :USER_NAME,
		"customcmds"       :str( CUSTOM_COMMANDS ),
		"channel_whitelist":str( EXCLUDE_CHANNEL_LIST ),
		"mark_list"        :str( MARKLIST ),
		"channel_list"     :str( CHANNELS )
	}

	if not os.path.exists( f"{SERVER_SETTINGS_PATH}\\{sid}" ):
		os.makedirs( f"{SERVER_SETTINGS_PATH}\\{sid}" )

	# <editor-fold desc="Disables">
	# writer = open( f"{server_settings}\\{sid}\\disables.txt", 'w' )
	# writer.write( str( disables ) )
	# writer.close( )
	writer = open( f"{DISCORD_SETTINGS_PATH}\\disables.txt", 'w' )
	writer.write( str( DISABLES ) )
	writer.close( )
	del writer
	# </editor-fold>
	# <editor-fold desc="Join Roles">
	writer = open( JOIN_ROLES_PATH, 'w' )
	writer.write( str( JOIN_ROLES ) )
	writer.close( )
	del writer
	# </editor-fold>
	# <editor-fold desc="Default Channel">
	writer = open( DEFAULT_CHANNELS_PATH, 'w' )
	writer.write( str( DEFAULT_CHANNEL ) )
	writer.close( )
	del writer
	# </editor-fold>
	# <editor-fold desc="Filter Settings">
	writer = open( FILTER_SETTINGS_PATH, "w" )
	writer.write( str( FILTER_SETTINGS ) )
	writer.close( )
	# </editor-fold>

	# <editor-fold desc="ini file">
	with open( f"{DISCORD_SETTINGS_PATH}\\data.ini", 'w' ) as configfile:
		PARSER.write( configfile )
	# </editor-fold>

def check ( *args ) -> str:
	"""
	Checks strings for non-ASCII characters.
	:param args: A list of strings.
	:return: The first string in args that passes inspection.
	"""
	for item in args:
		if item is not None and is_ascii( item ):
			return item

def format_message ( cont: str ) -> list:
	"""
	Splits `cont` into several strings, each a maximum of 2000 characters in length. Adds ``` at each end automatically.
	:param cont: The string to format.
	:return: A list of strings. Each formatted into 2000 characters, including ``` at each end.
	"""
	if len( cont ) > 1994:
		return [
			f"```{item}```"
			for item in [
				cont[ i:i + 1000 ]
				for i in range( 0, len( cont ), 1000 )
			]
		]
	return [ f"```{cont}```" ]

def update ( mid: str, cid: str ):
	"""
	Updates the bot.
	:param mid: The message id of the update message.
	:param cid: The channel of the message. Necessary for client.get_message() to work.
	"""
	subprocess.Popen( f"python {os.getcwd()}\\logbot.py -m {mid} -c {cid} -t {BOOTUP_TIME.month}.{BOOTUP_TIME.day}.{BOOTUP_TIME.year}.{BOOTUP_TIME.hour}.{BOOTUP_TIME.minute}.{BOOTUP_TIME.second}.{BOOTUP_TIME.microsecond}", False )
	exit( 1 )

def send_notification ( _nick: str, _name: str, _id: str, _server: str, _content: str, _who: discord.User ):
	"""
	Sends a windows notification.
	:param _nick: The nickname of the author.
	:param _name: The name of the author.
	:param _id: The id of the author.
	:param _server: The server the message was send in.
	:param _content: The content of the message.
	:param _who: The author of the message.
	"""
	_n = check( _nick, _name, _id )
	_header = f"{_n} ({_server}) mentioned {_who}!"
	STI.showMessage( _header, _content )
	del _n
	del _header

def notify ( header: str, body: str ):
	"""
	Sends a windows notification.
	:param header: The header for the notification.
	:param body: The body for the notification.
	"""
	STI.showMessage( header, body )

def sort ( ):
	"""
	Sorts all of the lists in the bot. This is an organizational tactic that allows for faster iterations of said lists.
	"""
	TIMES.sort( )

def _filter ( text: str ) -> str:
	"""
	Filters censored words out of text. Used mainly with the UrbanDictionary
	:param text: The uncensored text.
	:return: The censored text.
	"""
	return tools.filter_text( text )

async def check_purge ( message: discord.Message, limit=100, _check=None ) -> int:
	"""
	Checks the messages that might be purge, and returns the quantity that will be purged.
	:param message: The discord message that triggered the $purge command.
	:param limit: The number of messages to check.
	:param _check: The function to use to check each message. If none is provided, will return True for all instances.
	:return: The number of messages to be purged.
	"""
	# noinspection PyUnusedLocal
	def _dummycheck ( msg ) -> bool:
		"""
		Dummychecker.
		:param msg: The message.
		:return: True or False.
		"""
		if msg is not None:
			return True
		return False
	if _check is None:
		_check = _dummycheck
	count = 0
	logs = CLIENT.logs_from( message.channel, limit=limit ).iterate
	while True:
		try:
			item = await logs( )
			if _check( item ) is True:
				count += 1
			del item
		except Exception:
			break
	del logs
	return count

def get_diff ( then: datetime, now: datetime ) -> str:
	"""
	Gets the difference between two dates.
	:param then: Then.
	:param now: Now.
	:return: The difference.
	"""
	years = now.year - then.year
	months = now.month - then.month
	days = now.day - then.day
	weeks = 0
	hours = now.hour - then.hour
	minutes = now.minute - then.minute
	seconds = now.second - then.second
	# <editor-fold desc="Correcting the times">
	while seconds < 0:
		minutes -= 1
		seconds += 60
	while minutes < 0:
		hours -= 1
		minutes += 60
	while hours < 0:
		days -= 1
		hours += 24
	while days < 0:
		months -= 1
		days += 30
	while months < 0:
		years -= 1
		months += 12
	while seconds >= 60:
		minutes += 1
		seconds -= 60
	while minutes >= 60:
		hours += 1
		minutes -= 60
	while hours >= 24:
		days += 1
		hours -= 24
	while days >= 30:
		months += 1
		days -= 30
	while months >= 12:
		years += 1
		months -= 12
	while days >= 7:
		weeks += 1
		days -= 7
	# </editor-fold>

	_str = f"{years} {'years' if not years == 1 else 'year'}, {months} {'months' if not months == 1 else 'month'}, {weeks} {'weeks' if not weeks == 1 else 'week'}, {days} {'days' if not days == 1 else 'day'}, {hours} {'hours' if not hours == 1 else 'hour'}, {minutes} {'minutes' if not minutes == 1 else 'minute'}, {seconds} {'seconds' if not seconds == 1 else 'second'}"
	_str = _str.replace( "0 years,", "" ).replace( " 0 months,", "" ).replace( " 0 weeks,", "" ).replace( " 0 days,", "" ).replace( " 0 hours,", "" ).replace( " 0 minutes,", "" ).replace( " 0 seconds", "" )
	del years
	del months
	del days
	del weeks
	del hours
	del minutes
	del seconds
	return _str

# noinspection PyShadowingNames
def log_error ( error_text: str ):
	"""
	Logs the bot's errors.
	:param error_text: The error message.
	"""
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
	writer.write( f"{datetime.now()} (logbot.py) - {error_text}\n\n{prev_text}" )
	writer.close( )
	if "SystemExit" in error_text:
		exit( 1 )
	del prev_text
	del file
	del writer

class Commands:
	"""
	Command methods!
	"""
	class Member:
		"""
		For everyone!
		"""
		@staticmethod
		async def lyrics ( message: discord.Message, prefix: str ):
			cnt = message.content.replace( f"{prefix}lyrics ", "" ).split( "|" )
			print( cnt )
			song = cnt[ 0 ]
			artist = cnt[ 1 ]
			try:
				lyrics = str( lyricwikia.get_lyrics( artist, song ) ).split( '\n\n' )
				embed_obj = discord.Embed(title=song, description=f"By {artist}")
				for item in lyrics:
					embed_obj.add_field(name=".", value=item, inline=False)
				await CLIENT.send_message(message.channel, "", embed=embed_obj)
				# for msg in lyrics:
				# 	await CLIENT.send_message(message.channel, msg)
			except lyricwikia.LyricsNotFound:
				await CLIENT.send_message( message.channel, 'No lyrics found for this song.' )
			except Exception:
				await CLIENT.send_message( message.channel, 'An error occurred!' )
				log_error( traceback.format_exc( ) )
		@staticmethod
		async def tos ( message: discord.Message ):
			msg = [
				"This bot follows Discord' Terms of Service.",
				"Because of this, I am require to state, exactly, what information the bot stores.",
				"The bot stores only information necessary to continue running the bot. It stores logs of every channel in a server, but they are not able to be viewed by anyone except me, as the developer, and the admins of the server they belong to. I will not-and have not-viewed any logs of a server I am not moderating or that I do not own.",
				"Logs include status changes (when a member goes online/offline), server changes, channel changes, message actions, and other publicly available data (data which can be received from the Discord app), as well as leveling data (rank, tier, etc.) which is used by the Levels module.",
				"In addition, by using this bot, you agree that you will not abuse commands, such as spamming them or giving wild parameters to test it's durability, in any way, and that storing this information it perfectly acceptable by you."
			]
			embed_obj = discord.Embed( title="LogBot's Terms of Service." )
			for message in msg:
				embed_obj.add_field( name="", value=message )
			await CLIENT.send_message( message.channel, "", embed=embed_obj )
			pass
		@staticmethod
		async def eightball ( message: discord.Message ):
			"""
			Asks the magic 8ball a question.
			:param message: A discord.Message object.
			"""
			if "not" in message.content.lower( ):
				if "kill" in message.content.lower( ) or "bomb" in message.content.lower( ) or "suicide" in message.content.lower( ) or "murder" in message.content.lower( ):
					await CLIENT.send_message( message.channel, f"```{random.choice(EIGHTBALL_POS)}```" )
				else:
					choice = random.choice( [ "+", "-", "0" ] )
					if choice == "+":
						await CLIENT.send_message( message.channel, f"```{random.choice(EIGHTBALL_POS)}```" )
					elif choice == "-":
						await CLIENT.send_message( message.channel, f"```{random.choice(EIGHTBALL_NEG)}```" )
					else:
						await CLIENT.send_message( message.channel, f"```{random.choice(EIGHTBALL_NEU)}```" )
					del choice
			else:
				if "kill" in message.content or "bomb" in message.content or "suicide" in message.content or "murder" in message.content:
					await CLIENT.send_message( message.channel, f"```{random.choice(EIGHTBALL_NEG)}```" )
				else:
					choice = random.choice( [ "+", "-", "0" ] )
					if choice == "+":
						await CLIENT.send_message( message.channel, f"```{random.choice(EIGHTBALL_POS)}```" )
					elif choice == "-":
						await CLIENT.send_message( message.channel, f"```{random.choice(EIGHTBALL_NEG)}```" )
					else:
						await CLIENT.send_message( message.channel, f"```{random.choice(EIGHTBALL_NEU)}```" )
					del choice
		@staticmethod
		async def significant_figures ( message: discord.Message, prefix: str ):
			"""
			Counts significant figures.
			:param message: A discord.Message object.
			:param prefix: The server's prefix.
			"""
			num = message.content.replace( f"{prefix}sf ", "" )
			org_num = num
			# noinspection PyUnusedLocal
			sfs = 0
			dot_found = False
			while num[ 0 ] == "0" or num[ 0 ] == ".":
				if num[ 0 ] == ".":
					dot_found = True
				num = num[ 1: ]
			if "." in num:
				sfs = len( num ) - 1
			elif dot_found:
				sfs = len( num )
			else:
				while num[ -1 ] == "0":
					num = num[ 0:len( num ) - 1 ]
				sfs = len( num )
			await CLIENT.send_message( message.channel, f"```{org_num} has {sfs} significant figures ({num})!```" )
			del num
			del org_num
			del sfs
			del dot_found
		@staticmethod
		async def gif ( message: discord.Message, prefix: str ):
			"""
			Fetches a GIF image.
			:param message: A discord.Message object.
			:param prefix: The server's prefix.
			"""
			tag = message.content.replace( f"{prefix}gif", "" )
			image = GC.gifs_random_get( giphy_key, tag=tag ).data
			embed_obj = discord.Embed( ).set_image( url=image.image_url )
			await CLIENT.send_message( message.channel, "", embed=embed_obj )
			del embed_obj
			del image
			del tag
		@staticmethod
		async def user_restrict ( message: discord.Message, prefix: str ):
			"""
			Fetches a certain field of user information.
			:param message: A discord.Message object.
			:param prefix: The server's prefix.
			"""
			cnt = message.content.replace( f"{prefix}user:", "" )
			params = cnt.split( " " )
			field = params[ 0 ]
			params.remove( field )
			params = ' '.join( params )
			_user = discord.utils.find( lambda u:u.id == params or u.name == params or str( u ) == params or u.mention == params, message.server.members )
			if _user is None and message.mentions:
				_user = message.mentions[ 0 ]
			elif _user is None and not message.mentions:
				_user = message.author

			if field == "nick":
				await CLIENT.send_message( message.channel, str( _user.nick ) )
			elif field == "name":
				await CLIENT.send_message( message.channel, str( _user ) )
			elif field == "id":
				await CLIENT.send_message( message.channel, str( _user.id ) )
			elif field == "type":
				await CLIENT.send_message( message.channel, "Bot" if _user.bot is True else "User" )
			elif field == "date":
				user_created_at = format_time( _user.created_at )
				await CLIENT.send_message( message.channel, f"{get_diff(user_created_at, datetime.now())} ago ({user_created_at.month}.{user_created_at.day}.{user_created_at.year} {user_created_at.hour}:{user_created_at.minute})" )
			elif field == "status":
				await CLIENT.send_message( message.channel, str( _user.status ) )
			elif field == "avatar":
				await CLIENT.send_message( message.channel, _user.avatar_url )
			elif field == "default":
				await CLIENT.send_message( message.channel, _user.default_avatar_url )
			del cnt
			del params
			del field
			del _user
		@staticmethod
		async def user ( message: discord.Message, prefix: str ):
			"""
			Fetches information on a user.
			:param message: A discord.Message object.
			:param prefix: The server's prefix.
			"""
			cnt = message.content.replace( f"{prefix}user ", "" )
			_user = discord.utils.find( lambda u:u.id == cnt or u.name == cnt or str( u ) == cnt or u.mention == cnt, message.server.members )
			if _user is None and message.mentions:
				_user = message.mentions[ 0 ]
			user_created_at = format_time( _user.created_at )
			embed_obj = discord.Embed( title=_user.name, description=f"Information for {_user.name}", color=discord.Colour.gold( ) ) \
				.add_field( name="Nickname", value=str( _user.nick ) ) \
				.add_field( name="Name", value=str( _user ) ) \
				.add_field( name="ID", value=_user.id ) \
				.add_field( name="Type", value="Bot" if _user.bot is True else "User" ) \
				.add_field( name="Date Created", value=f"{get_diff(user_created_at, datetime.now())} ago ({user_created_at.month}.{user_created_at.day}.{user_created_at.year} {user_created_at.hour}:{user_created_at.minute})" ) \
				.add_field( name="Status", value=str( _user.status ) ) \
				.set_image( url=_user.avatar_url ) \
				.set_thumbnail( url=_user.default_avatar_url )
			await CLIENT.send_message( message.channel, "Here you go!", embed=embed_obj )
			del embed_obj
			del cnt
			del _user
			del user_created_at
		@staticmethod
		async def urban ( message: discord.Message, prefix: str ):
			"""
			Gets a definition from the UrbanDictionary.
			:param message: A discord.Message object.
			:param prefix: The server's prefix.
			"""
			_def = urbandictionary.define( message.content.replace( f"{prefix}urban ", "" ) )[ 0 ]
			_text = f"""```
			{_def.word}

			Definition:
			{_def.definition}

			Example:
			{_def.example}

			------

			{_def.upvotes} Upvotes
			{_def.downvotes} Downvotes
			```
			""".replace( "\t", "" )
			__definition = _filter( _def.definition )
			__example = _filter( _def.example )
			if not __example:
				__example = "No available examples..."
			embed_obj = discord.Embed( title=_def.word, description=f"Definition(s) of {_def.word}", colour=discord.Colour.blue( ) ) \
				.add_field( name="Definition", value=__definition, inline=False ) \
				.add_field( name="Example", value=__example, inline=False ) \
				.add_field( name="Upvotes", value=_def.upvotes ) \
				.add_field( name="Downvotes", value=_def.downvotes )
			try:
				await CLIENT.send_message( message.channel, "Here you go!", embed=embed_obj )
			except Exception:
				await CLIENT.send_message( message.channel, _text )
		@staticmethod
		async def role ( message: discord.Message, prefix: str ):
			"""
			Shows data on a role.
			:param message: A discord.Message object.
			:param prefix: The server's prefix.
			"""
			_cnt_ = message.content.replace( f"{prefix}role ", "" )
			if message.role_mentions:
				_role = message.role_mentions[ 0 ]
			else:
				_role = discord.utils.find( lambda r:r.name == _cnt_ or r.id == _cnt_, message.server.roles )
			_members_in_role = [
				str( m )
				for m in message.server.members
				if _role in m.roles
			]
			_position = _role.position
			permissions = _role.permissions
			_id = _role.id
			_name = str( _role )
			_created_at = _role.created_at
			_colour = _role.colour
			_mentionable = _role.mentionable
			embed_obj = discord.Embed( title="Role Information", description=_name, colour=_colour ) \
				.add_field( name="Members", value=', '.join( _members_in_role ), inline=False ) \
				.add_field( name="Position", value=str( _position ), inline=False ) \
				.add_field( name="ID", value=_id, inline=False ) \
				.add_field( name="Mentionable", value=str( _mentionable ), inline=False ) \
				.add_field( name="Create Instant Invite", value=str( permissions.create_instant_invite ), inline=True ) \
				.add_field( name="Kick Members", value=str( permissions.kick_members ), inline=True ) \
				.add_field( name="Ban Members", value=str( permissions.ban_members ), inline=True ) \
				.add_field( name="Administrator", value=str( permissions.administrator ), inline=True ) \
				.add_field( name="Manage Channels", value=str( permissions.manage_channels ), inline=True ) \
				.add_field( name="Manage Server", value=str( permissions.manage_server ), inline=True ) \
				.add_field( name="Read Messages", value=str( permissions.read_messages ), inline=True ) \
				.add_field( name="Send Messages", value=str( permissions.send_messages ), inline=True ) \
				.add_field( name="Send TTS Messages", value=str( permissions.send_tts_messages ), inline=True ) \
				.add_field( name="Manage Messages", value=str( permissions.manage_messages ), inline=True ) \
				.add_field( name="Embed Links", value=str( permissions.embed_links ), inline=True ) \
				.add_field( name="Attach Files", value=str( permissions.attach_files ), inline=True ) \
				.add_field( name="Read Message History", value=str( permissions.read_message_history ), inline=True ) \
				.add_field( name="Mention Everyone", value=str( permissions.mention_everyone ), inline=True ) \
				.add_field( name="Use External Emojis", value=str( permissions.external_emojis ), inline=True ) \
				.add_field( name="Change Nickname", value=str( permissions.change_nickname ), inline=True ) \
				.add_field( name="Manage Nicknames", value=str( permissions.manage_nicknames ), inline=True ) \
				.add_field( name="Manage Roles", value=str( permissions.manage_roles ), inline=True ) \
				.add_field( name="Manage Emojis", value=str( permissions.manage_emojis ), inline=True ) \
				.set_footer( text=f"Created at {_created_at}" )
			await CLIENT.send_message( message.channel, f"Here you go!", embed=embed_obj )
		@staticmethod
		async def channels ( message: discord.Message ):
			"""
			Lists the server's channels.
			:param message: A discord.Message object.
			"""
			_channels = [
				x
				for x in CLIENT.get_all_channels( )
				if x.server == message.server
			]
			voice_channels = [ ]
			text_channels = [ ]
			vappend = voice_channels.append
			tappend = text_channels.append
			for _channel in _channels:
				if _channel.type == discord.ChannelType.voice:
					vappend( str( _channel ) )
				else:
					tappend( str( _channel ) )
			voice_channels = [
				f"#{x}"
				for x in voice_channels
			]
			voice_channels.sort( )
			text_channels = [
				f"#{x}"
				for x in text_channels
			]
			text_channels.sort( )
			v_msg = format_message( f"Voice Channels:\n{', '.join(voice_channels)}" )
			t_msg = format_message( f"Text Channels:\n{', '.join(text_channels)}" )
			for msg in v_msg:
				await CLIENT.send_message( message.channel, msg )
			for msg in t_msg:
				await CLIENT.send_message( message.channel, msg )
			del vappend
			del tappend
		@staticmethod
		async def ping ( message: discord.Message ):
			"""
			Pings logbot.
			:param message: A discord.Message object from on_message.
			"""
			timestamp = datetime.now( ) - message.timestamp
			await CLIENT.send_message( message.channel, f"```LogBot Main Online ~ {round(round(timestamp.microseconds / 1000))}```" )
			del timestamp
		@staticmethod
		async def mutes ( message: discord.Message, muted_role: discord.Role ):
			"""
			Mutes all users mentioned my `message`
			:param muted_role: A discord.Role object representing a role without send message permissions.
			:param message: A discord.Message object from on_message.
			"""
			muted = "Muted Users:\n"
			for user in message.server.members:
				if muted_role in user.roles:
					muted += f"{user}\n"
			await CLIENT.send_message( message.channel, f"{muted}" )
			del muted
		@staticmethod
		async def convert ( message: discord.Message, prefix: str ):
			"""
			Converts text to other formats.
			:param message: A discord.Message object from on_message
			:param prefix: The server's prefix.
			"""
			content = message.content.replace( f"{prefix}convert ", "" )
			# noinspection PyUnusedLocal
			ret = ""
			if content.startswith( "unicode " ):
				ret = f"{codecs.unicode_escape_encode(content.replace('unicode ', ''), 'backslashreplace')[0]}" \
					.replace( "b'\\u", "" ) \
					.replace( "'", "" )
			elif content.startswith( "utf-8 ", ):
				ret = f"{codecs.utf_8_encode(content.replace('utf-8 ', ''), 'backslashreplace')[0]}".replace( "b'\\u", "" ).replace( "'", "" )
			elif content.startswith( "ascii " ):
				ret = f"{codecs.ascii_encode( content.replace( 'ascii ', '' ), 'backslashreplace' )[ 0 ]}".replace( "b'\\u", "" ).replace( "'", "" )
			elif content.startswith( "oem " ):
				ret = f"{codecs.oem_encode( content.replace( 'oem ', '' ), 'backslashreplace' )[ 0 ]}".replace( "b'\\u", "" ).replace( "'", "" )
			else:
				ret = "Not a valid value."
			msg = await CLIENT.send_message( message.channel, ret )
			await CLIENT.edit_message( msg, msg.content.replace( 'b', '', 1 ) )
			del content
			del msg
			del ret
		@staticmethod
		async def server ( message: discord.Message ):
			"""
			Fetches server information.
			:param message: A discord.Message object from on_message
			"""
			server_created_at = format_time( message.server.created_at )
			server = message.server
			roles = [
				f"{str(role).replace('@', '')} ({role.position}) [{role.id}]"
				for role in server.role_hierarchy
			]
			try:
				# <editor-fold desc="discord.Embed">
				embed_obj = discord.Embed( title=server.name, description=f"Information for {server.name}", colour=discord.Colour.teal( ) ) \
					.add_field( name="Total Members", value=str( server.member_count ), inline=True ) \
					.add_field( name="Owner", value=str( server.owner ), inline=True ) \
					.add_field( name="ID", value=server.id, inline=True ) \
					.add_field( name="Total Channels", value=str( len( server.channels ) ), inline=True ) \
					.add_field( name="Total Roles", value=str( len( server.roles ) ), inline=True ) \
					.add_field( name="Creation Time", value=f"{get_diff(server_created_at, datetime.now())} ago ({server_created_at.month}.{server_created_at.day}.{server_created_at.year} {server_created_at.hour}:{server_created_at.minute})" ) \
					.add_field( name="Default Channel", value=str( server.default_channel ) ) \
					.set_thumbnail( url=server.icon_url )
				try:
					embed_obj.add_field( name="Role Hierarchy", value='\n'.join( roles ) )
				except Exception:
					traceback.format_exc( )
				# </editor-fold>
				await CLIENT.send_message( message.channel, "", embed=embed_obj )
			except Exception:
				# <editor-fold desc="discord.Embed">
				embed_obj = discord.Embed( title=server.name, description=f"Information for {server.name}", colour=discord.Colour.teal( ) ) \
					.add_field( name="Total Members", value=str( server.member_count ), inline=True ) \
					.add_field( name="Owner", value=str( server.owner ), inline=True ) \
					.add_field( name="ID", value=server.id, inline=True ) \
					.add_field( name="Total Channels", value=str( len( server.channels ) ), inline=True ) \
					.add_field( name="Total Roles", value=str( len( server.roles ) ), inline=True ) \
					.add_field( name="Creation Time", value=f"{get_diff(server_created_at, datetime.now())} ago ({server_created_at.month}.{server_created_at.day}.{server_created_at.year} {server_created_at.hour}:{server_created_at.minute})" ) \
					.add_field( name="Default Channel", value=str( server.default_channel ) ) \
					.set_thumbnail( url=server.icon_url )
				# </editor-fold>
				hierarchy = '\n'.join( roles )
				try:
					await CLIENT.send_message( message.channel, f"Role Hierarchy:\n{hierarchy}", embed=embed_obj )
				except Exception:
					await CLIENT.send_message( message.channel, f"Could not fetch the Role Hierarchy...", embed=embed_obj )
			del server_created_at
			del server
			del roles
			del embed_obj
		@staticmethod
		async def disables ( message: discord.Message, prefix: str ):
			"""
			Sends a message with an embed of all disabled features for the `message`'s server
			:param message: A discord.Message object from on_message.
			:param prefix: The server's prefix.
			"""
			# <editor-fold desc="discord.Embed">
			embed_obj = discord.Embed( title="Disabled Features", descriptions="A list of disabled features in this server.", colour=discord.Colour.dark_purple( ) ) \
				.add_field( name=f"{prefix}exclude", value=str( DISABLES[ message.server.id ][ "exclude" ] ) ) \
				.add_field( name=f"{prefix}excludechannel", value=str( DISABLES[ message.server.id ][ "excludechannel" ] ) ) \
				.add_field( name=f"{prefix}includechannel", value=str( DISABLES[ message.server.id ][ "includechannel" ] ) ) \
				.add_field( name=f"{prefix}mark", value=str( DISABLES[ message.server.id ][ "mark" ] ) ) \
				.add_field( name=f"{prefix}showlist", value=str( DISABLES[ message.server.id ][ "showlist" ] ) ) \
				.add_field( name=f"{prefix}showmarks", value=str( DISABLES[ message.server.id ][ "showmarks" ] ) ) \
				.add_field( name=f"{prefix}channel", value=str( DISABLES[ message.server.id ][ "channel" ] ) ) \
				.add_field( name=f"{prefix}say", value=str( DISABLES[ message.server.id ][ "say" ] ) ) \
				.add_field( name=f"{prefix}query", value=str( DISABLES[ message.server.id ][ "query" ] ) ) \
				.add_field( name=f"{prefix}wiki", value=str( DISABLES[ message.server.id ][ "wiki" ] ) ) \
				.add_field( name=f"{prefix}decide", value=str( DISABLES[ message.server.id ][ "decide" ] ) ) \
				.add_field( name=f"{prefix}prune", value=str( DISABLES[ message.server.id ][ "prune" ] ) ) \
				.add_field( name=f"{prefix}purge", value=str( DISABLES[ message.server.id ][ "purge" ] ) ) \
				.add_field( name=f"{prefix}user", value=str( DISABLES[ message.server.id ][ "user" ] ) ) \
				.add_field( name=f"{prefix}translate", value=str( DISABLES[ message.server.id ][ "translate" ] ) ) \
				.add_field( name=f"{prefix}urban", value=str( DISABLES[ message.server.id ][ "urban" ] ) ) \
				.add_field( name=f"{prefix}roll", value=str( DISABLES[ message.server.id ][ "roll" ] ) ) \
				.add_field( name=f"{prefix}server", value=str( DISABLES[ message.server.id ][ "server" ] ) ) \
				.add_field( name=f"{prefix}convert", value=str( DISABLES[ message.server.id ][ "convert" ] ) ) \
				.add_field( name=f"{prefix}dict", value=str( DISABLES[ message.server.id ][ "dict" ] ) ) \
				.add_field( name=f"{prefix}permissions", value=str( DISABLES[ message.server.id ][ "permissions" ] ) ) \
				.add_field( name=f"{prefix}gif", value=str( DISABLES[ message.server.id ][ "gif" ] ) ) \
				.add_field( name="welcome", value=str( DISABLES[ message.server.id ][ "welcome" ] ) ) \
				.add_field( name="goodbye", value=str( DISABLES[ message.server.id ][ "goodbye" ] ) )
			# </editor-fold>
			await CLIENT.send_message( message.channel, f"Here you go!", embed=embed_obj )
			del embed_obj
		@staticmethod
		async def decide ( message: discord.Message, prefix: str ):
			"""
			Chooses a random value from those listed in `message.content`.
			:param message: A discord.Message object from on_message.
			:param prefix: The server's prefix.
			"""
			content = message.content.replace( f"{prefix}decide ", "" ).split( "|" )
			choice = random.choice( content )
			await CLIENT.send_message( message.channel, f"```I have chosen: {choice}```" )
			del content
			del choice
		@staticmethod
		async def suggest ( message: discord.Message, prefix: str ):
			"""
			Writes a suggestion to a file.
			:param message: A discord.Message object from on_message
			:param prefix: The server's prefix.
			"""
			suggestion = message.content.replace( f"{prefix}suggest ", "", 1 )
			# <editor-fold desc="WRITER: suggestions">
			writer = open( SUGGESTIONS_PATH, 'a' )
			writer.write( f"\n{suggestion}" )
			writer.close( )
			# </editor-fold>
			await CLIENT.send_message( message.channel, "```Thank you for your suggestion.```" )
			print( f"{Fore.YELLOW}{message.author} gave you a suggestion.{Fore.RESET}" )
			del writer
			del suggestion
		@staticmethod
		async def suggestions ( message: discord.Message ):
			"""
			Gets a list of suggestions given, then sends it through Discord.
			:param message: A discord.Message object from on_message.
			"""
			# <editor-fold desc="READER: suggestions">
			# noinspection PyShadowingNames
			reader_obj = open( SUGGESTIONS_PATH, 'r' )
			ret = f"Suggestions:{reader_obj.read()}"
			reader_obj.close( )
			# </editor-fold>
			for item in format_message( ret ):
				await CLIENT.send_message( message.channel, item )
			del ret
			del reader_obj
		@staticmethod
		async def showlist ( message: discord.Message ):
			"""
			Shows the list of excluded channels.
			:param message: A discord.Message object.
			"""
			msg = "Excluded Channels:\n"
			for channel in EXCLUDE_CHANNEL_LIST:
				for channel_obj in message.server.channels:
					if channel == channel_obj.id:
						msg += channel_obj.mention + "\n"
			await CLIENT.send_message( message.channel, msg )
			del msg
		@staticmethod
		async def showmarks ( message: discord.Message ):
			"""
			Shows the list of marked channels.
			:param message: A discord.Message object.
			"""
			msg = "Marked Channels\n"
			for item in MARKLIST:
				for channel in message.server.channels:
					if channel.id == item:
						msg += channel.mention + "\n"
			await CLIENT.send_message( message.channel, msg )
			del msg
		@staticmethod
		async def updates ( message: discord.Message ):
			"""
			Shows what is new with the bot.
			:param message: A discord.Message object.
			"""
			tmp = '\n'.join( WHATS_NEW )
			await CLIENT.send_message( message.channel, f"```Updates:\n{tmp}```" )
			del tmp
		@staticmethod
		async def planned ( message: discord.Message ):
			"""
			Shows what is planned with the bot.
			:param message: A discord.Message object.
			"""
			tmp = '\n'.join( PLANNED )
			await CLIENT.send_message( message.channel, f"```Coming Soon:\n{tmp}```" )
			del tmp
		@staticmethod
		async def query ( message: discord.Message, prefix: str ):
			"""
			Fetches information from Wolfram|Alpha.
			:param message: A discord.Message object.
			:param prefix: The server's prefix.
			"""
			try:
				content = message.content.replace( f"{prefix}query ", "" )
				await CLIENT.send_typing( message.channel )
				res = WCLIENT.query( content )
				ret = ""
				for pod in res.pods:
					for item in pod.texts:
						ret += f"{pod.title}: {item}\n"
				ret += "Powered by Wolfram|Alpha"
				for msg in format_message( ret ):
					await CLIENT.send_message( message.channel, msg )
				del ret
				del res
				del content
			except Exception:
				await CLIENT.send_message( message.channel, "```We couldn't get that information. Please try again.```" )
				print( f"{Fore.LIGHTGREEN_EX}{message.author} attempted to use $query, but failed.{Fore.RESET}" )
				print( traceback.format_exc( ) )
		@staticmethod
		async def wiki ( message: discord.Message, prefix: str ):
			"""
			Fetches information from Wikipedia.
			:param message: A discord.Message object.
			:param prefix: The server's prefix.
			"""
			content = message.content.replace( f"{prefix}wiki ", "" )
			await CLIENT.send_typing( message.channel )
			# noinspection PyUnusedLocal
			info = ""
			try:
				info = wikipedia.summary( content )
			except Exception:
				search = wikipedia.search( content )
				search_str = ""
				for item in search:
					search_str += item + "\n"
				await CLIENT.send_message( message.channel, f"```I found these results:\nSearched Item: {search_str}```" )
				msg = await CLIENT.wait_for_message( author=message.author )
				info = wikipedia.summary( msg.content )
				del msg
				del search
				del search_str
			for item in format_message( info ):
				await CLIENT.send_message( message.channel, item )
			del content
			del info
		@staticmethod
		async def user_permissions ( message: discord.Message, prefix: str ):
			"""
			Sends the user's permissions.
			:param message: A discord.Message object.
			:param prefix: The server's prefix.
			"""
			permparse = argparser.ArgParser( ", ", "=" )
			msg = permparse.parse( message.content.replace( f"{prefix}permissions ", "" ) )

			# <editor-fold desc="Fetch User">
			# noinspection PyUnusedLocal
			user = discord.User
			if msg.get( "user" ) is None:
				user = message.author
			else:
				if "<@" in msg.get( "user" ):
					user = discord.utils.find(
						lambda u:u.mention == msg.get( "user" ),
						message.server.members
					)
				else:
					user = message.server.get_member_named( msg.get( "user" ) )
			# </editor-fold>

			if message.channel_mentions:
				permissions = user.permissions_in( message.channel_mentions[ 0 ] )
				embed_obj = discord.Embed( title=f"Permissions for {user}", colour=discord.Colour.dark_blue( ) ) \
					.add_field( name="Create Instant Invite", value=str( permissions.create_instant_invite ), inline=True ) \
					.add_field( name="Kick Members", value=str( permissions.kick_members ), inline=True ) \
					.add_field( name="Ban Members", value=str( permissions.ban_members ), inline=True ) \
					.add_field( name="Administrator", value=str( permissions.administrator ), inline=True ) \
					.add_field( name="Manage Channels", value=str( permissions.manage_channels ), inline=True ) \
					.add_field( name="Manage Server", value=str( permissions.manage_server ), inline=True ) \
					.add_field( name="Read Messages", value=str( permissions.read_messages ), inline=True ) \
					.add_field( name="Send Messages", value=str( permissions.send_messages ), inline=True ) \
					.add_field( name="Send TTS Messages", value=str( permissions.send_tts_messages ), inline=True ) \
					.add_field( name="Manage Messages", value=str( permissions.manage_messages ), inline=True ) \
					.add_field( name="Embed Links", value=str( permissions.embed_links ), inline=True ) \
					.add_field( name="Attach Files", value=str( permissions.attach_files ), inline=True ) \
					.add_field( name="Read Message History", value=str( permissions.read_message_history ), inline=True ) \
					.add_field( name="Mention Everyone", value=str( permissions.mention_everyone ), inline=True ) \
					.add_field( name="Use External Emojis", value=str( permissions.external_emojis ), inline=True ) \
					.add_field( name="Change Nickname", value=str( permissions.change_nickname ), inline=True ) \
					.add_field( name="Manage Nicknames", value=str( permissions.manage_nicknames ), inline=True ) \
					.add_field( name="Manage Roles", value=str( permissions.manage_roles ), inline=True ) \
					.add_field( name="Manage Emojis", value=str( permissions.manage_emojis ), inline=True )
				await CLIENT.send_message( message.channel, "Here you go!", embed=embed_obj )
				del permissions
				del embed_obj
			else:
				permissions = user.server_permissions
				embed_obj = discord.Embed( title=f"Permissions for {user}", colour=discord.Colour.dark_blue( ) ) \
					.add_field( name="Create Instant Invite", value=str( permissions.create_instant_invite ), inline=True ) \
					.add_field( name="Kick Members", value=str( permissions.kick_members ), inline=True ) \
					.add_field( name="Ban Members", value=str( permissions.ban_members ), inline=True ) \
					.add_field( name="Administrator", value=str( permissions.administrator ), inline=True ) \
					.add_field( name="Manage Channels", value=str( permissions.manage_channels ), inline=True ) \
					.add_field( name="Manage Server", value=str( permissions.manage_server ), inline=True ) \
					.add_field( name="Read Messages", value=str( permissions.read_messages ), inline=True ) \
					.add_field( name="Send Messages", value=str( permissions.send_messages ), inline=True ) \
					.add_field( name="Send TTS Messages", value=str( permissions.send_tts_messages ), inline=True ) \
					.add_field( name="Manage Messages", value=str( permissions.manage_messages ), inline=True ) \
					.add_field( name="Embed Links", value=str( permissions.embed_links ), inline=True ) \
					.add_field( name="Attach Files", value=str( permissions.attach_files ), inline=True ) \
					.add_field( name="Read Message History", value=str( permissions.read_message_history ), inline=True ) \
					.add_field( name="Mention Everyone", value=str( permissions.mention_everyone ), inline=True ) \
					.add_field( name="Use External Emojis", value=str( permissions.external_emojis ), inline=True ) \
					.add_field( name="Change Nickname", value=str( permissions.change_nickname ), inline=True ) \
					.add_field( name="Manage Nicknames", value=str( permissions.manage_nicknames ), inline=True ) \
					.add_field( name="Manage Roles", value=str( permissions.manage_roles ), inline=True ) \
					.add_field( name="Manage Emojis", value=str( permissions.manage_emojis ), inline=True )
				await CLIENT.send_message( message.channel, "Here you go!", embed=embed_obj )
				del permissions
				del embed_obj
			del user
			del permparse
			del msg
		@staticmethod
		async def translate_get ( message: discord.Message ):
			"""
			Gets a list of language codes for the translator.
			:param message: A discord.Message object.
			"""
			# noinspection PyShadowingNames
			reader_obj = open( f"{DISCORD_SETTINGS_PATH}\\languages.txt", 'r' )
			ret = f"```Languages:\n{reader_obj.read()}```"
			await CLIENT.send_message( message.channel, ret )
			reader_obj.close( )
			del reader_obj
			del ret
		@staticmethod
		async def translate ( message: discord.Message, prefix: str ):
			"""
			Translates text.
			:param message: A discord.Message object.
			:param prefix: The server's prefix.
			"""
			content = message.content.replace( f"{prefix}translate ", "", 1 ).split( "|" )
			translator = translate.Translator( to_lang=content[ 1 ] )
			translator.from_lang = content[ 0 ]
			tmp = str( translator.translate( content[ 2 ] ) )
			tmp = str( tmp ).replace( '["', "" ).replace( '"]', "" ).replace( "\\n", "\n" )
			msg = await CLIENT.send_message( message.channel, format_message( tmp ) )
			await CLIENT.edit_message( msg, msg.content.replace( "\\n", "\n" ).replace( "['", '' ).replace( "']", "" ) )
			del content
			del translator
			del tmp
		@staticmethod
		async def dict ( message: discord.Message, prefix: str ):
			"""
			Fetches information from PyDictionary.
			:param message: A discord.Message object.
			:param prefix: The server's prefix.
			"""
			content = message.content.replace( f"{prefix}dict ", "", 1 )
			if content.startswith( "def" ):
				content = content.replace( "def ", "", 1 )
				tmp = PYDICT.meaning( content )
				ret = ""
				for key, value in tmp.items( ):
					ret += key + "\n"
					for item in value:
						ret += item + "\n"
					ret += "\n"
				await CLIENT.send_message( message.channel, f"```{ret}```" )
				del tmp
				del ret
			elif content.startswith( "ant " ):
				content = content.replace( "ant ", "", 1 )
				tmp = PYDICT.antonym( content )
				ret = ""
				for item in tmp:
					ret += item + "\n"
				await CLIENT.send_message( message.channel, f"```{ret}```" )
				del ret
				del tmp
			elif content.startswith( "syn " ):
				content = content.replace( "syn ", "", 1 )
				tmp = PYDICT.synonym( content )
				ret = ""
				for item in tmp:
					ret += item + "\n"
				await CLIENT.send_message( message.channel, f"```{ret}```" )
				del tmp
				del ret
			del content
	# noinspection PyShadowingNames
	class Admin:
		"""
		For admins only!
		"""
		@staticmethod
		async def filter ( message: discord.Message, admin_role: discord.Role ):
			"""
			Uses the filter on a message.
			:param message: A discord.Message object.
			:param admin_role: The server's admin role.
			"""
			# <editor-fold desc="Fetch the Server's Filter Settings">
			server_filter = FILTER_SETTINGS.get( message.server.id )
			if server_filter is None:
				FILTER_SETTINGS[ message.server.id ] = {
					"ACTIVE":False,
					"ADMCHK":False,
					"DELCPY":False,
					"DELINV":False
				}
				server_filter = FILTER_SETTINGS.get( message.server.id )
			# </editor-fold>
			if server_filter[ "ACTIVE" ] is True and not message.author.bot:
				if server_filter[ "ADMCHK" ] is True:
					if admin_role not in message.author.roles:
						if server_filter[ "DELCPY" ] is True:
							if len( message.content.split( "\n" ) ) >= 10 and (")" in message.content or "(" in message.content or "," in message.content or "▇" in message.content or "╰" in message.content or "▅" in message.content or "━" in message.content or "┣" in message.content or "▇" in message.content or "┃" in message.content or "━" in message.content or "╭" in message.content):
								await CLIENT.delete_message( message )
						if server_filter[ "DELINV" ] is True:
							if "discord.gg/" in message.content:
								await CLIENT.delete_message( message )
				else:
					if server_filter[ "DELCPY" ] is True:
						if len( message.content.split( "\n" ) ) >= 10 and (")" in message.content or "(" in message.content or "," in message.content or "▇" in message.content or "╰" in message.content or "▅" in message.content or "━" in message.content or "┣" in message.content or "▇" in message.content or "┃" in message.content or "━" in message.content or "╭" in message.content):
							await CLIENT.delete_message( message )
					if server_filter[ "DELINV" ] is True:
						if "discord.gg/" in message.content:
							await CLIENT.delete_message( message )
		@staticmethod
		async def filter_settings ( message: discord.Message, prefix: str ):
			"""
			Shows the filter settings.
			:param message: A discord.Message object.
			:param prefix: The server's prefix.
			"""
			# <editor-fold desc="Fetch the Server's Filter Settings">
			if FILTER_SETTINGS.get( message.server.id ) is None:
				FILTER_SETTINGS[ message.server.id ] = {
					"ACTIVE":False,
					"ADMCHK":False,
					"DELCPY":False,
					"DELINV":False
				}
			# </editor-fold>
			cnt = message.content.replace( f"{prefix}spamfilter settings", "" )
			if cnt:
				if cnt[ 0 ] == " ":
					cnt = cnt.replace( " ", "", 1 )
			tmp = cnt.split( " " )
			keys = { }

			if "=" in cnt:
				for item in tmp:
					_tmp = item.split( "=" )
					keys[ _tmp[ 0 ] ] = _tmp[ 1 ]
				if "ACTIVE" in keys.keys( ):
					FILTER_SETTINGS[ message.server.id ][ "ACTIVE" ] = ast.literal_eval( keys[ "ACTIVE" ] )
				if "ADMCHK" in keys.keys( ):
					FILTER_SETTINGS[ message.server.id ][ "ADMCHK" ] = ast.literal_eval( keys[ "ADMCHK" ] )
				if "DELCPY" in keys.keys( ):
					FILTER_SETTINGS[ message.server.id ][ "DELCPY" ] = ast.literal_eval( keys[ "DELCPY" ] )
				if "DELINV" in keys.keys( ):
					FILTER_SETTINGS[ message.server.id ][ "DELINV" ] = ast.literal_eval( keys[ "DELINV" ] )
			else:
				embed_obj = discord.Embed( title="Filter Settings", description=f"Filter Settings for {message.server.name}", colour=discord.Colour.dark_blue( ) ) \
					.add_field( name=f"ACTIVE", value=str( FILTER_SETTINGS[ message.server.id ][ 'ACTIVE' ] ) ) \
					.add_field( name=f"ADMCHK", value=str( FILTER_SETTINGS[ message.server.id ][ 'ADMCHK' ] ) ) \
					.add_field( name=f"DELCPY", value=str( FILTER_SETTINGS[ message.server.id ][ 'DELCPY' ] ) ) \
					.add_field( name=f"DELINV", value=str( FILTER_SETTINGS[ message.server.id ][ 'DELINV' ] ) )
				await CLIENT.send_message( message.channel, f"", embed=embed_obj )
		@staticmethod
		async def setup ( message: discord.Message, admin_role: discord.Role ):
			"""
			Sets the bot up for your server.
			:param message: A discord.Message object.
			:param admin_role: The server's admin role.
			"""
			# <editor-fold desc="Exclude">
			msg1 = await CLIENT.send_message( message.channel, "```Which channels would you like to exclude? Type None for no excluded channels.```" )
			msg2 = await CLIENT.wait_for_message( author=message.author, channel=message.channel )
			excludes = msg2.channel_mentions
			await CLIENT.delete_messages( [ msg1, msg2 ] )
			# </editor-fold>
			# <editor-fold desc="Admins">
			msg1 = await CLIENT.send_message( message.channel, "```Who would you like as Admins for your server? Server owners are automatically and permanently admins. Type None for no one.```" )
			msg2 = await CLIENT.wait_for_message( channel=message.channel, author=message.author )
			admins = msg2.mentions
			await CLIENT.delete_messages( [ msg1, msg2 ] )
			# </editor-fold>
			# <editor-fold desc="Marks">
			msg1 = await CLIENT.send_message( message.channel, "```What channels would you like to be marked? Type None for no channels.```" )
			msg2 = await CLIENT.wait_for_message( channel=message.channel, author=message.author )
			marks = msg2.channel_mentions
			await CLIENT.delete_messages( [ msg1, msg2 ] )
			# </editor-fold>
			# <editor-fold desc="Welcome">
			msg1 = await CLIENT.send_message( message.channel, "```What would you like the welcome message to be? Use {server} for the server name and {user} for the user name. Type None for no welcome message.```" )
			msg2 = await CLIENT.wait_for_message( channel=message.channel, author=message.author )
			welcome = msg2.content
			await CLIENT.delete_messages( [ msg1, msg2 ] )
			# </editor-fold>
			# <editor-fold desc="Goodbye">
			msg1 = await CLIENT.send_message( message.channel, "```What would you like the leave message to be? Type None for no leave message. Use {server} for the server name and {user} for the user's name.```" )
			msg2 = await CLIENT.wait_for_message( channel=message.channel, author=message.author )
			goodbye = msg2.content
			await CLIENT.delete_messages( [ msg1, msg2 ] )
			# </editor-fold>

			for _channel in excludes:
				if _channel.id not in EXCLUDE_CHANNEL_LIST:
					EXCLUDE_CHANNEL_LIST.append( _channel.id )
			for _user in admins:
				if admin_role not in _user.roles:
					await CLIENT.add_roles( _user, admin_role )
			for _channel in marks:
				if _channel.id not in MARKLIST:
					MARKLIST.append( _channel.id )

			if welcome.startswith( "read(" ):
				content = welcome.replace( "read(", "" )
				_file_cnt = content[ 0:len( content ) - 1 ]
				_file_path = f"{message.server.id}.txt"
				open( _file_path, 'w' ).write( _file_cnt )
				try:
					DB.write( "Welcomes", { "server":message.server.id, "message":f"read( {_file_path} )" } )
				except Exception:
					pass
				DB.update( "Welcomes", "message", f"read( {_file_path} )", message.server.id )
			else:
				if not welcome == "None":
					try:
						DB.write(
							"Welcomes",
							{
								"server" :message.server.id,
								"message":welcome
							}
						)
					except Exception:
						pass
					DB.update( "Welcomes", "message", welcome, message.server.id )
				else:
					DB.update( "Welcomes", "message", "", message.server.id )
			if not goodbye == "None":
				DB.write(
					"Goodbyes",
					{
						"server" :message.server.id,
						"message":goodbye
					}
				)
				DB.update(
					"Goodbyes",
					message.server.id,
					goodbye,
					message.server.id
				)
			await CLIENT.send_message( message.channel, "```The bot has been set up for your server!```" )
			del msg1, msg2, excludes, marks, admins, welcome, goodbye
		@staticmethod
		async def files ( message: discord.Message ):
			"""
			Shows the server's log files.
			:param message: A discord.Message object.
			"""
			files = [ ]
			for channel in message.server.channels:
				try:
					try:
						_file = f"{channel}.mark.txt"
						_reader_tmp = open( f"{DISCORD_LOGS_PATH}\\{message.server.name}\\{_file}", 'r' )
						tmp = _reader_tmp.read( )
						_reader_tmp.close( )
						files.append( _file )
						del tmp
						del _reader_tmp
						del _file
					except Exception:
						pass
					file = f"{channel}.txt"
					reader_tmp = open( f"{DISCORD_LOGS_PATH}\\{message.server.name}\\{file}", 'r' )
					tmp = reader_tmp.read( )
					reader_tmp.close( )
					files.append( file )
					del file
					del reader_tmp
					del tmp
				except Exception:
					pass
			fstr = f"```" + '\n'.join( files ) + "```"
			await CLIENT.send_message( message.channel, fstr )
			del fstr
			del files
		@staticmethod
		async def changeprefix ( message: discord.Message, prefix: str ):
			"""
			Changes the server's prefix.
			:param message: A discord.Message object.
			:param prefix: The server's prefix.
			"""
			new_prefix = message.content.replace( f"{prefix}changeprefix ", "" )
			if not new_prefix == "```":
				try:
					DB.write(
						"Prefixes",
						{
							"server":message.server.id,
							"prefix":new_prefix
						}
					)
				except Exception:
					pass
				DB.update(
					"Prefixes",
					"prefix",
					new_prefix,
					message.server.id
				)
				await CLIENT.send_message( message.channel, f"Changed the prefix to {new_prefix}" )
			else:
				await CLIENT.send_message( message.channel, f"The prefix cannot be ``` because it messes up the bot's message formatting." )
		@staticmethod
		async def mute ( message: discord.Message, muted_role: discord.Role ):
			"""
			Mutes a member.
			:param message: A discord.Message object.
			:param muted_role: The server's muted role.
			"""
			users_to_mute = list( )
			for item in message.content.split( " " ):
				if "<" in item:
					users_to_mute.append(
						discord.utils.find(
							lambda u:u.mention == item and not u.id == owner_id,
							message.server.members
						)
					)
				else:
					try:
						_m = message.server.get_member_named( item )
						if _m is not None:
							users_to_mute.append(
								(
									message.server.get_member_named(
										item
									) if not message.server.get_member_named(
										item
									).id == owner_id else None
								)
							)
					except Exception:
						traceback.format_exc( )
			while None in users_to_mute:
				users_to_mute.remove(
					None
				)
			for user in users_to_mute:
				await CLIENT.add_roles(
					user,
					muted_role
				)
			await CLIENT.send_message( message.channel, f"Muted {', '.join([str(x) for x in users_to_mute])} ({len(users_to_mute)}) users. :mute:" )
			del users_to_mute
		@staticmethod
		async def unmute ( message: discord.Message, muted_role: discord.Role ):
			"""
			Unmutes a server member.
			:param message: A discord.Message object.
			:param muted_role: The server's muted role.
			"""
			users_to_mute = list( )
			for item in message.content.split( " " ):
				if "<" in item:
					users_to_mute.append(
						discord.utils.find(
							lambda u:u.mention == item,
							message.server.members
						)
					)
				else:
					users_to_mute.append(
						message.server.get_member_named(
							item
						)
					)
			while None in users_to_mute:
				users_to_mute.remove( None )
			for user in users_to_mute:
				await CLIENT.remove_roles( user, muted_role )
			await CLIENT.send_message( message.channel, f"Unmuted {', '.join([str(x) for x in users_to_mute])} ({len(users_to_mute)}) users. :loud_sound:" )
			del users_to_mute
		@staticmethod
		async def disable ( message: discord.Message, prefix: str ):
			"""
			Disables commands.
			:param message: A discord.Message object.
			:param prefix: The server's prefix.
			"""
			temp = message.content.replace( f"{prefix}disable ", "" ).replace( prefix, "" )
			if temp == "[all]":
				for key in list( DISABLES[ message.server.id ].keys( ) ):
					DISABLES[ message.server.id ][ key ] = True
			else:
				DISABLES[ message.server.id ][ temp ] = True
			await CLIENT.send_message( message.channel, f"Disabled {temp} :no_entry_sign:" )
			del temp
		@staticmethod
		async def enable ( message: discord.Message, prefix: str ):
			"""
			Enables commands.
			:param message: A discord.Message object.
			:param prefix: The server's prefix.
			"""
			temp = message.content.replace( f"{prefix}enable ", "" ).replace( prefix, "" )
			if temp == "[all]":
				for key in list( DISABLES[ message.server.id ].keys( ) ):
					DISABLES[ message.server.id ][ key ] = False
			else:
				DISABLES[ message.server.id ][ temp ] = False
			await CLIENT.send_message( message.channel, f"Enabled {temp} :white_check_mark:" )
			del temp
		@staticmethod
		async def admin ( message: discord.Message, admin_role: discord.Role, prefix: str ):
			"""
			Edits the admins for the bot.
			:param message: A discord.Message object.
			:param admin_role: The admin role for the server.
			:param prefix: The server's prefix.
			"""
			content = message.content.replace( f"{prefix}admin ", "" )
			users = list( )
			for item in message.content.split( " " ):
				if "<" in item:
					users.append( discord.utils.find( lambda u:u.mention == item, message.server.members ) )
				else:
					users.append( message.server.get_member_named( item ) )
			while None in users:
				users.remove( None )
			if content[ 0 ] == 'a':
				added_list = [ ]
				for user in users:
					if admin_role not in user.roles:
						await CLIENT.add_roles( user, admin_role )
						added_list.append( str( user ) )
				await CLIENT.send_message( message.channel, f"Added {', '.join(added_list)} to the admin list. :heavy_plus_sign:" )
				del added_list
			elif content[ 0 ] == 'r':
				removed_list = [ ]
				for user in users:
					if admin_role in user.roles:
						await CLIENT.remove_roles( user, admin_role )
						removed_list.append( str( user ) )
				await CLIENT.send_message( message.channel, f"Removed {', '.join(removed_list)} from the admin list. :heavy_minus_sign:" )
				del removed_list
			elif content[ 0 ] == 's':
				ret = "```Admins:\n"
				for mem in message.server.members:
					if not discord.utils.find( lambda r:r == admin_role, mem.roles ) is None:
						ret += f"{mem}\n"
				await CLIENT.send_message( message.channel, f"{ret}```" )
				del ret
			del content
			del users
		@staticmethod
		async def channel ( message: discord.Message, prefix: str ):
			"""
			Creates, deletes, or edits a channel.
			:param message: A discord.Message object.
			:param prefix: The server's prefix.
			"""
			content = message.content.replace( f"{prefix}channel ", "" )
			if content.startswith( "new " ):
				content = content.replace( "new ", "", 1 )
				role = message.role_mentions[ 0 ] if message.role_mentions else None
				if isinstance( role, discord.Role ):
					them = discord.PermissionOverwrite(
						read_messages=False,
						send_messages=False,
						read_message_history=False,
						connect=False
					)
				else:
					them = discord.PermissionOverwrite(
						read_message=True,
						send_messages=True,
						read_message_history=True,
						attach_files=True,
						embed_links=True,
						mention_everyone=True,
						connect=True,
						use_voice_activity=True
					)
				# <editor-fold desc="discord.PermissionOverwrite us">
				ourselves = discord.PermissionOverwrite(
					read_messages=True,
					send_messages=True,
					read_message_history=True,
					attach_files=True,
					embed_links=True,
					mention_everyone=True,
					connect=True,
					use_voice_activity=True
				)
				# </editor-fold>
				them_perms = discord.ChannelPermissions( target=message.server.default_role, overwrite=them )
				us_perms = discord.ChannelPermissions( target=(role if isinstance( role, discord.Role ) else message.server.default_role), overwrite=ourselves )
				content = content.split( " " )
				if content[ 1 ].lower( ) == "voice":
					channel = await CLIENT.create_channel(
						message.server,
						content[ 0 ],
						them_perms,
						us_perms,
						type=discord.ChannelType.voice
					)
				else:
					channel = await CLIENT.create_channel(
						message.server,
						content[ 0 ],
						them_perms,
						us_perms
					)
				CHANNELS.append( channel.id )
				await CLIENT.send_message( message.channel, f"Created {channel.mention}" )
				del channel
				del role
				del them
				del ourselves
				del them_perms
				del us_perms
			elif content.startswith( 'del' ):
				try:
					for item in message.channel_mentions:
						await CLIENT.delete_channel( channel=item )
						CHANNELS.remove( item.id )
						await CLIENT.send_message( message.channel, f"Deleted {item}" )
				except Exception:
					await CLIENT.send_message( message.channel, "```Could not delete the channel.```" )
					print( f"{Fore.RED}Could not delete the channel.{Fore.RESET}" )
					print( traceback.format_exc( ) )
			elif content.startswith( 'show' ):
				ret = "Custom Channels:\n"
				for item in CHANNELS:
					for channel in message.server.channels:
						if channel.id == item:
							ret += f"#{item}\n"
				await CLIENT.send_message( message.channel, ret )
				del ret
			elif content.startswith( 'edit' ):
				content = content.replace( "edit ", "", 1 )
				channel = message.channel_mentions[ 0 ]
				role = message.role_mentions[ 0 ] if message.role_mentions else None
				mentions = message.mentions[ 0 ] if message.mentions else None
				overwrite = discord.PermissionOverwrite( )
				tmp = argparser.ArgParser( "&&", "=" ).parse( content )
				for key, value in tmp.items( ):
					tmp[ key ] = True if value == "True" else False
				overwrite.add_reactions = tmp.get( "add_reactions" )
				overwrite.read_messages = tmp.get( "read_messages" )
				overwrite.send_messages = tmp.get( "send_messages" )
				overwrite.send_tts_messages = tmp.get( "send_tts_messages" )
				overwrite.manage_messages = tmp.get( "manage_messages" )
				overwrite.embed_links = tmp.get( "embed_links" )
				overwrite.attach_files = tmp.get( "attach_files" )
				overwrite.read_message_history = tmp.get( "read_message_history" )
				overwrite.mention_everyone = tmp.get( "mention_everyone" )
				overwrite.external_emojis = tmp.get( "external_emojis" )
				overwrite.connect = tmp.get( "connect" )
				overwrite.speak = tmp.get( "speak" )
				overwrite.use_voice_activation = tmp.get( "use_voice_activation" )
				target_a = role if role is not None else message.server.default_role
				await CLIENT.edit_channel_permissions( channel, target_a if mentions is None else mentions, overwrite=overwrite )
				await CLIENT.send_message( message.channel, f"Changed permissions for {f'<@&{role.id}>' if not role is None else f'{mentions.mention}'}" )
				del content
				del channel
				del role
				del mentions
				del overwrite
				del tmp
				del target_a
			del content
		@staticmethod
		async def say ( message: discord.Message, prefix: str ):
			"""
			Sends a message in a certain channel using the bot.
			:param message: A discord.Message object.
			:param prefix: The server's prefix.
			"""
			if bot_id not in message.content:
				content = message.content.replace( f"{prefix}say ", "", 1 ).split( "|" )
				mentions = content[ 0 ].split( " " )
				text = content[ 1 ]
				mentions = [ CLIENT.get_channel( i.replace( "<#", "" ).replace( ">", "" ) ) for i in mentions ]
				for channel_obj in mentions:
					await CLIENT.send_message( channel_obj, text )
			else:
				await CLIENT.send_message( message.channel, f"```Please don't mention the bot in your message.```" )
		@staticmethod
		async def excludechannel ( message: discord.Message ):
			"""
			Excludes a channel from the logs.
			:param message: A discord.Message object.
			"""
			eapp = EXCLUDE_CHANNEL_LIST.append
			for channel in message.channel_mentions:
				if channel.id not in EXCLUDE_CHANNEL_LIST:
					eapp( channel.id )
					await CLIENT.send_message( message.channel, f"Excluding {channel.mention} from the logs." )
					send( f"Excluding {channel.id} from the logs.", message.server.name )
			if "all" in message.content.lower:
				for channel in message.server.channels:
					if channel.id not in EXCLUDE_CHANNEL_LIST:
						eapp( channel.id )
						await CLIENT.send_message( message.channel, f"Excluding {channel.mention} from the logs." )
						send( f"Excluding {channel.id} from the logs.", message.server.name )
		@staticmethod
		async def includechannel ( message: discord.Message ):
			"""
			Includes a channel in the logs.
			:param message: A discord.Message object.
			"""
			erem = EXCLUDE_CHANNEL_LIST.remove
			for channel in message.channel_mentions:
				if channel.id in EXCLUDE_CHANNEL_LIST:
					erem( channel.id )
					await CLIENT.send_message( message.channel, f"Including {channel.mention} in the logs." )
					send( f"Including {channel.mention} in the logs.", message.server.name )
			if "all" in message.content.lower:
				for channel in message.server.channels:
					if channel.id in EXCLUDE_CHANNEL_LIST:
						erem( channel.id )
						await CLIENT.send_message( message.channel, f"Including {channel.mention} in the logs." )
						send( f"Including {channel.mention} in the logs.", message.server.name )
		@staticmethod
		async def mark ( message: discord.Message, prefix: str ):
			"""
			Marks a channel to set aside logs.
			:param message: A discord.Message object.
			:param prefix: The server's prefix.
			"""
			content = message.content.replace( f"{prefix}mark ", "" )
			if content[ 0 ] == 'a':
				for channel in message.channel_mentions:
					if channel.id not in MARKLIST:
						MARKLIST.append( channel.id )
						await CLIENT.send_message( message.channel, f"Marking {channel.mention}" )
			elif content[ 0 ] == 'r':
				for channel in message.channel_mentions:
					MARKLIST.remove( channel.id )
					await CLIENT.send_message( message.channel, f"Unmarking {channel.mention}" )
			del content
		@staticmethod
		async def exclude ( message: discord.Message, time: datetime ):
			"""
			Excludes a message from the logs.
			:param message: A discord.Message object.
			:param time: The current time.
			"""
			print( f"{message.channel} ~ \"{message.content}\" ~ {message.author} ~ {time.day}.{time.month}.{time.year} {time.hour}:{time.minute} ~ {message.attachments}" )
		@staticmethod
		async def purge ( message: discord.Message, _limit: int, kwargs: dict ):
			"""
			Purges with conditions.
			:param message: A discord.Message object.
			:param _limit: Limiter option.
			:param kwargs: Other options.
			"""
			_from = kwargs.get( "from" )
			_before = kwargs.get( "before" )
			_after = kwargs.get( "after" )
			_contains = kwargs.get( "contains" )
			_pinned = ast.literal_eval( kwargs.get( "pinned" ) ) if not kwargs.get( "pinned" ) is None else None
			_embedded = ast.literal_eval( kwargs.get( "embedded" ) ) if not kwargs.get( "embedded" ) is None else None
			_attached = ast.literal_eval( kwargs.get( "attached" ) ) if not kwargs.get( "attached" ) is None else None
			_mentions = kwargs.get( "mentions" )
			_mentions_channel = kwargs.get( "mentions_channel" )
			_mentions_role = kwargs.get( "mentions_role" )

			if isinstance( _from, str ):
				_from = discord.utils.find( lambda u:u.mention == _from or u.name == _from or str( u ) == _from or u.nick == _from, message.server.members )
			if isinstance( _before, str ):
				_before = await CLIENT.get_message( message.channel, _before )
			if isinstance( _after, str ):
				_after = await CLIENT.get_message( message.channel, _after )
			if isinstance( _mentions, str ):
				_mentions = discord.utils.find( lambda u:u.mention == _mentions or u.name == _mentions or str( u ) == _mentions or u.nick == _mentions, message.server.members )
			if isinstance( _mentions_channel, str ):
				_mentions_channel = discord.utils.find( lambda c:c.mention == _mentions_channel or c.id == _mentions_channel, message.server.channels )
			if isinstance( _mentions_role, str ):
				_mentions_role = discord.utils.find(
					lambda c:c.mention == _mentions_role or c.name == _mentions_role,
					message.server.roles
				)
			def _check ( msg: discord.Message ) -> bool:
				res = [ ]
				if msg.author == _from or _from is None:
					res.append( True )
				else:
					res.append( False )
				if _contains is None or _contains.lower( ) in msg.content.lower( ):
					res.append( True )
				else:
					res.append( False )
				if _pinned == msg.pinned or _pinned is None:
					res.append( True )
				else:
					res.append( False )
				if bool( msg.embeds ) == _embedded or _embedded is None:
					res.append( True )
				else:
					res.append( False )
				if bool( msg.attachments ) == _attached or _attached is None:
					res.append( True )
				else:
					res.append( False )
				if _mentions in msg.mentions or _mentions is None:
					res.append( True )
				else:
					res.append( False )
				if _mentions_channel in msg.channel_mentions or _mentions_channel is None:
					res.append( True )
				else:
					res.append( False )
				if _mentions_role in msg.role_mentions or _mentions_role is None:
					res.append( True )
				else:
					res.append( False )

				return False not in res
			__num__ = await check_purge( message, _limit, _check=_check )
			tmp = await CLIENT.send_message( message.channel, f"```Doing this will purge {__num__} messages from this channel.\nAre you sure (Y/N)?```" )
			msg_ = await CLIENT.wait_for_message( author=message.author, channel=message.channel )
			await CLIENT.delete_message( msg_ )
			await CLIENT.delete_message( tmp )
			def equals ( msg: str, *args ):
				"""
				Checks for equality.
				:param msg: The object to check with.
				:param args: The objects to check against.
				:return: True or False.
				"""
				for arg in args:
					if msg.lower( ) == arg.lower( ):
						return True
				return False
			if equals( msg_.content, "yes", "yay", "yup", "y" ):
				# noinspection PyUnresolvedReferences
				purged_messages = await CLIENT.purge_from( message.channel, limit=_limit, check=lambda m:_check( m ), before=_before, after=_after )
				tmp = await CLIENT.send_message( message.channel, f"```Purged {len(purged_messages)} messages!```" )
				await sleep( 3 )
				await CLIENT.delete_message( tmp )
				del purged_messages
			else:
				tmp = await CLIENT.send_message( message.channel, f"```Canceled the purge.```" )
				await sleep( 3 )
				await CLIENT.delete_message( tmp )
			del tmp
			del msg_
			del __num__
			del _from
			del _before
			del _after
			del _contains
			del _pinned
			del _embedded
			del _attached
			del _mentions
			del _mentions_channel
			del _mentions_role
		@staticmethod
		async def loose_purge ( message: discord.Message ):
			"""
			Purges 100 messages from the channel.
			:param message: A discord.Message object.
			"""
			# noinspection PyUnresolvedReferences
			purged_messages = await CLIENT.purge_from( message.channel, limit=100 )
			tmp = await CLIENT.send_message( message.channel, f"```Purged 100 messages!```" )
			await sleep( 3 )
			await CLIENT.delete_message( tmp )
			del purged_messages
			del tmp
		@staticmethod
		async def welcome ( message: discord.Message, prefix: str ):
			"""
			Sets the server's welcome message.
			:param message: A discord.Message object.
			:param prefix: The server's prefix.
			"""
			content = message.content.replace( f"{prefix}welcome ", "" )
			if content.startswith( "read(" ):
				content = content.replace( "read(", "" )
				_file_cnt = content[ 0:len( content ) - 1 ]
				_file_path = f"{message.server.id}.txt"
				open( _file_path, 'w' ).write( _file_cnt )
				try:
					DB.write( "Welcomes", { "server":message.server.id, "message":f"read( {_file_path} )" } )
				except Exception:
					pass
				DB.update( "Welcomes", "message", f"read( {_file_path} )", message.server.id )
			else:
				if not content == "None":
					try:
						DB.write( "Welcomes", { "server":message.server.id, "message":content } )
					except Exception:
						pass
					DB.update( "Welcomes", "message", content, message.server.id )
				else:
					DB.update( "Welcomes", "message", "", message.server.id )
			await CLIENT.send_message( message.channel, "```Welcome message set!```" )
			del content
		@staticmethod
		async def goodbye ( message: discord.Message, prefix: str ):
			"""
			Sets the server's goodbye message.
			:param message: A discord.Message object.
			:param prefix: The server's prefix.
			"""
			content = message.content.replace( f"{prefix}goodbye ", "" )
			DB.write( "Goodbyes", { "server":message.server.id, "message":content } )
			DB.update( "Goodbyes", message.server.id, content, message.server.id )
			await CLIENT.send_message( message.channel, "```Goodbye message set!```" )
			del content
		@staticmethod
		async def show_welcome ( message: discord.Message ):
			"""
			Shows the server's welcome message.
			:param message: A discord.Message object.
			"""
			try:
				await CLIENT.send_message( message.channel, DB.read( "Welcomes", message.server.id ) )
			except Exception:
				await CLIENT.send_message( message.channel, "```No welcome message has been set!```" )
		@staticmethod
		async def show_goodbye ( message: discord.Message ):
			"""
			Shows the server's goodbye message.
			:param message: A discord.Message object.
			"""
			try:
				await CLIENT.send_message( message.channel, DB.read( "Goodbyes", message.server.id ) )
			except Exception:
				await CLIENT.send_message( message.channel, "```No goodbye message has been set!```" )
		@staticmethod
		async def prunes ( message: discord.Message, prefix: str ):
			"""
			Estimates the prunable members.
			:param message:
			:type message:
			:param prefix:
			:type prefix:
			:return:
			:rtype:
			"""
			cont = message.content.replace( f"{prefix}prunes ", "" )
			days = int( cont )
			# noinspection PyUnresolvedReferences
			num = await CLIENT.estimate_pruned_members( message.server, days=days )
			await CLIENT.send_message( message.channel, f"```{num} members will be pruned.```" )
			del cont
			del days
			del num
		@staticmethod
		async def prune ( message: discord.Message, prefix: str ):
			"""
			Prunes the server members.
			:param message: A discord.Message object.
			:param prefix: The server's prefix.
			"""
			days = int( message.content.replace( f"{prefix}prune ", "" ) )
			# noinspection PyUnresolvedReferences
			est = await CLIENT.estimate_pruned_members( message.server, days=days )
			await CLIENT.send_message( message.channel, f"```Are you sure you want to prune {est} members (y/n)?```" )
			msg = await CLIENT.wait_for_message( author=message.author, channel=message.channel )
			if msg.content.lower( ) == "y":
				# noinspection PyUnresolvedReferences
				pruned_members = await CLIENT.prune_members( message.server, days=days )
				await CLIENT.send_message( message.channel, f"```{pruned_members} members removed.```" )
				del pruned_members
			else:
				await CLIENT.send_message( message.channel, f"```Canceled the prune.```" )
			del days
		@staticmethod
		async def kick ( message: discord.Message, admin_role: discord.Role ):
			"""
			Kicks a user. Cannot kick admins.
			:param message: A discord.Message object.
			:param admin_role: The bot's admin role.
			"""
			for user in message.mentions:
				if admin_role not in user.roles:
					await CLIENT.kick( user )
					await CLIENT.send_message( message.channel, f"{user} has been kicked!" )
				else:
					await CLIENT.send_message( message.channel, "You cannot kick bot admins!" )
		@staticmethod
		async def ban ( message: discord.Message, admin_role: discord.Role ):
			"""
			Bans a user. Cannot ban admins.
			:param message: A discord.Message object.
			:param admin_role: The bot's admin role.
			"""
			for item in message.mentions:
				if admin_role not in item.roles:
					await CLIENT.ban( item )
					await CLIENT.send_message( message.channel, f"{item} has been banned." )
				else:
					await CLIENT.send_message( message.channel, f"You cannot ban bot admins!" )
		@staticmethod
		async def join_role ( message: discord.Message, prefix: str ):
			"""
			Sets the join role for the server.
			:param message: A discord.Message object.
			:param prefix: The server's prefix.
			"""
			cnt = message.content.replace( f"{prefix}joinrole ", "" )
			role = discord.utils.find( lambda r:r.name == cnt or r.id == cnt or r.mention == cnt, message.server.roles )
			try:
				JOIN_ROLES[ message.server.id ] = role.id
			except Exception:
				JOIN_ROLES[ message.server.id ] = "None"
			await CLIENT.send_message( message.channel, f"```Set the join role to {role}.```" )
		@staticmethod
		async def defaultchannel ( message: discord.Message ):
			"""
			Sets the default log channel.
			:param message: A discord.Message object.
			"""
			channel = message.channel_mentions[ 0 ]
			DEFAULT_CHANNEL[ message.server.id ] = channel.id
			await CLIENT.send_message( message.channel, f"Default channel set to #{channel}." )
			del channel
		@staticmethod
		async def get_defaultchannel ( message: discord.Message ):
			"""
			Gets the default channel for logs.
			:param message: A discord.Message object.
			"""
			await CLIENT.send_message( message.channel, f"Default channel is #{CLIENT.get_channel(DEFAULT_CHANNEL[message.server.id])}" )
	class Owner:
		"""
		For the developer only!
		"""
		@staticmethod
		async def exit ( ):
			"""
			Closes the bot.
			"""
			global EXITING
			EXITING = True
			await CLIENT.logout( )
		@staticmethod
		async def info ( message ):
			"""
			Sends stats on LogBot.
			:param message: A discord.Message object.
			"""
			_channels = list( CLIENT.get_all_channels( ) )
			_members = list( CLIENT.get_all_members( ) )
			_servers = list( CLIENT.servers )
			_messages = list( CLIENT.messages )
			_users = [ ]
			uapp = _users.append
			for mem in _members:
				if mem.id not in _users:
					uapp( mem.id )
			time_t = 0.0
			for time in TIMES:
				time_t += time
			print( time_t )
			try:
				time_t /= len( TIMES )
			except Exception:
				time_t = 0.0
			logbot_process = psutil.Process( os.getpid( ) )
			random_access_memory = round( logbot_process.memory_info( )[ 0 ] / float( 2 ** 20 ), 1 )
			current_time = datetime.now( )
			time_t = decimal.Decimal( time_t )
			embed_obj = discord.Embed( name="LogBot Information", description="Information on this running instance of LogBot.", colour=discord.Colour.gold( ) ) \
				.add_field( name="Visible Channels", value=str( len( _channels ) ) ) \
				.add_field( name="Visible Members", value=str( len( _members ) ) ) \
				.add_field( name="Servers", value=str( len( _servers ) ) ) \
				.add_field( name="Messages", value=str( len( _messages ) ) ) \
				.add_field( name="RAM Usage (MB)", value=str( random_access_memory ) + "MB" ) \
				.add_field( name="Average Response Time", value=f"{time_t:1.5} seconds" ) \
				.add_field( name="Discord Version", value=discord.__version__ ) \
				.add_field( name="LogBot Version", value=VERSION ) \
				.add_field( name="Online For", value=str( (current_time - BOOTUP_TIME) ).split( "." )[ 0 ].replace( ":", "h ", 1 ).replace( ":", "m ", 1 ) + "s" ) \
				.add_field( name="Total Users", value=str( len( _users ) ) )
			await CLIENT.send_message( message.channel, "My Information:", embed=embed_obj )
			del _channels
			del _members
			del _servers
			del _messages
			del time_t
			del logbot_process
			del random_access_memory
			del current_time
			del embed_obj
		@staticmethod
		async def refresh ( ):
			"""
			Refreshes the bot.
			"""
			global ICON
			os.system( "cls" )
			print( f"{Fore.MAGENTA}Signed in and waiting...\nRunning version: LogBot Version {VERSION}{Fore.RESET}" )
			await CLIENT.change_presence( game=None, status=discord.Status.online )
			ICON = Qt.QIcon( SELECTED_IMAGE )
			STI.setIcon( ICON )
	class DM:
		"""
		Private channel commands only!
		"""
		@staticmethod
		async def info ( message: discord.Message ):
			"""
			Shows some stats on LogBot.
			:param message: A discord.Message object.
			"""
			_channels = list( CLIENT.get_all_channels( ) )
			_members = list( CLIENT.get_all_members( ) )
			_servers = list( CLIENT.servers )
			_messages = list( CLIENT.messages )
			time_t = 0.0
			for time in TIMES:
				time_t += time
			print( time_t )
			try:
				time_t /= len( TIMES )
			except Exception:
				time_t = 0.0
			logbot_process = psutil.Process( os.getpid( ) )
			random_access_memory = round( logbot_process.memory_info( )[ 0 ] / float( 2 ** 20 ), 1 )
			current_time = datetime.now( )
			time_t = decimal.Decimal( time_t )
			# <editor-fold desc="Embed">
			embed_obj = discord.Embed( name="LogBot Information", description="Information on this running instance of LogBot.", colour=discord.Colour.gold( ) )
			embed_obj.add_field( name="Visible Channels", value=str( len( _channels ) ) )
			embed_obj.add_field( name="Visible Members", value=str( len( _members ) ) )
			embed_obj.add_field( name="Servers", value=str( len( _servers ) ) )
			embed_obj.add_field( name="Messages", value=str( len( _messages ) ) )
			embed_obj.add_field( name="RAM Usage (MB)", value=str( random_access_memory ) + "MB" )
			embed_obj.add_field( name="Average Response Time", value=f"{time_t:1.5} seconds" )
			embed_obj.add_field( name="Discord Version", value=discord.__version__ )
			embed_obj.add_field( name="LogBot Version", value=VERSION )
			embed_obj.add_field( name="Online For", value=str( (current_time - BOOTUP_TIME) ).split( "." )[ 0 ].replace( ":", "h ", 1 ).replace( ":", "m ", 1 ) + "s" )
			await CLIENT.send_message( message.channel, "My Information:", embed=embed_obj )
			# </editor-fold>
			del embed_obj
			del time_t
			del current_time
			del random_access_memory
			del logbot_process
			del _channels
			del _messages
			del _members
			del _servers
		@staticmethod
		async def planned ( message: discord.Message ):
			"""
			Shows a list of planned features for LogBot.
			:param message: A discord.Message object.
			"""
			tmp = '\n'.join( PLANNED )
			await CLIENT.send_message( message.channel, f"```Coming Soon:\n{tmp}```" )
			del tmp
		@staticmethod
		async def translate ( message: discord.Message ):
			"""
			Translates text in one language to another language.
			:param message: A discord.Message object.
			"""
			content = message.content.replace( f"$translate ", "", 1 ).split( "|" )
			tmp = translate.Translator( from_lang=content[ 0 ], to_lang=content[ 1 ] ).translate( content[ 2 ] )
			await CLIENT.send_message( message.channel, format_message( tmp ) )
			del content
			del tmp
		@staticmethod
		async def translate_get ( message: discord.Message ):
			"""
			Gets a list of translation codes for languages.
			:param message: A discord.Message object.
			"""
			lang_reader = open( f"{DISCORD_SETTINGS_PATH}\\languages.txt", 'r' )
			ret = f"```Languages:\n{lang_reader.read()}```"
			await CLIENT.send_message( message.channel, ret )
			lang_reader.close( )
			del lang_reader
			del ret
		@staticmethod
		async def wiki ( message: discord.Message ):
			"""
			Searches Wikipedia for a topic.
			:param message: A discord.Message object.
			"""
			content = message.content.replace( f"$wiki ", "" )
			await CLIENT.send_typing( message.channel )
			try:
				info = wikipedia.summary( content )
			except Exception:
				search = wikipedia.search( content )
				search_str = '\n'.join( [ item for item in search ] )
				await CLIENT.send_message( message.channel, f"```I found these results:\nSearched Item: {search_str}```" )
				msg = await CLIENT.wait_for_message( author=message.author )
				info = wikipedia.summary( msg.content )
				del msg
				del search
				del search_str
			for item in format_message( info ):
				await CLIENT.send_message( message.channel, item )
			del info
			del content
		@staticmethod
		async def updates ( message: discord.Message ):
			"""
			Shows the most recent updates within the bot.
			:param message: A discord.Message object.
			"""
			tmp = '\n'.join( WHATS_NEW )
			await CLIENT.send_message( message.channel, f"```Updates:\n{tmp}```" )
			del tmp
		@staticmethod
		async def refresh ( ):
			"""
			Refreshes the bot.
			"""
			global ICON
			os.system( "cls" )
			print( f"{Fore.MAGENTA}Signed in and waiting...\nRunning version: LogBot Version {VERSION}{Fore.RESET}" )
			ICON = Qt.QIcon( SELECTED_IMAGE )
			STI.setIcon( ICON )
		@staticmethod
		async def exit ( ):
			"""
			Closes the bot.
			"""
			await CLIENT.logout( )
		@staticmethod
		async def update ( message: discord.Message ):
			"""
			Updates the bot.
			:param message: A discord.Message object.
			"""
			msg = await CLIENT.send_message( message.channel, "```Updating...```" )
			print( f"{Fore.LIGHTCYAN_EX}Updating...{Fore.RESET}" )
			await CLIENT.close( )
			update( msg.id, message.channel.id )
		@staticmethod
		async def suggest ( message: discord.Message ):
			"""
			Suggests something for the dev to add.
			:param message: A discord.Message object.
			"""
			suggestion = message.content \
				.replace( f"$suggest ", "", 1 ) \
				.replace( "`", "\\`" ) \
				.replace( "```", "\\```" )
			# <editor-fold desc="WRITER: suggestions">
			writer = open( SUGGESTIONS_PATH, 'a' )
			writer.write( f"\n[{message.author}] {suggestion}" )
			writer.close( )
			# </editor-fold>
			await CLIENT.send_message( message.channel, "```Thank you for your suggestion.```" )
			print( f"{Fore.YELLOW}{message.author} gave you a suggestion.{Fore.RESET}" )
		@staticmethod
		async def suggestions ( message: discord.Message ):
			"""
			Sends the suggestions list.
			:param message: A discord.Message object.
			"""
			# <editor-fold desc="READER: suggestions">
			s_reader = open( SUGGESTIONS_PATH, 'r' )
			ret = f"Suggestions:{s_reader.read()}"
			s_reader.close( )
			# </editor-fold>
			for item in format_message( ret ):
				await CLIENT.send_message( message.channel, item )
			del ret
			del s_reader
		@staticmethod
		async def query ( message: discord.Message ):
			"""
			Asks Wolfram|Alpha a question.
			:param message: A discord.Message object.
			"""
			try:
				content = message.content.replace( f"$query ", "" )
				await CLIENT.send_typing( message.channel )
				res = WCLIENT.query( content )
				ret = ""
				for pod in res.pods:
					for item in pod.texts:
						ret += f"{pod.title}: {item}\n"
				ret += "Powered by Wolfram|Alpha"
				for msg in format_message( ret ):
					await CLIENT.send_message( message.channel, msg )
				del ret
				del res
				del content
			except Exception:
				await CLIENT.send_message( message.channel, "```We couldn't get that information.```" )
				print( traceback.format_exc( ) )
		@staticmethod
		async def dict ( message: discord.Message ):
			"""
			Searches for a word in a dictionary.
			:param message: A discord.Message object.
			"""
			content = message.content.split( " " )
			content.remove( content[ 0 ] )
			if content[ 0 ].startswith( "def" ):
				tmp = PYDICT.meaning( content[ 1 ] )
				ret = str
				for key, value in tmp.items( ):
					ret += f"{key}\n"
					for entry in value:
						ret += f"{entry}\n"
					ret += "\n"
				await CLIENT.send_message( message.channel, f"```{ret}```" )
				del tmp
				del ret
			elif content[ 0 ].startswith( "ant" ):
				tmp = PYDICT.antonym( content[ 1 ] )
				ret = ""
				for entry in tmp:
					ret += f"{entry}\n"
				await CLIENT.send_message( message.channel, f"```{ret}```" )
				del tmp
				del ret
			elif content[ 0 ].startswith( "syn" ):
				tmp = PYDICT.synonym( content[ 1 ] )
				ret = str
				for entry in tmp:
					ret += f"{entry}\n"
				await CLIENT.send_message( message.channel, f"```{ret}```" )
				del tmp
				del ret
			del content
		@staticmethod
		async def gif ( message: discord.Message, prefix: str ):
			"""
			Sends a GIF image.
			:param message: A discord.Message object.
			:param prefix: The server's prefix.
			"""
			tag = message.content.replace( f"{prefix}gif", "" )
			image = GC.gifs_random_get( giphy_key, tag=tag ).data
			embed_obj = discord.Embed( ).set_image( url=image.image_url )
			await CLIENT.send_message( message.channel, "", embed=embed_obj )
			del embed_obj
			del image
			del tag
		@staticmethod
		async def cmd_sf ( message: discord.Message ):
			"""
			SF command.
			:param message: A discord.Message object.
			"""
			num = message.content.replace( f"$sf ", "" )
			org_num = num
			dot_found = False
			while num[ 0 ] == "0" or num[ 0 ] == ".":
				if num[ 0 ] == ".":
					dot_found = True
				num = num[ 1: ]
			if "." in num:
				sfs = len( num ) - 1
			elif dot_found:
				sfs = len( num )
			else:
				while num[ -1 ] == "0":
					num = num[ 0:len( num ) - 1 ]
				sfs = len( num )
			await CLIENT.send_message( message.channel, f"```{org_num} has {sfs} significant figures ({num})!```" )
		@staticmethod
		async def eightball ( message: discord.Message ):
			"""
			Eigtball command.
			:param message: A discord.Message object.
			"""
			if "not" in message.content.lower( ):
				if "kill" in message.content.lower( ) or "bomb" in message.content.lower( ) or "suicide" in message.content.lower( ) or "murder" in message.content.lower( ):
					await CLIENT.send_message( message.channel, f"```{random.choice(EIGHTBALL_POS)}```" )
				else:
					choice = random.choice( [ "+", "-", "0" ] )
					if choice == "+":
						await CLIENT.send_message( message.channel, f"```{random.choice(EIGHTBALL_POS)}```" )
					elif choice == "-":
						await CLIENT.send_message( message.channel, f"```{random.choice(EIGHTBALL_NEG)}```" )
					else:
						await CLIENT.send_message( message.channel, f"```{random.choice(EIGHTBALL_NEU)}```" )
			else:
				if "kill" in message.content.lower( ) or "bomb" in message.content.lower( ) or "suicide" in message.content.lower( ) or "murder" in message.content.lower( ):
					await CLIENT.send_message( message.channel, f"```{random.choice(EIGHTBALL_NEG)}```" )
				else:
					choice = random.choice( [ "+", "-", "0" ] )
					if choice == "+":
						await CLIENT.send_message( message.channel, f"```{random.choice(EIGHTBALL_POS)}```" )
					elif choice == "-":
						await CLIENT.send_message( message.channel, f"```{random.choice(EIGHTBALL_NEG)}```" )
					else:
						await CLIENT.send_message( message.channel, f"```{random.choice(EIGHTBALL_NEU)}```" )

@CLIENT.event
async def send_no_perm ( message: discord.Message ):
	"""
	Sends a message telling a user that he/she does not have the necessary permissions to use a command.
	:param message: The message object from on_message.
	"""
	await CLIENT.send_message( message.channel, "```You do not have permission to use this command.```" )
	print( f"{Fore.LIGHTGREEN_EX}{message.author} attempted to use a command.{Fore.RESET}" )

# <editor-fold desc="Message Updates">
# noinspection PyShadowingNames
@CLIENT.event
async def on_message ( message: discord.Message ):
	"""
	Called when the bot receives a message.
	:param message: A discord.Message object.
	"""
	global DEFAULT_CHANNEL
	try:
		try:
			if DEFAULT_CHANNEL.get( message.server.id ) is None:
				DEFAULT_CHANNEL[ message.server.id ] = message.server.default_channel.id
		except Exception:
			pass

		muted_role = discord.utils.find( lambda r:r.name == "LogBot Muted", message.server.roles )

		if muted_role in message.author.roles and not message.author == message.server.owner:
			await CLIENT.delete_message( message )

		msgcont = message.content if is_ascii( message.content ) else u"{}".format( message.content )
		# noinspection PyShadowingNames
		def startswith ( *msgs: str, val: str = message.content, modifier: str = "" ) -> bool:
			"""
			Checks if `val` starts with any string in `msg`.
			:param msgs: Several str type parameters.
			:param val: The string to compare msg to.
			:param modifier: A special operation to perform on val. Can be "lower", "upper", or "capitalize"
			:return: True if a value in msg is at the beginning of val, False if not.
			"""
			if modifier == "lower":
				val = val.lower( )
			if modifier == "upper":
				val = val.upper( )
			if modifier == "capitalize":
				val = val.capitalize( )
			# noinspection PyShadowingNames
			for msg in msgs:
				if val.startswith( msg ):
					return True
			return False
		if not message.channel.is_private and muted_role not in message.author.roles:
			admin_role = discord.utils.find( lambda r:r.name == "LogBot Admin", message.server.roles )

			await Commands.Admin.filter( message, admin_role )

			if message.server.id not in list( DISABLES.keys( ) ):
				DISABLES[ message.server.id ] = {
					"exclude"       :False,
					"excludechannel":False,
					"includechannel":False,
					"mark"          :False,
					"showlist"      :False,
					"showmarks"     :False,
					"channel"       :False,
					"cmd"           :False,
					"query"         :False,
					"wiki"          :False,
					"say"           :False,
					"welcome"       :False,
					"goodbye"       :False,
					"decide"        :False,
					"prune"         :False,
					"purge"         :False,
					"user"          :False,
					"translate"     :False,
					"urban"         :False,
					"roll"          :False,
					"server"        :False,
					"convert"       :False,
					"dict"          :False,
					"permissions"   :False,
					"gif"           :False
				}
			if not isinstance( DISABLES[ message.server.id ], dict ):
				DISABLES[ message.server.id ] = {
					"exclude"       :False,
					"excludechannel":False,
					"includechannel":False,
					"mark"          :False,
					"showlist"      :False,
					"showmarks"     :False,
					"channel"       :False,
					"cmd"           :False,
					"query"         :False,
					"wiki"          :False,
					"say"           :False,
					"welcome"       :False,
					"goodbye"       :False,
					"decide"        :False,
					"prune"         :False,
					"purge"         :False,
					"user"          :False,
					"translate"     :False,
					"urban"         :False,
					"roll"          :False,
					"server"        :False,
					"convert"       :False,
					"dict"          :False,
					"permissions"   :False,
					"gif"           :False
				}
			if message.server.id not in list( PLAYLISTS.keys( ) ):
				PLAYLISTS[ message.server.id ] = { }

			sort( )

			# save( message.server.id )
			time = format_time( message.timestamp )

			try:
				prefix = DB.read( "Prefixes", message.server.id )
			except Exception:
				prefix = "$"
				traceback.format_exc( )
				DB.write( "Prefixes", { "server":message.server.id, "prefix":"$" } )

			if startswith( prefix ):
				if startswith( f"{prefix}exclude ", f"{prefix}ex " ):
					if (admin_role in message.author.roles and not DISABLES[ message.server.id ].get( "exclude" ) is True) or message.author.id == owner_id:
						await Commands.Admin.exclude( message, time )
					elif DISABLES[ message.server.id ][ "exclude" ]:
						await CLIENT.send_message( message.channel, "```That command has been disabled!```" )
					else:
						await send_no_perm( message )
				elif startswith( f"{prefix}excludechannel ", f"{prefix}exc " ):
					if (admin_role in message.author.roles and not DISABLES[ message.server.id ].get( "excludechannel" ) is True) or message.author.id == owner_id:
						await Commands.Admin.excludechannel( message )
					elif DISABLES[ message.server.id ][ "excludechannel" ]:
						await CLIENT.send_message( message.channel, "```That command has been disabled!```" )
					else:
						await send_no_perm( message )
				elif startswith( f"{prefix}includechannel ", f"{prefix}inc " ):
					if (admin_role in message.author.roles and not DISABLES[ message.server.id ].get( "includechannel" ) is True) or message.author.id == owner_id:
						await Commands.Admin.includechannel( message )
					elif DISABLES[ message.server.id ][ "includechannel" ]:
						await CLIENT.send_message( message.channel, "```That command has been disabled!```" )
					else:
						await send_no_perm( message )
				elif startswith( f"{prefix}mark " ):
					if (admin_role in message.author.roles and not DISABLES[ message.server.id ].get( "mark" ) is True) or message.author.id == owner_id:
						await Commands.Admin.mark( message, prefix )
					elif DISABLES[ message.server.id ][ "mark" ]:
						await CLIENT.send_message( message.channel, "```That command has been disabled!```" )
					else:
						await send_no_perm( message )
				elif startswith( f"{prefix}admin " ):
					if admin_role in message.author.roles or message.author.id == owner_id:
						await Commands.Admin.admin( message, admin_role, prefix )
					else:
						await send_no_perm( message )
				elif startswith( f"{prefix}showlist" ):
					if not DISABLES[ message.server.id ].get( "showlist" ) is True or message.author.id == owner_id:
						await Commands.Member.showlist( message )
					elif DISABLES[ message.server.id ][ "showlist" ]:
						await CLIENT.send_message( message.channel, "```That command has been disabled!```" )
					else:
						await send_no_perm( message )
				elif startswith( f"{prefix}showmarks" ):
					if not DISABLES[ message.server.id ].get( "showmarks" ) is True or message.author.id == owner_id:
						await Commands.Member.showmarks( message )
					elif DISABLES[ message.server.id ][ "showmarks" ]:
						await CLIENT.send_message( message.channel, "```That command has been disabled!```" )
					else:
						await send_no_perm( message )
				elif startswith( f"{prefix}version" ):
					await CLIENT.send_message( message.channel, f"```LogBot Version {VERSION}```" )
				elif startswith( f"{prefix}channel " ):
					if (admin_role in message.author.roles and not DISABLES[ message.server.id ].get( "channel" ) is True) or message.author.id == owner_id:
						await Commands.Admin.channel( message, prefix )
					elif DISABLES[ message.server.id ][ "channel" ]:
						await CLIENT.send_message( message.channel, "```That command has been disabled!```" )
					else:
						await send_no_perm( message )
				elif startswith( f"{prefix}updates" ):
					await Commands.Member.updates( message )
				elif startswith( f"{prefix}say" ):
					if (admin_role in message.author.roles and not DISABLES[ message.server.id ].get( "say" ) is True) or message.author.id == owner_id:
						await Commands.Admin.say( message, prefix )
					elif DISABLES[ message.server.id ][ "say" ]:
						await CLIENT.send_message( message.channel, "```That command has been disabled!```" )
					else:
						await send_no_perm( message )
				elif startswith( f"{prefix}planned" ):
					await Commands.Member.planned( message )
				# elif startswith( f"{prefix}cmd " ):
				# 	if not disables[message.server.id].get( "cmd" ) is True or message.author.id == owner_id:
				# 		await Commands.Member.cmd( message )
				# 	elif disables[ message.server.id ][ "cmd" ]:
				# 		await await client.send_message( message.channel, "```That command has been disabled!```" )
				# 	else:
				# 		await sendNoPerm( message )
				elif startswith( f"{prefix}query " ):
					if not DISABLES[ message.server.id ].get( "query" ) is True or message.author.id == owner_id:
						await Commands.Member.query( message, prefix )
					elif DISABLES[ message.server.id ][ "query" ]:
						await CLIENT.send_message( message.channel, "```That command has been disabled!```" )
					else:
						await send_no_perm( message )
				elif startswith( f"{prefix}wiki " ):
					if not DISABLES[ message.server.id ].get( "wiki" ) is True or message.author.id == owner_id:
						await Commands.Member.wiki( message, prefix )
					elif DISABLES[ message.server.id ][ "wiki" ]:
						await CLIENT.send_message( message.channel, "```That command has been disabled!```" )
					else:
						await send_no_perm( message )
				elif startswith( f"{prefix}disable " ):
					if admin_role in message.author.roles or message.author.id == owner_id:
						await Commands.Admin.disable( message, prefix )
					else:
						await send_no_perm( message )
				elif startswith( f"{prefix}enable " ):
					if admin_role in message.author.roles or message.author.id == owner_id:
						await Commands.Admin.enable( message, prefix )
					else:
						await send_no_perm( message )
				elif startswith( f"{prefix}suggest " ):
					await Commands.Member.suggest( message, prefix )
				elif startswith( f"{prefix}decide " ):
					if not DISABLES[ message.server.id ].get( "decide" ) is True or message.author.id == owner_id:
						await Commands.Member.decide( message, prefix )
					elif DISABLES[ message.server.id ][ "decide" ]:
						await CLIENT.send_message( message.channel, "```That command has been disabled!```" )
					else:
						await send_no_perm( message )
				elif startswith( f"{prefix}disables" ):
					await Commands.Member.disables( message, prefix )
				elif startswith( f"{prefix}welcome " ):
					if (admin_role in message.author.roles and not DISABLES[ message.server.id ].get( "welcome" ) is True) or message.author.id == owner_id:
						await Commands.Admin.welcome( message, prefix )
					elif DISABLES[ message.server.id ][ "welcome" ]:
						await CLIENT.send_message( message.channel, "```That command has been disabled!```" )
					else:
						await send_no_perm( message )
				elif startswith( f"{prefix}goodbye " ):
					if (admin_role in message.author.roles and not DISABLES[ message.server.id ].get( "goodbye" ) is True) or message.author.id == owner_id:
						await Commands.Admin.goodbye( message, prefix )
					elif DISABLES[ message.server.id ][ "goodbye" ]:
						await CLIENT.send_message( message.channel, "```That command has been disabled!```" )
					else:
						await send_no_perm( message )
				elif startswith( f"{prefix}welcome" ):
					if (admin_role in message.author.roles and not DISABLES[ message.server.id ].get( "welcome" ) is True) or message.author.id == owner_id:
						await Commands.Admin.show_welcome( message )
					elif DISABLES[ message.server.id ][ "welcome" ]:
						await CLIENT.send_message( message.channel, "```That command has been disabled!```" )
					else:
						await send_no_perm( message )
				elif startswith( f"{prefix}goodbye" ):
					if (admin_role in message.author.roles and not DISABLES[ message.server.id ].get( "goodbye" ) is True) or message.author.id == owner_id:
						await Commands.Admin.show_goodbye( message )
					elif DISABLES[ message.server.id ][ "goodbye" ]:
						await CLIENT.send_message( message.channel, "```That command has been disabled!```" )
					else:
						await send_no_perm( message )
				elif startswith( f"{prefix}prunes " ):
					if (admin_role in message.author.roles and not DISABLES[ message.server.id ].get( "prune" ) is True) or message.author.id == owner_id:
						await Commands.Admin.prunes( message, prefix )
					elif DISABLES[ message.server.id ][ "prune" ]:
						await CLIENT.send_message( message.channel, "```That command has been disabled!```" )
					else:
						await send_no_perm( message )
				elif startswith( f"{prefix}prune " ):
					if (admin_role in message.author.roles and not DISABLES[ message.server.id ].get( "prune" ) is True) or message.author.id == owner_id:
						await Commands.Admin.prune( message, prefix )
					elif DISABLES[ message.server.id ][ "prune" ]:
						await CLIENT.send_message( message.channel, "```That command has been disabled!```" )
					else:
						await send_no_perm( message )
				elif startswith( f"{prefix}user:" ):
					if not DISABLES[ message.server.id ].get( "user" ) is True or message.author.id == owner_id:
						await Commands.Member.user_restrict( message, prefix )
					elif DISABLES[ message.server.id ][ "user" ]:
						await CLIENT.send_message( message.channel, "```That command has been disabled!```" )
				elif startswith( f"{prefix}user" ):
					if not DISABLES[ message.server.id ].get( "user" ) is True or message.author.id == owner_id:
						await Commands.Member.user( message, prefix )
					elif DISABLES[ message.server.id ][ "user" ]:
						await CLIENT.send_message( message.channel, "```That command has been disabled!```" )
					else:
						await send_no_perm( message )
				elif startswith( f"{prefix}invite" ):
					await CLIENT.send_message( message.channel, "https://discordapp.com/oauth2/authorize?client_id=255379748828610561&scope=bot&permissions=268696670" )
				elif startswith( f"{prefix}purge " ):
					if (admin_role in message.author.roles and not DISABLES[ message.server.id ].get( "purge" ) is True) or message.author.id == owner_id:
						tmp = message.content.replace( f"{prefix}purge ", "" )
						switches = PURGEPARSER.parse( tmp )
						await Commands.Admin.purge( message, int( switches.get( "limit" ) ) + 1 if not switches.get( "limit" ) is None else 100, switches )
					elif DISABLES[ message.server.id ][ "purge" ]:
						await CLIENT.send_message( message.channel, "```That command has been disabled!```" )
					else:
						await send_no_perm( message )
				elif startswith( f"{prefix}purge" ):
					if (admin_role in message.author.roles and not DISABLES[ message.server.id ].get( "purge" ) is True) or message.author.id == owner_id:
						await Commands.Admin.loose_purge( message )
					elif DISABLES[ message.server.id ][ "purge" ]:
						await CLIENT.send_message( message.channel, "```That command has been disabled!```" )
					else:
						await send_no_perm( message )
				elif startswith( f"{prefix}kick " ):
					if admin_role in message.author.roles or message.author.id == owner_id:
						await Commands.Admin.kick( message, admin_role )
					else:
						await send_no_perm( message )
				elif startswith( f"{prefix}ban " ):
					if admin_role in message.author.roles or message.author.id == owner_id:
						await Commands.Admin.ban( message, admin_role )
					else:
						await send_no_perm( message )
				elif startswith( f"{prefix}permissions" ):
					if not DISABLES[ message.server.id ].get( "permissions" ) is True:
						await Commands.Member.user_permissions( message, prefix )
					else:
						await CLIENT.send_message( message.channel, "```That command has been disabled!```" )
				elif startswith( f"{prefix}translate.get" ):
					if not DISABLES[ message.server.id ].get( "translate" ) is True or message.author.id == owner_id:
						await Commands.Member.translate_get( message )
					elif DISABLES[ message.server.id ][ "translate" ]:
						await CLIENT.send_message( message.channel, "```That command has been disabled!```" )
					else:
						await send_no_perm( message )
				elif startswith( f"{prefix}translate " ):
					if not DISABLES[ message.server.id ].get( "translate" ) is True or message.author.id == owner_id:
						await Commands.Member.translate( message, prefix )
					elif DISABLES[ message.server.id ][ "translate" ]:
						await CLIENT.send_message( message.channel, "```That command has been disabled!```" )
					else:
						await send_no_perm( message )
				elif startswith( f"{prefix}dm" ):
					await CLIENT.send_message( message.author, f"Welcome, {message.author.name}" )
				elif startswith( f"{prefix}fetch " ):
					if admin_role in message.author.roles or message.author.id == owner_id:
						_file = f"{DISCORD_LOGS_PATH}\\{message.server.name}\\{message.content.replace(f'{prefix}fetch ', '')}"
						if not _file.endswith( '.txt' ):
							_file += ".txt"
						await CLIENT.send_file( message.channel, f"{_file}" )
					else:
						await send_no_perm( message )
				elif startswith( f"{prefix}refresh" ):
					if message.author.id == owner_id:
						await Commands.Owner.refresh( )
					else:
						await send_no_perm( message )
				elif startswith( f"{prefix}dict " ):
					if not DISABLES[ message.server.id ].get( "dict" ) is True:
						await Commands.Member.dict( message, prefix )
					else:
						await CLIENT.send_message( message.channel, "```That command has been disabled!```" )
				elif startswith( f"{prefix}setup" ):
					if message.author.id == message.server.owner.id or message.author.id == owner_id:
						await Commands.Admin.setup( message, admin_role )
					else:
						await send_no_perm( message )
				elif startswith( f"{prefix}server" ):
					if not DISABLES[ message.server.id ].get( "server" ) is True:
						await Commands.Member.server( message )
					else:
						await CLIENT.send_message( message.channel, "```That command has been disabled!```" )
				elif startswith( f"{prefix}convert " ):
					if not DISABLES[ message.server.id ].get( "convert" ) is True:
						await Commands.Member.convert( message, prefix )
					else:
						await CLIENT.send_message( message.channel, "```That command has been disabled!```" )
				elif startswith( f"{prefix}mute " ):
					if admin_role in message.author.roles or message.author.id == owner_id:
						await Commands.Admin.mute( message, muted_role )
					else:
						await send_no_perm( message )
				elif startswith( f"{prefix}unmute " ):
					if admin_role in message.author.roles or message.author.id == owner_id:
						await Commands.Admin.unmute( message, muted_role )
					else:
						await send_no_perm( message )
				elif startswith( f"{prefix}mutes" ):
					await Commands.Member.mutes( message, muted_role )
				elif startswith( f"{prefix}ping" ):
					await Commands.Member.ping( message )
				elif startswith( f"{prefix}clear" ):
					if admin_role in message.author.roles or message.author.id == owner_id:
						messages = list( CLIENT.messages )
						mtd = [ m if m.channel == message.channel else None for m in messages ]
						remove = mtd.remove
						while None in mtd:
							remove( None )
						for msg in mtd:
							# print(f"{m.author} ~ {m.content} ~ {len(m.attachments)}")
							await CLIENT.delete_message( msg )
				elif startswith( f"{prefix}hq" ):
					await CLIENT.send_message( message.channel, hq_link )
				elif startswith( f"{prefix}git" ):
					await CLIENT.send_message( message.channel, git_link )
				elif startswith( f"{prefix}joinrole " ):
					if (admin_role in message.author.roles and not DISABLES[ message.server.id ].get( "welcome" ) is True) or message.author.id == owner_id:
						await Commands.Admin.join_role( message, prefix )
					elif DISABLES[ message.server.id ][ "welcome" ]:
						await CLIENT.send_message( message.channel, "```That command has been disabled!```" )
					else: send_no_perm( message )
				elif startswith( f"{prefix}joinrole" ):
					if not DISABLES[ message.server.id ].get( "welcome" ) is True or message.author.id == owner_id:
						role = discord.utils.find( lambda r:r.id == JOIN_ROLES[ message.server.id ], message.server.roles )
						await CLIENT.send_message( message.channel, f"Join Role for {message.server.name}: {role}" )
					elif DISABLES[ message.server.id ][ "welcome" ]:
						await CLIENT.send_message( message.channel, "```That command has been disabled!```" )
					else: send_no_perm( message )
				elif startswith( f"{prefix}logchannel " ):
					if admin_role in message.author.roles:
						cmentions = message.channel_mentions
						if cmentions:
							channel_obj = cmentions[ 0 ].id
							PARSER[ message.server.id ][ "logchannel" ] = channel_obj
							await CLIENT.send_message( message.channel, f"```Set the log channel to {cmentions[0]}```" )
							del channel_obj
						else:
							PARSER[ message.server.id ][ "logchannel" ] = "None"
							await CLIENT.send_message( message.channel, f"```Set the log channel to None```" )
						del cmentions
					else:
						send_no_perm( message )
				elif startswith( f"{prefix}logchannel" ):
					if admin_role in message.author.roles:
						channel_obj = CLIENT.get_channel( PARSER[ message.server.id ][ "logchannel" ] )
						if channel_obj is None:
							await CLIENT.send_message( message.channel, "```There is no log channel.```" )
						else:
							await CLIENT.send_message( message.channel, f"```The log channel is #{channel_obj}.```" )
						del channel_obj
					else:
						send_no_perm( message )
				elif startswith( f"{prefix}roll" ):
					if not DISABLES[ message.server.id ].get( "roll" ) is True:
						await CLIENT.send_message( message.channel, f"You rolled {random.choice(range(1, int(message.content.replace('{prefix}roll ', ''))))}!" )
					else:
						await CLIENT.send_message( message.channel, "```That command has been disabled!```" )
				elif startswith( f"{prefix}channels" ):
					await Commands.Member.channels( message )
				elif startswith( f"{prefix}defaultchannel " ):
					if admin_role in message.author.roles or message.author.id == owner_id:
						await Commands.Admin.defaultchannel( message )
					else:
						send_no_perm( message )
				elif startswith( f"{prefix}defaultchannel" ):
					if admin_role in message.author.roles or message.author.id == owner_id:
						await Commands.Admin.get_defaultchannel( message )
					else:
						send_no_perm( message )
				elif startswith( f"{prefix}simwelcome" ):
					if message.author.id == owner_id:
						await on_member_join( message.author )
				elif startswith( f"{prefix}simgoodbye" ):
					if message.author.id == owner_id:
						await on_member_remove( message.author )
				elif startswith( f"{prefix}changeprefix " ):
					if admin_role in message.author.roles or message.author.id == owner_id:
						await Commands.Admin.changeprefix( message, prefix )
					else:
						send_no_perm( message )
				elif startswith( f"{prefix}prefix" ):
					await CLIENT.send_message( message.channel, f"You guessed it!" )
				elif startswith( f"{prefix}role " ):
					await Commands.Member.role( message, prefix )
				elif startswith( f"{prefix}urban " ):
					if not DISABLES[ message.server.id ].get( "urban" ) is True:
						await Commands.Member.urban( message, prefix )
					else:
						await CLIENT.send_message( message.channel, "```That command has been disabled!```" )
				elif startswith( f"{prefix}files" ):
					if admin_role in message.author.roles or message.author.id == owner_id:
						await Commands.Admin.files( message )
				elif startswith( f"{prefix}gif" ):
					if not DISABLES[ message.server.id ][ "gif" ] or message.author.id == owner_id:
						await Commands.Member.gif( message, prefix )
					else:
						await CLIENT.send_message( message.channel, "```That command has been disabled!```" )
				elif startswith( f"{prefix}sf " ):
					await Commands.Member.significant_figures( message, prefix )
				elif startswith( f"{prefix}spamfilter settings" ):
					if admin_role in message.author.roles:
						await Commands.Admin.filter_settings( message, prefix )
					else:
						send_no_perm( message )
				elif startswith( f"{prefix}8ball " ):
					await Commands.Member.eightball( message )
				elif startswith( f"{prefix}ToS" ):
					await Commands.Member.tos( message )
				elif startswith( f"{prefix}lyrics " ):
					await Commands.Member.lyrics( message, prefix )
				# elif startswith(f"{prefix}yoda "):
				# 	cnt = message.content.replace(f"{prefix}yoda ", "").replace(" ", "+")
				# 	response = unirest.get(f"https://yoda.p.mashape.com/yoda?sentence={cnt}",
				# 		headers={
				# 			"X-Mashape-Key":"RGua7KFPvXmshXY96pU0btMbDbmyp1yIZkpjsnC2za8zQ3OzgV",
				# 			"Accept"       :"text/plain"
				# 		}
				# 	)
				# 	_body = response.raw_body
				# 	print(_body)
			elif startswith( f"$update", "logbot.update" ):
				if message.author.id == owner_id:
					msg = await CLIENT.send_message( message.channel, "```Updating...```" )
					print( f"{Fore.LIGHTCYAN_EX}Updating...{Fore.RESET}" )
					await CLIENT.close( )
					update( msg.id, message.channel.id )
				else:
					await send_no_perm( message )
			elif startswith( "logbot.exit", "$exit" ):
				if message.author.id == owner_id:
					await Commands.Owner.exit( )
				else:
					await send_no_perm( message )
			elif startswith( "logbot.info" ):
				await Commands.Owner.info( message )
			elif startswith( "logbot.refresh" ):
				STI.hide( )
				STI.show( )
			elif startswith( "$prefix" ):
				await CLIENT.send_message( message.channel, f"The prefix is {prefix}" )
			elif startswith( f"mu$playlist " ):
				tmp = message.content.split( " " )
				tmp.remove( tmp[ 0 ] )
				if tmp[ 0 ] == "list":
					tmp.remove( tmp[ 0 ] )
					lines = [ ]
					for playlist in list( PLAYLISTS[ message.server.id ].keys( ) ):
						lines.append( f"{playlist} ({len(PLAYLISTS[message.server.id][playlist])})" )
					if lines:
						await CLIENT.send_message( message.channel, '\n'.join( lines ) )
					else:
						await CLIENT.send_message( message.channel, f"```There are no playlists for this server.```" )
				elif tmp[ 0 ] == "show":
					tmp.remove( tmp[ 0 ] )
					if not PLAYLISTS[ message.server.id ].get( ' '.join( tmp ) ) is None:
						await CLIENT.send_message( message.channel, '\n'.join( PLAYLISTS[ message.server.id ][ ' '.join( tmp ) ] ) )
					else:
						await CLIENT.send_message( message.channel, f"```No playlist with that name exists.```" )
				elif tmp[ 0 ] == "edit":
					tmp.remove( tmp[ 0 ] )
					stuffs = ' '.join( tmp ).split( "||" )
					playlist_name = stuffs[ 0 ]
					new_songs = stuffs[ 1 ].split( "\n" )
					PLAYLISTS[ message.server.id ][ playlist_name ] = new_songs
					await CLIENT.send_message( message.channel, f"```Edited the playlist!```" )
				elif tmp[ 0 ] == "new":
					tmp.remove( tmp[ 0 ] )
					tmp = ' '.join( tmp ).split( "||" )
					playlist_name = tmp[ 0 ]
					songs = tmp[ 1 ]
					PLAYLISTS[ message.server.id ][ playlist_name ] = songs.split( "\n" )
					await CLIENT.send_message( message.channel, f"```Created the playlist!```" )
				elif tmp[ 0 ] == "remove":
					tmp.remove( tmp[ 0 ] )
					tmp = ' '.join( tmp )
					try:
						del PLAYLISTS[ message.server.id ][ tmp ]
						await CLIENT.send_message( message.channel, f"```Deleted the playlist!```" )
					except Exception:
						await CLIENT.send_message( message.channel, f"```No playlist with that name exists.```" )
				writer = open( PLAYLISTS_PATH, 'w' )
				writer.write( str( PLAYLISTS ) )
				writer.close( )
				del writer

			for item in list( CUSTOM_COMMANDS.keys( ) ):
				if startswith( item ):
					await CLIENT.send_message( message.channel, CUSTOM_COMMANDS[ item ] )

			save( message.server.id )

			with open( CHANNEL_SETTINGS_PATH, 'w' ) as configfile:
				CHANNELPARSER.write( configfile )

			try:
				EXCLUDE_CHANNEL_LIST.index( message.channel.id )
			except Exception:
				if not message.content.startswith( f"$exclude " ) and not message.content.startswith( f"$ex " ):
					ret = f"Message Sent: {message.server.name} ~ {message.channel} ~ \"{msgcont}\" ~ {message.author} ~ {time.day}.{time.month}.{time.year} {time.hour}:{time.minute} ~ {message.attachments}"
					send( ret, message.server.name, message.channel.name )
		elif message.channel.is_private:
			if message.content.startswith( "logbot.info" ):
				await Commands.DM.info( message )
			elif message.content.startswith( "$planned" ):
				await Commands.DM.planned( message )
			elif message.content.startswith( "$translate.get" ):
				await Commands.DM.translate_get( message )
			elif message.content.startswith( "$translate " ):
				await Commands.DM.translate( message )
			elif message.content.startswith( "$wiki" ):
				await Commands.DM.wiki( message )
			elif message.content.startswith( "logbot.exit" ):
				if message.author.id == owner_id:
					await Commands.DM.exit( )
				else:
					await send_no_perm( message )
			elif message.content.startswith( "$updates" ):
				await Commands.DM.updates( message )
			elif message.content.startswith( "$refresh" ):
				if message.author.id == owner_id:
					await Commands.DM.refresh( )
			elif message.content.startswith( "$update" ) or message.content.startswith( "logbot.update" ):
				if message.author.id == owner_id:
					await Commands.DM.update( message )
			elif message.content.startswith( "$suggest " ):
				await Commands.DM.suggest( message )
			elif message.content.startswith( "$decide" ):
				content = message.content.split( ' ' )
				content.remove( content[ 0 ] )
				content = ' '.join( content ).split( "|" )
				choice = random.choice( content )
				await CLIENT.send_message( message.channel, f"```I have chosen: {choice}```" )
			elif message.content.startswith( "$invite" ):
				await CLIENT.send_message( message.channel, "https://discordapp.com/oauth2/authorize?client_id=255379748828610561&scope=bot&permissions=2146958463" )
			elif message.content.startswith( "$query " ):
				await Commands.DM.query( message )
			elif message.content.startswith( "$dict " ):
				await Commands.DM.dict( message )

		timestamp = int( (datetime.now( ) - message.timestamp).microseconds ) / 1000000
		TIMES.append( timestamp )
		del timestamp
	except Exception:
		log_error( traceback.format_exc( ) )

# noinspection PyShadowingNames
@CLIENT.event
async def on_message_delete ( message: discord.Message ):
	"""
	Called when a message is deleted.
	:param message: The message.
	"""
	try:
		EXCLUDE_CHANNEL_LIST.index( message.channel.id )
	except Exception:
		current_time = format_time( message.timestamp )
		author_name = str( message.author )
		ret = f"Message Deleted: {message.server.name} ~ {message.channel} ~ \"{message.content}\" was deleted ~ {author_name} ~ {current_time.day}.{current_time.month}.{current_time.year} {current_time.hour}:{current_time.minute} ~ {message.attachments}"
		send( ret, message.server.name, message.channel.name )
		channel_obj = CLIENT.get_channel( PARSER[ message.server.id ][ "logchannel" ] )
		if channel_obj is not None:
			embed_obj = discord.Embed( title="Message Deleted!", description="A message was deleted!", colour=discord.Colour.red( ) ) \
				.add_field( name="Author", value=str( message.author ), inline=False ) \
				.add_field( name="Content", value=message.content, inline=False ) \
				.add_field( name="ID", value=message.id, inline=False ) \
				.add_field( name="Channel", value=str( message.channel ), inline=False ) \
				.set_footer( text=str( current_time ) )
			await CLIENT.send_message( channel_obj, "", embed=embed_obj )

@CLIENT.event
async def on_message_edit ( before: discord.Message, after: discord.Message ):
	"""
	Called when a message is edited.
	:param before: The old message.
	:param after: The new message.
	"""
	try:
		EXCLUDE_CHANNEL_LIST.index( before.channel.id )
	except Exception:
		current_time = format_time( after.timestamp )
		attachments = after.attachments
		ret = f"Message Edited: {after.server.name} ~ {before.channel.name} ~ \"{before.content}\" ~ \"{after.content}\" ~ {attachments} ~ {before.author} ~ {current_time.day}.{current_time.month}.{current_time.year} {current_time.hour}:{current_time.minute}"
		send( ret, after.server.name, after.channel.name )
		channel_obj = CLIENT.get_channel( PARSER[ before.server.id ][ "logchannel" ] )
		if channel_obj is not None and not before.content == after.content:
			embed_obj = discord.Embed( title="Message Edited!", description="A message was edited!", colour=discord.Colour.red( ) ) \
				.add_field( name="Author", value=str( before.author ), inline=False ) \
				.add_field( name="Old Content", value=before.content, inline=False ) \
				.add_field( name="New Content", value=after.content, inline=False ) \
				.add_field( name="ID", value=before.id, inline=False ) \
				.add_field( name="Channel", value=str( before.channel ), inline=False ) \
				.set_footer( text=f"edited on {after.edited_timestamp}" )
			await CLIENT.send_message( channel_obj, "", embed=embed_obj )

# </editor-fold>
# <editor-fold desc="Member Updates">
@CLIENT.event
async def on_member_join ( member: discord.Member ):
	"""
	Called when a member joins.
	:param member: The new member.
	"""
	current_time = datetime.now( )
	ret = f"Member Joined: {member.server.name} ~ {member} joined ~ {current_time.day}.{current_time.month}.{current_time.year} {current_time.hour}:{current_time.minute}"
	send( ret, member.server.name )
	if not DISABLES[ "welcome" ]:
		welcome_tmp = DB.read( "Welcomes", member.server.id )

		if welcome_tmp.startswith( "read(" ):
			welcome_tmp = open( welcome_tmp[ 6:len( welcome_tmp ) - 2 ], 'r' ).read( )
		else:
			welcome_tmp = re.sub( "{server}", member.server.name, welcome_tmp, flags=2 )
			welcome_tmp = re.sub( "{user}", member.mention, welcome_tmp, flags=2 )
		try:
			await CLIENT.add_roles( member, discord.utils.find( lambda r:r.id == JOIN_ROLES[ member.server.id ], member.server.roles ) )
		except Exception:
			print( traceback.format_exc( ) )
		try:
			_dchannel = CLIENT.get_channel( DEFAULT_CHANNEL[ member.server.id ] )
			if _dchannel is None:
				_dchannel = member.server.default_channel
			await CLIENT.send_message( _dchannel, welcome_tmp )
		except Exception:
			await CLIENT.send_message( member.server.default_channel, welcome_tmp )
	channel_obj = CLIENT.get_channel( PARSER[ member.server.id ][ "logchannel" ] )
	if channel_obj is not None:
		embed_obj = discord.Embed( title="Member Joined!", description="A member joined!", colour=discord.Colour.red( ) )
		embed_obj.add_field( name="Name", value=str( member ), inline=False )
		embed_obj.add_field( name="ID", value=member.id, inline=False )
		embed_obj.set_footer( text=str( current_time ) )
		await CLIENT.send_message( channel_obj, "", embed=embed_obj )

@CLIENT.event
async def on_member_remove ( member: discord.Member ):
	"""
	Called when a member is removed.
	:param member: The member.
	"""
	current_time = datetime.now( )
	time = f"{current_time.day}.{current_time.month}.{current_time.year} {current_time.hour}:{current_time.minute}"
	ret = f"Member Left: {member.server.name} ~ {member} left ~ {time}"
	send( ret, member.server.name )
	if not DISABLES[ "goodbye" ]:
		goodbye_tmp = DB.read( "Goodbyes", member.server.id )
		goodbye_tmp = re.sub( "{server}", member.server.name, goodbye_tmp, flags=2 )
		goodbye_tmp = re.sub( "{user}", member.mention, goodbye_tmp, flags=2 )
		await CLIENT.send_message( member.server.default_channel, goodbye_tmp )
	channel_obj = CLIENT.get_channel( PARSER[ member.server.id ][ "logchannel" ] )
	if channel_obj is not None:
		embed_obj = discord.Embed( title="Member Left!", description="A member left!", colour=discord.Colour.red( ) )
		embed_obj.add_field( name="Name", value=str( member ), inline=False )
		embed_obj.add_field( name="ID", value=member.id, inline=False )
		embed_obj.set_footer( text=str( current_time ) )
		await CLIENT.send_message( channel_obj, "", embed=embed_obj )

@CLIENT.event
async def on_member_update ( before: discord.Member, after: discord.Member ):
	"""
	Called when a member is updated.
	:param before: The old member.
	:param after: The new member.
	"""
	current_time = datetime.now( )
	sent_str = ""
	if before.status != after.status:
		sent_str = f"Member Updated: {after.server.name} ~ {after} changed his/her status from {before.status} to {after.status}"
	elif before.game != after.game:
		sent_str = f"Member Updated: {after.server.name} ~ {after} changed his/her game from {before.game} to {after.game}"
	elif before.avatar != after.avatar:
		sent_str = f"Member Updated: {after.server.name} ~ {after} changed his/her avatar."
	elif before.nick != after.nick:
		sent_str = f"Member Updated: {after.server.name} ~ {after}'s nickname was changed to {after.nick}"
	elif before.roles != after.roles:
		if not discord.utils.find( lambda r:r.name == "LogBot Admin" or r.name == "LogBot Member", after.server.roles ) in after.roles:
			is_role_added = False
			is_role_removed = False
			role = after.server.default_role
			for item in before.roles:
				if item not in after.roles:
					is_role_removed = True
					role = item
			for item in after.roles:
				if item not in before.roles:
					is_role_added = True
					role = item
			if is_role_added:
				sent_str = f"Member Updated: {after.server.name} ~ Role {role} was added to {before}."
			elif is_role_removed:
				sent_str = f"Member Updated: {after.server.name} ~ Role {role} was removed from {before}."
	if sent_str != "":
		sent_str += f" ~ {current_time.day}.{current_time.month}.{current_time.year} {current_time.hour}:{current_time.minute}"
		send( sent_str, before.server.name )

@CLIENT.event
async def on_member_ban ( member: discord.Member ):
	"""
	Called when a member is banned.
	:param member: The member.
	"""
	current_time = datetime.now( )
	sent_str = f"Member Banned: {member.server.name} ~ {check(member.nick, member.name, member.id)} was banned ~ {current_time.day}.{current_time.month}.{current_time.year} {current_time.hour}:{current_time.minute}"
	send( sent_str, member.server.name )
	channel_obj = CLIENT.get_channel( PARSER[ member.server.id ][ "logchannel" ] )
	if channel_obj is not None:
		embed_obj = discord.Embed( title="Member Banned!", description="A member was banned!", colour=discord.Colour.red( ) )
		embed_obj.add_field( name="Name", value=str( member ), inline=False )
		embed_obj.add_field( name="ID", value=member.id, inline=False )
		embed_obj.set_footer( text=str( current_time ) )
		await CLIENT.send_message( channel_obj, "", embed=embed_obj )

@CLIENT.event
async def on_member_unban ( server: discord.Server, user: discord.User ):
	"""
	Called when a member is unbanned.
	:param server: The server.
	:param user: The user.
	"""
	current_time = datetime.now( )
	sent_str = f"Member Unbanned: {server.name} ~ {check(user.display_name, user.name, user.id)} was unbanned ~ {current_time.day}.{current_time.month}.{current_time.year} {current_time.hour}:{current_time.minute}"
	send( sent_str, server.name )
	channel_obj = CLIENT.get_channel( PARSER[ server.id ][ "logchannel" ] )
	if channel_obj is not None:
		embed_obj = discord.Embed( title="Member Unbanned!", description="A member was unbanned!", colour=discord.Colour.red( ) )
		embed_obj.add_field( name="Name", value=str( user ), inline=False )
		embed_obj.add_field( name="ID", value=user.id, inline=False )
		embed_obj.set_footer( text=str( current_time ) )
		await CLIENT.send_message( channel_obj, "", embed=embed_obj )

# </editor-fold>
# <editor-fold desc="Channel Updates">
@CLIENT.event
async def on_channel_update ( before: discord.Channel, after: discord.Channel ):
	"""
	Called when a channel is updated.
	:param before: The old channel.
	:param after: The new channel.
	"""
	current_time = datetime.now( )
	if before.name != after.name:
		send( f"Channel Updated: {after.server.name} ~ {after}'s name was changed from {before.name} to {after.name}", after.server.name )
		with f"{DISCORD_LOGS_PATH}\\{before.server.name}\\{before.name}.mark.txt" as old_loc:
			if os.path.exists( old_loc ):
				os.rename( old_loc, f"{DISCORD_LOGS_PATH}\\{before.server.name}\\{after.name}.mark.txt" )
		with f"{DISCORD_LOGS_PATH}\\{before.server.name}\\{before.name}.txt" as old_loc_unmarked:
			if os.path.exists( old_loc_unmarked ):
				os.rename( old_loc_unmarked, f"{DISCORD_LOGS_PATH}\\{before.server.name}\\{after.name}.txt" )
	elif before.topic is not after.topic:
		send( f"Channel Updated: {after.server.name} ~ {after}'s topic was changed from \"{before.topic}\" to \"{after.topic}\"", after.server.name )
	elif before.position is not after.position:
		send( f"Channel Updated: {after.server.name} ~ {after}'s position was changed from {before.position} to {after.position}", after.server.name )
	elif before.user_limit is not after.user_limit:
		send( f"Channel Updated: {after.server.name} ~ {after}'s user limit was changed from {before.user_limit} to {after.user_limit}", after.server.name )
	elif before.bitrate is not after.bitrate:
		send( f"Channel Updated: {after.server.name} ~ {after.name}'s bitrate was changed from {before.bitrate} to {after.bitrate}", after.server.name )
	else: send( f"Channel Updated: {after.server.name} ~ {after.name} was updated.", after.server.name )
	channel_obj = CLIENT.get_channel( PARSER[ before.server.id ][ "logchannel" ] )
	if channel_obj is not None:
		embed_obj = discord.Embed( title="Channel Updated!", description="A channel was updated!", colour=discord.Colour.gold( ) )
		if str( before ) != str( after ):
			embed_obj.add_field( name="Old Name", value=str( before ), inline=False )
			embed_obj.add_field( name="New Name", value=str( after ), inline=False )
		else: embed_obj.add_field( name="Name", value=str( after ), inline=False )
		embed_obj.add_field( name="ID", value=after.id, inline=False )
		if not before.topic == after.topic:
			embed_obj.add_field( name="Old Topic", value=str( before.topic ), inline=False )
			embed_obj.add_field( name="New Topic", value=str( after.topic ), inline=False )
		if not before.position == after.position:
			embed_obj.add_field( name="Old Position", value=str( before.position ), inline=False )
			embed_obj.add_field( name="New Position", value=str( after.position ), inline=False )
		if not before.bitrate == after.bitrate:
			embed_obj.add_field( name="Old Bitrate", value=str( before.bitrate ), inline=False )
			embed_obj.add_field( name="New Bitrate", value=str( after.bitrate ), inline=False )
		if not before.user_limit == after.user_limit:
			embed_obj.add_field( name="Old User Limit", value=str( before.user_limit ), inline=False )
			embed_obj.add_field( name="New User Limit", value=str( after.user_limit ), inline=False )
		embed_obj.set_footer( text=str( current_time ) )
		await CLIENT.send_message( channel_obj, "", embed=embed_obj )

@CLIENT.event
async def on_voice_state_update ( before: discord.Member, after: discord.Member ):
	"""
	Called when a user's voice state is updated.
	:param before: The old voice state.
	:param after: The new voice state.
	"""
	current_time = datetime.now( )
	sent_str = "Voice Status Updated: {after.server.name} ~ "
	if before.voice.deaf is not after.voice.deaf:
		sent_str = f"{before} was deafened by the server."
	elif before.voice.mute is not after.voice.mute:
		if after.voice.mute:
			sent_str = f"{before} was muted by the server."
		else:
			sent_str = f"{before} was unmuted by the server."
	elif before.voice.self_mute is not after.voice.self_mute:
		if after.voice.self_mute:
			sent_str = f"{before} muted him/her self."
		else:
			sent_str = f"{before} unmuted him/her self."
	elif before.voice.self_deaf is not after.voice.self_deaf:
		if after.voice.self_deaf:
			sent_str = f"{before} deafened him/her self."
		else:
			sent_str = f"{before} undeafened him/her self."
	elif before.voice.voice_channel is not after.voice.voice_channel:
		if after.voice.voice_channel is not None:
			sent_str = f"{before} joined {after.voice.voice_channel}"
		else:
			sent_str = f"{before} left {before.voice.voice_channel}"
	sent_str += f" ~ {current_time.day}.{current_time.month}.{current_time.year} {current_time.hour}:{current_time.minute}"
	send( sent_str, before.server.name )

@CLIENT.event
async def on_channel_delete ( channel: discord.Channel ):
	"""
	Called when a channel is deleted.
	:param channel: The deleted channel.
	"""
	current_time = datetime.now( )
	ret = f"Channel Deleted: {channel.server.name} ~ \"{channel.name}\" was deleted ~ {current_time.day}.{current_time.month}.{current_time.year} {current_time.hour}:{current_time.minute}"
	send( ret, channel.server.name )
	channel_obj = CLIENT.get_channel( PARSER[ channel.server.id ][ "logchannel" ] )
	if channel_obj is not None:
		embed_obj = discord.Embed( title="Channel Deleted!", description="A channel was deleted!", colour=discord.Colour.red( ) )
		embed_obj.add_field( name="Name", value=str( channel ), inline=False )
		embed_obj.add_field( name="ID", value=channel.id, inline=False )
		embed_obj.set_footer( text=str( current_time ) )
		await CLIENT.send_message( channel_obj, "", embed=embed_obj )

@CLIENT.event
async def on_channel_create ( channel: discord.Channel ):
	"""
	Called when a channel is created.
	:param channel: The new channel.
	"""
	current_time = datetime.now( )
	ret = f"Channel Created: {channel.server.name} ~ \"{channel.name}\" was created ~ {current_time.day}.{current_time.month}.{current_time.year} {current_time.hour}:{current_time.minute}"
	if channel.server is not None:
		send( ret, channel.server.name )
	else:
		send( ret, f"DM{channel.name}" )
	channel_obj \
		= CLIENT.get_channel( PARSER[ channel.server.id ][ "logchannel" ] )
	if channel_obj is not None:
		embed_obj = discord.Embed( title="Channel Created!", description="A channel was created!", colour=discord.Colour.green( ) )
		embed_obj.add_field( name="Name", value=str( channel ), inline=False )
		embed_obj.add_field( name="ID", value=channel.id, inline=False )
		embed_obj.add_field( name="Position", value=str( channel.position ), inline=False )
		embed_obj.add_field( name="Bitrate", value=str( channel.bitrate ), inline=False )
		embed_obj.add_field( name="Topic", value=channel.topic, inline=False )
		embed_obj.add_field( name="User Limit", value=str( channel.user_limit ), inline=False )
		embed_obj.set_footer( text=str( channel.created_at ) )
		await CLIENT.send_message( channel_obj, "", embed=embed_obj )

# </editor-fold>
# <editor-fold desc="Server Updates">
# noinspection PyShadowingNames
@CLIENT.event
async def on_server_update ( before: discord.Server, after: discord.Server ):
	"""
	Occurs when a server is updated.
	:param before: The server before update.
	:param after: The server after update.
	"""
	current_time = datetime.now( )
	# If the server's properties were changed, do the appropriate actions and log them.
	if before.name != after.name:
		with f"{DISCORD_LOGS_PATH}\\{before.name}" as old_loc:
			with f"{DISCORD_LOGS_PATH}\\{after.name}" as new_loc:
				os.rename( old_loc, new_loc )
		send( f"Server Updated: {after.name} ~ The server name was changed from {before.name} to {after.name}.", after.name )
	if before.default_channel != after.default_channel:
		send( f"Server Updated: {after.name} ~ The server's default channel was changed from {before.default_channel} to {after.default_channel}.", after.name )
	if before.afk_channel != after.afk_channel:
		send( f"Server Updated: {after.name} ~ The server's AFK channel was changed from {before.afk_channel} to {after.afk_channel}.", after.name )
	if before.default_role != after.default_role:
		send( f"Server Updated: {after.name} ~ The server's default role was changed from {before.default_role} to {after.default_role}.", after.name )
	if before.verification_level != after.verification_level:
		send( f"Server Updated: {after.name} ~ The server's verification level was changed from {before.verification_level} to {after.verification_level}.", after.name )
	channel_obj = CLIENT.get_channel( PARSER[ before.id ][ "logchannel" ] )
	if channel_obj is not None:
		embed_obj = discord.Embed( title="Server Updated!", description="The server was updated!", colour=discord.Colour.gold( ) )
		if str( before ) != str( after ):
			embed_obj.add_field( name="Old Name", value=str( before ), inline=False )
			embed_obj.add_field( name="New Name", value=str( after ), inline=False )
		embed_obj.add_field( name="ID", value=after.id, inline=False )
		if before.default_channel != after.default_channel:
			embed_obj.add_field( name="Old Default Channel", value=str( before.default_channel ), inline=False )
			embed_obj.add_field( name="New Default Channel", value=str( after.default_channel ), inline=False )
		if before.afk_channel != after.afk_channel:
			embed_obj.add_field( name="Old AFK Channel", value=str( before.afk_channel ), inline=False )
			embed_obj.add_field( name="New AFK Channel", value=str( after.afk_channel ), inline=False )
		if before.default_role != after.default_role:
			embed_obj.add_field( name="Old Default Role", value=str( before.default_role ), inline=False )
			embed_obj.add_field( name="New Default Role", value=str( after.default_role ), inline=False )
		embed_obj.set_footer( text=str( current_time ) )
		await CLIENT.send_message( channel_obj, "", embed=embed_obj )

@CLIENT.event
async def on_server_role_create ( role: discord.Role ):
	"""
	Occurs when a role is created in a server.
	:param role: A discord.Role object.
	"""
	occurrence_time = datetime.now( )
	sent_str = f"Role Created: {role.server.name} ~ {role.name} was created ~ {occurrence_time.day}.{occurrence_time.month}.{occurrence_time.year} {occurrence_time.hour}:{occurrence_time.minute}"
	send( sent_str, role.server.name )
	channel_obj = CLIENT.get_channel( PARSER[ role.server.id ][ "logchannel" ] )
	if channel_obj is not None:
		embed_obj = discord.Embed( title="Role Created!", description="A role was created!", colour=discord.Colour.green( ) )
		embed_obj.add_field( name="Name", value=str( role ), inline=False )
		embed_obj.add_field( name="ID", value=role.id, inline=False )
		embed_obj.add_field( name="Permissions", value=str( role.permissions ), inline=False )
		embed_obj.set_footer( text=str( role.created_at ) )
		await CLIENT.send_message( channel_obj, "", embed=embed_obj )

@CLIENT.event
async def on_server_role_delete ( role: discord.Role ):
	"""
	Occurs when a role is deleted in a server.
	:param role: The role that was deleted.
	"""
	occurrence_time = datetime.now( )
	sent_str = f"Role Deleted: {role.server.name} ~ {role.name} was deleted ~ {occurrence_time.day}.{occurrence_time.month}.{occurrence_time.year} {occurrence_time.hour}:{occurrence_time.minute}"
	send( sent_str, role.server.name )
	channel_obj = CLIENT.get_channel( PARSER[ role.server.id ][ "logchannel" ] )
	if channel_obj is not None:
		embed_obj = discord.Embed( title="Role Deleted!", description="A role was deleted!", colour=discord.Colour.red( ) ) \
			.add_field( name="Name", value=str( role ), inline=False ) \
			.add_field( name="ID", value=role.id, inline=False ) \
			.set_footer( text=str( occurrence_time ) )
		await CLIENT.send_message( channel_obj, "", embed=embed_obj )

def check_perms ( perms, nperms ):
	"""
	Checks the permissions for on_server_role_update.
	:param perms: Old object permissions.
	:param nperms: New object permissions.
	:return: old and new dictionaries
	"""
	old = { }
	new = { }
	perms = perms.__dict__
	nperms = nperms.__dict__
	for key in perms.keys( ):
		if perms[ key ] != nperms[ key ]:
			old[ key ] = perms[ key ]
			new[ key ] = nperms[ key ]

	# if not perms.create_instant_invite is nperms.create_instant_invite:
	# 	old[ 'create_instant_invite' ] = perms.create_instant_invite
	# 	new[ 'create_instant_invite' ] = nperms.create_instant_invite
	# if not perms.kick_members is nperms.kick_members:
	# 	old[ 'kick_members' ] = perms.kick_members
	# 	new[ 'kick_members' ] = nperms.kick_members
	# if not perms.ban_members is nperms.ban_members:
	# 	old[ 'ban_members' ] = perms.ban_members
	# 	new[ 'ban_members' ] = nperms.ban_members
	# if not perms.administrator is nperms.administrator:
	# 	old[ 'administrator' ] = perms.administrator
	# 	new[ 'administrator' ] = nperms.administrator
	# if not perms.manage_channels is nperms.manage_channels:
	# 	old[ 'manage_channels' ] = perms.manage_channels
	# 	new[ 'manage_channels' ] = nperms.manage_channels
	# if not perms.manage_server is nperms.manage_server:
	# 	old[ 'manage_server' ] = perms.manage_server
	# 	new[ 'manage_server' ] = nperms.manage_server
	# if not perms.read_messages is nperms.read_messages:
	# 	old[ 'read_messages' ] = perms.read_messages
	# 	new[ 'read_messages' ] = nperms.read_messages
	# if not perms.send_messages is nperms.send_messages:
	# 	old[ 'send_messages' ] = perms.send_messages
	# 	new[ 'send_messages' ] = nperms.send_messages
	# if not perms.send_tts_messages is nperms.send_tts_messages:
	# 	old[ 'send_tts_messages' ] = perms.send_tts_messages
	# 	new[ 'send_tts_messages' ] = nperms.send_tts_messages
	# if not perms.manage_messages is nperms.manage_messages:
	# 	old[ 'manage_messages' ] = perms.manage_messages
	# 	new[ 'manage_messages' ] = nperms.manage_messages
	# if not perms.embed_links is nperms.embed_links:
	# 	old[ 'embed_links' ] = perms.embed_links
	# 	new[ 'embed_links' ] = nperms.embed_links
	# if not perms.attach_files is nperms.attach_files:
	# 	old[ 'attach_files' ] = perms.attach_files
	# 	new[ 'attach_files' ] = nperms.attach_files
	# if not perms.read_message_history is nperms.read_message_history:
	# 	old[ 'read_message_history' ] = perms.read_message_history
	# 	new[ 'read_message_history' ] = nperms.read_message_history
	# if not perms.mention_everyone is nperms.mention_everyone:
	# 	old[ 'mention_everyone' ] = perms.mention_everyone
	# 	new[ 'mention_everyone' ] = nperms.mention_everyone
	# if not perms.external_emojis is nperms.external_emojis:
	# 	old[ 'external_emojis' ] = perms.external_emojis
	# 	new[ 'external_emojis' ] = nperms.external_emojis
	# if not perms.connect is nperms.connect:
	# 	old[ 'connect' ] = perms.connect
	# 	new[ 'connect' ] = nperms.connect
	# if not perms.speak is nperms.speak:
	# 	old[ 'speak' ] = perms.speak
	# 	new[ 'speak' ] = nperms.speak
	# if not perms.mute_members is nperms.mute_members:
	# 	old[ 'mute_members' ] = perms.mute_members
	# 	new[ 'mute_members' ] = nperms.mute_members
	# if not perms.deafen_members is nperms.deafen_members:
	# 	old[ 'deafen_members' ] = perms.deafen_members
	# 	new[ 'deafen_members' ] = nperms.deafen_members
	# if not perms.move_members is nperms.move_members:
	# 	old[ 'move_members' ] = perms.move_members
	# 	new[ 'move_members' ] = nperms.move_members
	# if not perms.use_voice_activation is nperms.use_voice_activation:
	# 	old[ 'use_voice_activation' ] = perms.use_voice_activation
	# 	new[ 'use_voice_activation' ] = nperms.use_voice_activation
	# if not perms.change_nickname is nperms.change_nickname:
	# 	old[ 'change_nickname' ] = perms.change_nickname
	# 	new[ 'change_nickname' ] = nperms.change_nickname
	# if not perms.manage_nicknames is nperms.manage_nicknames:
	# 	old[ 'manage_nicknames' ] = perms.manage_nicknames
	# 	new[ 'manage_nicknames' ] = nperms.manage_nicknames
	# if not perms.manage_roles is nperms.manage_roles:
	# 	old[ 'manage_roles' ] = perms.manage_roles
	# 	new[ 'manage_roles' ] = nperms.manage_roles
	# if not perms.manage_emojis is nperms.manage_emojis:
	# 	old[ 'manage_emojis' ] = perms.manage_emojis
	# 	new[ 'manage_emojis' ] = nperms.manage_emojis
	return old, new

@CLIENT.event
async def on_server_role_update ( before: discord.Role, after: discord.Role ):
	"""
	Occurs when a role is updated in a server.
	:param before: The role before it was updated.
	:param after: The role after it was updated.
	"""
	occurrence_time = datetime.now( )
	perms = before.permissions
	# noinspection SpellCheckingInspection
	nperms = after.permissions
	res = check_perms( perms, nperms )
	old = res[ 0 ]
	new = res[ 1 ]

	sent_str = f"Role Updated: {before.server.name} ~ {before} : {old} : {before.position} -> {after} : {new} : {after.position} ~ {occurrence_time.day}.{occurrence_time.month}.{occurrence_time.year} {occurrence_time.hour}:{occurrence_time.minute}"
	send( sent_str, before.server.name )

	channel_obj = CLIENT.get_channel( PARSER[ before.server.id ][ "logchannel" ] )
	if channel_obj is not None:
		embed_obj = discord.Embed( title="Role Updated!", description="A role was updated!", colour=discord.Colour.gold( ) )
		if str( before ) != str( after ):
			embed_obj.add_field( name="Old Name", value=str( before ), inline=False )
			embed_obj.add_field( name="New Name", value=str( after ), inline=False )
		embed_obj.add_field( name="ID", value=after.id, inline=False )
		if old != new:
			embed_obj.add_field( name="Old Permissions", value=str( old ), inline=False )
			embed_obj.add_field( name="New Permissions", value=str( new ), inline=False )
		if before.position != after.position:
			embed_obj.add_field( name="Old Position", value=str( before.position ), inline=False )
			embed_obj.add_field( name="New Position", value=str( after.position ), inline=False )
		embed_obj.set_footer( text=str( occurrence_time ) )
		await CLIENT.send_message( channel_obj, "", embed=embed_obj )

	del sent_str
	del old
	del new
	del occurrence_time
	del channel_obj

# </editor-fold>
# <editor-fold desc="Reaction Events">
@CLIENT.event
async def on_reaction_add ( reaction: discord.Reaction, user: Union[ discord.User, discord.Member ] ):
	"""
	Occurs when a reaction is added to a message.
	:param reaction: A discord.Reaction object.
	:param user: A discord.User or discord.Member object.
	"""
	emj = codecs.unicode_escape_encode( reaction.emoji, 'strict' )
	msgcont = reaction.message.content if is_ascii( reaction.message.content ) else codecs.unicode_escape_encode( reaction.message.content, 'strict' )
	sent_str = f"Reaction Added: {reaction.message.server.name} ~ {reaction.message.channel.name} ~ {'Custom ' if reaction.custom_emoji else ''}Reaction {emj} was added to message \"{msgcont}\" {reaction.count} time(s) by {user}"
	send( sent_str, reaction.message.server.name )

@CLIENT.event
async def on_reaction_remove ( reaction: discord.Reaction, user: Union[ discord.User, discord.Member ] ):
	"""
	Occurs when a reaction is removed from a message.
	:param reaction: a discord.Reaction object.
	:param user: A discord.User or discord.Member object.
	"""
	emj = codecs.unicode_escape_encode( reaction.emoji, 'strict' )
	msgcont = reaction.message.content if is_ascii( reaction.message.content ) else codecs.unicode_escape_encode( reaction.message.content, 'strict' )
	sent_str = f"Reaction Removed: {reaction.message.server.name} ~ {reaction.message.channel.name} ~ {'Custom ' if reaction.custom_emoji else ''}Reaction {emj} was removed from message \"{msgcont}\" {reaction.count} time(s) by {user}"
	send( sent_str, reaction.message.server.name )

@CLIENT.event
async def on_reaction_clear ( message: discord.Message, reactions: List[ discord.Reaction ] ):
	"""
	Occurs when a reaction is cleared from a message.
	:param message: A discord.Message object
	:param reactions: A list of discord.Reaction objects.
	"""
	emjs = [ ]
	for item in reactions:
		emjs.append( codecs.unicode_escape_encode( item.emoji, 'strict' ) )
	msgcont = message.content if is_ascii( message.content ) else codecs.unicode_escape_encode( message.content, 'strict' )
	sent_str = f"Reaction(s) Cleared: {message.server.name} ~ {message.channel.name} ~ Reactions [{','.join(emjs)}] were cleared from message \"{msgcont}\""
	send( sent_str, message.server.name )

# </editor-fold>

@CLIENT.event
async def on_ready ( ):
	"""
	Occurs when the bot logs in.
	"""
	global ICON, BOOTUP_TIME
	# gets and deletes the Update message from the parameters.
	if argv:
		index = -1
		index2 = -1
		if "-m" in argv:
			index = argv.index( "-m" )
		if "-c" in argv:
			index2 = argv.index( "-c" )
		if index != -1 and index2 != -1:
			channel_tmp = CLIENT.get_channel( argv[ index2 + 1 ] )
			message_tmp = await CLIENT.get_message( channel_tmp, argv[ index + 1 ] )
			await CLIENT.delete_message( message_tmp )

		if "-t" in argv:
			t_arg = argv[ argv.index( "-t" ) + 1 ].split( "." )
			BOOTUP_TIME = datetime( year=int( t_arg[ 2 ] ), month=int( t_arg[ 0 ] ), day=int( t_arg[ 1 ] ), hour=int( t_arg[ 3 ] ), minute=int( t_arg[ 4 ] ), second=int( t_arg[ 5 ] ), microsecond=int( t_arg[ 6 ] ) )
	# os.system( 'cls' )
	print( f"{Fore.MAGENTA}Signed in and waiting...\nRunning version: Logbot Version {VERSION}{Fore.RESET}" )
	for server in CLIENT.servers:
		if server.id not in PARSER.sections( ):
			PARSER[ server.id ] = {
				"logchannel":"None"
			}
	# Updates bot icon, status, and game.
	await CLIENT.change_presence( game=discord.Game( name="Prefix: $" ), status=None )
	try:
		avatar_tmp = open( SELECTED_IMAGE, "rb" )
		await CLIENT.edit_profile( avatar=avatar_tmp.read( ) )
		avatar_tmp.close( )
		ICON = Qt.QIcon( SELECTED_IMAGE )
		STI.setIcon( ICON )
		del avatar_tmp
	except Exception:
		pass

CLIENT.run( token )

if not EXITING:
	subprocess.Popen( f"python {os.getcwd()}\\logbot.py -t {BOOTUP_TIME.month}.{BOOTUP_TIME.day}.{BOOTUP_TIME.year}.{BOOTUP_TIME.hour}.{BOOTUP_TIME.minute}.{BOOTUP_TIME.second}.{BOOTUP_TIME.microsecond}", False )
	exit( 0 )
