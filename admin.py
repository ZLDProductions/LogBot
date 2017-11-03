import os
import sqlite3
import subprocess

from colorama import Fore, init
from discord import Client, Message
from discord.utils import find

import argparser
from logbot_data import owner_id, token

client = Client( max_messages=1000000 )
init( )
purge_parser = argparser.ArgParser( "&&", "=" )
sql = sqlite3.connect( f"{os.getcwd()}\\Discord Logs\\SETTINGS\\logbot.db" )
cursor = sql.cursor( )
exiting = False

class Commands:
	class Admin:
		@staticmethod
		async def a_count ( message: Message ):
			count = 0
			logs = client.logs_from( message.channel, limit=1000000000 ).iterate
			while True:
				try:
					await logs( )
					count += 1
					pass
				except: break
				pass
			await client.send_message( message.channel, f"```{count} messages found!```" )
			pass
		@staticmethod
		async def a_total ( message: Message ):
			count = 0
			for channel in message.server.channels:
				logs = client.logs_from( channel, limit=1000000000 ).iterate
				while True:
					try:
						await logs( )
						count += 1
						pass
					except: break
					pass
				pass
			await client.send_message( message.channel, f"```{count} messages found!```" )
			pass
		# noinspection PyShadowingNames
		@staticmethod
		async def a_count_param ( message: Message, prefix: str ):
			_cnt = message.content.replace( f"a{prefix}count ", "" ).split( " " )
			_type = _cnt[ 0 ].lower( )
			_param = _cnt[ 1 ]
			user = find( lambda m:m.id == _param or m.name == _param or str( m ) == _param or m.mention == _param, message.server.members )

			msgs = list( )
			count = 0
			logs = client.logs_from( message.channel, limit=1000000000 ).iterate
			app = msgs.append
			while True:
				try: item = await logs( ); app( item )
				except: break
				pass
			for m in msgs:
				if isinstance( m, Message ):
					if _type == "&text":
						if _param in m.content: count += 1
						pass
					elif _type == "&from":
						if m.author.id == user.id: count += 1
						pass
					pass
				pass
			await client.send_message( message.channel, f"```{count} messages found!```" )
			pass
		pass
	pass

def sqlread ( cmd: str ):
	cursor.execute( cmd )
	return cursor.fetchall( )

@client.event
async def on_message ( message: Message ):
	do_update = False
	def startswith ( *args: str, val: str = message.content ) -> bool:
		for arg in args:
			if val.startswith( arg ): return True
			pass
		return False
	prefix = sqlread( f"SELECT prefix FROM Prefixes WHERE server='{message.server.id}';" )[ 0 ][ 0 ]
	if not message.channel.is_private:
		admin_role = find( lambda r:r.name == "LogBot Admin", message.server.roles )
		if startswith( f"a{prefix}count " ):
			if admin_role in message.author.roles or message.author.id == owner_id: await Commands.Admin.a_count_param( message, prefix )
			pass
		elif startswith( f"a{prefix}count" ):
			if admin_role in message.author.roles or message.author.id == owner_id: await Commands.Admin.a_count( message )
			pass
		elif startswith( f"a{prefix}total" ):
			if admin_role in message.author.roles or message.author.id == owner_id: await Commands.Admin.a_total( message )
			pass
		pass

	if startswith( "a$update", "logbot.admin.update", "$update" ):
		if message.author.id == owner_id: do_update = True
		pass
	elif startswith( "logbot.admin.exit", "$exit" ):
		if message.author.id == owner_id:
			# noinspection PyUnusedLocal,PyShadowingNames
			exiting = True
			await client.logout( )
			pass
		pass

	if do_update is True:
		print( f"{Fore.LIGHTCYAN_EX}Updating...{Fore.RESET}" )
		subprocess.Popen( f"python {os.getcwd()}\\admin.py" )
		exit( 0 )
		pass
	pass

@client.event
async def on_ready ( ):
	os.system( "cls" )
	print( f"{Fore.MAGENTA}Ready!!!{Fore.RESET}" )
	pass

client.run( token )

if exiting == False:
	subprocess.Popen( f"python {os.getcwd()}\\admin.py" )
	exit( 0 )
	pass
