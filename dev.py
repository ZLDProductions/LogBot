"""
Developer Module
"""
import os
import subprocess
import traceback
from datetime import datetime

import discord
from colorama import Fore, init

from logbot_data import owner_id, token

CLIENT = discord.Client( )
init( )
EXITING = False

DISCORD_SETTINGS_PATH = f"{os.getcwd()}\\Discord Logs\\SETTINGS"
SUGGESTIONS_PATH = f"{DISCORD_SETTINGS_PATH}\\suggestions.txt"
REPORTS_PATH = f"{DISCORD_SETTINGS_PATH}\\bugs.txt"

def format_message ( msg: str, _tag: str ) -> list:
	"""
	:param msg: The string to format
	:param _tag: The tag to insert. Can be None.
	:return: A list of strings from `msg`, where each string is no more than 2000 characters long.
	"""
	if not _tag is None:
		len_tag = len( _tag ) * 2
		len_str = 2000 - len_tag
		ret = [
			f"{_tag}{msg[i:i+len_str]}{_tag}"
			for i in range(
				0,
				len( msg ),
				len_str
			)
		]
	else:
		ret = [
			msg[ i:i + 2000 ]
			for i in range(
				0,
				len( msg ),
				2000
			)
		]
	return ret

def log_error ( error_text: str ):
	"""
	Logs the bot's errors.
	:param error_text: The error message.
	"""
	file = f"{os.getcwd()}\\error_log.txt"
	prev_text = ""
	try:
		reader = open(
			file,
			'r'
		)
		prev_text = reader.read( )
		reader.close( )
		del reader
	except Exception:
		pass
	writer = open(
		file,
		'w'
	)
	writer.write( f"{datetime.now()} (dev.py) - {error_text}\n\n{prev_text}" )
	writer.close( )
	if "SystemExit" in error_text:
		exit( 0 )
	del writer

@CLIENT.event
async def on_message ( message: discord.Message ):
	"""
	Occurs when the bot receives a message.
	:param message: A discord.Message object.
	"""
	global EXITING
	try:
		begins = message.content.startswith
		if message.author.id == owner_id:
			if begins( "$edit-suggestions" ):
				if not " " in message.content:
					page = 0
				else:
					page = int(
						message.content.replace(
							"$edit-suggestions ",
							""
						)
					)
				items = [ ]
				# <editor-fold desc="Reading the Suggestions">
				reader = open(
					SUGGESTIONS_PATH,
					'r'
				)
				ret = reader.read( )
				reader.close( )
				# </editor-fold>
				# <editor-fold desc="Splitting the Suggestions">
				tmp = ret.split( "\n" )
				index = 0
				for item in tmp:
					if not item == "":
						if index % 5 == 0:
							items.append( f"\n{item}" )
						else:
							items[ -1 ] += f"\n{item}"
				# </editor-fold>
				msg1 = await CLIENT.send_message(
					message.channel,
					f"```{items[page]}```"
				)
				msg2 = await CLIENT.send_message(
					message.channel,
					f"```Type the new content:```"
				)
				msg = await CLIENT.wait_for_message(
					author=message.author,
					channel=message.channel
				)
				items[ page ] = msg.content
				items = ''.join( items )
				# <editor-fold desc="Saving the Suggestions">
				writer = open(
					SUGGESTIONS_PATH,
					'w'
				)
				writer.write( "\n" + str( items ) )
				writer.close( )
				# </editor-fold>
				await CLIENT.delete_messages(
					[
						msg1,
						msg2
					]
				)
				del writer
				del msg
				del msg1
				del msg2
				del tmp
				del items
				del page
				del index
				del reader
			elif begins( "$suggestions" ):
				# <editor-fold desc="READER: suggestions">
				# noinspection PyShadowingNames
				reader = open(
					SUGGESTIONS_PATH,
					'r'
				)
				ret = f"Suggestions:{reader.read()}"
				reader.close( )
				# </editor-fold>
				for item in format_message( ret, "```" ):
					await CLIENT.send_message(
						message.channel,
						item
					)
				del ret
				del reader
			elif begins( "d$update" ) or begins( "logbot.dev.update" ):
				print( "{Fore.LIGHTCYAN_EX}Updating...{Fore.RESET}" )
				await CLIENT.close( )
				subprocess.Popen( "python " + os.getcwd( ) + "\\dev.py", False )
				exit( 0 )
			elif begins( "$exit" ) or begins( "logbot.dev.exit" ):
				EXITING = True
				await CLIENT.logout( )
			elif begins( "$eval " ):
				cnt = message.content.replace(
					"$eval ",
					""
				).split( "\n" )
				def doeval ( lines ):
					"""
					Evaluates a piece of code.
					:param lines: The code.
					"""
					_vars = { }
					for line in lines:
						try:
							if " = " in line:
								name = line.split( " = " )[ 0 ]
								func = eval( line.split( " = " )[ 1 ] )
								_vars[ name ] = func
							else:
								return str( eval( line ) ), "Success!"
						except Exception:
							break
					return "ERROR", "Improper Syntax"
				tmp = doeval( cnt )
				embed_obj = discord.Embed(
					title=f"Evaluate {'; '.join(cnt)}",
					description="Results",
					colour=discord.Colour.dark_grey( )
				)
				if tmp[ 1 ] == "Success!":
					embed_obj.add_field(
						name="Result",
						value=tmp[ 1 ]
					)
					embed_obj.add_field(
						name="Return",
						value=tmp[ 0 ]
					)
				else:
					embed_obj.add_field(
						name="Result",
						value=tmp[ 0 ]
					)
					embed_obj.add_field(
						name="Problem",
						value=tmp[ 1 ]
					)
				await CLIENT.send_message(
					message.channel,
					"Here you go!",
					embed=embed_obj
				)
				del cnt
				del tmp
				del embed_obj
		if begins( "$report " ):
			cnt = "-" + message.content.replace(
				'$report ',
				''
			).replace(
				"```",
				"'''"
			)
			try:
				reader = open(
					REPORTS_PATH,
					'r'
				)
				text = reader.read( )
				reader.close( )
				del reader
			except Exception:
				text = ""
			if f"{cnt}\n" in text:
				await CLIENT.send_message(
					message.channel,
					f"```There is already a report for \"{cnt}\"```"
				)
			else:
				writer = open(
					REPORTS_PATH,
					'a'
				)
				writer.write( f"{cnt}\n" )
				writer.close( )
				await CLIENT.send_message( message.channel, f"```Thank you for your report.```" )
				del writer
			del text
			del cnt
		elif begins( "$reports" ):
			reader = open(
				REPORTS_PATH,
				'r'
			)
			text = reader.read( )
			reader.close( )
			if text:
				msgs = format_message(
					text,
					"```"
				)
				for msg in msgs:
					await CLIENT.send_message(
						message.channel,
						msg
					)
			else:
				await CLIENT.send_message(
					message.channel,
					f"```There are no bug reports yet.```"
				)
			del reader
	except Exception:
		log_error( traceback.format_exc( ) )

@CLIENT.event
async def on_ready ( ):
	"""
	Occurs when the bot logs in.
	"""
	# os.system( "cls" )
	print( f"{Fore.MAGENTA}Dev Ready!!!{Fore.RESET}" )

CLIENT.run( token )

if not EXITING:
	subprocess.Popen( f"python {os.getcwd()}\\dev.py" )
	exit( 0 )
