import os
import subprocess
import traceback
from datetime import datetime

import discord
from colorama import Fore, init

from logbot_data import owner_id, token

client = discord.Client( )
init( )
exiting = False

discord_settings = f"{os.getcwd()}\\Discord Logs\\SETTINGS"
suggestions = f"{discord_settings}\\suggestions.txt"
reports = f"{discord_settings}\\bugs.txt"

def format_message ( msg: str, _tag: str ) -> list:
	"""
	:param msg: The string to format
	:param _tag: The tag to insert. Can be None. If not None, will insert tag at the beginning and end of each string in the result.
	:return: A list of strings from `msg`, where each string is no more than 2000 characters long.
	"""
	if not _tag is None:
		len_tag = len( _tag ) * 2
		len_str = 2000 - len_tag
		ret = [ f"{_tag}{msg[i:i+len_str]}{_tag}" for i in range( 0, len( msg ), len_str ) ]
		pass
	else:
		ret = [
			msg[ i:i + 2000 ]
			for i in range( 0, len( msg ), 2000 )
		]
		pass
	return ret

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
	writer.write( f"{datetime.now()} (dev.py) - {error_text}\n\n{prev_text}" )
	writer.close( )
	if "SystemExit" in error_text:
		exit( 0 )
		pass
	del writer
	pass

@client.event
async def on_message ( message: discord.Message ):
	global exiting
	try:
		begins = message.content.startswith
		if message.author.id == owner_id:
			if begins( "$edit-suggestions" ):
				if not " " in message.content:
					page = 0
					pass
				else:
					page = int( message.content.replace( "$edit-suggestions ", "" ) )
					pass
				items = [ ]
				# <editor-fold desc="Reading the Suggestions">
				reader = open( suggestions, 'r' )
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
							pass
						else:
							items[ -1 ] += f"\n{item}"
							pass
						pass
					pass
				# </editor-fold>
				msg1 = await client.send_message( message.channel, f"```{items[page]}```" )
				msg2 = await client.send_message( message.channel, f"```Type the new content:```" )
				msg = await client.wait_for_message( author=message.author, channel=message.channel )
				items[ page ] = msg.content
				items = ''.join( items )
				# <editor-fold desc="Saving the Suggestions">
				writer = open( suggestions, 'w' )
				writer.write( "\n" + str( items ) )
				writer.close( )
				# </editor-fold>
				await client.delete_messages( [ msg1, msg2 ] )
				del writer
				del msg
				del msg1
				del msg2
				del tmp
				del items
				del page
				del index
				del reader
				pass
			elif begins( "$suggestions" ):
				# <editor-fold desc="READER: suggestions">
				# noinspection PyShadowingNames
				reader = open( suggestions, 'r' )
				ret = f"Suggestions:{reader.read()}"
				reader.close( )
				# </editor-fold>
				for item in format_message( ret, "```" ):
					await client.send_message( message.channel, item )
					pass
				del ret
				del reader
				pass
			elif begins( "d$update" ) or begins( "logbot.dev.update" ):
				print( "{Fore.LIGHTCYAN_EX}Updating...{Fore.RESET}" )
				await client.close( )
				subprocess.Popen( "python " + os.getcwd( ) + "\\dev.py", False )
				exit( 0 )
				pass
			elif begins( "$exit" ) or begins( "logbot.dev.exit" ):
				exiting = True
				await client.logout( )
				pass
			elif begins( "$eval " ):
				cnt = message.content.replace( "$eval ", "" ).split( "\n" )
				def doeval ( lines ):
					_vars = { }
					for line in lines:
						try:
							if " = " in line:
								name = line.split( " = " )[ 0 ]
								func = eval( line.split( " = " )[ 1 ] )
								_vars[ name ] = func
								pass
							else:
								return str( eval( line ) ), "Success!"
							pass
						except: break
						pass
					return "ERROR", "Improper Syntax"
					pass
				tmp = doeval( cnt )
				e = discord.Embed( title=f"Evaluate {'; '.join(cnt)}", description="Results", colour=discord.Colour.dark_grey( ) )
				if tmp[ 1 ] == "Success!":
					e.add_field( name="Result", value=tmp[ 1 ] )
					e.add_field( name="Return", value=tmp[ 0 ] )
					pass
				else:
					e.add_field( name="Result", value=tmp[ 0 ] )
					e.add_field( name="Problem", value=tmp[ 1 ] )
					pass
				await client.send_message( message.channel, "Here you go!", embed=e )
				pass

			pass

		if begins( "$report " ):
			cnt = "-" + message.content.replace( '$report ', '' ).replace( "```", "'''" )
			try:
				reader = open( reports, 'r' )
				text = reader.read( )
				reader.close( )
				pass
			except:
				text = ""
				pass
			if f"{cnt}\n" in text:
				await client.send_message( message.channel, f"```There is already a report for \"{cnt}\"```" )
				pass
			else:
				writer = open( reports, 'a' )
				writer.write( f"{cnt}\n" )
				writer.close( )
				await client.send_message( message.channel, f"```Thank you for your report.```" )
				del writer
				pass
			del text
			del cnt
			pass
		elif begins( "$reports" ):
			reader = open( reports, 'r' )
			text = reader.read( )
			reader.close( )
			if len( text ) > 0:
				msgs = format_message( text, "```" )
				for msg in msgs:
					await client.send_message( message.channel, msg )
					pass
				pass
			else:
				await client.send_message( message.channel, f"```There are no bug reports yet.```" )
				pass
			del reader
			pass
		pass
	except:
		log_error( traceback.format_exc( ) )
		pass
	pass

@client.event
async def on_ready ( ):
	# os.system( "cls" )
	print( f"{Fore.MAGENTA}Dev Ready!!!{Fore.RESET}" )
	pass

client.run( token )

if not exiting:
	subprocess.Popen( f"python {os.getcwd()}\\dev.py" )
	exit( 0 )
	pass
