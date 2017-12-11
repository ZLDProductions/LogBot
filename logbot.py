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
import psutil
import translate
# import unirest
import urbandictionary
import wikipedia
import wolframalpha
from PyDictionary import PyDictionary
from PyQt5 import Qt
from colorama import Fore, init

import argparser
import sql
import tools
from logbot_data import *

# <editor-fold desc="Base Variables">
version = '16.7.4 Python'
whats_new = [
	"•Fixed custom commands. Now, each server can have their own commands. No more awkward moments!",
	"•Revised the original polling system to make voting much simpler.",
	"•Added $gif.",
	"•Fixed $disable commands.",
	"•Major speed increase in the levels plugin.",
	"•Added the ability to fetch only a certain field for a user when using the $user command.",
	"•Fixed 3/5 bugs regarding the $setup command!"
] # list of recent changes to the code.
planned = [
	"There is nothing planned at the moment."
] # list of what I plan to do.
bootup_time = datetime.now( ) # the time the bot started.
exiting = False # determines if the bot is closing. If False, the bot automatically restarts.
# </editor-fold>

# <editor-fold desc="Clients and Classes">
client = discord.Client( ) # Discord client
init( ) # Colorama client (color the console!)
wclient = wolframalpha.Client( app_id=wa_token ) # Wolfram|Alpha client
parser = configparser.ConfigParser( ) # ConfigParser init
channel_parser = configparser.ConfigParser( ) # ConfigParser init
pydict = PyDictionary( ) # PyDictionary client
purge_parser = argparser.ArgParser( "&&", "=" ) # ArgParser (my own class) init
gc = giphy_client.DefaultApi( ) # Giphy client
# </editor-fold>

# <editor-fold desc="Tray Icon">
selected_image = f"{os.getcwd()}\\Discord Logs\\SETTINGS\\avatar5.jpg" # Bot image
app = Qt.QApplication( argv )
sti = Qt.QSystemTrayIcon( Qt.QIcon( selected_image ), app )
icon = Qt.QIcon( selected_image )
sti.setIcon( icon )
sti.show( )
sti.setToolTip( "LogBot" )
# </editor-fold>

# <editor-fold desc="Databases">
db = sql.SQL( )
db.create( "Welcomes", "server", "message" )
db.create( "Goodbyes", "server", "message" )
db.create( "Prefixes", "server", "prefix" )
# </editor-fold>

# <editor-fold desc="Instance Variables">
exclude_channel_list = [ ]
marklist = [ ]
channels = [ ]
user_name = ""
disables = { }
custom_commands = { }
times = [ ]
join_roles = { }
log_channel = { }
default_channel = { }
dict_words = [ ]
# </editor-fold>

# <editor-fold desc="Paths">
discord_logs = f"{os.getcwd()}\\Discord Logs"
discord_settings = f"{discord_logs}\\SETTINGS"
server_settings = f"{discord_settings}\\SERVER SETTINGS"
channel_whitelist = f"{discord_settings}\\channel_whitelist.txt"
mark_list = f"{discord_settings}\\mark_list.txt"
channel_list = f"{discord_settings}\\channels.txt"
name = f"{discord_settings}\\name.txt"
customcmds = f"{discord_settings}\\commands.txt"
suggestions = f"{discord_settings}\\suggestions.txt"
channel_settings = f"{discord_settings}\\channel_settings.ini"
_join_roles = f"{discord_settings}\\join_roles.txt"
_defaults = f"{discord_settings}\\default_channels.txt"
_dictionary = f"{discord_settings}\\censored_words.txt"
_disables = f"{discord_settings}\\disables.txt"
# </editor-fold>

if not os.path.exists( discord_settings ): os.makedirs( discord_settings )

# <editor-fold desc="data loading">
parser.read( f'{discord_settings}\\data.ini' )

# Load the join roles.
try:
	reader = open( _join_roles, 'r' )
	join_roles = ast.literal_eval( reader.read( ) )
	reader.close( )
	del reader
	pass
except: traceback.format_exc( )

# Load the default channels.
try:
	reader = open( _defaults, 'r' )
	default_channel = ast.literal_eval( reader.read( ) )
	reader.close( )
	del reader
	pass
except: traceback.format_exc( )

# Load the banned words.
try:
	reader = open( _dictionary, 'r' )
	dict_words = reader.read( ).split( "\n" )
	reader.close( )
	del reader
	pass
except: pass

# Load the disabled features.
try:
	reader = open( _disables, 'r' )
	disables = ast.literal_eval( reader.read( ) )
	reader.close( )
	del reader
	pass
except: pass

if not "SETTINGS" in parser.sections( ):
	parser[ "SETTINGS" ] = {
		"name"      :input( f"{Fore.CYAN}What is your name on Discord? {Fore.RESET}" ),
		"customcmds":str( custom_commands )
	}
	pass

if "SETTINGS" in parser.sections( ):
	if "name" in parser[ "SETTINGS" ]: user_name = parser[ "SETTINGS" ][ "name" ]
	else:
		# noinspection PyUnresolvedReferences,PyUnresolvedReferences
		user_name = input( f"{Fore.CYAN}What is your nickname on Discord? {Fore.RESET}" )
		parser[ "SETTINGS" ][ "name" ] = user_name
		pass
	try:
		custom_commands = ast.literal_eval( parser[ "SETTINGS" ][ "customcmds" ] )
		exclude_channel_list = ast.literal_eval( parser[ "SETTINGS" ][ "channel_whitelist" ] )
		marklist = ast.literal_eval( parser[ "SETTINGS" ][ "mark_list" ] )
		channels = ast.literal_eval( parser[ "SETTINGS" ][ "channel_list" ] )
		pass
	except: traceback.format_exc( )
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
	if not os.path.exists( f"{discord_logs}\\{servername}" ): os.makedirs( f"{discord_logs}\\{servername}" )
	try:
		# logs if the channel is marked.
		marklist.index( channel )
		writer = open( f"{discord_logs}\\{servername}\\{channel}.mark.txt", 'a' )
		writer.write( f"{message if is_ascii else codecs.unicode_escape_encode(message, 'ignore')[0]}\n" )
		writer.close( )
		del writer
		pass
	except:
		# logs if the channel is not marked.
		writer = open( f"{discord_logs}\\{servername}\\{channel}.txt", 'a' )
		writer.write( f"{message if is_ascii(message) else codecs.unicode_escape_encode(message, 'ignore')[0]}\n" )
		writer.close( )
		del writer
		pass
	try:
		# converts the message to unicode, then prints to the pyconsole.
		message = u"{}".format( message )
		print( message )
		pass
	except: print( f"{servername} ~ {Fore.LIGHTRED_EX}There was an error with the encoding of the message.{Fore.RESET}" )
	pass

def is_ascii ( s: str ) -> bool:
	"""
	Determines if a string, `s`, is non-unicode.
	:param s: The string to analyze.
	:return: True if `s` is not unicode, otherwise False.
	"""
	return all( ord( c ) < 128 for c in s ) # Returns true if the string has no unicode characters.

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
	parser[ "SETTINGS" ] = {
		"name"             :user_name,
		"customcmds"       :str( custom_commands ),
		"channel_whitelist":str( exclude_channel_list ),
		"mark_list"        :str( marklist ),
		"channel_list"     :str( channels )
	}

	if not os.path.exists( f"{server_settings}\\{sid}" ): os.makedirs( f"{server_settings}\\{sid}" )

	# <editor-fold desc="Disables">
	# writer = open( f"{server_settings}\\{sid}\\disables.txt", 'w' )
	# writer.write( str( disables ) )
	# writer.close( )
	writer = open( f"{discord_settings}\\disables.txt", 'w' )
	writer.write( str( disables ) )
	writer.close( )
	# </editor-fold>
	# <editor-fold desc="Join Roles">
	writer = open( _join_roles, 'w' )
	writer.write( str( join_roles ) )
	writer.close( )
	del writer
	# </editor-fold>
	# <editor-fold desc="Default Channel">
	writer = open( _defaults, 'w' )
	writer.write( str( default_channel ) )
	writer.close( )
	del writer
	# </editor-fold>

	# <editor-fold desc="ini file">
	with open( f"{discord_settings}\\data.ini", 'w' ) as configfile: parser.write( configfile )
	# </editor-fold>
	pass

def check ( *args ) -> str:
	"""
	Checks strings for non-ASCII characters.
	:param args: A list of strings.
	:return: The first string in args that passes inspection.
	"""
	for item in args:
		if item is not None and is_ascii( item ): return item
	pass

def format_message ( cont: str ) -> list:
	"""
	Splits `cont` into several strings, each a maximum of 2000 characters in length. Adds ``` at each end automatically.
	:param cont: The string to format.
	:return: A list of strings. Each formatted into 2000 characters, including ``` at each end.
	"""
	if len( cont ) > 1994: return [ f"```{item}```" for item in [ cont[ i:i + 1000 ] for i in range( 0, len( cont ), 1000 ) ] ]
	else: return [ f"```{cont}```" ]
	pass

def update ( mid: str, cid: str ):
	"""
	Updates the bot.
	:param mid: The message id of the update message.
	:param cid: The channel of the message. Necessary for client.get_message() to work.
	"""
	subprocess.Popen( f"python {os.getcwd()}\\logbot.py -m {mid} -c {cid} -t {bootup_time.month}.{bootup_time.day}.{bootup_time.year}.{bootup_time.hour}.{bootup_time.minute}.{bootup_time.second}.{bootup_time.microsecond}", False )
	exit( 0 )
	pass

# noinspection PyUnusedLocal
def read ( sid: str ):
	"""
	Reads the data for the specified server.
	:param sid: The server id.
	"""
	# global disables

	# # <editor-fold desc="Disables">
	# # noinspection PyShadowingNames
	# reader = open( f"{server_settings}\\{sid}\\disables.txt", 'r' )
	# disables = ast.literal_eval( reader.read( ) )
	# reader.close( )
	# del reader
	# # </editor-fold>
	pass

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
	sti.showMessage( _header, _content )
	pass

def notify ( header: str, body: str ):
	"""
	Sends a windows notification.
	:param header: The header for the notification.
	:param body: The body for the notification.
	"""
	sti.showMessage( header, body )
	pass

def sort ( ):
	"""
	Sorts all of the lists in the bot. This is an organizational tactic that allows for faster iterations of said lists.
	"""
	times.sort( )
	pass

def _filter ( text: str ) -> str:
	"""
	Filters censored words out of text. Used mainly with the UrbanDictionary
	:param text: The uncensored text.
	:return: The censored text.
	"""
	# words = text.replace( ",", "" ).replace( ".", "" ).replace( "!", "" ).replace( "?", "" ).split( " " )
	# for word in words:
	# 	if word.lower( ) in dict_words:
	# 		words[ words.index( word ) ] = "\\*" * len( word )
	# 		pass
	# 	pass
	# if "\\*" in ' '.join( words ): return ' '.join( words )
	# else: return text
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
	def _dummycheck ( m ) -> bool: return True
	if _check is None: _check = _dummycheck
	count = 0
	logs = client.logs_from( message.channel, limit=limit ).iterate
	while True:
		try:
			item = await logs( )
			if _check( item ) is True: count += 1
			del item
			pass
		except: break
		pass
	del logs
	return count
	pass

def get_diff ( then: datetime, now: datetime ) -> str:
	years = now.year - then.year
	months = now.month - then.month
	days = now.day - then.day
	weeks = 0
	hours = now.hour - then.hour
	minutes = now.minute - then.minute
	seconds = now.second - then.second
	# <editor-fold desc="Correcting the times">
	while seconds < 0: minutes -= 1; seconds += 60
	while minutes < 0: hours -= 1; minutes += 60
	while hours < 0: days -= 1; hours += 24
	while days < 0: months -= 1; days += 30
	while months < 0: years -= 1; months += 12
	while seconds >= 60: minutes += 1; seconds -= 60
	while minutes >= 60: hours += 1; minutes -= 60
	while hours >= 24: days += 1; hours -= 24
	while days >= 30: months += 1; days -= 30
	while months >= 12: years += 1; months -= 12
	while days >= 7: weeks += 1; days -= 7
	# </editor-fold>

	_str = f"{years} {'years' if not years == 1 else 'year'}, {months} {'months' if not months == 1 else 'month'}, {weeks} {'weeks' if not weeks == 1 else 'week'}, {days} {'days' if not days == 1 else 'day'}, {hours} {'hours' if not hours == 1 else 'hour'}, {minutes} {'minutes' if not minutes == 1 else 'minute'}, {seconds} {'seconds' if not seconds == 1 else 'second'}"
	_str = _str.replace( "0 years,", "" ).replace( " 0 months,", "" ).replace( " 0 weeks,", "" ).replace( " 0 days,", "" ).replace( " 0 hours,", "" ).replace( " 0 minutes,", "" ).replace( " 0 seconds", "" )
	return _str

