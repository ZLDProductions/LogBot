"""
Levels module.
"""
import ast
import os
import random
import sqlite3
import subprocess
import traceback
from datetime import datetime
from math import floor
from typing import Union

import discord
from colorama import Fore, init

from logbot_data import token, owner_id, bot_id

EXITING = False
init( )
CLIENT = discord.Client( )
DATA_PATH = f"{os.getcwd()}\\Discord Logs\\SETTINGS\\level_data"
DISABLES_PATH = f"{DATA_PATH}\\disables\\"
SQLA = sqlite3.connect( f"{DATA_PATH}\\data.db" )
CURSORA = SQLA.cursor( )

SQLB = sqlite3.connect( f"{os.getcwd()}\\Discord Logs\\SETTINGS\\logbot.db" )
CURSORB = SQLB.cursor( )

DEFAULTS = { }
DEFAULTS_PATH = f"{DATA_PATH}\\defaults.txt"

try:
	READER = open( DEFAULTS_PATH, 'r' )
	DEFAULTS = ast.literal_eval( READER.read( ) )
	READER.close( )
	del READER
except Exception:
	WRITER = open( DEFAULTS_PATH, 'w' )
	WRITER.write( str( DEFAULTS ) )
	WRITER.close( )
	del WRITER

def sqlread ( cmd: str ):
	"""
	Reads from an SQL DB
	:param cmd: The SQL Read command.
	:return: The data retrieved.
	"""
	CURSORA.execute( cmd )
	return CURSORA.fetchall( )

def sqlexecute ( cmd: str ):
	"""
	Executes an SQL statement.
	:param cmd: The SQL statement.
	"""
	CURSORA.executescript( cmd )
	SQLA.commit( )

def getprefix ( server: str ) -> str:
	"""
	Fetches the server's prefix.
	:param server: The server.
	:return: The prefix.
	"""
	CURSORB.execute( f"SELECT prefix FROM Prefixes WHERE server='{server}';" )
	return CURSORB.fetchall( )[ 0 ][ 0 ]

BASE = 200
MULTI = 1.5
DISABLED = False

SLOTS_RULES = """2 Consecutive Symbols : Bid\\*2
3 Consecutive Symbols : Bid\\*3
3 :atm: : Bid\\*10
3 :free: : Bid
3 :dollar: : +300
3 :moneybag: : +3000
3 :gem: : +30000"""
SLOTS_PATTERNS = [
	":one:",
	":two:",
	":three:",
	":four:",
	":atm:",
	":free:",
	":dollar:",
	":moneybag:",
	":gem:"
]

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
	writer_obj = open( file, 'w' )
	writer_obj.write( f"{datetime.now()} (levels.py) - {error_text}\n\n{prev_text}" )
	writer_obj.close( )
	if "SystemExit" in error_text:
		exit( 0 )
	del writer_obj

def read ( sid: str ):
	"""
	Reads server data.
	:param sid: The server id.
	"""
	global DISABLED

	# <editor-fold desc="Disables Check">
	res = sqlread( f"""
	SELECT COUNT(*)
	FROM disables
	WHERE server='{sid}';
	""".replace( "\t", "" ) )
	if res[ 0 ][ 0 ] == 0:
		sqlexecute( f"""
		INSERT INTO disables (server, disabled)
		VALUES ('{sid}', 0);
		""".replace( "\t", "" ) )
	# </editor-fold>
	# <editor-fold desc="Defaults">
	if not sid in DEFAULTS.keys( ):
		DEFAULTS[ sid ] = { "DM":"FALSE", "AlertChannel":"None" }
	# </editor-fold>

def save ( sid: str ):
	"""
	Saves plugin data.
	:param sid: The server id.
	"""
	global DISABLED
	# <editor-fold desc="_disables">
	sqlexecute( f"""
	UPDATE disables
	SET disabled={1 if DISABLED else 0}
	WHERE server='{sid}';
	""".replace( "\t", "" ) )
	# </editor-fold>
	# <editor-fold desc="Defaults">
	open( DEFAULTS_PATH, 'w' ).write( str( DEFAULTS ) )

# </editor-fold>

def parse_num ( num ) -> str:
	"""
	Parses a num to a more readable format.
	:param num: The number.
	:return: A more readable number.
	"""
	_num = str( num )
	_num = _num[ ::-1 ]
	if "e" in _num:
		_num = _num[ ::-1 ]
	else:
		_num = ','.join( [
			_num[ i:i + 3 ]
			for i in range( 0, len( _num ), 3 )
		] )[ ::-1 ]
	return str( _num )

def format_message ( cont: str ) -> list:
	"""
	Splits `cont` into several strings, each a maximum of 2000 characters in length. Adds ``` at each end automatically.
	:param cont: The string to format.
	:return: A list of strings. Each formatted into 2000 characters, including ``` at each end.
	"""
	return [
		f"```dos\n{item}```"
		for item in [
			cont[ i:i + 1000 ]
			for i in range( 0, len( cont ), 1000 )
		]
	] if len( cont ) > 1990 else [ f"```dos\n{cont}```" ]

def clamp ( _min: Union[ int, float ], _max: Union[ int, float ], val: Union[ int, float ] ) -> int:
	"""
	Clamps an int between two variables.
	:param _min: The minimum value.
	:param _max: The maximum value.
	:param val: The original integer.
	:return: The resulting integer.
	"""
	if val < _min:
		val = _min
	elif val > _max:
		val = _max
	return val

