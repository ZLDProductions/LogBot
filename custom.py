import ast
import os
import sqlite3

from colorama import init, Fore
from discord import Client, Message

from logbot_data import token

client = Client( )
init( )

commands = { }
_settings = f"{os.getcwd()}\\Discord Logs\\SETTINGS"
_commands = f"{_settings}\\custom_commands.txt"

sql = sqlite3.connect( f"{_settings}\\logbot.db" )
cursor = sql.cursor( )

try:
	reader = open( _commands, 'r' )
	commands = ast.literal_eval( reader.read( ) )
	reader.close( )
	del reader
	pass
except:
	writer = open( _commands, 'w' )
	writer.write( "" )
	writer.close( )
	del writer
	pass

def sqlread ( cmd: str ):
	cursor.execute( cmd )
	return cursor.fetchall( )

@client.event
async def on_ready ( ):
	os.system( "cls" )
	print( f"{Fore.MAGENTA}Ready!!!{Fore.RESET}" )
	pass

@client.event
async def on_message ( message: Message ):
	prefix = sqlread( f"SELECT prefix FROM Prefixes WHERE server='{message.server.id}';" )[ 0 ][ 0 ]
	begins = message.content.startswith
	if not message.server.id in commands.keys(): commands[message.server.id] = dict()

	if begins( f"c{prefix}add " ):
		cmd = message.content.replace( f'c{prefix}add ', '' ).split( '||' )
		if not cmd[0] == "":
			commands[message.server.id][cmd[0]] = cmd[1]
			await client.send_message(message.channel, f"```Created the command.```")
			print(f"{Fore.LIGHTMAGENTA_EX}Command {cmd[0]}:{cmd[1]} was created.{Fore.RESET}")
			pass
		else: await client.send_message(message.channel, f"```A command cannot be triggered like that!```")
		del cmd
		pass
	elif begins(f"c{prefix}remove "):
		cmd = message.content.replace(f"c{prefix}remove ", "")
		data = {cmd:commands[message.server.id][cmd]}
		del commands[message.server.id][cmd]
		await client.send_message(message.channel, "```Deleted the command.```")
		print(f"{Fore.LIGHTMAGENTA_EX}Command {cmd}:{data[cmd]} was deleted.{Fore.RESET}")
		del data
		del cmd
		pass
	elif begins(f"c{prefix}show"):
		tmp = '\n'.join(list(commands[message.server.id].keys()))
		await client.send_message(message.channel, f"```Commands:\n{tmp}```")
		del tmp
		pass

	for item in list(commands[message.server.id].keys()):
		if begins(item): await client.send_message(message.channel, commands[message.server.id][item])
		pass
	pass

client.run( token )