class Commands:
	class Member:
		@staticmethod
		async def gif ( message: discord.Message, prefix: str ):
			tag = message.content.replace( f"{prefix}gif", "" )
			image = gc.gifs_random_get( giphy_key, tag=tag ).data
			e = discord.Embed( ).set_image( url=image.image_url )
			await client.send_message( message.channel, "", embed=e )
			del e
			del image
			del tag
			pass
		@staticmethod
		async def user_restrict ( message: discord.Message, prefix: str ):
			cnt = message.content.replace( f"{prefix}user:", "" )
			params = cnt.split( " " )
			field = params[ 0 ]
			params.remove( field )
			params = ' '.join( params )
			_user = discord.utils.find( lambda u:u.id == params or u.name == params or str( u ) == params or u.mention == params, message.server.members )
			if _user is None and len( message.mentions ) > 0: _user = message.mentions[ 0 ]
			elif _user is None and len( message.mentions ) == 0: _user = message.author

			if field == "nick": await client.send_message( message.channel, str( _user.nick ) )
			elif field == "name": await client.send_message( message.channel, str( _user ) )
			elif field == "id": await client.send_message( message.channel, str( _user.id ) )
			elif field == "type": await client.send_message( message.channel, "Bot" if _user.bot is True else "User" )
			elif field == "date":
				m = format_time( _user.created_at )
				await client.send_message( message.channel, f"{get_diff(m, datetime.now())} ago ({m.month}.{m.day}.{m.year} {m.hour}:{m.minute})" )
				pass
			elif field == "status": await client.send_message( message.channel, str( _user.status ) )
			elif field == "avatar": await client.send_message( message.channel, _user.avatar_url )
			elif field == "default": await client.send_message( message.channel, _user.default_avatar_url )
			del cnt
			del params
			del field
			del _user
			pass
		@staticmethod
		async def user ( message: discord.Message, prefix: str ):
			cnt = message.content.replace( f"{prefix}user ", "" )
			_user = discord.utils.find( lambda u:u.id == cnt or u.name == cnt or str( u ) == cnt or u.mention == cnt, message.server.members )
			if _user is None and len( message.mentions ) > 0: _user = message.mentions[ 0 ]
			m = format_time( _user.created_at )
			e = discord.Embed( title=_user.name, description=f"Information for {_user.name}", color=discord.Colour.gold( ) ) \
				.add_field( name="Nickname", value=str( _user.nick ) ) \
				.add_field( name="Name", value=str( _user ) ) \
				.add_field( name="ID", value=_user.id ) \
				.add_field( name="Type", value="Bot" if _user.bot is True else "User" ) \
				.add_field( name="Date Created", value=f"{get_diff(m, datetime.now())} ago ({m.month}.{m.day}.{m.year} {m.hour}:{m.minute})" ) \
				.add_field( name="Status", value=str( _user.status ) ) \
				.set_image( url=_user.avatar_url ) \
				.set_thumbnail( url=_user.default_avatar_url )
			await client.send_message( message.channel, "Here you go!", embed=e )
			del e
			del cnt
			del _user
			del m
			pass
		@staticmethod
		async def urban ( message: discord.Message, prefix: str ):
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
			if len( __example ) == 0: __example = "No available examples..."
			e = discord.Embed( title=_def.word, description=f"Definition(s) of {_def.word}", colour=discord.Colour.blue( ) ) \
				.add_field( name="Definition", value=__definition, inline=False ) \
				.add_field( name="Example", value=__example, inline=False ) \
				.add_field( name="Upvotes", value=_def.upvotes ) \
				.add_field( name="Downvotes", value=_def.downvotes )
			try: await client.send_message( message.channel, "Here you go!", embed=e )
			except: await client.send_message( message.channel, _text )
			pass
		@staticmethod
		async def role ( message: discord.Message, prefix: str ):
			_cnt_ = message.content.replace( f"{prefix}role ", "" )
			if len( message.role_mentions ) > 0: _role = message.role_mentions[ 0 ]
			else: _role = discord.utils.find( lambda r:r.name == _cnt_ or r.id == _cnt_, message.server.roles )
			_members_in_role = [ str( m ) for m in message.server.members if _role in m.roles ]
			_position = _role.position
			p = _role.permissions
			_id = _role.id
			_name = str( _role )
			_created_at = _role.created_at
			_colour = _role.colour
			_mentionable = _role.mentionable
			e = discord.Embed( title="Role Information", description=_name, colour=_colour ) \
				.add_field( name="Members", value=', '.join( _members_in_role ), inline=False ) \
				.add_field( name="Position", value=str( _position ), inline=False ) \
				.add_field( name="ID", value=_id, inline=False ) \
				.add_field( name="Mentionable", value=str( _mentionable ), inline=False ) \
				.add_field( name="Create Instant Invite", value=str( p.create_instant_invite ), inline=True ) \
				.add_field( name="Kick Members", value=str( p.kick_members ), inline=True ) \
				.add_field( name="Ban Members", value=str( p.ban_members ), inline=True ) \
				.add_field( name="Administrator", value=str( p.administrator ), inline=True ) \
				.add_field( name="Manage Channels", value=str( p.manage_channels ), inline=True ) \
				.add_field( name="Manage Server", value=str( p.manage_server ), inline=True ) \
				.add_field( name="Read Messages", value=str( p.read_messages ), inline=True ) \
				.add_field( name="Send Messages", value=str( p.send_messages ), inline=True ) \
				.add_field( name="Send TTS Messages", value=str( p.send_tts_messages ), inline=True ) \
				.add_field( name="Manage Messages", value=str( p.manage_messages ), inline=True ) \
				.add_field( name="Embed Links", value=str( p.embed_links ), inline=True ) \
				.add_field( name="Attach Files", value=str( p.attach_files ), inline=True ) \
				.add_field( name="Read Message History", value=str( p.read_message_history ), inline=True ) \
				.add_field( name="Mention Everyone", value=str( p.mention_everyone ), inline=True ) \
				.add_field( name="Use External Emojis", value=str( p.external_emojis ), inline=True ) \
				.add_field( name="Change Nickname", value=str( p.change_nickname ), inline=True ) \
				.add_field( name="Manage Nicknames", value=str( p.manage_nicknames ), inline=True ) \
				.add_field( name="Manage Roles", value=str( p.manage_roles ), inline=True ) \
				.add_field( name="Manage Emojis", value=str( p.manage_emojis ), inline=True ) \
				.set_footer( text=f"Created at {_created_at}" )
			await client.send_message( message.channel, f"Here you go!", embed=e )
			pass
		@staticmethod
		async def channels ( message: discord.Message ):
			_channels = [ x for x in client.get_all_channels( ) if x.server == message.server ]
			voice_channels = [ ]
			text_channels = [ ]
			vappend = voice_channels.append
			tappend = text_channels.append
			for c in _channels:
				if c.type == discord.ChannelType.voice: vappend( str( c ) )
				else: tappend( str( c ) )
				pass
			voice_channels = [ f"#{x}" for x in voice_channels ]
			voice_channels.sort( )
			text_channels = [ f"#{x}" for x in text_channels ]
			text_channels.sort( )
			v_msg = format_message( f"Voice Channels:\n{', '.join(voice_channels)}" )
			t_msg = format_message( f"Text Channels:\n{', '.join(text_channels)}" )
			for msg in v_msg: await client.send_message( message.channel, msg )
			for msg in t_msg: await client.send_message( message.channel, msg )
			del vappend
			del tappend
			pass
		@staticmethod
		async def ping ( message: discord.Message ):
			"""
			Pings logbot.
			:param message: A discord.Message object from on_message.
			"""
			tm = datetime.now( ) - message.timestamp
			await client.send_message( message.channel, f"```LogBot Main Online ~ {round(round(tm.microseconds / 1000))}```" )
			del tm
			pass
		@staticmethod
		async def mutes ( message: discord.Message, muted_role: discord.Role ):
			"""
			Mutes all users mentioned my `message`
			:param muted_role: A discord.Role object representing a role without send message permissions.
			:param message: A discord.Message object from on_message.
			"""
			mu = "Muted Users:\n"
			for user in message.server.members:
				if muted_role in user.roles: mu += f"{user}\n"
				pass
			await client.send_message( message.channel, f"{mu}" )
			del mu
			pass
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
				pass
			elif content.startswith( "utf-8 ", ):
				ret = "{}".format( codecs.utf_8_encode( content.replace( "utf-8 ", "" ), 'backslashreplace' )[ 0 ] ).replace( "b'\\u", "" ).replace( "'", "" )
				pass
			elif content.startswith( "ascii " ):
				ret = "{}".format( codecs.ascii_encode( content.replace( "ascii ", "" ), 'backslashreplace' )[ 0 ] ).replace( "b'\\u", "" ).replace( "'", "" )
				pass
			elif content.startswith( "oem " ):
				ret = "{}".format( codecs.oem_encode( content.replace( "oem ", "" ), 'backslashreplace' )[ 0 ] ).replace( "b'\\u", "" ).replace( "'", "" )
				pass
			else:
				ret = "Not a valid value."
				pass
			m = await client.send_message( message.channel, ret )
			await client.edit_message( m, m.content.replace( 'b', '', 1 ) )
			del content
			del m
			del ret
			pass
		@staticmethod
		async def server ( message: discord.Message ):
			"""
			Fetches server information.
			:param message: A discord.Message object from on_message
			"""
			m = format_time( message.server.created_at )
			server = message.server
			roles = [ f"{str(role).replace('@', '')} ({role.position}) [{role.id}]" for role in server.role_hierarchy ]
			try:
				# <editor-fold desc="discord.Embed">
				e = discord.Embed( title=server.name, description=f"Information for {server.name}", colour=discord.Colour.teal( ) ) \
					.add_field( name="Total Members", value=str( server.member_count ), inline=True ) \
					.add_field( name="Owner", value=str( server.owner ), inline=True ) \
					.add_field( name="ID", value=server.id, inline=True ) \
					.add_field( name="Total Channels", value=str( len( server.channels ) ), inline=True ) \
					.add_field( name="Total Roles", value=str( len( server.roles ) ), inline=True ) \
					.add_field( name="Creation Time", value=f"{get_diff(m, datetime.now())} ago ({m.month}.{m.day}.{m.year} {m.hour}:{m.minute})" ) \
					.add_field( name="Default Channel", value=str( server.default_channel ) ) \
					.set_thumbnail( url=server.icon_url )
				try: e.add_field( name="Role Hierarchy", value='\n'.join( roles ) )
				except: traceback.format_exc( )
				# </editor-fold>
				await client.send_message( message.channel, "", embed=e )
				pass
			except:
				# <editor-fold desc="discord.Embed">
				e = discord.Embed( title=server.name, description=f"Information for {server.name}", colour=discord.Colour.teal( ) ) \
					.add_field( name="Total Members", value=str( server.member_count ), inline=True ) \
					.add_field( name="Owner", value=str( server.owner ), inline=True ) \
					.add_field( name="ID", value=server.id, inline=True ) \
					.add_field( name="Total Channels", value=str( len( server.channels ) ), inline=True ) \
					.add_field( name="Total Roles", value=str( len( server.roles ) ), inline=True ) \
					.add_field( name="Creation Time", value=f"{get_diff(m, datetime.now())} ago ({m.month}.{m.day}.{m.year} {m.hour}:{m.minute})" ) \
					.add_field( name="Default Channel", value=str( server.default_channel ) ) \
					.set_thumbnail( url=server.icon_url )
				# </editor-fold>
				hierarchy = '\n'.join( roles )
				try: await client.send_message( message.channel, f"Role Hierarchy:\n{hierarchy}", embed=e )
				except: await client.send_message( message.channel, f"Could not fetch the Role Hierarchy...", embed=e )
				pass
			del m
			del server
			del roles
			del e
			pass
		@staticmethod
		async def disables ( message: discord.Message, prefix: str ):
			"""
			Sends a message with an embed of all disabled features for the `message`'s server
			:param message: A discord.Message object from on_message.
			:param prefix: The server's prefix.
			"""
			# <editor-fold desc="discord.Embed">
			e = discord.Embed( title="Disabled Features", descriptions="A list of disabled features in this server.", colour=discord.Colour.dark_purple( ) ) \
				.add_field( name=f"{prefix}exclude", value=str( disables[ message.server.id ][ "exclude" ] ) ) \
				.add_field( name=f"{prefix}excludechannel", value=str( disables[ message.server.id ][ "excludechannel" ] ) ) \
				.add_field( name=f"{prefix}includechannel", value=str( disables[ message.server.id ][ "includechannel" ] ) ) \
				.add_field( name=f"{prefix}mark", value=str( disables[ message.server.id ][ "mark" ] ) ) \
				.add_field( name=f"{prefix}showlist", value=str( disables[ message.server.id ][ "showlist" ] ) ) \
				.add_field( name=f"{prefix}showmarks", value=str( disables[ message.server.id ][ "showmarks" ] ) ) \
				.add_field( name=f"{prefix}channel", value=str( disables[ message.server.id ][ "channel" ] ) ) \
				.add_field( name=f"{prefix}say", value=str( disables[ message.server.id ][ "say" ] ) ) \
				.add_field( name=f"{prefix}query", value=str( disables[ message.server.id ][ "query" ] ) ) \
				.add_field( name=f"{prefix}wiki", value=str( disables[ message.server.id ][ "wiki" ] ) ) \
				.add_field( name=f"{prefix}decide", value=str( disables[ message.server.id ][ "decide" ] ) ) \
				.add_field( name=f"{prefix}prune", value=str( disables[ message.server.id ][ "prune" ] ) ) \
				.add_field( name=f"{prefix}purge", value=str( disables[ message.server.id ][ "purge" ] ) ) \
				.add_field( name=f"{prefix}user", value=str( disables[ message.server.id ][ "user" ] ) ) \
				.add_field( name=f"{prefix}translate", value=str( disables[ message.server.id ][ "translate" ] ) ) \
				.add_field( name=f"{prefix}urban", value=str( disables[ message.server.id ][ "urban" ] ) ) \
				.add_field( name=f"{prefix}roll", value=str( disables[ message.server.id ][ "roll" ] ) ) \
				.add_field( name=f"{prefix}server", value=str( disables[ message.server.id ][ "server" ] ) ) \
				.add_field( name=f"{prefix}convert", value=str( disables[ message.server.id ][ "convert" ] ) ) \
				.add_field( name=f"{prefix}dict", value=str( disables[ message.server.id ][ "dict" ] ) ) \
				.add_field( name=f"{prefix}permissions", value=str( disables[ message.server.id ][ "permissions" ] ) ) \
				.add_field( name=f"{prefix}gif", value=str( disables[ message.server.id ][ "gif" ] ) ) \
				.add_field( name="welcome", value=str( disables[ message.server.id ][ "welcome" ] ) ) \
				.add_field( name="goodbye", value=str( disables[ message.server.id ][ "goodbye" ] ) )
			# </editor-fold>
			await client.send_message( message.channel, f"Here you go!", embed=e )
			del e
			pass
		@staticmethod
		async def decide ( message: discord.Message, prefix: str ):
			"""
			Chooses a random value from those listed in `message.content`.
			:param message: A discord.Message object from on_message.
			:param prefix: The server's prefix.
			"""
			content = message.content.replace( f"{prefix}decide ", "" ).split( "|" )
			choice = random.choice( content )
			await client.send_message( message.channel, f"```I have chosen: {choice}```" )
			del content
			del choice
			pass
		@staticmethod
		async def suggest ( message: discord.Message, prefix: str ):
			"""
			Writes a suggestion to a file.
			:param message: A discord.Message object from on_message
			:param prefix: The server's prefix.
			"""
			suggestion = message.content.replace( f"{prefix}suggest ", "", 1 )
			# <editor-fold desc="WRITER: suggestions">
			writer = open( suggestions, 'a' )
			writer.write( f"\n{suggestion}" )
			writer.close( )
			# </editor-fold>
			await client.send_message( message.channel, "```Thank you for your suggestion.```" )
			print( f"{Fore.YELLOW}{message.author} gave you a suggestion.{Fore.RESET}" )
			del writer
			del suggestion
			pass
		@staticmethod
		async def suggestions ( message: discord.Message ):
			"""
			Gets a list of suggestions given, then sends it through Discord.
			:param message: A discord.Message object from on_message.
			"""
			# <editor-fold desc="READER: suggestions">
			# noinspection PyShadowingNames
			reader = open( suggestions, 'r' )
			ret = f"Suggestions:{reader.read()}"
			reader.close( )
			# </editor-fold>
			for item in format_message( ret ): await client.send_message( message.channel, item )
			del ret
			del reader
			pass
		@staticmethod
		async def showlist ( message: discord.Message ):
			msg = "Excluded Channels:\n"
			for channel in exclude_channel_list:
				for c in message.server.channels:
					if channel == c.id: msg += c.mention + "\n"
					pass
				pass
			await client.send_message( message.channel, msg )
			del msg
			pass
		@staticmethod
		async def showmarks ( message: discord.Message ):
			msg = "Marked Channels\n"
			for item in marklist:
				for c in message.server.channels:
					if c.id == item: msg += c.mention + "\n"
					pass
				pass
			await client.send_message( message.channel, msg )
			del msg
			pass
		@staticmethod
		async def updates ( message: discord.Message ):
			tmp = '\n'.join( whats_new )
			await client.send_message( message.channel, f"```Updates:\n{tmp}```" )
			del tmp
			pass
		@staticmethod
		async def planned ( message: discord.Message ):
			tmp = '\n'.join( planned )
			await client.send_message( message.channel, f"```Coming Soon:\n{tmp}```" )
			del tmp
			pass
		# @staticmethod
		# async def cmd ( message: discord.Message ):
		# 	content = message.content.split( ' ' )
		# 	content.remove( content[ 0 ] )
		# 	if content[ 0 ] == 'a':
		# 		content.remove( content[ 0 ] )
		# 		text = ' '.join( content )
		# 		cmd = text.split( "|" )
		# 		if cmd[ 0 ] is not None:
		# 			custom_commands[ cmd[ 0 ] ] = cmd[ 1 ]
		# 			await client.send_message( message.channel, "```Created the command.```" )
		# 			print( f"{Fore.LIGHTMAGENTA_EX}Command {cmd[0]}:{cmd[1]} was created.{Fore.RESET}" )
		# 			send( f"Command {cmd[0]}{cmd[1]} was created.", message.server.name )
		# 			pass
		# 		else:
		# 			await client.send_message( message.channel, "```A command cannot be nothing!!!```" )
		# 			print( f"{Fore.LIGHTMAGENTA_EX}{message.author} attempted to create a universal command!{Fore.RESET}" )
		# 			send( f"{message.author} attempted to create a universal command!", message.server.name )
		# 			pass
		# 		del text
		# 		del cmd
		# 		pass
		# 	elif content[ 0 ] == 'r':
		# 		content.remove( content[ 0 ] )
		# 		cmd = ' '.join( content )
		# 		data = { cmd:custom_commands[ cmd ] }
		# 		del custom_commands[ cmd ]
		# 		await client.send_message( message.channel, "```Deleted the command.```" )
		# 		print( f"{Fore.LIGHTMAGENTA_EX}Command {cmd}:{data[cmd]} was deleted.{Fore.RESET}" )
		# 		send( f"Command {cmd}:{data[cmd]} was deleted.", message.server.name )
		# 		del data
		# 		del cmd
		# 		pass
		# 	elif content[ 0 ] == 's':
		# 		tmp = '\n'.join( list( custom_commands.keys( ) ) )
		# 		ret = f"```Commands:\n{tmp}```"
		# 		await client.send_message( message.channel, ret )
		# 		del tmp
		# 		del ret
		# 		pass
		# 	del content
		# 	pass
		@staticmethod
		async def query ( message: discord.Message, prefix: str ):
			try:
				content = message.content.replace( f"{prefix}query ", "" )
				await client.send_typing( message.channel )
				res = wclient.query( content )
				ret = ""
				for pod in res.pods:
					for item in pod.texts: ret += f"{pod.title}: {item}\n"
					pass
				ret += "Powered by Wolfram|Alpha"
				[ await client.send_message( message.channel, m ) for m in format_message( ret ) ]
				del ret
				del res
				del content
				pass
			except:
				notify( "There was an exception!", traceback.format_exc( ) )
				await client.send_message( message.channel, "```We couldn't get that information. Please try again.```" )
				print( f"{Fore.LIGHTGREEN_EX}{message.author} attempted to use $query, but failed.{Fore.RESET}" )
				print( traceback.format_exc( ) )
				pass
			pass
		@staticmethod
		async def wiki ( message: discord.Message, prefix: str ):
			content = message.content.replace( f"{prefix}wiki ", "" )
			await client.send_typing( message.channel )
			# noinspection PyUnusedLocal
			info = ""
			try: info = wikipedia.summary( content )
			except:
				search = wikipedia.search( content )
				search_str = ""
				for item in search: search_str += item + "\n"
				await client.send_message( message.channel, f"```I found these results:\nSearched Item: {search_str}```" )
				msg = await client.wait_for_message( author=message.author )
				info = wikipedia.summary( msg.content )
				del msg
				del search
				del search_str
				pass
			for item in format_message( info ): await client.send_message( message.channel, item )
			del content
			del info
			pass
		@staticmethod
		async def user_permissions ( message: discord.Message, prefix: str ):
			permparse = argparser.ArgParser( ", ", "=" )
			msg = permparse.parse( message.content.replace( f"{prefix}permissions ", "" ) )

			# <editor-fold desc="Fetch User">
			# noinspection PyUnusedLocal
			user = discord.User
			if msg.get( "user" ) is None: user = message.author
			else:
				if "<@" in msg.get( "user" ): user = discord.utils.find( lambda u:u.mention == msg.get( "user" ), message.server.members )
				else: user = message.server.get_member_named( msg.get( "user" ) )
				pass
			# </editor-fold>

			if len( message.channel_mentions ) > 0:
				p = user.permissions_in( message.channel_mentions[ 0 ] )
				e = discord.Embed( title=f"Permissions for {user}", colour=discord.Colour.dark_blue( ) ) \
					.add_field( name="Create Instant Invite", value=str( p.create_instant_invite ), inline=True ) \
					.add_field( name="Kick Members", value=str( p.kick_members ), inline=True ) \
					.add_field( name="Ban Members", value=str( p.ban_members ), inline=True ) \
					.add_field( name="Administrator", value=str( p.administrator ), inline=True ) \
					.add_field( name="Manage Channels", value=str( p.manage_channels ), inline=True ) \
					.add_field( name="Manage Server", value=str( p.manage_server ), inline=True ) \
					.add_field( name="Read Messages", value=str( p.read_messages ), inline=True ) \
					.add_field( name="Send Messages", value=str( p.send_messages ), inline=True ) \
					.add_field( name="Send TTS Messages", value=str( p.send_tts_messages ), inline=True ) \
					.add_field( name="Manage Messages", value=str( p.manage_messages ), inline=True ) \
					.add_field( name="Embed Links", value=str( p.embed_links ), inline=True ) \
					.add_field( name="Attach Files", value=str( p.attach_files ), inline=True ) \
					.add_field( name="Read Message History", value=str( p.read_message_history ), inline=True ) \
					.add_field( name="Mention Everyone", value=str( p.mention_everyone ), inline=True ) \
					.add_field( name="Use External Emojis", value=str( p.external_emojis ), inline=True ) \
					.add_field( name="Change Nickname", value=str( p.change_nickname ), inline=True ) \
					.add_field( name="Manage Nicknames", value=str( p.manage_nicknames ), inline=True ) \
					.add_field( name="Manage Roles", value=str( p.manage_roles ), inline=True ) \
					.add_field( name="Manage Emojis", value=str( p.manage_emojis ), inline=True )
				await client.send_message( message.channel, "Here you go!", embed=e )
				del p
				del e
				pass
			else:
				p = user.server_permissions
				e = discord.Embed( title=f"Permissions for {user}", colour=discord.Colour.dark_blue( ) ) \
					.add_field( name="Create Instant Invite", value=str( p.create_instant_invite ), inline=True ) \
					.add_field( name="Kick Members", value=str( p.kick_members ), inline=True ) \
					.add_field( name="Ban Members", value=str( p.ban_members ), inline=True ) \
					.add_field( name="Administrator", value=str( p.administrator ), inline=True ) \
					.add_field( name="Manage Channels", value=str( p.manage_channels ), inline=True ) \
					.add_field( name="Manage Server", value=str( p.manage_server ), inline=True ) \
					.add_field( name="Read Messages", value=str( p.read_messages ), inline=True ) \
					.add_field( name="Send Messages", value=str( p.send_messages ), inline=True ) \
					.add_field( name="Send TTS Messages", value=str( p.send_tts_messages ), inline=True ) \
					.add_field( name="Manage Messages", value=str( p.manage_messages ), inline=True ) \
					.add_field( name="Embed Links", value=str( p.embed_links ), inline=True ) \
					.add_field( name="Attach Files", value=str( p.attach_files ), inline=True ) \
					.add_field( name="Read Message History", value=str( p.read_message_history ), inline=True ) \
					.add_field( name="Mention Everyone", value=str( p.mention_everyone ), inline=True ) \
					.add_field( name="Use External Emojis", value=str( p.external_emojis ), inline=True ) \
					.add_field( name="Change Nickname", value=str( p.change_nickname ), inline=True ) \
					.add_field( name="Manage Nicknames", value=str( p.manage_nicknames ), inline=True ) \
					.add_field( name="Manage Roles", value=str( p.manage_roles ), inline=True ) \
					.add_field( name="Manage Emojis", value=str( p.manage_emojis ), inline=True )
				await client.send_message( message.channel, "Here you go!", embed=e )
				del p
				del e
				pass
			del user
			del permparse
			del msg
			pass
		@staticmethod
		async def translate_get ( message: discord.Message ):
			# noinspection PyShadowingNames
			reader = open( f"{discord_settings}\\languages.txt", 'r' )
			ret = f"```Languages:\n{reader.read()}```"
			await client.send_message( message.channel, ret )
			reader.close( )
			del reader
			del ret
			pass
		@staticmethod
		async def translate ( message: discord.Message, prefix: str ):
			content = message.content.replace( f"{prefix}translate ", "", 1 ).split( "|" )
			ts = translate.Translator( to_lang=content[ 1 ] )
			ts.from_lang = content[ 0 ]
			tmp = str( ts.translate( content[ 2 ] ) )
			tmp = str( tmp ).replace( '["', "" ).replace( '"]', "" ).replace( "\\n", "\n" )
			msg = await client.send_message( message.channel, format_message( tmp ) )
			await client.edit_message( msg, msg.content.replace( "\\n", "\n" ).replace( "['", '' ).replace( "']", "" ) )
			del content
			del ts
			del tmp
			pass
		@staticmethod
		async def dict ( message: discord.Message, prefix: str ):
			content = message.content.replace( f"{prefix}dict ", "", 1 )
			if content.startswith( "def" ):
				content = content.replace( "def ", "", 1 )
				tmp = pydict.meaning( content )
				ret = ""
				for k in tmp.keys( ):
					ret += k + "\n"
					for v in tmp[ k ]: ret += v + "\n"
					ret += "\n"
					pass
				await client.send_message( message.channel, f"```{ret}```" )
				del tmp
				del ret
				pass
			elif content.startswith( "ant " ):
				content = content.replace( "ant ", "", 1 )
				tmp = pydict.antonym( content )
				ret = ""
				for v in tmp:
					ret += v + "\n"
					pass
				await client.send_message( message.channel, f"```{ret}```" )
				del ret
				del tmp
				pass
			elif content.startswith( "syn " ):
				content = content.replace( "syn ", "", 1 )
				tmp = pydict.synonym( content )
				ret = ""
				for v in tmp:
					ret += v + "\n"
					pass
				await client.send_message( message.channel, f"```{ret}```" )
				del tmp
				del ret
				pass
			del content
			pass
		pass
	# noinspection PyShadowingNames
	class Admin:
		@staticmethod
		async def setup ( message: discord.Message, admin_role: discord.Role ):
			# <editor-fold desc="Exclude">
			msg1 = await client.send_message( message.channel, "```Which channels would you like to exclude? Type None for no excluded channels.```" )
			msg2 = await client.wait_for_message( author=message.author, channel=message.channel )
			excludes = msg2.channel_mentions
			await client.delete_messages( [ msg1, msg2 ] )
			# </editor-fold>
			# <editor-fold desc="Admins">
			msg1 = await client.send_message( message.channel, "```Who would you like as Admins for your server? Server owners are automatically and permanently admins. Type None for no one.```" )
			msg2 = await client.wait_for_message( channel=message.channel, author=message.author )
			admins = msg2.mentions
			await client.delete_messages( [ msg1, msg2 ] )
			# </editor-fold>
			# <editor-fold desc="Marks">
			msg1 = await client.send_message( message.channel, "```What channels would you like to be marked? Type None for no channels.```" )
			msg2 = await client.wait_for_message( channel=message.channel, author=message.author )
			marks = msg2.channel_mentions
			await client.delete_messages( [ msg1, msg2 ] )
			# </editor-fold>
			# <editor-fold desc="Welcome">
			msg1 = await client.send_message( message.channel, "```What would you like the welcome message to be? Use {server} for the server name and {user} for the user name. Type None for no welcome message.```" )
			msg2 = await client.wait_for_message( channel=message.channel, author=message.author )
			welcome = msg2.content
			await client.delete_messages( [ msg1, msg2 ] )
			# </editor-fold>
			# <editor-fold desc="Goodbye">
			msg1 = await client.send_message( message.channel, "```What would you like the leave message to be? Type None for no leave message. Use {server} for the server name and {user} for the user's name.```" )
			msg2 = await client.wait_for_message( channel=message.channel, author=message.author )
			goodbye = msg2.content
			await client.delete_messages( [ msg1, msg2 ] )
			# </editor-fold>

			for _channel in excludes:
				if not _channel.id in exclude_channel_list: exclude_channel_list.append( _channel.id )
				pass
			for _user in admins:
				if not admin_role in _user.roles: await client.add_roles( _user, admin_role )
				pass
			for _channel in marks:
				if not _channel.id in marklist: marklist.append( _channel.id )
				pass

			if welcome.startswith( "read(" ):
				content = welcome.replace( "read(", "" )
				_file_cnt = content[ 0:len( content ) - 1 ]
				_file_path = f"{message.server.id}.txt"
				open( _file_path, 'w' ).write( _file_cnt )
				try: db.write( "Welcomes", { "server":message.server.id, "message":f"read( {_file_path} )" } )
				except: pass
				db.update( "Welcomes", "message", f"read( {_file_path} )", message.server.id )
				pass
			else:
				if not welcome == "None":
					try: db.write( "Welcomes", { "server":message.server.id, "message":welcome } )
					except: pass
					db.update( "Welcomes", "message", welcome, message.server.id )
					pass
				else: db.update( "Welcomes", "message", "", message.server.id )
				pass
			if not goodbye == "None": db.write( "Goodbyes", { "server":message.server.id, "message":goodbye } ); db.update( "Goodbyes", message.server.id, goodbye, message.server.id )
			await client.send_message( message.channel, "```The bot has been set up for your server!```" )
			del msg1, msg2, excludes, marks, admins, welcome, goodbye
			pass
		@staticmethod
		async def files ( message: discord.Message ):
			files = [ ]
			for channel in message.server.channels:
				try:
					try:
						_file = f"{channel}.mark.txt"
						_reader_tmp = open( f"{discord_logs}\\{message.server.name}\\{_file}", 'r' )
						tmp = _reader_tmp.read( )
						_reader_tmp.close( )
						files.append( _file )
						del tmp
						del _reader_tmp
						del _file
						pass
					except: pass
					file = f"{channel}.txt"
					reader_tmp = open( f"{discord_logs}\\{message.server.name}\\{file}", 'r' )
					tmp = reader_tmp.read( )
					reader_tmp.close( )
					files.append( file )
					del file
					del reader_tmp
					del tmp
				except: pass
				pass
			fstr = f"```" + '\n'.join( files ) + "```"
			await client.send_message( message.channel, fstr )
			del fstr
			del files
			pass
		@staticmethod
		async def changeprefix ( message: discord.Message, prefix: str ):
			new_prefix = message.content.replace( f"{prefix}changeprefix ", "" )
			if not new_prefix == "```":
				try: db.write( "Prefixes", { "server":message.server.id, "prefix":new_prefix } )
				except: pass
				db.update( "Prefixes", "prefix", new_prefix, message.server.id )
				await client.send_message( message.channel, f"Changed the prefix to {new_prefix}" )
				pass
			else:
				await client.send_message( message.channel, f"The prefix cannot be ``` because it messes up the bot's message formatting." )
				pass
			pass
		@staticmethod
		async def mute ( message: discord.Message, muted_role: discord.Role ):
			users_to_mute = list( )
			for item in message.content.split( " " ):
				if "<" in item: users_to_mute.append( discord.utils.find( lambda u:u.mention == item and not u.id == owner_id, message.server.members ) )
				else:
					try:
						_m = message.server.get_member_named( item )
						if not _m is None:
							users_to_mute.append( (message.server.get_member_named( item ) if not message.server.get_member_named( item ).id == owner_id else None) )
							pass
						pass
					except: traceback.format_exc( )
					pass
				pass
			while None in users_to_mute: users_to_mute.remove( None )
			for u in users_to_mute: await client.add_roles( u, muted_role )
			await client.send_message( message.channel, f"Muted {', '.join([str(x) for x in users_to_mute])} ({len(users_to_mute)}) users. :mute:" )
			del users_to_mute
			pass
		@staticmethod
		async def unmute ( message: discord.Message, muted_role: discord.Role ):
			users_to_mute = list( )
			for item in message.content.split( " " ):
				if "<" in item: users_to_mute.append( discord.utils.find( lambda u:u.mention == item, message.server.members ) )
				else: users_to_mute.append( message.server.get_member_named( item ) )
				pass
			while None in users_to_mute:
				users_to_mute.remove( None )
				pass
			for u in users_to_mute:
				await client.remove_roles( u, muted_role )
				pass
			await client.send_message( message.channel, f"Unmuted {', '.join([str(x) for x in users_to_mute])} ({len(users_to_mute)}) users. :loud_sound:" )
			del users_to_mute
			pass
		@staticmethod
		async def disable ( message: discord.Message, prefix: str ):
			temp = message.content.replace( f"{prefix}disable ", "" ).replace( prefix, "" )
			if temp == "[all]":
				for key in list( disables[ message.server.id ].keys( ) ): disables[ message.server.id ][ key ] = True
				pass
			else: disables[ message.server.id ][ temp ] = True
			await client.send_message( message.channel, f"Disabled {temp} :no_entry_sign:" )
			del temp
			pass
		@staticmethod
		async def enable ( message: discord.Message, prefix: str ):
			temp = message.content.replace( f"{prefix}enable ", "" ).replace( prefix, "" )
			if temp == "[all]":
				for key in list( disables[ message.server.id ].keys( ) ): disables[ message.server.id ][ key ] = False
				pass
			else: disables[ message.server.id ][ temp ] = False
			await client.send_message( message.channel, f"Enabled {temp} :white_check_mark:" )
			del temp
			pass
		@staticmethod
		async def admin ( message: discord.Message, admin_role: discord.Role, prefix: str ):
			content = message.content.replace( f"{prefix}admin ", "" )
			users = list( )
			for item in message.content.split( " " ):
				if "<" in item: users.append( discord.utils.find( lambda u:u.mention == item, message.server.members ) )
				else: users.append( message.server.get_member_named( item ) )
				pass
			while None in users:
				users.remove( None )
				pass
			if content[ 0 ] == 'a':
				added_list = [ ]
				for user in users:
					if not admin_role in user.roles: await client.add_roles( user, admin_role ); added_list.append( str( user ) )
					pass
				await client.send_message( message.channel, f"Added {', '.join(added_list)} to the admin list. :heavy_plus_sign:" )
				del added_list
				pass
			elif content[ 0 ] == 'r':
				removed_list = [ ]
				for user in users:
					if admin_role in user.roles: await client.remove_roles( user, admin_role ); removed_list.append( str( user ) )
					pass
				await client.send_message( message.channel, f"Removed {', '.join(removed_list)} from the admin list. :heavy_minus_sign:" )
				del removed_list
				pass
			elif content[ 0 ] == 's':
				ret = "```Admins:\n"
				for mem in message.server.members:
					if not discord.utils.find( lambda r:r == admin_role, mem.roles ) is None:
						ret += f"{mem}\n"
						pass
					pass
				await client.send_message( message.channel, f"{ret}```" )
				del ret
				pass
			del content
			del users
			pass
		@staticmethod
		async def channel ( message: discord.Message, prefix: str ):
			content = message.content.replace( f"{prefix}channel ", "" )
			if content.startswith( "new " ):
				content = content.replace( "new ", "", 1 )
				role = message.role_mentions[ 0 ] if len( message.role_mentions ) > 0 else None
				if isinstance( role, discord.Role ):
					them = discord.PermissionOverwrite(
						read_messages=False,
						send_messages=False,
						read_message_history=False,
						connect=False
					)
					pass
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
					pass
				# <editor-fold desc="discord.PermissionOverwrite us">
				us = discord.PermissionOverwrite(
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
				us_perms = discord.ChannelPermissions( target=(role if isinstance( role, discord.Role ) else message.server.default_role), overwrite=us )
				content = content.split( " " )
				if content[ 1 ].lower( ) == "voice": c = await client.create_channel( message.server, content[ 0 ], them_perms, us_perms, type=discord.ChannelType.voice )
				else: c = await client.create_channel( message.server, content[ 0 ], them_perms, us_perms )
				channels.append( c.id )
				await client.send_message( message.channel, f"Created {c.mention}" )
				del c
				del role
				del them
				del us
				del them_perms
				del us_perms
				pass
			elif content.startswith( 'del' ):
				try:
					for item in message.channel_mentions:
						await client.delete_channel( channel=item )
						channels.remove( item.id )
						await client.send_message( message.channel, f"Deleted {item}" )
						pass
					pass
				except:
					notify( "There was an exception!", traceback.format_exc( ) )
					await client.send_message( message.channel, "```Could not delete the channel.```" )
					print( f"{Fore.RED}Could not delete the channel.{Fore.RESET}" )
					print( traceback.format_exc( ) )
					pass
				pass
			elif content.startswith( 'show' ):
				ret = "Custom Channels:\n"
				for item in channels:
					for c in message.server.channels:
						if c.id == item: ret += f"#{item}\n"
						pass
					pass
				await client.send_message( message.channel, ret )
				del ret
				pass
			elif content.startswith( 'edit' ):
				content = content.replace( "edit ", "", 1 )
				c = message.channel_mentions[ 0 ]
				role = message.role_mentions[ 0 ] if len( message.role_mentions ) > 0 else None
				mentions = message.mentions[ 0 ] if len( message.mentions ) > 0 else None
				o = discord.PermissionOverwrite( )
				tmp = argparser.ArgParser( "&&", "=" ).parse( content )
				for key in tmp.keys( ):
					if tmp[ key ] == "True": tmp[ key ] = True
					else: tmp[ key ] = False
					pass
				o.add_reactions = tmp.get( "add_reactions" )
				o.read_messages = tmp.get( "read_messages" )
				o.send_messages = tmp.get( "send_messages" )
				o.send_tts_messages = tmp.get( "send_tts_messages" )
				o.manage_messages = tmp.get( "manage_messages" )
				o.embed_links = tmp.get( "embed_links" )
				o.attach_files = tmp.get( "attach_files" )
				o.read_message_history = tmp.get( "read_message_history" )
				o.mention_everyone = tmp.get( "mention_everyone" )
				o.external_emojis = tmp.get( "external_emojis" )
				o.connect = tmp.get( "connect" )
				o.speak = tmp.get( "speak" )
				o.use_voice_activation = tmp.get( "use_voice_activation" )
				targetA = role if not role is None else message.server.default_role
				await client.edit_channel_permissions( c, targetA if mentions is None else mentions, overwrite=o )
				await client.send_message( message.channel, f"Changed permissions for {f'<@&{role.id}>' if not role is None else f'{mentions.mention}'}" )
				del content
				del c
				del role
				del mentions
				del o
				del tmp
				del targetA
				pass
			del content
			pass
		@staticmethod
		async def say ( message: discord.Message, prefix: str ):
			if not bot_id in message.content:
				content = message.content.replace( f"{prefix}say ", "", 1 ).split( "|" )
				mentions = content[ 0 ].split( " " )
				text = content[ 1 ]
				mentions = [ client.get_channel( i.replace( "<#", "" ).replace( ">", "" ) ) for i in mentions ]
				for c in mentions: await client.send_message( c, text )
				pass
			# if not bot_id in message.content:
			# 	content = message.content.replace( f"{prefix}say ", "", 1 ).split( "|" )
			# 	for item in message.channel_mentions: await client.send_message( item, content[ 0 ], tts=ast.literal_eval( content[ 2 ].capitalize( ) ) )
			# 	del content
			# 	pass
			else:
				await client.send_message( message.channel, f"```Please don't mention the bot in your message.```" )
				pass
			pass
		@staticmethod
		async def excludechannel ( message: discord.Message ):
			eapp = exclude_channel_list.append
			for channel in message.channel_mentions:
				if not channel.id in exclude_channel_list:
					eapp( channel.id )
					await client.send_message( message.channel, f"Excluding {channel.mention} from the logs." )
					send( f"Excluding {channel.id} from the logs.", message.server.name )
					pass
				pass
			if "all" in message.content.lower:
				for channel in message.server.channels:
					if not channel.id in exclude_channel_list:
						eapp( channel.id )
						await client.send_message( message.channel, f"Excluding {channel.mention} from the logs." )
						send( f"Excluding {channel.id} from the logs.", message.server.name )
						pass
					pass
				pass
			pass
		@staticmethod
		async def includechannel ( message: discord.Message ):
			erem = exclude_channel_list.remove
			for channel in message.channel_mentions:
				if channel.id in exclude_channel_list:
					erem( channel.id )
					await client.send_message( message.channel, f"Including {channel.mention} in the logs." )
					send( f"Including {channel.mention} in the logs.", message.server.name )
					pass
				pass
			if "all" in message.content.lower:
				for channel in message.server.channels:
					if channel.id in exclude_channel_list:
						erem( channel.id )
						await client.send_message( message.channel, f"Including {channel.mention} in the logs." )
						send( f"Including {channel.mention} in the logs.", message.server.name )
						pass
					pass
				pass
			pass
		@staticmethod
		async def mark ( message: discord.Message, prefix: str ):
			content = message.content.replace( f"{prefix}mark ", "" )
			if content[ 0 ] == 'a':
				for channel in message.channel_mentions:
					if not channel.id in marklist:
						marklist.append( channel.id )
						await client.send_message( message.channel, f"Marking {channel.mention}" )
						pass
					pass
				pass
			elif content[ 0 ] == 'r':
				for channel in message.channel_mentions:
					marklist.remove( channel.id )
					await client.send_message( message.channel, f"Unmarking {channel.mention}" )
					pass
				pass
			del content
			pass
		@staticmethod
		async def exclude ( message: discord.Message, time: datetime ):
			print( f"{message.channel} ~ \"{message.content}\" ~ {message.author} ~ {time.day}.{time.month}.{time.year} {time.hour}:{time.minute} ~ {message.attachments}" )
			pass
		@staticmethod
		async def purge ( message: discord.Message, _limit: int, kwargs: dict ):
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

			if isinstance( _from, str ): _from = discord.utils.find( lambda u:u.mention == _from or u.name == _from or str( u ) == _from or u.nick == _from, message.server.members )
			if isinstance( _before, str ): _before = await client.get_message( message.channel, _before )
			if isinstance( _after, str ): _after = await client.get_message( message.channel, _after )
			if isinstance( _mentions, str ): _mentions = discord.utils.find( lambda u:u.mention == _mentions or u.name == _mentions or str( u ) == _mentions or u.nick == _mentions, message.server.members )
			if isinstance( _mentions_channel, str ): _mentions_channel = discord.utils.find( lambda c:c.mention == _mentions_channel or c.id == _mentions_channel, message.server.channels )
			if isinstance( _mentions_role, str ): _mentions_role = discord.utils.find( lambda c:c.mention == _mentions_role or c.name == _mentions_role, message.server.roles )
			def _check ( m: discord.Message ) -> bool:
				res = [ ]
				if m.author == _from or _from is None: res.append( True )
				else: res.append( False )
				if _contains is None or _contains.lower( ) in m.content.lower( ): res.append( True )
				else: res.append( False )
				if _pinned == m.pinned or _pinned is None: res.append( True )
				else: res.append( False )
				if (len( m.embeds ) > 0) == _embedded or _embedded is None: res.append( True )
				else: res.append( False )
				if (len( m.attachments ) > 0) == _attached or _attached is None: res.append( True )
				else: res.append( False )
				if _mentions in m.mentions or _mentions is None: res.append( True )
				else: res.append( False )
				if _mentions_channel in m.channel_mentions or _mentions_channel is None: res.append( True )
				else: res.append( False )
				if _mentions_role in m.role_mentions or _mentions_role is None: res.append( True )
				else: res.append( False )

				return False not in res
				pass
			__num__ = await check_purge( message, _limit, _check=_check )
			tmp = await client.send_message( message.channel, f"```Doing this will purge {__num__} messages from this channel.\nAre you sure (Y/N)?```" )
			msg_ = await client.wait_for_message( author=message.author, channel=message.channel )
			await client.delete_message( msg_ )
			await client.delete_message( tmp )
			def equals ( msg: str, *args ):
				for arg in args:
					if msg.lower( ) == arg.lower( ): return True
					pass
				return False
			if equals( msg_.content, "yes", "yay", "yup", "y" ):
				# noinspection PyUnresolvedReferences
				purged_messages = await client.purge_from( message.channel, limit=_limit, check=lambda m:_check( m ), before=_before, after=_after )
				tmp = await client.send_message( message.channel, f"```Purged {len(purged_messages)} messages!```" )
				await sleep( 3 )
				await client.delete_message( tmp )
				del purged_messages
				pass
			else:
				tmp = await client.send_message( message.channel, f"```Canceled the purge.```" )
				await sleep( 3 )
				await client.delete_message( tmp )
				pass
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
			pass
		@staticmethod
		async def loose_purge ( message: discord.Message ):
			# noinspection PyUnresolvedReferences
			purged_messages = await client.purge_from( message.channel, limit=100 )
			tmp = await client.send_message( message.channel, f"```Purged {len(purged_messages)} messages!```" )
			await sleep( 3 )
			await client.delete_message( tmp )
			del purged_messages
			del tmp
			pass
		@staticmethod
		async def welcome ( message: discord.Message, prefix: str ):
			content = message.content.replace( f"{prefix}welcome ", "" )
			if content.startswith( "read(" ):
				content = content.replace( "read(", "" )
				_file_cnt = content[ 0:len( content ) - 1 ]
				_file_path = f"{message.server.id}.txt"
				open( _file_path, 'w' ).write( _file_cnt )
				try: db.write( "Welcomes", { "server":message.server.id, "message":f"read( {_file_path} )" } )
				except: pass
				db.update( "Welcomes", "message", f"read( {_file_path} )", message.server.id )
				pass
			else:
				if not content == "None":
					try: db.write( "Welcomes", { "server":message.server.id, "message":content } )
					except: pass
					db.update( "Welcomes", "message", content, message.server.id )
					pass
				else: db.update( "Welcomes", "message", "", message.server.id )
				pass
			await client.send_message( message.channel, "```Welcome message set!```" )
			del content
			pass
		@staticmethod
		async def goodbye ( message: discord.Message, prefix: str ):
			content = message.content.replace( f"{prefix}goodbye ", "" )
			db.write( "Goodbyes", { "server":message.server.id, "message":content } )
			db.update( "Goodbyes", message.server.id, content, message.server.id )
			await client.send_message( message.channel, "```Goodbye message set!```" )
			del content
			pass
		@staticmethod
		async def show_welcome ( message: discord.Message ):
			try: await client.send_message( message.channel, db.read( "Welcomes", message.server.id ) )
			except: await client.send_message( message.channel, "```No welcome message has been set!```" )
			pass
		@staticmethod
		async def show_goodbye ( message: discord.Message ):
			try: await client.send_message( message.channel, db.read( "Goodbyes", message.server.id ) )
			except: await client.send_message( message.channel, "```No goodbye message has been set!```" )
			pass
		@staticmethod
		async def prunes ( message: discord.Message, prefix: str ):
			cont = message.content.replace( f"{prefix}prunes ", "" )
			days = int( cont )
			# noinspection PyUnresolvedReferences
			n = await client.estimate_pruned_members( message.server, days=days )
			await client.send_message( message.channel, f"```{n} members will be pruned.```" )
			del cont
			del days
			del n
			pass
		@staticmethod
		async def prune ( message: discord.Message, prefix: str ):
			days = int( message.content.replace( f"{prefix}prune ", "" ) )
			# noinspection PyUnresolvedReferences
			est = await client.estimate_pruned_members( message.server, days=days )
			await client.send_message( message.channel, f"```Are you sure you want to prune {est} members (y/n)?```" )
			msg = await client.wait_for_message( author=message.author, channel=message.channel )
			if msg.content.lower( ) == "y":
				# noinspection PyUnresolvedReferences
				pruned_members = await client.prune_members( message.server, days=days )
				await client.send_message( message.channel, f"```{pruned_members} members removed.```" )
				del pruned_members
				pass
			else:
				await client.send_message( message.channel, f"```Canceled the prune.```" )
				pass
			del days
			pass
		@staticmethod
		async def kick ( message: discord.Message, admin_role: discord.Role ):
			for user in message.mentions:
				if not admin_role in user.roles: await client.kick( user ); await client.send_message( message.channel, f"{user} has been kicked!" )
				else: await client.send_message( message.channel, "You cannot kick bot admins!" )
				pass
			pass
		@staticmethod
		async def ban ( message: discord.Message, admin_role: discord.Role ):
			for item in message.mentions:
				if not admin_role in item.roles: await client.ban( item ); await client.send_message( message.channel, f"{item} has been banned." )
				else: await client.send_message( message.channel, f"You cannot ban bot admins!" )
				pass
			pass
		@staticmethod
		async def join_role ( message: discord.Message, prefix: str ):
			cnt = message.content.replace( f"{prefix}joinrole ", "" )
			role = discord.utils.find( lambda r:r.name == cnt or r.id == cnt or r.mention == cnt, message.server.roles )
			try: join_roles[ message.server.id ] = role.id
			except: join_roles[ message.server.id ] = "None"
			await client.send_message( message.channel, f"```Set the join role to {role}.```" )
			pass
		@staticmethod
		async def defaultchannel ( message: discord.Message ):
			channel = message.channel_mentions[ 0 ]
			default_channel[ message.server.id ] = channel.id
			await client.send_message( message.channel, f"Default channel set to #{channel}." )
			del channel
			pass
		@staticmethod
		async def get_defaultchannel ( message: discord.Message ):
			await client.send_message( message.channel, f"Default channel is #{client.get_channel(default_channel[message.server.id])}" )
			pass
		pass
	class Owner:
		@staticmethod
		async def exit ( ):
			global exiting
			exiting = True
			await client.logout( )
			pass
		@staticmethod
		async def info ( message ):
			_channels = list( client.get_all_channels( ) )
			_members = list( client.get_all_members( ) )
			_servers = list( client.servers )
			_messages = list( client.messages )
			_users = [ ]
			uapp = _users.append
			for mem in _members:
				if not mem.id in _users:
					uapp( mem.id )
					pass
				pass
			time_t = 0.0
			for t in times: time_t += t
			print( time_t )
			try: time_t /= len( times )
			except: time_t = 0.0
			logbot_process = psutil.Process( os.getpid( ) )
			RAM = round( logbot_process.memory_info( )[ 0 ] / float( 2 ** 20 ), 1 )
			dt = datetime.now( )
			time_t = decimal.Decimal( time_t )
			e = discord.Embed( name="LogBot Information", description="Information on this running instance of LogBot.", colour=discord.Colour.gold( ) ) \
				.add_field( name="Visible Channels", value=str( len( _channels ) ) ) \
				.add_field( name="Visible Members", value=str( len( _members ) ) ) \
				.add_field( name="Servers", value=str( len( _servers ) ) ) \
				.add_field( name="Messages", value=str( len( _messages ) ) ) \
				.add_field( name="RAM Usage (MB)", value=str( RAM ) + "MB" ) \
				.add_field( name="Average Response Time", value=f"{time_t:1.5} seconds" ) \
				.add_field( name="Discord Version", value=discord.__version__ ) \
				.add_field( name="LogBot Version", value=version ) \
				.add_field( name="Online For", value=str( (dt - bootup_time) ).split( "." )[ 0 ].replace( ":", "h ", 1 ).replace( ":", "m ", 1 ) + "s" ) \
				.add_field( name="Total Users", value=str( len( _users ) ) )
			await client.send_message( message.channel, "My Information:", embed=e )
			del _channels
			del _members
			del _servers
			del _messages
			del time_t
			del logbot_process
			del RAM
			del dt
			del e
			pass
		@staticmethod
		async def refresh ( ):
			global icon
			os.system( "cls" )
			print( f"{Fore.MAGENTA}Signed in and waiting...\nRunning version: LogBot Version {version}{Fore.RESET}" )
			await client.change_presence( game=None, status=discord.Status.online )
			icon = Qt.QIcon( selected_image )
			sti.setIcon( icon )
			pass
		pass
	class DM:
		@staticmethod
		async def info ( message: discord.Message ):
			_channels = list( client.get_all_channels( ) )
			_members = list( client.get_all_members( ) )
			_servers = list( client.servers )
			_messages = list( client.messages )
			time_t = 0.0
			for t in times: time_t += t
			print( time_t )
			try: time_t /= len( times )
			except: time_t = 0.0
			logbot_process = psutil.Process( os.getpid( ) )
			RAM = round( logbot_process.memory_info( )[ 0 ] / float( 2 ** 20 ), 1 )
			dt = datetime.now( )
			time_t = decimal.Decimal( time_t )
			# <editor-fold desc="Embed">
			e = discord.Embed( name="LogBot Information", description="Information on this running instance of LogBot.", colour=discord.Colour.gold( ) )
			e.add_field( name="Visible Channels", value=str( len( _channels ) ) )
			e.add_field( name="Visible Members", value=str( len( _members ) ) )
			e.add_field( name="Servers", value=str( len( _servers ) ) )
			e.add_field( name="Messages", value=str( len( _messages ) ) )
			e.add_field( name="RAM Usage (MB)", value=str( RAM ) + "MB" )
			e.add_field( name="Average Response Time", value=f"{time_t:1.5} seconds" )
			e.add_field( name="Discord Version", value=discord.__version__ )
			e.add_field( name="LogBot Version", value=version )
			e.add_field( name="Online For", value=str( (dt - bootup_time) ).split( "." )[ 0 ].replace( ":", "h ", 1 ).replace( ":", "m ", 1 ) + "s" )
			await client.send_message( message.channel, "My Information:", embed=e )
			# </editor-fold>
			del e
			del time_t
			del dt
			del RAM
			del logbot_process
			del _channels
			del _messages
			del _members
			del _servers
			pass
		@staticmethod
		async def planned ( message: discord.Message ):
			tmp = '\n'.join( planned )
			await client.send_message( message.channel, f"```Coming Soon:\n{tmp}```" )
			del tmp
			pass
		@staticmethod
		async def translate ( message: discord.Message ):
			content = message.content.replace( f"$translate ", "", 1 ).split( "|" )
			tmp = translate.Translator( from_lang=content[ 0 ], to_lang=content[ 1 ] ).translate( content[ 2 ] )
			await client.send_message( message.channel, format_message( tmp ) )
			del content
			del tmp
			pass
		@staticmethod
		async def translate_get ( message: discord.Message ):
			lang_reader = open( f"{discord_settings}\\languages.txt", 'r' )
			ret = f"```Languages:\n{lang_reader.read()}```"
			await client.send_message( message.channel, ret )
			lang_reader.close( )
			del lang_reader
			del ret
			pass
		@staticmethod
		async def wiki ( message: discord.Message ):
			content = message.content.replace( f"$wiki ", "" )
			await client.send_typing( message.channel )
			try: info = wikipedia.summary( content )
			except:
				search = wikipedia.search( content )
				search_str = '\n'.join( [ item for item in search ] )
				await client.send_message( message.channel, f"```I found these results:\nSearched Item: {search_str}```" )
				msg = await client.wait_for_message( author=message.author )
				info = wikipedia.summary( msg.content )
				pass
			msgs = format_message( info )
			for item in msgs: await client.send_message( message.channel, item )
			pass
		@staticmethod
		async def updates ( message: discord.Message ):
			tmp = '\n'.join( whats_new )
			await client.send_message( message.channel, f"```Updates:\n{tmp}```" )
			del tmp
			pass
		@staticmethod
		async def refresh ( ):
			global icon
			os.system( "cls" )
			print( f"{Fore.MAGENTA}Signed in and waiting...\nRunning version: LogBot Version {version}{Fore.RESET}" )
			icon = Qt.QIcon( selected_image )
			sti.setIcon( icon )
			pass
		@staticmethod
		async def exit ( ):
			await client.logout( )
			pass
		@staticmethod
		async def update ( message: discord.Message ):
			m = await client.send_message( message.channel, "```Updating...```" )
			print( f"{Fore.LIGHTCYAN_EX}Updating...{Fore.RESET}" )
			await client.close( )
			update( m.id, message.channel.id )
			pass
		@staticmethod
		async def suggest ( message: discord.Message ):
			suggestion = message.content \
				.replace( f"$suggest ", "", 1 ) \
				.replace( "`", "\\`" ) \
				.replace( "```", "\\```" )
			# <editor-fold desc="WRITER: suggestions">
			writer = open( suggestions, 'a' )
			writer.write( f"\n[{message.author}] {suggestion}" )
			writer.close( )
			# </editor-fold>
			await client.send_message( message.channel, "```Thank you for your suggestion.```" )
			print( f"{Fore.YELLOW}{message.author} gave you a suggestion.{Fore.RESET}" )
			pass
		@staticmethod
		async def suggestions ( message: discord.Message ):
			# <editor-fold desc="READER: suggestions">
			s_reader = open( suggestions, 'r' )
			ret = f"Suggestions:{s_reader.read()}"
			s_reader.close( )
			# </editor-fold>
			for item in format_message( ret ): await client.send_message( message.channel, item )
			del ret
			del s_reader
			pass
		@staticmethod
		async def query ( message: discord.Message ):
			try:
				content = message.content.replace( f"$query ", "" )
				await client.send_typing( message.channel )
				res = wclient.query( content )
				ret = ""
				for pod in res.pods:
					for item in pod.texts: ret += f"{pod.title}: {item}\n"
					pass
				ret += "Powered by Wolfram|Alpha"
				[ await client.send_message( message.channel, m ) for m in format_message( ret ) ]
				del ret
				del res
				del content
				pass
			except:
				notify( "There was an exception!", traceback.format_exc( ) )
				await client.send_message( message.channel, "```We couldn't get that information.```" )
				print( f"{Fore.LIGHTGREEN_EX}{message.author} attempted to use $query, but failed.{Fore.RESET}" )
				print( traceback.format_exc( ) )
				pass
			pass
		@staticmethod
		async def dict ( message: discord.Message ):
			content = message.content.split( " " )
			content.remove( content[ 0 ] )
			if content[ 0 ].startswith( "def" ):
				tmp = pydict.meaning( content[ 1 ] )
				ret = str
				for k in tmp.keys( ):
					ret += f"{k}\n"
					for v in tmp[ k ]: ret += f"{v}\n"
					ret += "\n"
					pass
				await client.send_message( message.channel, f"```{ret}```" )
				del tmp
				del ret
				pass
			elif content[ 0 ].startswith( "ant" ):
				tmp = pydict.antonym( content[ 1 ] )
				ret = ""
				for v in tmp: ret += f"{v}\n"
				await client.send_message( message.channel, f"```{ret}```" )
				del tmp
				del ret
				pass
			elif content[ 0 ].startswith( "syn" ):
				tmp = pydict.synonym( content[ 1 ] )
				ret = str
				for v in tmp: ret += f"{v}\n"
				await client.send_message( message.channel, f"```{ret}```" )
				del tmp
				del ret
				pass
			del content
			pass
		pass
	pass

@client.event
async def sendNoPerm ( message: discord.Message ):
	"""
	Sends a message telling a user that he/she does not have the necessary permissions to use a command.
	:param message: The message object from on_message.
	"""
	await client.send_message( message.channel, "```You do not have permission to use this command.```" )
	print( f"{Fore.LIGHTGREEN_EX}{message.author} attempted to use a command.{Fore.RESET}" )
	pass

# <editor-fold desc="Message Updates">
# noinspection PyShadowingNames
@client.event
async def on_message ( message: discord.Message ):
	global default_channel
	try:
		if default_channel.get( message.server.id ) is None: default_channel[ message.server.id ] = message.server.default_channel.id
	except: pass

	muted_role = discord.utils.find( lambda r:r.name == "LogBot Muted", message.server.roles )

	if muted_role in message.author.roles and not message.author == message.server.owner: await client.delete_message( message )

	msgcont = message.content if is_ascii( message.content ) else u"{}".format( message.content )
	# noinspection PyShadowingNames
	def startswith ( *msg: str, val: str = message.content, modifier: str = "" ) -> bool:
		"""
		Checks if `val` starts with any string in `msg`.
		:param msg: Several str type parameters.
		:param val: The string to compare msg to.
		:param modifier: A special operation to perform on val. Can be "lower", "upper", or "capitalize"
		:return: True if a value in msg is at the beginning of val, False if not.
		"""
		if modifier == "lower": val = val.lower( )
		if modifier == "upper": val = val.upper( )
		if modifier == "capitalize": val = val.capitalize( )
		# noinspection PyShadowingNames
		for m in msg:
			if val.startswith( m ):
				return True
			pass
		return False
	if not message.channel.is_private and not muted_role in message.author.roles:
		admin_role = discord.utils.find( lambda r:r.name == "LogBot Admin", message.server.roles )

		if not message.server.id in list( disables.keys( ) ): disables[ message.server.id ] = {
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
		if not isinstance( disables[ message.server.id ], dict ): disables[ message.server.id ] = {
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

		sort( )

		# save( message.server.id )
		time = format_time( message.timestamp )

		try: prefix = db.read( "Prefixes", message.server.id )
		except: prefix = "$"; traceback.format_exc( ); db.write( "Prefixes", { "server":message.server.id, "prefix":"$" } )

		if startswith( prefix ):
			if startswith( f"{prefix}exclude ", f"{prefix}ex " ):
				if (admin_role in message.author.roles and not disables[ message.server.id ].get( "exclude" ) is True) or message.author.id == owner_id: await Commands.Admin.exclude( message, time )
				elif disables[ message.server.id ][ "exclude" ]: await client.send_message( message.channel, "```That command has been disabled!```" )
				else: await sendNoPerm( message )
				pass
			elif startswith( f"{prefix}excludechannel ", f"{prefix}exc " ):
				if (admin_role in message.author.roles and not disables[ message.server.id ].get( "excludechannel" ) is True) or message.author.id == owner_id:
					await Commands.Admin.excludechannel( message )
					pass
				elif disables[ message.server.id ][ "excludechannel" ]: await client.send_message( message.channel, "```That command has been disabled!```" )
				else:
					await sendNoPerm( message )
					pass
				pass
			elif startswith( f"{prefix}includechannel ", f"{prefix}inc " ):
				if (admin_role in message.author.roles and not disables[ message.server.id ].get( "includechannel" ) is True) or message.author.id == owner_id:
					await Commands.Admin.includechannel( message )
					pass
				elif disables[ message.server.id ][ "includechannel" ]: await client.send_message( message.channel, "```That command has been disabled!```" )
				else:
					await sendNoPerm( message )
					pass
				pass
			elif startswith( f"{prefix}mark " ):
				if (admin_role in message.author.roles and not disables[ message.server.id ].get( "mark" ) is True) or message.author.id == owner_id:
					await Commands.Admin.mark( message, prefix )
					pass
				elif disables[ message.server.id ][ "mark" ]: await client.send_message( message.channel, "```That command has been disabled!```" )
				else:
					await sendNoPerm( message )
					pass
				pass
			elif startswith( f"{prefix}admin " ):
				if admin_role in message.author.roles or message.author.id == owner_id:
					await Commands.Admin.admin( message, admin_role, prefix )
					pass
				else:
					await sendNoPerm( message )
					pass
				pass
			elif startswith( f"{prefix}showlist" ):
				if not disables[ message.server.id ].get( "showlist" ) is True or message.author.id == owner_id:
					await Commands.Member.showlist( message )
					pass
				elif disables[ message.server.id ][ "showlist" ]: await client.send_message( message.channel, "```That command has been disabled!```" )
				else:
					await sendNoPerm( message )
					pass
				pass
			elif startswith( f"{prefix}showmarks" ):
				if not disables[ message.server.id ].get( "showmarks" ) is True or message.author.id == owner_id:
					await Commands.Member.showmarks( message )
					pass
				elif disables[ message.server.id ][ "showmarks" ]: await client.send_message( message.channel, "```That command has been disabled!```" )
				else:
					await sendNoPerm( message )
					pass
				pass
			elif startswith( f"{prefix}version" ):
				await client.send_message( message.channel, f"```LogBot Version {version}```" )
				pass
			elif startswith( f"{prefix}channel " ):
				if (admin_role in message.author.roles and not disables[ message.server.id ].get( "channel" ) is True) or message.author.id == owner_id:
					await Commands.Admin.channel( message, prefix )
					pass
				elif disables[ message.server.id ][ "channel" ]: await client.send_message( message.channel, "```That command has been disabled!```" )
				else:
					await sendNoPerm( message )
					pass
				pass
			elif startswith( f"{prefix}updates" ):
				await Commands.Member.updates( message )
				pass
			elif startswith( f"{prefix}say" ):
				if (admin_role in message.author.roles and not disables[ message.server.id ].get( "say" ) is True) or message.author.id == owner_id:
					await Commands.Admin.say( message, prefix )
					pass
				elif disables[ message.server.id ][ "say" ]: await client.send_message( message.channel, "```That command has been disabled!```" )
				else:
					await sendNoPerm( message )
					pass
				pass
			elif startswith( f"{prefix}planned" ):
				await Commands.Member.planned( message )
				pass
			# elif startswith( f"{prefix}cmd " ):
			# 	if not disables[message.server.id].get( "cmd" ) is True or message.author.id == owner_id:
			# 		await Commands.Member.cmd( message )
			# 		pass
			# 	elif disables[ message.server.id ][ "cmd" ]:
			# 		await await client.send_message( message.channel, "```That command has been disabled!```" )
			# 		pass
			# 	else:
			# 		await sendNoPerm( message )
			# 		pass
			# 	pass
			elif startswith( f"{prefix}query " ):
				if not disables[ message.server.id ].get( "query" ) is True or message.author.id == owner_id:
					await Commands.Member.query( message, prefix )
					pass
				elif disables[ message.server.id ][ "query" ]: await client.send_message( message.channel, "```That command has been disabled!```" )
				else:
					await sendNoPerm( message )
					pass
				pass
			elif startswith( f"{prefix}wiki " ):
				if not disables[ message.server.id ].get( "wiki" ) is True or message.author.id == owner_id:
					await Commands.Member.wiki( message, prefix )
					pass
				elif disables[ message.server.id ][ "wiki" ]: await client.send_message( message.channel, "```That command has been disabled!```" )
				else:
					await sendNoPerm( message )
					pass
				pass
			elif startswith( f"{prefix}disable " ):
				if admin_role in message.author.roles or message.author.id == owner_id:
					await Commands.Admin.disable( message, prefix )
					pass
				else:
					await sendNoPerm( message )
					pass
				pass
			elif startswith( f"{prefix}enable " ):
				if admin_role in message.author.roles or message.author.id == owner_id:
					await Commands.Admin.enable( message, prefix )
					pass
				else:
					await sendNoPerm( message )
					pass
				pass
			elif startswith( f"{prefix}suggest " ):
				await Commands.Member.suggest( message, prefix )
				pass
			elif startswith( f"{prefix}decide " ):
				if not disables[ message.server.id ].get( "decide" ) is True or message.author.id == owner_id:
					await Commands.Member.decide( message, prefix )
					pass
				elif disables[ message.server.id ][ "decide" ]: await client.send_message( message.channel, "```That command has been disabled!```" )
				else:
					await sendNoPerm( message )
					pass
				pass
			elif startswith( f"{prefix}disables" ):
				await Commands.Member.disables( message, prefix )
				pass
			elif startswith( f"{prefix}welcome " ):
				if (admin_role in message.author.roles and not disables[ message.server.id ].get( "welcome" ) is True) or message.author.id == owner_id:
					await Commands.Admin.welcome( message, prefix )
					pass
				elif disables[ message.server.id ][ "welcome" ]: await client.send_message( message.channel, "```That command has been disabled!```" )
				else:
					await sendNoPerm( message )
					pass
				pass
			elif startswith( f"{prefix}goodbye " ):
				if (admin_role in message.author.roles and not disables[ message.server.id ].get( "goodbye" ) is True) or message.author.id == owner_id:
					await Commands.Admin.goodbye( message, prefix )
					pass
				elif disables[ message.server.id ][ "goodbye" ]: await client.send_message( message.channel, "```That command has been disabled!```" )
				else:
					await sendNoPerm( message )
					pass
				pass
			elif startswith( f"{prefix}welcome" ):
				if (admin_role in message.author.roles and not disables[ message.server.id ].get( "welcome" ) is True) or message.author.id == owner_id:
					await Commands.Admin.show_welcome( message )
					pass
				elif disables[ message.server.id ][ "welcome" ]: await client.send_message( message.channel, "```That command has been disabled!```" )
				else:
					await sendNoPerm( message )
					pass
				pass
			elif startswith( f"{prefix}goodbye" ):
				if (admin_role in message.author.roles and not disables[ message.server.id ].get( "goodbye" ) is True) or message.author.id == owner_id:
					await Commands.Admin.show_goodbye( message )
					pass
				elif disables[ message.server.id ][ "goodbye" ]: await client.send_message( message.channel, "```That command has been disabled!```" )
				else:
					await sendNoPerm( message )
					pass
				pass
			elif startswith( f"{prefix}prunes " ):
				if (admin_role in message.author.roles and not disables[ message.server.id ].get( "prune" ) is True) or message.author.id == owner_id:
					await Commands.Admin.prunes( message, prefix )
					pass
				elif disables[ message.server.id ][ "prune" ]: await client.send_message( message.channel, "```That command has been disabled!```" )
				else:
					await sendNoPerm( message )
					pass
				pass
			elif startswith( f"{prefix}prune " ):
				if (admin_role in message.author.roles and not disables[ message.server.id ].get( "prune" ) is True) or message.author.id == owner_id:
					await Commands.Admin.prune( message, prefix )
					pass
				elif disables[ message.server.id ][ "prune" ]: await client.send_message( message.channel, "```That command has been disabled!```" )
				else:
					await sendNoPerm( message )
					pass
				pass
			elif startswith( f"{prefix}user:" ):
				if not disables[ message.server.id ].get( "user" ) is True or message.author.id == owner_id: await Commands.Member.user_restrict( message, prefix )
				elif disables[ message.server.id ][ "user" ]: await client.send_message( message.channel, "```That command has been disabled!```" )
				pass
			elif startswith( f"{prefix}user" ):
				if not disables[ message.server.id ].get( "user" ) is True or message.author.id == owner_id: await Commands.Member.user( message, prefix )
				elif disables[ message.server.id ][ "user" ]: await client.send_message( message.channel, "```That command has been disabled!```" )
				else: await sendNoPerm( message )
				pass
			elif startswith( f"{prefix}invite" ):
				await client.send_message( message.channel, "https://discordapp.com/oauth2/authorize?client_id=255379748828610561&scope=bot&permissions=268696670" )
				pass
			elif startswith( f"{prefix}purge " ):
				if (admin_role in message.author.roles and not disables[ message.server.id ].get( "purge" ) is True) or message.author.id == owner_id:
					tmp = message.content.replace( f"{prefix}purge ", "" )
					switches = purge_parser.parse( tmp )
					await Commands.Admin.purge( message, int( switches.get( "limit" ) ) if not switches.get( "limit" ) is None else 100, switches )
					pass
				elif disables[ message.server.id ][ "purge" ]: await client.send_message( message.channel, "```That command has been disabled!```" )
				else:
					await sendNoPerm( message )
					pass
				pass
			elif startswith( f"{prefix}purge" ):
				if (admin_role in message.author.roles and not disables[ message.server.id ].get( "purge" ) is True) or message.author.id == owner_id:
					await Commands.Admin.loose_purge( message )
					pass
				elif disables[ message.server.id ][ "purge" ]: await client.send_message( message.channel, "```That command has been disabled!```" )
				else:
					await sendNoPerm( message )
					pass
				pass
			elif startswith( f"{prefix}kick " ):
				if admin_role in message.author.roles or message.author.id == owner_id:
					await Commands.Admin.kick( message, admin_role )
					pass
				else:
					await sendNoPerm( message )
					pass
				pass
			elif startswith( f"{prefix}ban " ):
				if admin_role in message.author.roles or message.author.id == owner_id:
					await Commands.Admin.ban( message, admin_role )
					pass
				else:
					await sendNoPerm( message )
					pass
				pass
			elif startswith( f"{prefix}permissions" ):
				if not disables[ message.server.id ].get( "permissions" ) is True: await Commands.Member.user_permissions( message, prefix )
				else: await client.send_message( message.channel, "```That command has been disabled!```" )
				pass
			elif startswith( f"{prefix}translate.get" ):
				if not disables[ message.server.id ].get( "translate" ) is True or message.author.id == owner_id:
					await Commands.Member.translate_get( message )
					pass
				elif disables[ message.server.id ][ "translate" ]: await client.send_message( message.channel, "```That command has been disabled!```" )
				else:
					await sendNoPerm( message )
					pass
				pass
			elif startswith( f"{prefix}translate " ):
				if not disables[ message.server.id ].get( "translate" ) is True or message.author.id == owner_id:
					await Commands.Member.translate( message, prefix )
					pass
				elif disables[ message.server.id ][ "translate" ]: await client.send_message( message.channel, "```That command has been disabled!```" )
				else:
					await sendNoPerm( message )
					pass
				pass
			elif startswith( f"{prefix}dm" ):
				await client.send_message( message.author, f"Welcome, {message.author.name}" )
				pass
			elif startswith( f"{prefix}fetch " ):
				if admin_role in message.author.roles or message.author.id == owner_id:
					_file = f"{discord_logs}\\{message.server.name}\\{message.content.replace(f'{prefix}fetch ', '')}"
					if not _file.endswith( '.txt' ): _file += ".txt"
					await client.send_file( message.channel, f"{_file}" )
					pass
				else:
					await sendNoPerm( message )
					pass
				pass
			elif startswith( f"{prefix}refresh" ):
				if message.author.id == owner_id:
					await Commands.Owner.refresh( )
					pass
				else:
					await sendNoPerm( message )
					pass
				pass
			elif startswith( f"{prefix}dict " ):
				if not disables[ message.server.id ].get( "dict" ) is True: await Commands.Member.dict( message, prefix )
				else: await client.send_message( message.channel, "```That command has been disabled!```" )
				pass
			elif startswith( f"{prefix}setup" ):
				if message.author.id == message.server.owner.id or message.author.id == owner_id:
					await Commands.Admin.setup( message, admin_role )
					pass
				else:
					await sendNoPerm( message )
					pass
				pass
			elif startswith( f"{prefix}server" ):
				if not disables[ message.server.id ].get( "server" ) is True: await Commands.Member.server( message )
				else: await client.send_message( message.channel, "```That command has been disabled!```" )
				pass
			elif startswith( f"{prefix}convert " ):
				if not disables[ message.server.id ].get( "convert" ) is True: await Commands.Member.convert( message, prefix )
				else: await client.send_message( message.channel, "```That command has been disabled!```" )
				pass
			elif startswith( f"{prefix}mute " ):
				if admin_role in message.author.roles or message.author.id == owner_id:
					await Commands.Admin.mute( message, muted_role )
					pass
				else:
					await sendNoPerm( message )
					pass
				pass
			elif startswith( f"{prefix}unmute " ):
				if admin_role in message.author.roles or message.author.id == owner_id:
					await Commands.Admin.unmute( message, muted_role )
					pass
				else:
					await sendNoPerm( message )
					pass
				pass
			elif startswith( f"{prefix}mutes" ):
				await Commands.Member.mutes( message, muted_role )
				pass
			elif startswith( f"{prefix}ping" ):
				await Commands.Member.ping( message )
				pass
			elif startswith( f"{prefix}clear" ):
				if admin_role in message.author.roles or message.author.id == owner_id:
					messages = list( client.messages )
					mtd = [ m if m.channel == message.channel else None for m in messages ]
					remove = mtd.remove
					while None in mtd: remove( None )
					for m in mtd:
						# print(f"{m.author} ~ {m.content} ~ {len(m.attachments)}")
						await client.delete_message( m )
						pass
					pass
				pass
			elif startswith( f"{prefix}hq" ):
				await client.send_message( message.channel, hq_link )
				pass
			elif startswith( f"{prefix}git" ):
				await client.send_message( message.channel, git_link )
				pass
			elif startswith( f"{prefix}joinrole " ):
				if (admin_role in message.author.roles and not disables[ message.server.id ].get( "welcome" ) is True) or message.author.id == owner_id: await Commands.Admin.join_role( message, prefix )
				elif disables[ message.server.id ][ "welcome" ]: await client.send_message( message.channel, "```That command has been disabled!```" )
				else: sendNoPerm( message )
				pass
			elif startswith( f"{prefix}joinrole" ):
				if not disables[ message.server.id ].get( "welcome" ) is True or message.author.id == owner_id:
					role = discord.utils.find( lambda r:r.id == join_roles[ message.server.id ], message.server.roles )
					await client.send_message( message.channel, f"Join Role for {message.server.name}: {role}" )
					pass
				elif disables[ message.server.id ][ "welcome" ]: await client.send_message( message.channel, "```That command has been disabled!```" )
				else: sendNoPerm( message )
				pass
			elif startswith( f"{prefix}logchannel " ):
				if admin_role in message.author.roles:
					cmentions = message.channel_mentions
					if len( cmentions ) > 0:
						c = cmentions[ 0 ].id
						parser[ message.server.id ][ "logchannel" ] = c
						await client.send_message( message.channel, f"```Set the log channel to {cmentions[0]}```" )
						del c
						pass
					else:
						parser[ message.server.id ][ "logchannel" ] = "None"
						await client.send_message( message.channel, f"```Set the log channel to None```" )
						pass
					del cmentions
					pass
				else: sendNoPerm( message )
				pass
			elif startswith( f"{prefix}logchannel" ):
				if admin_role in message.author.roles:
					c = client.get_channel( parser[ message.server.id ][ "logchannel" ] )
					if c is None: await client.send_message( message.channel, "```There is no log channel.```" )
					else: await client.send_message( message.channel, f"```The log channel is #{c}.```" )
					del c
					pass
				else: sendNoPerm( message )
				pass
			elif startswith( f"{prefix}roll" ):
				if not disables[ message.server.id ].get( "roll" ) is True: await client.send_message( message.channel, f"You rolled {random.choice(range(1, int(message.content.replace('{prefix}roll ', ''))))}!" )
				else: await client.send_message( message.channel, "```That command has been disabled!```" )
				pass
			elif startswith( f"{prefix}channels" ):
				await Commands.Member.channels( message )
				pass
			elif startswith( f"{prefix}defaultchannel " ):
				if admin_role in message.author.roles or message.author.id == owner_id: await Commands.Admin.defaultchannel( message )
				else: sendNoPerm( message )
				pass
			elif startswith( f"{prefix}defaultchannel" ):
				if admin_role in message.author.roles or message.author.id == owner_id: await Commands.Admin.get_defaultchannel( message )
				else: sendNoPerm( message )
				pass
			elif startswith( f"{prefix}simwelcome" ):
				if message.author.id == owner_id: await on_member_join( message.author )
				pass
			elif startswith( f"{prefix}simgoodbye" ):
				if message.author.id == owner_id: await on_member_remove( message.author )
				pass
			elif startswith( f"{prefix}changeprefix " ):
				if admin_role in message.author.roles or message.author.id == owner_id: await Commands.Admin.changeprefix( message, prefix )
				else: sendNoPerm( message )
				pass
			elif startswith( f"{prefix}prefix" ):
				await client.send_message( message.channel, f"The prefix is {prefix}" )
				pass
			elif startswith( f"{prefix}role " ):
				await Commands.Member.role( message, prefix )
				pass
			elif startswith( f"{prefix}urban " ):
				if not disables[ message.server.id ].get( "urban" ) is True: await Commands.Member.urban( message, prefix )
				else: await client.send_message( message.channel, "```That command has been disabled!```" )
				pass
			elif startswith( f"{prefix}files" ):
				if admin_role in message.author.roles or message.author.id == owner_id: await Commands.Admin.files( message )
				pass
			elif startswith( f"{prefix}gif" ):
				if not disables[ message.server.id ][ "gif" ] or message.author.id == owner_id: await Commands.Member.gif( message, prefix )
				else: await client.send_message( message.channel, "```That command has been disabled!```" )
				pass
			elif startswith( f"{prefix}sf " ):
				num = message.content.replace( f'{prefix}sf ', '' )
				org_num = num
				sfs = 0
				dot_found = False
				while num[ 0 ] == "0" or num[ 0 ] == ".":
					if num[ 0 ] == ".": dot_found = True
					num = num[ 1: ]
					pass
				if "." in num: sfs = len( num ) - 1
				elif dot_found: sfs = len( num )
				else:
					while num[ -1 ] == "0": num = num[ 0:len( num ) - 1 ]
					sfs = len( num )
					pass
				await client.send_message( message.channel, f"```{org_num} has {sfs} significant figures ({num})!```" )
				pass

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
			# 	pass
			pass
		elif startswith( f"$update", "logbot.update" ):
			if message.author.id == owner_id:
				m = await client.send_message( message.channel, "```Updating...```" )
				print( f"{Fore.LIGHTCYAN_EX}Updating...{Fore.RESET}" )
				await client.close( )
				update( m.id, message.channel.id )
				pass
			else: await sendNoPerm( message )
			pass
		elif startswith( "logbot.exit", "$exit" ):
			if message.author.id == owner_id: await Commands.Owner.exit( )
			else: await sendNoPerm( message )
			pass
		elif startswith( "logbot.info" ):
			await Commands.Owner.info( message )
			pass
		elif startswith( "$prefix" ):
			await client.send_message( message.channel, f"The prefix is {prefix}" )
			pass

		for item in list( custom_commands.keys( ) ):
			if startswith( item ):
				await client.send_message( message.channel, custom_commands[ item ] )
				pass
			pass

		save( message.server.id )

		with open( channel_settings, 'w' ) as configfile:
			channel_parser.write( configfile )
			pass

		try:
			exclude_channel_list.index( message.channel.id )
			pass
		except:
			if not message.content.startswith( f"$exclude " ) and not message.content.startswith( f"$ex " ):
				ret = f"Message Sent: {message.server.name} ~ {message.channel} ~ \"{msgcont}\" ~ {message.author} ~ {time.day}.{time.month}.{time.year} {time.hour}:{time.minute} ~ {message.attachments}"
				send( ret, message.server.name, message.channel.name )
				pass
			pass

		pass
	elif message.channel.is_private:
		if message.content.startswith( "logbot.info" ): await Commands.DM.info( message )
		elif message.content.startswith( "$planned" ): await Commands.DM.planned( message )
		elif message.content.startswith( "$translate.get" ): await Commands.DM.translate_get( message )
		elif message.content.startswith( "$translate " ): await Commands.DM.translate( message )
		elif message.content.startswith( "$wiki" ): await Commands.DM.wiki( message )
		elif message.content.startswith( "logbot.exit" ):
			if message.author.id == owner_id: await Commands.DM.exit( )
			else: await sendNoPerm( message )
			pass
		elif message.content.startswith( "$updates" ): await Commands.DM.updates( message )
		elif message.content.startswith( "$refresh" ):
			if message.author.id == owner_id: await Commands.DM.refresh( )
			pass
		elif message.content.startswith( "$update" ) or message.content.startswith( "logbot.update" ):
			if message.author.id == owner_id: await Commands.DM.update( message )
			pass
		elif message.content.startswith( "$suggest " ): await Commands.DM.suggest( message )
		# elif message.content.startswith("$suggestions"): await Commands.DM.suggestions(message)
		elif message.content.startswith( "$decide" ):
			content = message.content.split( ' ' )
			content.remove( content[ 0 ] )
			content = ' '.join( content ).split( "|" )
			choice = random.choice( content )
			await client.send_message( message.channel, f"```I have chosen: {choice}```" )
			pass
		elif message.content.startswith( "$invite" ):
			await client.send_message( message.channel, "https://discordapp.com/oauth2/authorize?client_id=255379748828610561&scope=bot&permissions=2146958463" )
			pass
		elif message.content.startswith( "$query " ): await Commands.DM.query( message )
		elif message.content.startswith( "$dict " ): await Commands.DM.dict( message )
		pass

	tm = int( (datetime.now( ) - message.timestamp).microseconds ) / 1000000
	print( tm )
	times.append( tm )
	del tm
	pass

# noinspection PyShadowingNames
@client.event
async def on_message_delete ( message: discord.Message ):
	try: exclude_channel_list.index( message.channel.id )
	except:
		m = format_time( message.timestamp )
		name = str( message.author )
		ret = f"Message Deleted: {message.server.name} ~ {message.channel} ~ \"{message.content}\" was deleted ~ {name} ~ {m.day}.{m.month}.{m.year} {m.hour}:{m.minute} ~ {message.attachments}"
		send( ret, message.server.name, message.channel.name )
		c = client.get_channel( parser[ message.server.id ][ "logchannel" ] )
		if not c is None:
			e = discord.Embed( title="Message Deleted!", description="A message was deleted!", colour=discord.Colour.red( ) ) \
				.add_field( name="Author", value=str( message.author ), inline=False ) \
				.add_field( name="Content", value=message.content, inline=False ) \
				.add_field( name="ID", value=message.id, inline=False ) \
				.add_field( name="Channel", value=str( message.channel ), inline=False ) \
				.set_footer( text=str( m ) )
			await client.send_message( c, "", embed=e )
			pass
		pass
	pass

@client.event
async def on_message_edit ( before: discord.Message, after: discord.Message ):
	try: exclude_channel_list.index( before.channel.id )
	except:
		m = format_time( after.timestamp )
		attachments = after.attachments
		ret = f"Message Edited: {after.server.name} ~ {before.channel.name} ~ \"{before.content}\" ~ \"{after.content}\" ~ {attachments} ~ {before.author} ~ {m.day}.{m.month}.{m.year} {m.hour}:{m.minute}"
		send( ret, after.server.name, after.channel.name )
		c = client.get_channel( parser[ before.server.id ][ "logchannel" ] )
		if not c is None and not before.content == after.content:
			e = discord.Embed( title="Message Edited!", description="A message was edited!", colour=discord.Colour.red( ) ) \
				.add_field( name="Author", value=str( before.author ), inline=False ) \
				.add_field( name="Old Content", value=before.content, inline=False ) \
				.add_field( name="New Content", value=after.content, inline=False ) \
				.add_field( name="ID", value=before.id, inline=False ) \
				.add_field( name="Channel", value=str( before.channel ), inline=False ) \
				.set_footer( text=f"edited on {after.edited_timestamp}" )
			await client.send_message( c, "", embed=e )
			pass
		pass
	pass

# </editor-fold>
# <editor-fold desc="Member Updates">
@client.event
async def on_member_join ( member: discord.Member ):
	m = datetime.now( )
	ret = f"Member Joined: {member.server.name} ~ {member} joined ~ {m.day}.{m.month}.{m.year} {m.hour}:{m.minute}"
	send( ret, member.server.name )
	read( member.server.id )
	if not disables[ "welcome" ]:
		welcome_tmp = db.read( "Welcomes", member.server.id )

		if welcome_tmp.startswith( "read(" ):
			welcome_tmp = open( welcome_tmp[ 6:len( welcome_tmp ) - 2 ], 'r' ).read( )
			pass
		else:
			welcome_tmp = re.sub( "{server}", member.server.name, welcome_tmp, flags=2 )
			welcome_tmp = re.sub( "{user}", member.mention, welcome_tmp, flags=2 )
			pass
		try: await client.add_roles( member, discord.utils.find( lambda r:r.id == join_roles[ member.server.id ], member.server.roles ) )
		except: print( traceback.format_exc( ) )
		try:
			_dchannel = client.get_channel( default_channel[ member.server.id ] )
			if _dchannel is None: _dchannel = member.server.default_channel
			await client.send_message( _dchannel, welcome_tmp )
			pass
		except: await client.send_message( member.server.default_channel, welcome_tmp )
		pass
	c = client.get_channel( parser[ member.server.id ][ "logchannel" ] )
	if not c is None:
		e = discord.Embed( title="Member Joined!", description="A member joined!", colour=discord.Colour.red( ) )
		e.add_field( name="Name", value=str( member ), inline=False )
		e.add_field( name="ID", value=member.id, inline=False )
		e.set_footer( text=str( m ) )
		await client.send_message( c, "", embed=e )
		pass
	pass

@client.event
async def on_member_remove ( member: discord.Member ):
	m = datetime.now( )
	time = f"{m.day}.{m.month}.{m.year} {m.hour}:{m.minute}"
	ret = f"Member Left: {member.server.name} ~ {member} left ~ {time}"
	send( ret, member.server.name )
	read( member.server.id )
	if not disables[ "goodbye" ]:
		goodbye_tmp = db.read( "Goodbyes", member.server.id )
		goodbye_tmp = re.sub( "{server}", member.server.name, goodbye_tmp, flags=2 )
		goodbye_tmp = re.sub( "{user}", member.mention, goodbye_tmp, flags=2 )
		await client.send_message( member.server.default_channel, goodbye_tmp )
		pass
	c = client.get_channel( parser[ member.server.id ][ "logchannel" ] )
	if not c is None:
		e = discord.Embed( title="Member Left!", description="A member left!", colour=discord.Colour.red( ) )
		e.add_field( name="Name", value=str( member ), inline=False )
		e.add_field( name="ID", value=member.id, inline=False )
		e.set_footer( text=str( m ) )
		await client.send_message( c, "", embed=e )
		pass
	pass

@client.event
async def on_member_update ( before: discord.Member, after: discord.Member ):
	m = datetime.now( )
	sent_str = ""
	if before.status != after.status: sent_str = f"Member Updated: {after.server.name} ~ {after} changed his/her status from {before.status} to {after.status}"
	elif before.game != after.game: sent_str = f"Member Updated: {after.server.name} ~ {after} changed his/her game from {before.game} to {after.game}"
	elif before.avatar != after.avatar: sent_str = f"Member Updated: {after.server.name} ~ {after} changed his/her avatar."
	elif before.nick != after.nick: sent_str = f"Member Updated: {after.server.name} ~ {after}'s nickname was changed to {after.nick}"
	elif before.roles != after.roles:
		if not discord.utils.find( lambda r:r.name == "LogBot Admin" or r.name == "LogBot Member", after.server.roles ) in after.roles:
			is_role_added = False
			is_role_removed = False
			role = after.server.default_role
			for item in before.roles:
				if not item in after.roles: is_role_removed = True; role = item
				pass
			for item in after.roles:
				if not item in before.roles: is_role_added = True; role = item
				pass
			if is_role_added: sent_str = f"Member Updated: {after.server.name} ~ Role {role} was added to {before}."
			elif is_role_removed: sent_str = f"Member Updated: {after.server.name} ~ Role {role} was removed from {before}."
			pass
		pass
	if not sent_str == "":
		sent_str += f" ~ {m.day}.{m.month}.{m.year} {m.hour}:{m.minute}"
		send( sent_str, before.server.name )
		pass
	pass

@client.event
async def on_member_ban ( member: discord.Member ):
	m = datetime.now( )
	sent_str = f"Member Banned: {member.server.name} ~ {check(member.nick, member.name, member.id)} was banned ~ {m.day}.{m.month}.{m.year} {m.hour}:{m.minute}"
	send( sent_str, member.server.name )
	c = client.get_channel( parser[ member.server.id ][ "logchannel" ] )
	if not c is None:
		e = discord.Embed( title="Member Banned!", description="A member was banned!", colour=discord.Colour.red( ) )
		e.add_field( name="Name", value=str( member ), inline=False )
		e.add_field( name="ID", value=member.id, inline=False )
		e.set_footer( text=str( m ) )
		await client.send_message( c, "", embed=e )
		pass
	pass

@client.event
async def on_member_unban ( server: discord.Server, user: discord.User ):
	m = datetime.now( )
	sent_str = f"Member Unbanned: {server.name} ~ {check(user.display_name, user.name, user.id)} was unbanned ~ {m.day}.{m.month}.{m.year} {m.hour}:{m.minute}"
	send( sent_str, server.name )
	c = client.get_channel( parser[ server.id ][ "logchannel" ] )
	if not c is None:
		e = discord.Embed( title="Member Unbanned!", description="A member was unbanned!", colour=discord.Colour.red( ) )
		e.add_field( name="Name", value=str( user ), inline=False )
		e.add_field( name="ID", value=user.id, inline=False )
		e.set_footer( text=str( m ) )
		await client.send_message( c, "", embed=e )
		pass
	pass

# </editor-fold>
# <editor-fold desc="Channel Updates">
@client.event
async def on_channel_update ( before: discord.Channel, after: discord.Channel ):
	m = datetime.now( )
	if before.name != after.name:
		send( f"Channel Updated: {after.server.name} ~ {after}'s name was changed from {before.name} to {after.name}", after.server.name )
		with f"{discord_logs}\\{before.server.name}\\{before.name}.mark.txt" as old_loc:
			if os.path.exists( old_loc ): os.rename( old_loc, f"{discord_logs}\\{before.server.name}\\{after.name}.mark.txt" )
			pass
		with f"{discord_logs}\\{before.server.name}\\{before.name}.txt" as old_loc_unmarked:
			if os.path.exists( old_loc_unmarked ): os.rename( old_loc_unmarked, f"{discord_logs}\\{before.server.name}\\{after.name}.txt" )
			pass
		pass
	elif before.topic is not after.topic: send( f"Channel Updated: {after.server.name} ~ {after}'s topic was changed from \"{before.topic}\" to \"{after.topic}\"", after.server.name )
	elif before.position is not after.position: send( f"Channel Updated: {after.server.name} ~ {after}'s position was changed from {before.position} to {after.position}", after.server.name )
	elif before.user_limit is not after.user_limit: send( f"Channel Updated: {after.server.name} ~ {after}'s user limit was changed from {before.user_limit} to {after.user_limit}", after.server.name )
	elif before.bitrate is not after.bitrate: send( f"Channel Updated: {after.server.name} ~ {after.name}'s bitrate was changed from {before.bitrate} to {after.bitrate}", after.server.name )
	else: send( f"Channel Updated: {after.server.name} ~ {after.name} was updated.", after.server.name )
	c = client.get_channel( parser[ before.server.id ][ "logchannel" ] )
	if not c is None:
		e = discord.Embed( title="Channel Updated!", description="A channel was updated!", colour=discord.Colour.gold( ) )
		if not str( before ) == str( after ):
			e.add_field( name="Old Name", value=str( before ), inline=False )
			e.add_field( name="New Name", value=str( after ), inline=False )
			pass
		else: e.add_field( name="Name", value=str( after ), inline=False )
		e.add_field( name="ID", value=after.id, inline=False )
		if not before.topic == after.topic:
			e.add_field( name="Old Topic", value=str( before.topic ), inline=False )
			e.add_field( name="New Topic", value=str( after.topic ), inline=False )
			pass
		if not before.position == after.position:
			e.add_field( name="Old Position", value=str( before.position ), inline=False )
			e.add_field( name="New Position", value=str( after.position ), inline=False )
			pass
		if not before.bitrate == after.bitrate:
			e.add_field( name="Old Bitrate", value=str( before.bitrate ), inline=False )
			e.add_field( name="New Bitrate", value=str( after.bitrate ), inline=False )
			pass
		if not before.user_limit == after.user_limit:
			e.add_field( name="Old User Limit", value=str( before.user_limit ), inline=False )
			e.add_field( name="New User Limit", value=str( after.user_limit ), inline=False )
			pass
		e.set_footer( text=str( m ) )
		await client.send_message( c, "", embed=e )
		pass
	pass

@client.event
async def on_voice_state_update ( before: discord.Member, after: discord.Member ):
	m = datetime.now( )
	sent_str = "Voice Status Updated: {after.server.name} ~ "
	if before.voice.deaf is not after.voice.deaf: sent_str = f"{before} was deafened by the server."
	elif before.voice.mute is not after.voice.mute:
		if after.voice.mute: sent_str = f"{before} was muted by the server."
		else: sent_str = f"{before} was unmuted by the server."
		pass
	elif before.voice.self_mute is not after.voice.self_mute:
		if after.voice.self_mute: sent_str = f"{before} muted him/her self."
		else: sent_str = f"{before} unmuted him/her self."
		pass
	elif before.voice.self_deaf is not after.voice.self_deaf:
		if after.voice.self_deaf: sent_str = f"{before} deafened him/her self."
		else: sent_str = f"{before} undeafened him/her self."
		pass
	elif before.voice.voice_channel is not after.voice.voice_channel:
		if after.voice.voice_channel is not None: sent_str = f"{before} joined {after.voice.voice_channel}"
		else: sent_str = f"{before} left {before.voice.voice_channel}"
		pass
	sent_str += f" ~ {m.day}.{m.month}.{m.year} {m.hour}:{m.minute}"
	send( sent_str, before.server.name )
	pass

@client.event
async def on_channel_delete ( channel: discord.Channel ):
	m = datetime.now( )
	ret = f"Channel Deleted: {channel.server.name} ~ \"{channel.name}\" was deleted ~ {m.day}.{m.month}.{m.year} {m.hour}:{m.minute}"
	send( ret, channel.server.name )
	c = client.get_channel( parser[ channel.server.id ][ "logchannel" ] )
	if not c is None:
		e = discord.Embed( title="Channel Deleted!", description="A channel was deleted!", colour=discord.Colour.red( ) )
		e.add_field( name="Name", value=str( channel ), inline=False )
		e.add_field( name="ID", value=channel.id, inline=False )
		e.set_footer( text=str( m ) )
		await client.send_message( c, "", embed=e )
		pass
	pass

@client.event
async def on_channel_create ( channel: discord.Channel ):
	m = datetime.now( )
	ret = f"Channel Created: {channel.server.name} ~ \"{channel.name}\" was created ~ {m.day}.{m.month}.{m.year} {m.hour}:{m.minute}"
	if channel.server is not None: send( ret, channel.server.name )
	else: send( ret, f"DM{channel.name}" )
	c = client.get_channel( parser[ channel.server.id ][ "logchannel" ] )
	if not c is None:
		e = discord.Embed( title="Channel Created!", description="A channel was created!", colour=discord.Colour.green( ) )
		e.add_field( name="Name", value=str( channel ), inline=False )
		e.add_field( name="ID", value=channel.id, inline=False )
		e.add_field( name="Position", value=str( channel.position ), inline=False )
		e.add_field( name="Bitrate", value=str( channel.bitrate ), inline=False )
		e.add_field( name="Topic", value=channel.topic, inline=False )
		e.add_field( name="User Limit", value=str( channel.user_limit ), inline=False )
		e.set_footer( text=str( channel.created_at ) )
		await client.send_message( c, "", embed=e )
		pass
	pass

# </editor-fold>
# <editor-fold desc="Server Updates">
# noinspection PyShadowingNames
@client.event
async def on_server_update ( before: discord.Server, after: discord.Server ):
	m = datetime.now( )
	# If the server's properties were changed, do the appropriate actions and log them.
	if before.name != after.name:
		with f"{discord_logs}\\{before.name}" as old_loc:
			with f"{discord_logs}\\{after.name}" as new_loc:
				os.rename( old_loc, new_loc )
				pass
			pass
		send( f"Server Updated: {after.name} ~ The server name was changed from {before.name} to {after.name}.", after.name )
		pass
	if before.default_channel != after.default_channel:
		send( f"Server Updated: {after.name} ~ The server's default channel was changed from {before.default_channel} to {after.default_channel}.", after.name )
		pass
	if before.afk_channel != after.afk_channel:
		send( f"Server Updated: {after.name} ~ The server's AFK channel was changed from {before.afk_channel} to {after.afk_channel}.", after.name )
		pass
	if before.default_role != after.default_role:
		send( f"Server Updated: {after.name} ~ The server's default role was changed from {before.default_role} to {after.default_role}.", after.name )
		pass
	if before.verification_level != after.verification_level:
		send( f"Server Updated: {after.name} ~ The server's verification level was changed from {before.verification_level} to {after.verification_level}.", after.name )
		pass
	c = client.get_channel( parser[ before.id ][ "logchannel" ] )
	if not c is None:
		e = discord.Embed( title="Server Updated!", description="The server was updated!", colour=discord.Colour.gold( ) )
		if not str( before ) == str( after ):
			e.add_field( name="Old Name", value=str( before ), inline=False )
			e.add_field( name="New Name", value=str( after ), inline=False )
			pass
		e.add_field( name="ID", value=after.id, inline=False )
		if not before.default_channel == after.default_channel:
			e.add_field( name="Old Default Channel", value=str( before.default_channel ), inline=False )
			e.add_field( name="New Default Channel", value=str( after.default_channel ), inline=False )
			pass
		if not before.afk_channel == after.afk_channel:
			e.add_field( name="Old AFK Channel", value=str( before.afk_channel ), inline=False )
			e.add_field( name="New AFK Channel", value=str( after.afk_channel ), inline=False )
			pass
		if not before.default_role == after.default_role:
			e.add_field( name="Old Default Role", value=str( before.default_role ), inline=False )
			e.add_field( name="New Default Role", value=str( after.default_role ), inline=False )
			pass
		e.set_footer( text=str( m ) )
		await client.send_message( c, "", embed=e )
		pass
	pass

@client.event
async def on_server_role_create ( role: discord.Role ):
	m = datetime.now( )
	sent_str = f"Role Created: {role.server.name} ~ {role.name} was created ~ {m.day}.{m.month}.{m.year} {m.hour}:{m.minute}"
	send( sent_str, role.server.name )
	c = client.get_channel( parser[ role.server.id ][ "logchannel" ] )
	if not c is None:
		e = discord.Embed( title="Role Created!", description="A role was created!", colour=discord.Colour.green( ) )
		e.add_field( name="Name", value=str( role ), inline=False )
		e.add_field( name="ID", value=role.id, inline=False )
		e.add_field( name="Permissions", value=str( role.permissions ), inline=False )
		e.set_footer( text=str( role.created_at ) )
		await client.send_message( c, "", embed=e )
		pass
	pass

@client.event
async def on_server_role_delete ( role: discord.Role ):
	m = datetime.now( )
	sent_str = f"Role Deleted: {role.server.name} ~ {role.name} was deleted ~ {m.day}.{m.month}.{m.year} {m.hour}:{m.minute}"
	send( sent_str, role.server.name )
	c = client.get_channel( parser[ role.server.id ][ "logchannel" ] )
	if not c is None:
		e = discord.Embed( title="Role Deleted!", description="A role was deleted!", colour=discord.Colour.red( ) )
		e.add_field( name="Name", value=str( role ), inline=False )
		e.add_field( name="ID", value=role.id, inline=False )
		e.set_footer( text=str( m ) )
		await client.send_message( c, "", embed=e )
		pass
	pass

@client.event
async def on_server_role_update ( before: discord.Role, after: discord.Role ):
	m = datetime.now( )
	old = { }
	new = { }
	perms = before.permissions
	# noinspection SpellCheckingInspection
	nperms = after.permissions

	if not perms.create_instant_invite is nperms.create_instant_invite:
		old[ 'create_instant_invite' ] = perms.create_instant_invite
		new[ 'create_instant_invite' ] = nperms.create_instant_invite
		pass
	if not perms.kick_members is nperms.kick_members:
		old[ 'kick_members' ] = perms.kick_members
		new[ 'kick_members' ] = nperms.kick_members
		pass
	if not perms.ban_members is nperms.ban_members:
		old[ 'ban_members' ] = perms.ban_members
		new[ 'ban_members' ] = nperms.ban_members
		pass
	if not perms.administrator is nperms.administrator:
		old[ 'administrator' ] = perms.administrator
		new[ 'administrator' ] = nperms.administrator
		pass
	if not perms.manage_channels is nperms.manage_channels:
		old[ 'manage_channels' ] = perms.manage_channels
		new[ 'manage_channels' ] = nperms.manage_channels
		pass
	if not perms.manage_server is nperms.manage_server:
		old[ 'manage_server' ] = perms.manage_server
		new[ 'manage_server' ] = nperms.manage_server
		pass
	if not perms.read_messages is nperms.read_messages:
		old[ 'read_messages' ] = perms.read_messages
		new[ 'read_messages' ] = nperms.read_messages
		pass
	if not perms.send_messages is nperms.send_messages:
		old[ 'send_messages' ] = perms.send_messages
		new[ 'send_messages' ] = nperms.send_messages
		pass
	if not perms.send_tts_messages is nperms.send_tts_messages:
		old[ 'send_tts_messages' ] = perms.send_tts_messages
		new[ 'send_tts_messages' ] = nperms.send_tts_messages
		pass
	if not perms.manage_messages is nperms.manage_messages:
		old[ 'manage_messages' ] = perms.manage_messages
		new[ 'manage_messages' ] = nperms.manage_messages
		pass
	if not perms.embed_links is nperms.embed_links:
		old[ 'embed_links' ] = perms.embed_links
		new[ 'embed_links' ] = nperms.embed_links
		pass
	if not perms.attach_files is nperms.attach_files:
		old[ 'attach_files' ] = perms.attach_files
		new[ 'attach_files' ] = nperms.attach_files
		pass
	if not perms.read_message_history is nperms.read_message_history:
		old[ 'read_message_history' ] = perms.read_message_history
		new[ 'read_message_history' ] = nperms.read_message_history
		pass
	if not perms.mention_everyone is nperms.mention_everyone:
		old[ 'mention_everyone' ] = perms.mention_everyone
		new[ 'mention_everyone' ] = nperms.mention_everyone
		pass
	if not perms.external_emojis is nperms.external_emojis:
		old[ 'external_emojis' ] = perms.external_emojis
		new[ 'external_emojis' ] = nperms.external_emojis
		pass
	if not perms.connect is nperms.connect:
		old[ 'connect' ] = perms.connect
		new[ 'connect' ] = nperms.connect
		pass
	if not perms.speak is nperms.speak:
		old[ 'speak' ] = perms.speak
		new[ 'speak' ] = nperms.speak
		pass
	if not perms.mute_members is nperms.mute_members:
		old[ 'mute_members' ] = perms.mute_members
		new[ 'mute_members' ] = nperms.mute_members
		pass
	if not perms.deafen_members is nperms.deafen_members:
		old[ 'deafen_members' ] = perms.deafen_members
		new[ 'deafen_members' ] = nperms.deafen_members
		pass
	if not perms.move_members is nperms.move_members:
		old[ 'move_members' ] = perms.move_members
		new[ 'move_members' ] = nperms.move_members
		pass
	if not perms.use_voice_activation is nperms.use_voice_activation:
		old[ 'use_voice_activation' ] = perms.use_voice_activation
		new[ 'use_voice_activation' ] = nperms.use_voice_activation
		pass
	if not perms.change_nickname is nperms.change_nickname:
		old[ 'change_nickname' ] = perms.change_nickname
		new[ 'change_nickname' ] = nperms.change_nickname
		pass
	if not perms.manage_nicknames is nperms.manage_nicknames:
		old[ 'manage_nicknames' ] = perms.manage_nicknames
		new[ 'manage_nicknames' ] = nperms.manage_nicknames
		pass
	if not perms.manage_roles is nperms.manage_roles:
		old[ 'manage_roles' ] = perms.manage_roles
		new[ 'manage_roles' ] = nperms.manage_roles
		pass
	if not perms.manage_emojis is nperms.manage_emojis:
		old[ 'manage_emojis' ] = perms.manage_emojis
		new[ 'manage_emojis' ] = nperms.manage_emojis
		pass

	sent_str = f"Role Updated: {before.server.name} ~ {before} : {old} : {before.position} -> {after} : {new} : {after.position} ~ {m.day}.{m.month}.{m.year} {m.hour}:{m.minute}"
	send( sent_str, before.server.name )

	c = client.get_channel( parser[ before.server.id ][ "logchannel" ] )
	if not c is None:
		e = discord.Embed( title="Role Updated!", description="A role was updated!", colour=discord.Colour.gold( ) )
		if not str( before ) == str( after ):
			e.add_field( name="Old Name", value=str( before ), inline=False )
			e.add_field( name="New Name", value=str( after ), inline=False )
			pass
		e.add_field( name="ID", value=after.id, inline=False )
		if not old == new:
			e.add_field( name="Old Permissions", value=str( old ), inline=False )
			e.add_field( name="New Permissions", value=str( new ), inline=False )
			pass
		if not before.position == after.position:
			e.add_field( name="Old Position", value=str( before.position ), inline=False )
			e.add_field( name="New Position", value=str( after.position ), inline=False )
			pass
		e.set_footer( text=str( m ) )
		await client.send_message( c, "", embed=e )
		pass

	del sent_str
	del old
	del new
	del m
	del c
	pass

# </editor-fold>
# <editor-fold desc="Reaction Events">
@client.event
async def on_reaction_add ( reaction: discord.Reaction, user: Union[ discord.User, discord.Member ] ):
	emj = codecs.unicode_escape_encode( reaction.emoji, 'strict' )
	msgcont = reaction.message.content if is_ascii( reaction.message.content ) else codecs.unicode_escape_encode( reaction.message.content, 'strict' )
	sent_str = f"Reaction Added: {reaction.message.server.name} ~ {reaction.message.channel.name} ~ {'Custom ' if reaction.custom_emoji else ''}Reaction {emj} was added to message \"{msgcont}\" {reaction.count} time(s) by {user}"
	send( sent_str, reaction.message.server.name )
	pass

@client.event
async def on_reaction_remove ( reaction: discord.Reaction, user: Union[ discord.User, discord.Member ] ):
	emj = codecs.unicode_escape_encode( reaction.emoji, 'strict' )
	msgcont = reaction.message.content if is_ascii( reaction.message.content ) else codecs.unicode_escape_encode( reaction.message.content, 'strict' )
	sent_str = f"Reaction Removed: {reaction.message.server.name} ~ {reaction.message.channel.name} ~ {'Custom ' if reaction.custom_emoji else ''}Reaction {emj} was removed from message \"{msgcont}\" {reaction.count} time(s) by {user}"
	send( sent_str, reaction.message.server.name )
	pass

@client.event
async def on_reaction_clear ( message: discord.Message, reactions: List[ discord.Reaction ] ):
	emjs = [ ]
	for item in reactions: emjs.append( codecs.unicode_escape_encode( item.emoji, 'strict' ) )
	msgcont = message.content if is_ascii( message.content ) else codecs.unicode_escape_encode( message.content, 'strict' )
	sent_str = f"Reaction(s) Cleared: {message.server.name} ~ {message.channel.name} ~ Reactions [{','.join(emjs)}] were cleared from message \"{msgcont}\""
	send( sent_str, message.server.name )
	pass

# </editor-fold>

@client.event
async def on_ready ( ):
	global icon, bootup_time
	# gets and deletes the Update message from the parameters.
	if not len( argv ) == 0:
		index = -1
		index2 = -1
		if "-m" in argv: index = argv.index( "-m" )
		if "-c" in argv: index2 = argv.index( "-c" )
		if index != -1 and index2 != -1:
			c = client.get_channel( argv[ index2 + 1 ] )
			m = await client.get_message( c, argv[ index + 1 ] )
			await client.delete_message( m )
			pass

		if "-t" in argv:
			t = argv[ argv.index( "-t" ) + 1 ].split( "." )
			bootup_time = datetime( year=int( t[ 2 ] ), month=int( t[ 0 ] ), day=int( t[ 1 ] ), hour=int( t[ 3 ] ), minute=int( t[ 4 ] ), second=int( t[ 5 ] ), microsecond=int( t[ 6 ] ) )
			pass
		pass
	os.system( 'cls' )
	print( f"{Fore.MAGENTA}Signed in and waiting...\nRunning version: Logbot Version {version}{Fore.RESET}" )
	for server in client.servers:
		if not server.id in parser.sections( ):
			parser[ server.id ] = {
				"logchannel":"None"
			}
		pass
	# Updates bot icon, status, and game.
	await client.change_presence( game=discord.Game( name="Prefix: $" ), status=None )
	avatar_tmp = open( selected_image, "rb" )
	await client.edit_profile( avatar=avatar_tmp.read( ) )
	avatar_tmp.close( )
	del avatar_tmp
	icon = Qt.QIcon( selected_image )
	sti.setIcon( icon )
	pass

client.run( token )

if not exiting:
	subprocess.Popen( f"python {os.getcwd()}\\logbot.py -t {bootup_time.month}.{bootup_time.day}.{bootup_time.year}.{bootup_time.hour}.{bootup_time.minute}.{bootup_time.second}.{bootup_time.microsecond}", False )
	exit( 0 )
	pass