# noinspection PyTypeChecker,PyShadowingNames,PyUnresolvedReferences
@CLIENT.event
async def on_message ( message: discord.Message ):
	"""
	Occurs when the bot receives a message.
	:param message: A discord.Message object.
	"""
	global BASE, DISABLED, EXITING
	try:
		if not message.server is None:
			prefix = getprefix( message.server.id )
			try:
				if not message.server is None:
					read( message.server.id )
					for member in message.server.members:
						if sqlread( f"""
						SELECT COUNT(*)
						FROM levels
						WHERE server='{message.server.id}'
						AND member='{member.id}';
						""".replace( "\t", "" ) )[ 0 ][ 0 ] == 0:
							try:
								sqlexecute( f"""
								INSERT INTO levels (server, member, tier, rank, xp, xp_limit, multiplier, credits, cpm, dm, alert_channel)
								VALUES ('{message.server.id}', '{member.id}', 1, 0, 0, 200, 1.0, 0, 0, '{DEFAULTS[message.server.id]['DM']}', '{DEFAULTS[message.server.id]['AlertChannel']}');
								""".replace( "\t", "" ) )
							except Exception:
								sqlexecute( f"""
								INSERT INTO levels (server, member, tier, rank, xp, xp_limit, multiplier, credits, cpm, dm, alert_channel)
								VALUES ('{message.server.id}', '{member.id}', 1, 0, 0, 200, 1.0, 0, 0, 'TRUE', 'None');
								""".replace( "\t", "" ) )
				else:
					read( message.channel.id )
			except Exception:
				for member in message.server.members:
					sqlexecute( f"""
					UPDATE levels
					SET credits=0
					AND rank=0
					AND xp=0
					AND xp_limit=200
					AND cpm=0
					AND multiplier=1.0
					AND tier=1
					WHERE server='{message.server.id}'
					AND member='{member.id}';
					""".replace( "\t", "" ) )
			def startswith ( *msgs, val=message.content ):
				"""
				Checks a string for beginning substrings.
				:param msgs: The substrings.
				:param val: The string.
				:return: True or False.
				"""
				# noinspection PyShadowingNames
				for msg in msgs:
					if val.startswith( msg ):
						return True
				return False
			admin_role = discord.utils.find( lambda ro:ro.name == "LogBot Admin", message.server.roles )
			do_update = False
			bot = await CLIENT.get_user_info( "255379748828610561" )
			print( f"{message.author} : {message.server} : {message.content}" )

			DISABLED = sqlread( f"""
			SELECT disabled
			FROM disables
			WHERE server='{message.server.id}';
			""".replace( "\t", "" ) )[ 0 ][ 0 ]
			DISABLED = True if DISABLED == 1 else False

			if not DISABLED or message.author.id == owner_id:
				content = message.content
				if not content:
					content = " "
				earned = round( random.choice( range( 15, 26 ) ) * int( sqlread( f"""
				SELECT multiplier
				FROM levels
				WHERE server='{message.server.id}'
				AND member='{message.author.id}';
				""".replace( "\t", "" ) )[ 0 ][ 0 ] ) * clamp( 0.0, 1.0, len( content ) / 5 ) )
				sqlexecute( f"""
				UPDATE levels
				SET xp = xp+{earned}
				WHERE server='{message.server.id}'
				AND member='{message.author.id}';
				""".replace( "\t", "" ) )
				if len( content ) > 4:
					sqlexecute( f"""
					UPDATE levels
					SET credits=credits+(cpm*{round(len(content)/5)})
					WHERE server='{message.server.id}'
					AND member='{message.author.id}';
					""".replace( "\t", "" ) )

				_xp_limit = round( BASE * (MULTI ** (sqlread( f"""
				SELECT rank
				FROM levels
				WHERE server='{message.server.id}'
				AND member='{message.author.id}';
				""".replace( "\t", "" ) )[ 0 ][ 0 ])) )
				sqlexecute( f"""
				UPDATE levels
				SET xp_limit={_xp_limit}
				WHERE server='{message.server.id}'
				AND member='{message.author.id}';
				""".replace( "\t", "" ) )
				is_ranked_up = False
				prev_rank = sqlread( f"""
				SELECT rank
				FROM levels
				WHERE server='{message.server.id}'
				AND member='{message.author.id}';
				""".replace( "\t", "" ) )[ 0 ][ 0 ]
				while sqlread( f"""
				SELECT xp
				FROM levels
				WHERE server='{message.server.id}'
				AND member='{message.author.id}';
				""".replace( "\t", "" ) )[ 0 ][ 0 ] >= sqlread( f"""
				SELECT xp_limit
				FROM levels
				WHERE server='{message.server.id}'
				AND member='{message.author.id}';
				""".replace( "\t", "" ) )[ 0 ][ 0 ]:
					sqlexecute( f"""
					UPDATE levels
					SET xp=xp-xp_limit
					WHERE server='{message.server.id}'
					AND member='{message.author.id}';
					""".replace( "\t", "" ) )
					sqlexecute( f"""
					UPDATE levels
					SET xp_limit=xp_limit*1.5
					WHERE server='{message.server.id}'
					AND member='{message.author.id}';
					""".replace( "\t", "" ) )
					sqlexecute( f"""
					UPDATE levels
					SET rank=rank+1
					WHERE server='{message.server.id}'
					AND member='{message.author.id}';
					""".replace( "\t", "" ) )
					sqlexecute( f"""
					UPDATE levels
					SET credits=credits+(tier*50)
					WHERE server='{message.server.id}'
					AND member='{message.author.id}';
					""".replace( "\t", "" ) )
					is_ranked_up = True
				if is_ranked_up:
					do_dm = sqlread( f"""
					SELECT dm, alert_channel
					FROM levels
					WHERE server='{message.server.id}'
					AND member='{message.author.id}';
					""".replace( "\t", "" ) )[ 0 ]
					_tdat = sqlread( f"""
					SELECT rank, tier*50
					FROM levels
					WHERE server='{message.server.id}'
					AND member='{message.author.id}';
					""".replace( "\t", "" ) )[ 0 ]
					if do_dm[ 0 ].lower( ) == "true":
						await CLIENT.send_message( message.author, f"Congrats, {message.author}, you just leveled up to rank {_tdat[0]} from rank {prev_rank} and have earned {parse_num((_tdat[0] - prev_rank) * _tdat[1])} credits in {message.server.name}!" )
						print( f"{Fore.GREEN}{message.author} has leveled up to {_tdat[0]}!{Fore.RESET}" )
					else:
						alert_channel = discord.utils.find( lambda c:c.id == do_dm[ 1 ], message.server.channels )
						if not alert_channel is None:
							await CLIENT.send_message( alert_channel, f"Congrats, {message.author}, you just leveled up to rank {_tdat[0]} from rank {prev_rank} and have earned {parse_num((_tdat[0] - prev_rank) * _tdat[1])} credits!" )
						else:
							if do_dm[ 1 ].lower( ) == "self":
								await CLIENT.send_message( message.channel, f"Congrats, {message.author}, you just leveled up to rank {_tdat[0]} from rank {prev_rank} and have earned {parse_num((_tdat[0] - prev_rank) * _tdat[1])} credits!" )
						print( f"{Fore.GREEN}{message.author} has leveled up to {_tdat[0]}!{Fore.RESET}" )
					if message.author == bot:
						if _tdat[ 0 ] >= 100:
							sqlexecute( f"""
							UPDATE levels
							SET tier=tier+{floor(_tdat[0]/100)}
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace( "\t", "" ) )
							sqlexecute( f"""
							UPDATE levels
							SET credits=0
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace( "\t", "" ) )
							sqlexecute( f"""
							UPDATE levels
							SET rank=0
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace( "\t", "" ) )
							sqlexecute( f"""
							UPDATE levels
							SET xp=0
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace( "\t", "" ) )
							sqlexecute( f"""
							UPDATE levels
							SET cpm=0
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace( "\t", "" ) )
							sqlexecute( f"""
							UPDATE levels
							SET multiplier=1.0*tier
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace( "\t", "" ) )

				# <editor-fold desc="milestones">
				try:
					_milestone_tmp = sqlread( f"""
					SELECT item, _limit, role
					FROM milestones
					WHERE server="{message.server.id}";
					""".replace( "\t", "" ) )
					for _item_, _limit_, _role_ in _milestone_tmp:
						if _item_ == "tier":
							tmp_role = discord.utils.find( lambda _r:_r.id == _role_, message.server.roles )
							_tmp_res = sqlread( f"""
							SELECT tier
							FROM levels
							WHERE server="{message.server.id}"
							AND member="{message.author.id}";
							""".replace( "\t", "" ) )[ 0 ][ 0 ]
							if _tmp_res >= _limit_:
								await CLIENT.add_roles( message.author, tmp_role )
						elif _item_ == "rank":
							tmp_role = discord.utils.find( lambda _r:_r.id == _role_, message.server.roles )
							_tmp_res = sqlread( f"""
							SELECT rank
							FROM levels
							WHERE server="{message.server.id}"
							AND member="{message.author.id}";
							""".replace( "\t", "" ) )[ 0 ][ 0 ]
							if _tmp_res >= _limit_:
								await CLIENT.add_roles( message.author, tmp_role )
				except Exception:
					traceback.format_exc( )
				# </editor-fold>

				if startswith( f"l{prefix}rank" ):
					if not message.mentions:
						u_data = sqlread( f"""
						SELECT tier, rank, xp, xp_limit, multiplier, credits, cpm, dm, alert_channel
						FROM levels
						WHERE server='{message.server.id}'
						AND member='{message.author.id}';
						""".replace( "\t", "" ) )[ 0 ]
						bar = """```
						┌────────────────────┐
						│                    │
						└────────────────────┘
						```""".replace( "\t", "" )
						curr_xp = round( u_data[ 2 ] )
						need_xp = round( u_data[ 3 ] )
						bar_len = round( ((curr_xp / need_xp) * 2) * 10 )
						bar = bar.replace( " ", "█", bar_len )
						precision = len( str( u_data[ 4 ] ).split( '.' )[ 0 ] ) + 1
						_m = f"{float(u_data[4]):1.{precision}}"
						_t = _m.split( "." )
						if len( _t ) == 1:
							_t.append( "0" )
						embed_obj = discord.Embed( title=str( message.author ), description=f"Ranking Information for {str(message.author)}", colour=message.author.colour ) \
							.add_field( name="Rank", value=str( u_data[ 1 ] ), inline=False ) \
							.add_field( name="XP", value=str( parse_num( round( u_data[ 2 ] ) ) ) + "/" + parse_num( round( int( u_data[ 3 ] ) ) ), inline=False ) \
							.add_field( name="Credits", value=parse_num( u_data[ 5 ] ), inline=False ) \
							.add_field( name="Multiplier", value=f"{parse_num(_t[0])}.{_t[1]}", inline=False ) \
							.add_field( name="CPM", value=parse_num( u_data[ 6 ] ), inline=False ) \
							.add_field( name="Tier", value=str( u_data[ 0 ] ), inline=False ) \
							.add_field( name="DM", value=str( u_data[ 7 ] ), inline=False ) \
							.add_field( name="Alert Channel", value=str( discord.utils.find( lambda c:c.id == u_data[ 8 ], message.server.channels ) ), inline=False )
						await CLIENT.send_message( message.channel, bar, embed=embed_obj )
					else:
						user = message.mentions[ 0 ]
						u_data = sqlread( f"""
						SELECT tier, rank, xp, xp_limit, multiplier, credits, cpm, dm, alert_channel
						FROM levels
						WHERE server='{message.server.id}'
						AND member='{user.id}';
						""".replace( "\t", "" ) )[ 0 ]
						bar = """```
						┌────────────────────┐
						│                    │
						└────────────────────┘
						```""".replace( "\t", "" )
						curr_xp = round( u_data[ 2 ] )
						need_xp = round( u_data[ 3 ] )
						bar_len = round( ((curr_xp / need_xp) * 2) * 10 )
						bar = bar.replace( " ", "█", bar_len )
						tmp = round( BASE * (MULTI ** u_data[ 1 ]) )
						precision = len( str( u_data[ 4 ] ).split( '.' )[ 0 ] ) + 1
						_m = f"{float(u_data[4]):1.{precision}}"
						_t = _m.split( "." )
						if len( _t ) == 1:
							_t.append( "0" )
						embed_obj = discord.Embed( title=str( user ), description=f"Ranking Information for {str(user)}", colour=user.colour ) \
							.add_field( name="Rank", value=str( u_data[ 1 ] ), inline=False ) \
							.add_field( name="XP", value=str( parse_num( round( u_data[ 2 ] ) ) ) + "/" + parse_num( round( tmp ) ), inline=False ) \
							.add_field( name="Credits", value=parse_num( u_data[ 5 ] ), inline=False ) \
							.add_field( name="Multiplier", value=f"{parse_num(_t[0])}.{_t[1]}", inline=False ) \
							.add_field( name="CPM", value=parse_num( u_data[ 6 ] ), inline=False ) \
							.add_field( name="Tier", value=str( u_data[ 0 ] ), inline=False ) \
							.add_field( name="DM", value=str( u_data[ 7 ] ), inline=False ) \
							.add_field( name="Alert Channel", value=str( discord.utils.find( lambda c:c.id == u_data[ 8 ], message.server.channels ) ), inline=False )
						await CLIENT.send_message( message.channel, bar, embed=embed_obj )
				elif startswith( f"l{prefix}levels" ):
					ret = [ ]
					user_rank = 0
					tmp = [ ]
					result = sqlread( f"""
					SELECT member, tier-1, rank
					FROM levels
					WHERE ((tier - 1) * 100) + rank > 0
					AND server = '{message.server.id}'
					ORDER BY ((tier - 1) * 100) + rank DESC, xp DESC;
					""".replace( "\t", "" ) )
					append = ret.append
					for index, item in enumerate( result ):
						if item[ 0 ] == message.author.id:
							user_rank = index + 1
						# user = await client.get_user_info( result[ i ][ 0 ] )
						user = message.server.get_member( item[ 0 ] )
						append( f"{user} : {(item[1]*100)+item[2]}" )
					append = tmp.append
					for index, item in enumerate( ret ):
						if index % 50 == 0:
							append( item + "\n" )
						else:
							tmp[ len( tmp ) - 1 ] += item + "\n"
					for item in tmp:
						await CLIENT.send_message( message.channel, f"```{item}```" )
					await CLIENT.send_message( message.channel, f"```You are ranked: #{user_rank}```" )
				elif startswith( f"l{prefix}place" ):
					leaderboard = sqlread( f"""
					SELECT member, ((tier - 1) * 100), rank
					FROM levels
					WHERE ((tier-1)*100) + rank > 0
					AND server='{message.server.id}'
					ORDER BY ((tier - 1) * 100) + rank DESC, xp DESC;
					""".replace( "\t", "" ) )
					if message.mentions:
						users = message.mentions
						for user in users:
							is_ranked = False
							rank = 0
							for index, item in enumerate( leaderboard ):
								if item[ 0 ] == user.id:
									is_ranked = True
									rank = index
									break
							if is_ranked:
								await CLIENT.send_message( message.channel, f"```{user} is ranked #{rank+1}```" )
							else:
								await CLIENT.send_message( message.channel, f"```{user} is not ranked.```" )
					else:
						is_ranked = False
						rank = 0
						for index, item in enumerate( leaderboard ):
							if item[ 0 ] == message.author.id:
								is_ranked = True
								rank = index
								break
						if is_ranked:
							await CLIENT.send_message( message.channel, f"```{message.author} is ranked #{rank + 1}```" )
						else:
							await CLIENT.send_message( message.channel, f"```{message.author} is not ranked.```" )
				elif startswith( f"l{prefix}buy " ):
					content = message.content.replace( f"l{prefix}buy ", "" ).split( " " )
					if content[ 0 ].lower( ) == "mul" or content[ 0 ].lower( ) == "multiplier":
						if len( content ) > 1:
							if sqlread( f"""
							SELECT credits
							FROM levels
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace( "\t", "" ) )[ 0 ][ 0 ] >= floor( 250 * int( content[ 1 ] ) ):
								sqlexecute( f"""
								UPDATE levels
								SET multiplier=multiplier+(0.1*{int(content[1])})
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace( "\t", "" ) )
								sqlexecute( f"""
								UPDATE levels
								SET credits=credits-{floor(250*int(content[1]))}
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace( "\t", "" ) )
								await CLIENT.send_message( message.channel, f"```Bought {parse_num(int(content[1]))} multipliers, spending {parse_num(250*int(content[1]))} credits.```" )
							elif sqlread( f"""
							SELECT credits
							FROM levels
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace( "\t", "" ) )[ 0 ][ 0 ] >= 250:
								num = floor( sqlread( f"""
							SELECT credits
							FROM levels
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace( "\t", "" ) )[ 0 ][ 0 ] / 250 )
								sqlexecute( f"""
								UPDATE levels
								SET multiplier=multiplier+(0.1*{num})
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace( "\t", "" ) )
								sqlexecute( f"""
								UPDATE levels
								SET credits=credits-{floor(250*num)}
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace( "\t", "" ) )
								await CLIENT.send_message( message.channel, f"```Bought {parse_num(num)} multipliers, spending {parse_num(floor(num*250))} credits.```" )
							else:
								await CLIENT.send_message( message.channel, "```You do not have enough credits to purchase this. Earn more by leveling up.```" )
						else:
							num = floor( sqlread( f"""
							SELECT credits
							FROM levels
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace( "\t", "" ) )[ 0 ][ 0 ] / 250 )
							sqlexecute( f"""
							UPDATE levels
							SET multiplier=multiplier+(0.1*{num})
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace( "\t", "" ) )
							sqlexecute( f"""
							UPDATE levels
							SET credits=credits-{floor(250*num)}
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace( "\t", "" ) )
							await CLIENT.send_message( message.channel, f"```Bought {parse_num(num)} multipliers, spending {parse_num(floor(num*250))} credits.```" )
					elif content[ 0 ].lower( ) == "cpm":
						if len( content ) > 1:
							if sqlread( f"""
							SELECT credits
							FROM levels
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace( "\t", "" ) )[ 0 ][ 0 ] >= floor( 1000 * int( content[ 1 ] ) ):
								sqlexecute( f"""
								UPDATE levels
								SET cpm=cpm+(5*{int(content[1])})
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace( "\t", "" ) )
								sqlexecute( f"""
								UPDATE levels
								SET credits=credits-{floor(1000*int(content[1]))}
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace( "\t", "" ) )
								await CLIENT.send_message( message.channel, f"```Bought {parse_num(int(content[1])*5)} CPM, spending {parse_num(1000*int(content[1]))} credits.```" )
							elif sqlread( f"""
							SELECT credits
							FROM levels
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace( "\t", "" ) )[ 0 ][ 0 ] >= 1000:
								num = floor( sqlread( f"""
								SELECT credits
								FROM levels
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace( "\t", "" ) )[ 0 ][ 0 ] / 1000 )
								sqlexecute( f"""
								UPDATE levels
								SET cpm=cpm+(5*{num})
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace( "\t", "" ) )
								sqlexecute( f"""
								UPDATE levels
								SET credits=credits-{floor(1000*num)}
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace( "\t", "" ) )
								await CLIENT.send_message( message.channel, f"```Bought {parse_num(num*5)} CPM, spending {parse_num(floor(num*1000))} credits.```" )
							else:
								await CLIENT.send_message( message.channel, "```You do not have enough credits to purchase this. Earn more by leveling up.```" )
						else:
							num = floor( sqlread( f"""
							SELECT credits
							FROM levels
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace( "\t", "" ) )[ 0 ][ 0 ] / 1000 )
							sqlexecute( f"""
							UPDATE levels
							SET cpm=cpm+(5*{num})
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace( "\t", "" ) )
							sqlexecute( f"""
							UPDATE levels
							SET credits=credits-{floor(1000*num)}
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace( "\t", "" ) )
							await CLIENT.send_message( message.channel, f"```Bought {parse_num(num*5)} CPM, spending {parse_num(floor(num*1000))} credits.```" )
					elif content[ 0 ].lower( ) == "tier":
						if len( content ) > 1:
							if sqlread( f"""
							SELECT credits
							FROM levels
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace( "\t", "" ) )[ 0 ][ 0 ] >= floor( 10000 * int( content[ 1 ] ) ) and sqlread( f"""
							SELECT rank
							FROM levels
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace( "\t", "" ) )[ 0 ][ 0 ] >= floor( 100 * int( content[ 1 ] ) ):
								num = int( content[ 1 ] )
								sqlexecute( f"""
								UPDATE levels
								SET tier=tier+num
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace( "\t", "" ) )
								sqlexecute( f"""
								UPDATE levels
								SET credits=credits-{floor(num*10000)}
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace( "\t", "" ) )
								sqlexecute( f"""
								UPDATE levels
								SET rank=rank-{floor(num*100)}
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace( "\t", "" ) )
								sqlexecute( f"""
								UPDATE levels
								SET xp=0
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace( "\t", "" ) )
								sqlexecute( f"""
								UPDATE levels
								SET cpm=0
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace( "\t", "" ) )
								sqlexecute( f"""
								UPDATE levels
								SET multiplier=1.0*tier
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace( "\t", "" ) )
								if not message.author == bot:
									do_dm = sqlread( f"""
									SELECT dm, tier
									FROM levels
									WHERE server='{message.server.id}'
									AND member='{message.author.id}';
									""".replace( "\t", "" ) )[ 0 ]
									if do_dm[ 0 ].lower( ) == 'true':
										await CLIENT.send_message( message.author, f"You have tiered up, {message.author}. You are now Tier {do_dm[1]}!" )
										print( f"{Fore.GREEN}{message.author} has tiered up to {do_dm[1]} in {message.server}!{Fore.RESET}" )
									else:
										await CLIENT.send_message( message.channel, f"You have tiered up, {message.author}. You are now Tier {do_dm[1]}!" )
										print( f"{Fore.GREEN}{message.author} has tiered up to {do_dm[1]} in {message.server}!{Fore.RESET}" )
								await CLIENT.send_message( message.channel, f"```Bought {parse_num(num)} Tiers, spending {parse_num(floor(num*10000))} credits and {parse_num(floor(num*100))} ranks.```" )
							elif sqlread( f"""
							SELECT credits
							FROM levels
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace( "\t", "" ) )[ 0 ][ 0 ] >= 10000 and sqlread( f"""
							SELECT rank
							FROM levels
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace( "\t", "" ) )[ 0 ][ 0 ] >= 100:
								creds = floor( sqlread( f"""
							SELECT credits
							FROM levels
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace( "\t", "" ) )[ 0 ][ 0 ] / 10000 )
								ranks = floor( sqlread( f"""
							SELECT rank
							FROM levels
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace( "\t", "" ) )[ 0 ][ 0 ] / 100 )
								num = creds if creds <= ranks else ranks
								sqlexecute( f"""
								UPDATE levels
								SET tier=tier+{num}
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace( "\t", "" ) )
								sqlexecute( f"""
								UPDATE levels
								SET credits=credits-{floor(num*10000)}
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace( "\t", "" ) )
								sqlexecute( f"""
								UPDATE levels
								SET rank=rank-{floor(num*100)}
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace( "\t", "" ) )
								sqlexecute( f"""
								UPDATE levels
								SET xp=0
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace( "\t", "" ) )
								sqlexecute( f"""
								UPDATE levels
								SET cpm=0
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace( "\t", "" ) )
								sqlexecute( f"""
								UPDATE levels
								SET multiplier=1.0*tier
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace( "\t", "" ) )
								if not message.author == bot:
									do_dm = sqlread( f"""
									SELECT dm, tier
									FROM levels
									WHERE server='{message.server.id}'
									AND member='{message.author.id}';
									""".replace( "\t", "" ) )[ 0 ]
									if do_dm[ 0 ].lower( ) == "true":
										await CLIENT.send_message( message.author, f"You have tiered up, {message.author}. You are now Tier {do_dm[1]}!" )
										print( f"{Fore.GREEN}{message.author} has tiered up to {do_dm[1]} in {message.server}!{Fore.RESET}" )
									else:
										await CLIENT.send_message( message.channel, f"You have tiered up, {message.author}. You are now Tier {do_dm[1]}!" )
										print( f"{Fore.GREEN}{message.author} has tiered up to {do_dm[1]} in {message.server}!{Fore.RESET}" )
								await CLIENT.send_message( message.channel, f"```Bought {parse_num(num)} Tiers, spending {parse_num(floor(num*10000))} credits and {parse_num(floor(num*100))} ranks.```" )
							else:
								await CLIENT.send_message( message.channel, "```You do not have enough credits/ranks to purchase this. Earn more by leveling up." )
						else:
							creds = floor( sqlread( f"""
							SELECT credits
							FROM levels
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace( "\t", "" ) )[ 0 ][ 0 ] / 10000 )
							ranks = floor( sqlread( f"""
							SELECT rank
							FROM levels
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace( "\t", "" ) )[ 0 ][ 0 ] / 100 )
							num = creds if creds <= ranks else ranks
							sqlexecute( f"""
							UPDATE levels
							SET tier=tier+{num}
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace( "\t", "" ) )
							sqlexecute( f"""
							UPDATE levels
							SET credits=0
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace( "\t", "" ) )
							sqlexecute( f"""
							UPDATE levels
							SET rank=0
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace( "\t", "" ) )
							sqlexecute( f"""
							UPDATE levels
							SET xp=0
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace( "\t", "" ) )
							sqlexecute( f"""
							UPDATE levels
							SET cpm=0
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace( "\t", "" ) )
							sqlexecute( f"""
							UPDATE levels
							SET multiplier=1.0*tier
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace( "\t", "" ) )
							if not message.author == bot:
								do_dm = sqlread( f"""
								SELECT dm, tier
								FROM levels
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace( "\t", "" ) )[ 0 ]
								if do_dm[ 0 ].lower( ) == "true":
									await CLIENT.send_message( message.author, f"You have tiered up, {message.author}. You are now Tier {do_dm[1]}!" )
									print( f"{Fore.GREEN}{message.author} has tiered up to {do_dm[1]} in {message.server}!{Fore.RESET}" )
								else:
									await CLIENT.send_message( message.channel, f"You have tiered up, {message.author}. You are now Tier {do_dm[1]}!" )
									print( f"{Fore.GREEN}{message.author} has tiered up to {do_dm[1]} in {message.server}!{Fore.RESET}" )
							await CLIENT.send_message( message.channel, f"```Bought {parse_num(num)} Tiers, spending {parse_num(floor(num*10000))} credits and {parse_num(floor(num*100))} ranks.```" )
				elif startswith( f"l{prefix}shop" ):
					udat = sqlread( f"""
					SELECT credits, rank
					FROM levels
					WHERE server='{message.server.id}'
					AND member='{message.author.id}';
					""".replace( "\t", "" ) )[ 0 ]
					creds = floor( udat[ 0 ] / 100000 )
					ranks = floor( udat[ 1 ] / 100 )
					buy_tier = creds if creds < ranks else ranks

					string = f"""```
					Items:
					mul • Multiplier +0.1 - 250 credits ~ Buyable: {parse_num(floor(udat[0] / 250))}
					cpm • Credits Per Message +5 - 1,000 credits ~ Buyable: {parse_num(floor(udat[0] / 1000))}
					tier • Tier +1 - 10,000 credits + 100 ranks ~ Buyable: {parse_num(buy_tier)}
					```
					""".replace( "\t", "" )
					await CLIENT.send_message( message.channel, string )
					del udat
					del creds
					del ranks
					del buy_tier
					del string
				elif startswith( f"l{prefix}gift " ):
					content = message.content.replace( f"l{prefix}gift ", "" ).split( " " )
					gift = float( content[ 1 ] )
					user = message.mentions[ 0 ]
					_type = content[ 0 ]
					if _type == "xp":
						if sqlread( f"""
						SELECT xp
						FROM levels
						WHERE server='{message.server.id}'
						AND member='{message.author.id}';
						""".replace( "\t", "" ) )[ 0 ][ 0 ] >= gift:
							sqlexecute( f"""
							UPDATE levels
							SET xp=xp+{gift}
							WHERE server='{message.server.id}'
							AND member='{user.id}';
							""".replace( "\t", "" ) )
							sqlexecute( f"""
							UPDATE levels
							SET xp=xp-{gift}
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace( "\t", "" ) )
							await CLIENT.send_message( message.channel, f"```Gifted {user} with {parse_num(str(gift).split('.')[0]) + str(gift).split('.')[1]} XP!```" )
						else:
							await CLIENT.send_message( message.channel, f"```You do not have enough XP for that!```" )
					elif _type == "cred":
						if sqlread( f"""SELECT credits FROM levels WHERE server='{message.server.id}' AND member='{message.author.id}';""" )[ 0 ][ 0 ] >= gift:
							sqlexecute( f"""
							UPDATE levels
							SET credits=credits+{gift}
							WHERE server='{message.server.id}'
							AND member='{user.id}';
							""".replace( "\t", "" ) )
							sqlexecute( f"""
							UPDATE levels
							SET credits=credits-{gift}
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace( "\t", "" ) )
							await CLIENT.send_message( message.channel, f"```Gifted {user} with {parse_num(str(gift).split('.')[0])} credits!```" )
						else:
							await CLIENT.send_message( message.channel, f"```You do not have enough credits to do that!```" )
					elif _type == "cpm":
						if sqlread( f"""
						SELECT cpm
						FROM levels
						WHERE server='{message.server.id}'
						AND member='{message.author.id}';
						""".replace( "\t", "" ) )[ 0 ][ 0 ] >= gift:
							sqlexecute( f"""
							UPDATE levels
							SET cpm=cpm+{gift}
							WHERE server='{message.server.id}'
							AND member='{user.id}';
							""".replace( "\t", "" ) )
							sqlexecute( f"""
							UPDATE levels
							SET cpm=cpm-{gift}
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace( "\t", "" ) )
							await CLIENT.send_message( message.channel, f"```Gifted {user} with {parse_num(str(gift).split('.')[0]) + str(gift).split('.')[1]} CPM!```" )
						else:
							await CLIENT.send_message( message.channel, f"```You do not have enough CPM to do that!```" )
					elif _type == "mul":
						if sqlread( f"""
						SELECT multiplier
						FROM levels
						WHERE server='{message.server.id}'
						AND member='{message.author.id}';
						""".replace( "\t", "" ) )[ 0 ][ 0 ] >= gift:
							sqlexecute( f"""
							UPDATE levels
							SET multiplier=multiplier+{gift}
							WHERE server='{message.server.id}'
							AND member='{user.id}';
							""".replace( "\t", "" ) )
							sqlexecute( f"""
							UPDATE levels
							SET multiplier=multiplier-{gift}
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace( "\t", "" ) )
							await CLIENT.send_message( message.channel, f"```Gifted {user} with {parse_num(str(gift).split('.')[0]) + str(gift).split('.')[1]} multipliers!```" )
						else:
							await CLIENT.send_message( message.channel, f"```You do not have enough credits to do that!```" )
					del content
					del gift
					del user
					del _type
				elif startswith( f"l{prefix}award " ):
					if admin_role in message.author.roles or message.author.id == owner_id:
						content = message.content.replace( f"l{prefix}award ", "" )
						content = content.split( " " )
						selection = None
						_type = content[ 0 ].lower( )
						gift = int( content[ 1 ] ) if not len( content[ 1 ] ) > 16 else int( "9999999999999999" )
						user = message.mentions
						role = message.role_mentions
						if not role and not user:
							role.append( message.server.default_role )
						if _type == "cred":
							_type = "credits"
							if len( role ) >= 1:
								for member in message.server.members:
									for _role in role:
										if _role in member.roles:
											sqlexecute( f"""
											UPDATE levels
											SET credits=credits+{gift}
											WHERE server='{message.server.id}'
											AND member='{member.id}';
											""".replace( "\t", "" ) )
								selection = ', '.join( [ str( r ) for r in role ] )
							else:
								if isinstance( user, list ):
									for uobj in user:
										sqlexecute( f"""
										UPDATE levels
										SET credits=credits+{gift}
										WHERE server='{message.server.id}'
										AND member='{uobj.id}';
										""".replace( "\t", "" ) )
									selection = ', '.join( [ str( u ) for u in user ] )
								else:
									sqlexecute( f"""
									UPDATE levels
									SET credits=credits+{gift}
									WHERE server='{message.server.id}'
									AND member='{message.author.id}'
									""".replace( "\t", "" ) )
									selection = user
						elif _type == "cpm":
							_type = "CPM"
							if len( role ) >= 1:
								for member in message.server.members:
									for _role in role:
										if _role in member.roles:
											sqlexecute( f"""
											UPDATE levels
											SET cpm=cpm+{gift}
											WHERE server='{message.server.id}'
											AND member='{member.id}';
											""".replace( "\t", "" ) )
								if isinstance( role, list ):
									selection = ', '.join( [
										str( r )
										for r in role
									] )
								else:
									selection = str( role )
							else:
								if isinstance( user, list ):
									for _user in user:
										sqlexecute( f"""
										UPDATE levels
										SET cpm=cpm+{gift}
										WHERE server='{message.server.id}'
										AND member='{_user.id}';
										""".replace( "\t", "" ) )
									selection = ', '.join( [
										str( u )
										for u in user
									] )
								else:
									sqlexecute( f"""
									UPDATE levels
									SET cpm=cpm+{gift}
									WHERE server='{message.server.id}'
									AND member='{user.id}';
									""".replace( "\t", "" ) )
									selection = user
						elif _type == "xp":
							_type = "experience"
							if len( role ) >= 1:
								for member in message.server.members:
									for _role in role:
										if _role in member.roles:
											sqlexecute( f"""
											UPDATE levels
											SET xp=xp+{gift}
											WHERE server='{message.server.id}'
											AND member='{member.id}';
											""".replace( "\t", "" ) )
								if isinstance( role, list ):
									selection = ', '.join( [
										str( r )
										for r in role
									] )
								else:
									selection = role.name
							else:
								if isinstance( user, list ):
									for _user in user:
										sqlexecute( f"""UPDATE levels SET xp=xp+{gift} WHERE server='{message.server.id}' AND member='{_user.id}';""".replace( "\t", "" ) )
									selection = user[ 0 ]
								else:
									sqlexecute( f"""
									UPDATE levels
									SET xp=xp+{gift}
									WHERE server='{message.server.id}'
									AND member='{user.id}';
									""".replace( "\t", "" ) )
									selection = user
						elif _type == "rank":
							_type = "ranks"
							if len( role ) >= 1:
								for member in message.server.members:
									for _role in role:
										if _role in member.roles:
											sqlexecute( f"""
											UPDATE levels
											SET rank=rank+{gift}
											WHERE server='{message.server.id}'
											AND member='{member.id}';
											""".replace( "\t", "" ) )
								if isinstance( role, list ):
									selection = ', '.join( [
										str( r )
										for r in role
									] )
								else:
									selection = role.name
							else:
								if isinstance( user, list ):
									for _user in user:
										sqlexecute( f"""
										UPDATE levels
										SET rank=rank+{gift}
										WHERE server='{message.server.id}'
										AND member='{_user.id}';
										""".replace( "\t", "" ) )
									selection = ', '.join( [
										str( u )
										for u in user
									] )
								else:
									sqlexecute( f"""
									UPDATE levels
									SET rank=rank+{gift}
									WHERE server='{message.server.id}'
									AND member='{user.id}';
									""".replace( "\t", "" ) )
									selection = user
						elif _type == "mul":
							_type = "multipliers"
							if len( role ) >= 1:
								for member in message.server.members:
									for _role in role:
										if _role in member.roles:
											sqlexecute( f"""
											UPDATE levels
											SET multiplier=multiplier+{gift}
											WHERE server='{message.server.id}'
											AND member='{member.id}';
											""".replace( "\t", "" ) )
								if isinstance( role, list ):
									selection = ', '.join( [
										str( r )
										for r in role
									] )
								else:
									selection = role.name
							else:
								if isinstance( user, list ):
									for _user in user:
										sqlexecute( f"""
										UPDATE levels
										SET multiplier=multiplier+{gift}
										WHERE server='{message.server.id}'
										AND member='{_user.id}';
										""".replace( "\t", "" ) )
									selection = ', '.join( [
										str( u )
										for u in user
									] )
								# if isinstance(user, list):
								# 	sqlexecute(f"""
								# 	UPDATE levels
								# 	SET multiplier=multiplier+{gift}
								# 	WHERE server='{message.server.id}'
								# 	AND member='{_user.id}';
								# 	""".replace("\t", ""))
								# 	selection = str(user)
								# 	pass
						elif _type == "tier":
							_type = "tiers"
							if len( role ) >= 1:
								for member in message.server.members:
									for _role in role:
										if _role in member.roles:
											sqlexecute( f"""
											UPDATE levels
											SET tier=tier+{gift}
											WHERE server='{message.server.id}'
											AND member='{member.id}';
											""".replace( "\t", "" ) )
								if isinstance( role, list ):
									selection = ', '.join( [
										str( r )
										for r in role
									] )
								else:
									selection = role.name
							else:
								if isinstance( user, list ):
									for _user in user:
										sqlexecute( f"""
										UPDATE levels
										SET tier=tier+{gift}
										WHERE server='{message.server.id}'
										AND member='{_user.id}';
										""".replace( "\t", "" ) )
									selection = ', '.join( [
										str( u )
										for u in user
									] )

						save( message.server.id )
						await CLIENT.send_message( message.channel, f"```Awarded {selection} with {parse_num(gift)} {_type}!```" )
						del selection
						del _type
						del gift
						del content
						del user
						del role
					else:
						await CLIENT.send_message( message.channel, "```Only admins can award users!```" )
				elif startswith( f"l{prefix}estimate " ):
					content = message.content.replace( f"l{prefix}estimate ", "" )
					content = content.split( "->" )
					try:
						total = 0
						for i in range( int( content[ 0 ] ), int( content[ 1 ] ) + 1 ):
							total += round( BASE * (MULTI ** int( i )) )
						await CLIENT.send_message( message.channel, f"{content[0]}->{content[1]}\n{parse_num(total)} xp needed." )
						del total
					except Exception:
						await CLIENT.send_message( message.channel, f"∞" )
				elif startswith( f"l{prefix}slots " ):
					cnt = message.content.replace( f"l{prefix}slots ", "" ).replace( "max", str( sqlread( f"SELECT credits FROM levels WHERE server='{message.server.id}' AND member='{message.author.id}'" )[ 0 ][ 0 ] ) )
					bid = int( cnt )
					if 5 <= bid <= sqlread( f"""SELECT credits FROM levels WHERE server='{message.server.id}' AND member='{message.author.id}'""" )[ 0 ][ 0 ]:
						grid = [ random.choice( SLOTS_PATTERNS ), random.choice( SLOTS_PATTERNS ), random.choice( SLOTS_PATTERNS ), random.choice( SLOTS_PATTERNS ), random.choice( SLOTS_PATTERNS ), random.choice( SLOTS_PATTERNS ), random.choice( SLOTS_PATTERNS ), random.choice( SLOTS_PATTERNS ), random.choice( SLOTS_PATTERNS ) ]
						machine_text = f"--{grid[0]} {grid[1]} {grid[2]}\n>>{grid[3]} {grid[4]} {grid[5]}\n--{grid[6]} {grid[7]} {grid[8]}\n"
						if grid[ 3 ] == grid[ 4 ] and grid[ 4 ] == grid[ 5 ]:
							if grid[ 3 ] == ":atm:":
								bid *= 10
								sqlexecute( f"""
								UPDATE levels
								SET credits=credits+{bid}
								WHERE server="{message.server.id}"
								AND member="{message.author.id}"
								""".replace( "\t", "" ) )
								machine_text += f"{message.author.mention} Bid x10!"
							elif grid[ 3 ] == ":free:":
								machine_text = f"{message.author.mention} Nothing!"
							elif grid[ 3 ] == ":dollar:":
								sqlexecute( f"""
								UPDATE levels
								SET credits=credits+300
								WHERE server="{message.server.id}"
								AND member="{message.author.id}";
								""".replace( "\t", "" ) )
								machine_text += f"{message.author.mention} +300 Credits!"
							elif grid[ 3 ] == ":moneybag:":
								sqlexecute( f"""
								UPDATE levels
								SET credits=credits+3000
								WHERE server="{message.server.id}"
								AND member="{message.author.id}";
								""".replace( "\t", "" ) )
								machine_text += f"{message.author.mention} +3,000 Credits!"
							elif grid[ 3 ] == ":gem:":
								sqlexecute( f"""
								UPDATE levels
								SET credits=credits+30000
								WHERE server="{message.server.id}"
								AND member="{message.author.id}";
								""".replace( "\t", "" ) )
								machine_text += f"{message.author.mention} +30,000 Credits!"
							else:
								bid *= 3
								sqlexecute( f"""
								UPDATE levels
								SET credits=credits+{bid}
								WHERE server="{message.server.id}"
								AND member="{message.author.id}";
								""".replace( "\t", "" ) )
								machine_text += f"{message.author.mention} Bid x3!"
						elif grid[ 3 ] == grid[ 4 ] or grid[ 4 ] == grid[ 5 ]:
							sqlexecute( f"""
							UPDATE levels
							SET credits=credits+{bid*2}
							WHERE server="{message.server.id}"
							AND member="{message.author.id}";
							""".replace( "\t", "" ) )
							machine_text += f"{message.author.mention} Bid x2!"
						else:
							sqlexecute( f"""
							UPDATE levels
							SET credits=credits-{bid}
							WHERE server="{message.server.id}"
							AND member="{message.author.id}";
							""".replace( "\t", "" ) )
							machine_text += f"{message.author.mention} You lost {parse_num(bid)} Credits!"
						await CLIENT.send_message( message.channel, machine_text )
					else:
						await CLIENT.send_message( message.channel, "Your bid must be greater than or equal to 5." )
					del bid
					del cnt
				elif startswith( f"l{prefix}slots" ):
					await CLIENT.send_message( message.channel, SLOTS_RULES )
				elif startswith( f"l{prefix}milestone " ):
					if admin_role in message.author.roles or message.author.id == owner_id:
						cnt = message.content.replace( f"l{prefix}milestone ", "" ).split( " " )
						if startswith( "a", val=cnt[ 0 ] ):
							cnt.remove( cnt[ 0 ] )
							_role = message.role_mentions[ 0 ]
							_item = cnt[ 0 ]
							_lim = int( cnt[ 1 ] )
							res = sqlread( f"""
							SELECT COUNT(*)
							FROM milestones
							WHERE server="{message.server.id}"
							AND item="{_item}"
							AND role="{_role.id}"
							AND _limit={_lim};
							""".replace( "\t", "" ) )[ 0 ]
							if res[ 0 ] == 0:
								sqlexecute( f"""
								INSERT INTO milestones (server, item, _limit, role)
								VALUES ("{message.server.id}", "{_item}", {_lim}, "{_role.id}");
								""".replace( "\t", "" ) )
								await CLIENT.send_message( message.channel, "```Added milestone {_item} : {_lim} : {_role}" )
							else:
								await CLIENT.send_message( message.channel, "```That milestone already exists!```" )
							del _role
							del _item
							del _lim
							del res
						elif startswith( "_role", val=cnt[ 0 ] ):
							cnt.remove( cnt[ 0 ] )
							_role = message.role_mentions[ 0 ]
							_lim = int( cnt[ 1 ] )
							_item = cnt[ 0 ]
							sqlexecute( f"""
							DELETE FROM milestones
							WHERE server="{message.server.id}"
							AND item="{_item}"
							AND _limit={_lim}
							AND role="{_role.id}";
							""".replace( "\t", "" ) )
							await CLIENT.send_message( message.channel, "```Removed milestone(s)```" )
							del _role
							del _lim
							del _item
						elif startswith( "s", val=cnt[ 0 ] ):
							cnt.remove( cnt[ 0 ] )
							milestones_data = sqlread( f"""
							SELECT *
							FROM milestones
							WHERE server="{message.server.id}";
							""".replace( "\t", "" ) )
							stuffs = [ ]
							app = stuffs.append
							for server, item, limit, role in milestones_data:
								_role = discord.utils.find( lambda r:r.id == role, message.server.roles )
								if _role is None:
									sqlexecute( f"DELETE FROM milestones WHERE server='{server}' AND role='{role}';" )
								else:
									app( f"{item} {limit} {_role}" )
								del _role
							await CLIENT.send_message( message.channel, '\n'.join( stuffs ) )
							del app
							del stuffs
							del milestones_data
							del cnt
						del cnt
					else:
						await CLIENT.send_message( message.channel, "```You do not have permission to use this command.```" )
				elif startswith( f"l{prefix}leaderboards " ):
					await CLIENT.send_typing( message.channel )
					_lim = int( message.content.split( " " )[ 1 ] )
					ret = [ ]
					user_rank = 0
					tmp = [ ]
					result = sqlread( f"""
					SELECT member, tier-1, rank
					FROM levels
					WHERE ((tier - 1) * 100) + rank > 0
					AND server = '{message.server.id}'
					ORDER BY ((tier - 1) * 100) + rank DESC, xp DESC;
					""".replace( "\t", "" ) )
					append = ret.append
					for i in range( 0, _lim if len( result ) > _lim else len( result ) ):
						if result[ i ][ 0 ] == message.author.id:
							user_rank = i + 1
						user = await CLIENT.get_user_info( result[ i ][ 0 ] )
						append( f"{user} : {(result[i][1]*100)+result[i][2]}" )
						del user
					append = tmp.append
					for index, item in enumerate( ret ):
						if index % 5 == 0:
							append( item + "\n" )
						else:
							tmp[ len( tmp ) - 1 ] += item + "\n"
					for item in tmp:
						await CLIENT.send_message( message.channel, f"```{item}```" )
					await CLIENT.send_message( message.channel, f"```You are ranked: #{user_rank}```" )
					del _lim
					del ret
					del user_rank
					del tmp
					del result
					del append
				elif startswith( f"l{prefix}leaderboards" ):
					await CLIENT.send_typing( message.channel )
					ret = [ ]
					user_rank = 0
					tmp = [ ]
					result = sqlread( f"""
									SELECT member, tier-1, rank
									FROM levels
									WHERE ((tier - 1) * 100) + rank > 0
									AND server = '{message.server.id}'
									ORDER BY ((tier - 1) * 100) + rank DESC, xp DESC;
									""".replace( "\t", "" ) )
					append = ret.append
					for i in range( 0, 10 if len( result ) > 10 else len( result ) ):
						if result[ i ][ 0 ] == message.author.id:
							user_rank = i + 1
						user = await CLIENT.get_user_info( result[ i ][ 0 ] )
						append( f"{user} : {(result[i][1]*100)+result[i][2]}" )
						del user
					append = tmp.append
					for index, item in enumerate( ret ):
						if index % 5 == 0:
							append( item + '\n' )
						else:
							tmp[ len( tmp ) - 1 ] += item + "\n"
					for item in tmp:
						await CLIENT.send_message( message.channel, f"```{item}```" )
					await CLIENT.send_message( message.channel, f"```You are ranked: #{user_rank}```" )
					del append
					del ret
					del user_rank
					del tmp
					del result
			if startswith( f"$update", "logbot.levels.update" ):
				if message.author.id == owner_id:
					do_update = True
				else:
					await CLIENT.send_message( message.channel, "```You do not have permission to use this command.```" )
					print( f"{Fore.LIGHTGREEN_EX}{str(message.author)} attempted to use a command.{Fore.RESET}" )
			elif startswith( "logbot.levels.exit", "$exit" ):
				if message.author.id == owner_id:
					EXITING = True
					await CLIENT.logout( )
				else:
					await CLIENT.send_message( message.channel, "```You do not have permission to use this command.```" )
					print( f"{Fore.LIGHTGREEN_EX}{str(message.author)} attempted to use a command.{Fore.RESET}" )
			elif startswith( f"{prefix}ping" ):
				timestamp = datetime.now( ) - message.timestamp
				await CLIENT.send_message( message.channel, f"```LogBot Levels Online ~ {round(timestamp.microseconds / 1000)}```" )
				del timestamp
			elif startswith( f"l{prefix}disabled" ):
				await CLIENT.send_message( message.channel, f"```{DISABLED}```" )
			elif startswith( f"l{prefix}disable" ):
				if admin_role in message.author.roles or message.author.id == owner_id:
					DISABLED = True
					await CLIENT.send_message( message.channel, "```Disabled levels plugin for this server.```" )
				else:
					await CLIENT.send_message( message.channel, "```You do not have permission to use this command.```" )
					print( f"{Fore.LIGHTGREEN_EX}{str(message.author)} attempted to use a command.{Fore.RESET}" )
			elif startswith( f"l{prefix}enable" ):
				if admin_role in message.author.roles or message.author.id == owner_id:
					DISABLED = False
					await CLIENT.send_message( message.channel, "```Enabled levels plugin for this server.```" )
				else:
					await CLIENT.send_message( message.channel, "```You do not have permission to use this command.```" )
					print( f"{Fore.LIGHTGREEN_EX}{str(message.author)} attempted to use a command.{Fore.RESET}" )
			elif startswith( f"l{prefix}execute\n", "```sql\n--execute" ):
				if message.author.id == owner_id or message.author.id == bot_id:
					sqlexecute( message.content.replace( f"l{prefix}execute\n", "" ).replace( "```sql\n--execute", "" ).replace( "```", "" ).replace( "{sid}", message.server.id ).replace( "{uid}", message.author.id ) )
					await CLIENT.send_message( message.channel, "```Execution Successful.```" )
				else:
					await CLIENT.send_message( message.channel, "```You do not have permission to use this command.```" )
					print( f"{Fore.LIGHTGREEN_EX}{str(message.author)} attempted to use a command.{Fore.RESET}" )
			elif startswith( f"l{prefix}get\n", "```sql\n--get\n" ):
				if message.author.id == owner_id:
					try:
						res = sqlread( message.content.replace( f"l{prefix}get\n", "" ).replace( "```sql\n--get\n", "" ).replace( "```", "" ).replace( "{sid}", message.server.id ).replace( "{uid}", message.author.id ) )
						_res = str( res )
						if startswith( "```sql\n--get\n--format_id\n" ):
							for server in CLIENT.servers:
								_res = _res.replace( server.id, str( server ) )
							for member in CLIENT.get_all_members( ):
								_res = _res.replace( member.id, str( member ) )
						ret = format_message( f"Execution Successful. Result:\n{_res}" )
						for retu in ret:
							await CLIENT.send_message( message.channel, retu )
						del _res
						del ret
					except Exception:
						for i in format_message( traceback.format_exc( ).replace( "```", "`" ) ):
							await CLIENT.send_message( message.channel, i )
				else:
					await CLIENT.send_message( message.channel, "```You do not have permission to use this command.```" )
					print( f"{Fore.LIGHTGREEN_EX}{str(message.author)} attempted to use a command.{Fore.RESET}" )
			elif startswith( f"l{prefix}dm " ):
				content = message.content.replace( f"l{prefix}dm ", "" )
				if "t" in content.lower( ):
					sqlexecute( f"""
					UPDATE levels
					SET dm='TRUE'
					WHERE server='{message.server.id}'
					AND member='{message.author.id}';
					""".replace( "\t", "" ) )
				else:
					sqlexecute( f"""
					UPDATE levels
					SET dm='FALSE'
					WHERE server='{message.server.id}'
					AND member='{message.author.id}';
					""".replace( "\t", "" ) )
				await CLIENT.send_message( message.channel, "```Updated DM Channel.```" )
				del content
			elif startswith( f"l{prefix}alert " ):
				cnt = message.content.replace( f"l{prefix}alert ", "" )
				if cnt.capitalize( ) == "None":
					new_alert = None
				else:
					new_alert = discord.utils.find( lambda c:c.id == cnt or c.name == cnt or str( c ) == cnt or c.mention == cnt, message.server.channels )
				if isinstance( new_alert, discord.Channel ):
					new_alert = new_alert.id
				sqlexecute( f"""
				UPDATE levels
				SET alert_channel="{new_alert}"
				WHERE server="{message.server.id}"
				AND member="{message.author.id}";
				""".replace( "\t", "" ) )
				await CLIENT.send_message( message.channel, f"```Updated Alert Channel```" )
				del new_alert
				del cnt
			elif startswith( f"l{prefix}default " ):
				if admin_role in message.author.roles or message.author.id == owner_id:
					cnt = message.content.split( " " )
					cnt.remove( cnt[ 0 ] )
					if cnt[ 0 ] == "DM":
						if cnt[ 1 ].lower( ) == "on" or cnt[ 1 ].lower( ) == "true" or cnt[ 1 ].lower( ) == "1":
							DEFAULTS[ message.server.id ][ "DM" ] = "TRUE"
							await CLIENT.send_message( message.channel, f"```Set the DM default to TRUE```" )
						else:
							DEFAULTS[ message.server.id ][ "DM" ] = "FALSE"
							await CLIENT.send_message( message.channel, f"```Set the DM default to FALSE```" )
					elif cnt[ 0 ] == "AlertChannel":
						channel_obj = message.channel_mentions
						if channel_obj:
							channel_obj = channel_obj[ 0 ].id
						else:
							channel_obj = "None"
						DEFAULTS[ message.server.id ][ "AlertChannel" ] = channel_obj
						await CLIENT.send_message(
							message.channel,
							f"```Set the alert channel to {CLIENT.get_channel(channel_obj)}```"
						)
						del channel_obj
					del cnt
			elif startswith( f"l{prefix}defaults" ):
				await CLIENT.send_message(
					message.channel,
					f"```DM: {DEFAULTS[message.server.id]['DM']}\n"
					f"Alert Channel: {CLIENT.get_channel(DEFAULTS[message.server.id]['AlertChannel'])}```"
				)
			elif startswith( f"l{prefix}reset" ):
				if admin_role in message.author.roles or message.author.id == owner_id:
					sqlexecute( f"""
					UPDATE levels
					SET dm='{DEFAULTS[message.server.id]['DM']}'
					WHERE server='{message.server.id}';
					UPDATE levels
					SET alert_channel='{DEFAULTS[message.server.id]['AlertChannel']}'
					WHERE server='{message.server.id}';
					""".replace( "\t", "" ) )
					await CLIENT.send_message(
						message.channel,
						f"```Reset DM and AlertChannel to their default server values.```"
					)

			save( message.server.id if not message.server is None else message.channel.id )
			if do_update:
				print( f"{Fore.LIGHTCYAN_EX}Updating...{Fore.RESET}" )
				await CLIENT.close( )
				subprocess.Popen( f"python {os.getcwd()}\\levels.py", False )
				exit( 0 )
	except Exception:
		log_error( traceback.format_exc( ) )

@CLIENT.event
async def on_ready ( ):
	"""
	Occurs when the bot logs in.
	"""
	if not os.path.exists( DATA_PATH ):
		os.makedirs( DATA_PATH )
	if not os.path.exists( DISABLES_PATH ):
		os.makedirs( DISABLES_PATH )
	# os.system( "cls" )
	print( f"{Fore.MAGENTA}Levels Ready!!!{Fore.RESET}" )
	try:
		sqlexecute( f"""
		CREATE TABLE levels (server VARCHAR(50), member VARCHAR(50), tier LONG, rank INTEGER(3), xp LONG, xp_limit LONG, multiplier DECIMAL(50,1), credits LONG, cpm LONG, dm BOOLEAN);
		""".replace( "\t", "" ) )
	except Exception:
		pass
	try:
		sqlexecute( f"""
		CREATE INDEX i
		ON levels (server, member, tier, rank, xp, xp_limit, multiplier, credits, cpm, dm);
		""".replace( "\t", "" ) )
	except Exception:
		pass
	try:
		sqlexecute( f"""
		CREATE TABLE disables (server VARCHAR(50), disabled INTEGER);
		""".replace( "\t", "" ) )
	except Exception:
		pass
	try:
		sqlexecute( f"""
		CREATE INDEX di
		ON disables (server, disabled);
		""".replace( "\t", "" ) )
	except Exception:
		pass
	try:
		sqlexecute( f"""
		CREATE TABLE milestones (server VARCHAR(50), item VARCHAR(20), _limit INTEGER, role VARCHAR(50));
		""".replace( "\t", "" ) )
	except Exception:
		pass
	try:
		sqlexecute( f"""
		CREATE INDEX mi
		ON milestones (server, item, _limit, role);
		""".replace( "\t", "" ) )
	except Exception:
		pass

CLIENT.run( token )

if not EXITING:
	subprocess.Popen( f"python {os.getcwd()}\\levels.py" )
	exit( 0 )
