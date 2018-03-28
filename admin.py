"""
Admin Module.
"""
import os
import sqlite3
import subprocess
import traceback
from datetime import datetime

from colorama import Fore, init
from discord import Client, Message
from discord.utils import find

import argparser
from logbot_data import owner_id, token

CLIENT = Client( max_messages=1000000 )
init( )
PURGE_PARSER = argparser.ArgParser( "&&", "=" )
SQL = sqlite3.connect( f"{os.getcwd()}\\Discord Logs\\SETTINGS\\logbot.db" )
CURSOR = SQL.cursor( )
EXITING = False

def log_error ( error_text: str ):
	"""
	Logs errors to errors.txt.
	:param error_text: The exception message.
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
	writer.write( f"{datetime.now()} (admin.py) - {error_text}\n\n{prev_text}" )
	writer.close( )
	if "SystemExit" in error_text:
		exit( 0 )
	del writer
	del file
	del prev_text

class Commands:
	"""
	Command methods.
	"""
	class Admin:
		"""
		Admins only.
		"""
		@staticmethod
		async def a_count ( message: Message ):
			"""
			Counts the total number of messages in a channel.
			:param message: a discord.Message object.
			"""
			count = 0
			logs = CLIENT.logs_from(
				message.channel,
				limit=1000000000
			).iterate
			while True:
				try:
					await logs( )
					count += 1
				except Exception:
					break
			await CLIENT.send_message(
				message.channel,
				f"```{count} messages found!```"
			)
			del count
			del logs
		@staticmethod
		async def a_total ( message: Message ):
			"""
			Counts the total number of messages in a server.
			:param message: a discord.Message object.
			"""
			count = 0
			for channel in message.server.channels:
				logs = CLIENT.logs_from(
					channel,
					limit=1000000000
				).iterate
				while True:
					try:
						await logs( )
						count += 1
					except Exception:
						break
				del logs
			await CLIENT.send_message(
				message.channel,
				f"```{count} messages found!```"
			)
			del count
		# noinspection PyShadowingNames
		@staticmethod
		async def a_count_param ( message: Message, prefix: str ):
			"""
			Counts messages with a filter.
			:param message: a discord.Message object.
			:param prefix: The server prefix.
			"""
			_cnt = message.content.replace(
				f"a{prefix}count ",
				""
			).split( " " )
			_type = _cnt[ 0 ].lower( )
			_param = _cnt[ 1 ]
			user = find(
				lambda m:
				m.id == _param or
				m.name == _param or
				str( m ) == _param or
				m.mention == _param,
				message.server.members
			)

			msgs = list( )
			count = 0
			logs = CLIENT.logs_from(
				message.channel,
				limit=1000000000
			).iterate
			app = msgs.append
			while True:
				try:
					item = await logs( )
					app( item )
					del item
				except Exception:
					break
			for msg in msgs:
				if isinstance( msg, Message ):
					if _type == "&text":
						if _param in msg.content:
							count += 1
					elif _type == "&from":
						if msg.author.id == user.id:
							count += 1
			await CLIENT.send_message(
				message.channel,
				f"```{count} messages found!```"
			)
			del _cnt
			del _type
			del _param
			del user
			del msgs
			del count
			del logs
			del app

def sqlread ( cmd: str ):
	"""
	Reads from SQL.
	:param cmd: The read command to use.
	:return: The results.
	"""
	CURSOR.execute( cmd )
	return CURSOR.fetchall( )

@CLIENT.event
async def on_message ( message: Message ):
	"""
	Occurs when the bot receives a message.
	:param message: A discord.Message object.
	"""
	global EXITING
	try:
		do_update = False
		def startswith ( *args: str, val: str = message.content ) -> bool:
			"""
			Checks a string to see if it starts with any number of characters.
			:param args: The string(s) to check for.
			:param val: The string to check.
			:return: True or False
			"""
			for arg in args:
				if val.startswith( arg ):
					return True
			return False
		prefix = sqlread(
			f"SELECT prefix FROM Prefixes WHERE server='{message.server.id}';"
		)[ 0 ][ 0 ]
		if not message.channel.is_private:
			admin_role = find(
				lambda r:r.name == "LogBot Admin",
				message.server.roles
			)
			if admin_role in message.author.roles or message.author.id == owner_id:
				if startswith( f"a{prefix}count " ):
					await Commands.Admin.a_count_param( message, prefix )
				elif startswith( f"a{prefix}count" ):
					await Commands.Admin.a_count( message )
				elif startswith( f"a{prefix}total" ):
					await Commands.Admin.a_total( message )
			del admin_role

		if startswith(
				"a$update",
				"logbot.admin.update",
				"$update"
		) and message.author.id == owner_id:
			do_update = True
		elif startswith(
				"logbot.admin.exit",
				"$exit"
		) and message.author.id == owner_id:
			EXITING = True
			await CLIENT.logout( )

		if do_update is True:
			print( f"{Fore.LIGHTCYAN_EX}Updating...{Fore.RESET}" )
			subprocess.Popen( f"python {os.getcwd()}\\admin.py" )
			exit( 0 )
		del do_update
		del prefix
	except Exception:
		log_error( traceback.format_exc( ) )

@CLIENT.event
async def on_ready ( ):
	"""
	Occurs when the bot logs in.
	"""
	# os.system( "cls" )
	print( f"{Fore.MAGENTA}Admin Ready!!!{Fore.RESET}" )

CLIENT.run( token )

if not EXITING:
	subprocess.Popen( f"python {os.getcwd()}\\admin.py" )
	exit( 0 )
