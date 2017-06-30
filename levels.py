import os
import random
import sqlite3
import subprocess
import traceback
from datetime import datetime
from math import floor
from sys import exit

import discord
from colorama import Fore, init

# from symbols import symbols

init()
client = discord.Client()
token = 'MjU1Mzc5NzQ4ODI4NjEwNTYx.CycwfQ.c6n0jvVrV5lGbbke68dHdlYMRX0'
owner_id = "239500860336373761"
_data = os.path.expanduser("~\\Documents\\Discord Logs\\SETTINGS\\level_data")
_disables = f"{_data}\\disables\\"
_sql = sqlite3.connect(f"{_data}\\data.db")
_sql_cursor = _sql.cursor()

def sqlread(cmd: str):
	_sql_cursor.execute(cmd)
	return _sql_cursor.fetchall()
	pass

def sqlexecute(cmd: str):
	_sql_cursor.execute(cmd)
	_sql.commit()
	pass

base = 200
multi = 1.5
disabled = False

def read(sid: str):
	"""
	Reads server data.
	:param sid: The server id.
	"""
	global disabled

	# <editor-fold desc="Disables Check">
	res = sqlread(f"""
	SELECT COUNT(*)
	FROM disables
	WHERE server='{sid}';
	""".replace("\t", ""))
	if res[0][0] == 0: sqlexecute(f"""
		INSERT INTO disables (server, disabled)
		VALUES ('{sid}', 0);
		""".replace("\t", ""))
	# </editor-fold>
	pass

def save(sid: str):
	"""
	Saves plugin data.
	:param sid: The server id.
	"""
	global disabled
	# <editor-fold desc="_disables">
	sqlexecute(f"""
	UPDATE disables
	SET disabled={1 if disabled == True else 0}
	WHERE server='{sid}';
	""".replace("\t", ""))
	# </editor-fold>
	pass

def parse_num(num) -> str:
	_num = str(num)
	_num = _num[::-1]
	_num = ','.join([_num[i:i + 3] for i in range(0, len(_num), 3)])[::-1]
	return str(_num)
	pass

def format_message(cont: str) -> list:
	"""
	Splits `cont` into several strings, each a maximum of 2000 characters in length. Adds ``` at each end automatically.
	:param cont: The string to format.
	:return: A list of strings. Each formatted into 2000 characters, including ``` at each end.
	"""
	if len(cont) > 1990: return [f"```dos\n{item}```" for item in [cont[i:i + 1000] for i in range(0, len(cont), 1000)]]
	else: return [f"```dos\n{cont}```"]
	pass

# noinspection PyTypeChecker
@client.event
async def on_message(message):
	global base, disabled
	if not message.server is None:
		try:
			if not message.server is None:
				read(message.server.id)
				for m in message.server.members:
					if sqlread(f"""
					SELECT COUNT(*)
					FROM levels
					WHERE server='{message.server.id}'
					AND member='{m.id}';
					""".replace("\t", ""))[0][0] == 0:
						sqlexecute(f"""
						INSERT INTO levels (server, member, tier, rank, xp, xp_limit, multiplier, credits, cpm, dm)
						VALUES ('{message.server.id}', '{m.id}', 1, 0, 0, 200, 1.0, 0, 0, 'TRUE');
						""".replace("\t", ""))
						pass
					pass
				pass
			else: read(message.channel.id)
			pass
		except:
			for member in message.server.members: sqlexecute(f"""
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
					""".replace("\t", ""))
			pass
		def startswith(*msgs, val=message.content):
			# noinspection PyShadowingNames
			for m in msgs:
				if val.startswith(m): return True
				pass
			return False
		admin_role = discord.utils.find(lambda ro:ro.name == "LogBot Admin", message.server.roles)
		do_update = False
		bot = await client.get_user_info("255379748828610561")
		print(f"{message.author} : {message.server} : {message.content}")

		disabled = sqlread(f"""
		SELECT disabled
		FROM disables
		WHERE server='{message.server.id}';
		""".replace("\t", ""))[0][0]
		disabled = True if disabled == 1 else False

		if not disabled or message.author.id == owner_id:
			if not message.author == bot:
				content = message.content
				if not len(content) > 0: content = " "
				earned = round(random.choice(range(15, 31)) * int(sqlread(f"""
				SELECT multiplier
				FROM levels
				WHERE server='{message.server.id}'
				AND member='{message.author.id}';
				""".replace("\t", ""))[0][0]) * len(content) / 5)
				sqlexecute(f"""
				UPDATE levels
				SET xp = xp+{earned}
				WHERE server='{message.server.id}'
				AND member='{message.author.id}';
				""".replace("\t", ""))
				if len(content) > 4: sqlexecute(f"""
					UPDATE levels
					SET credits=credits+(cpm*{round(len(content)/5)})
					WHERE server='{message.server.id}'
					AND member='{message.author.id}';
					""".replace("\t", ""))

				_xp_limit = round(base * (multi ** (sqlread(f"""
				SELECT rank
				FROM levels
				WHERE server='{message.server.id}'
				AND member='{message.author.id}';
				""".replace("\t", ""))[0][0])))
				sqlexecute(f"""
				UPDATE levels
				SET xp_limit={_xp_limit}
				WHERE server='{message.server.id}'
				AND member='{message.author.id}';
				""".replace("\t", ""))
				is_ranked_up = False
				prev_rank = sqlread(f"""
				SELECT rank
				FROM levels
				WHERE server='{message.server.id}'
				AND member='{message.author.id}';
				""".replace("\t", ""))[0][0]
				while sqlread(f"""
				SELECT xp
				FROM levels
				WHERE server='{message.server.id}'
				AND member='{message.author.id}';
				""".replace("\t", ""))[0][0] >= sqlread(f"""
				SELECT xp_limit
				FROM levels
				WHERE server='{message.server.id}'
				AND member='{message.author.id}';
				""".replace("\t", ""))[0][0]:
					sqlexecute(f"""
					UPDATE levels
					SET xp=xp-xp_limit
					WHERE server='{message.server.id}'
					AND member='{message.author.id}';
					""".replace("\t", ""))
					sqlexecute(f"""
					UPDATE levels
					SET xp_limit=xp_limit*1.5
					WHERE server='{message.server.id}'
					AND member='{message.author.id}';
					""".replace("\t", ""))
					sqlexecute(f"""
					UPDATE levels
					SET rank=rank+1
					WHERE server='{message.server.id}'
					AND member='{message.author.id}';
					""".replace("\t", ""))
					sqlexecute(f"""
					UPDATE levels
					SET credits=credits+(tier*50)
					WHERE server='{message.server.id}'
					AND member='{message.author.id}';
					""".replace("\t", ""))
					is_ranked_up = True
					pass
				if is_ranked_up:
					do_dm = sqlread(f"""
					SELECT dm, alert_channel
					FROM levels
					WHERE server='{message.server.id}'
					AND member='{message.author.id}';
					""".replace("\t", ""))[0]
					_tdat = sqlread(f"""
					SELECT rank, tier*50
					FROM levels
					WHERE server='{message.server.id}'
					AND member='{message.author.id}';
					""".replace("\t", ""))[0]
					if do_dm[0].lower() == "true":
						await client.send_message(message.author, f"Congrats, {message.author.mention}, you just leveled up to rank {_tdat[0]} from rank {prev_rank} and have earned {parse_num((_tdat[0] - prev_rank) * _tdat[1])} credits in {message.server.name}!")
						print(f"{Fore.GREEN}{message.author} has leveled up to {_tdat[0]}!{Fore.RESET}")
						pass
					else:
						alert_channel = discord.utils.find(lambda c: c.id == do_dm[1], message.server.channels)
						if not alert_channel is None:
							await client.send_message(alert_channel, f"Congrats, {message.author.mention}, you just leveled up to rank {_tdat[0]} from rank {prev_rank} and have earned {parse_num((_tdat[0] - prev_rank) * _tdat[1])} credits!")
							pass
						else:
							await client.send_message(message.channel, f"Congrats, {message.author.mention}, you just leveled up to rank {_tdat[0]} from rank {prev_rank} and have earned {parse_num((_tdat[0] - prev_rank) * _tdat[1])} credits!")
							pass
						print(f"{Fore.GREEN}{message.author} has leveled up to {_tdat[0]}!{Fore.RESET}")
						pass
					pass

				if startswith(f"l$rank"):
					if len(message.mentions) == 0:
						u_data = sqlread(f"""
						SELECT tier, rank, xp, xp_limit, multiplier, credits, cpm, dm, alert_channel
						FROM levels
						WHERE server='{message.server.id}'
						AND member='{message.author.id}';
						""".replace("\t", ""))[0]
						precision = len(str(u_data[4]).split('.')[0]) + 1
						_m = f"{float(u_data[4]):1.{precision}}"
						_t = _m.split(".")
						if len(_t) == 1: _t.append("0")
						e = discord.Embed(title=str(message.author), description=f"Ranking Information for {str(message.author)}", colour=message.author.colour) \
							.add_field(name="Rank", value=str(u_data[1])) \
							.add_field(name="XP", value=str(parse_num(round(u_data[2]))) + "/" + parse_num(round(int(u_data[3])))) \
							.add_field(name="Credits", value=parse_num(u_data[5])) \
							.add_field(name="Multiplier", value=f"{parse_num(_t[0])}.{_t[1]}") \
							.add_field(name="CPM", value=parse_num(u_data[6])) \
							.add_field(name="Tier", value=str(u_data[0])) \
							.add_field(name="DM", value=str(u_data[7])) \
							.add_field(name="Alert Channel", value=str(discord.utils.find(lambda c: c.id == u_data[8], message.server.channels)))
						await client.send_message(message.channel, "Here you go!", embed=e)
						pass
					else:
						user = message.mentions[0]
						u_data = sqlread(f"""
						SELECT tier, rank, xp, xp_limit, multiplier, credits, cpm, dm, alert_channel
						FROM levels
						WHERE server='{message.server.id}'
						AND member='{user.id}';
						""".replace("\t", ""))[0]
						tmp = round(base * (multi ** u_data[1]))
						precision = len(str(u_data[4]).split('.')[0]) + 1
						_m = f"{float(u_data[4]):1.{precision}}"
						_t = _m.split(".")
						if len(_t) == 1: _t.append("0")
						e = discord.Embed(title=str(user), description=f"Ranking Information for {str(user)}", colour=user.colour) \
							.add_field(name="Rank", value=str(u_data[1])) \
							.add_field(name="XP", value=str(u_data[2]) + "/" + parse_num(tmp)) \
							.add_field(name="Credits", value=parse_num(u_data[5])) \
							.add_field(name="Multiplier", value=f"{parse_num(_t[0])}.{_t[1]}") \
							.add_field(name="CPM", value=parse_num(u_data[6])) \
							.add_field(name="Tier", value=str(u_data[0])) \
							.add_field(name="DM", value=str(u_data[7])) \
							.add_field(name="Alert Channel", value=str(discord.utils.find(lambda c: c.id == u_data[8], message.server.channels)))
						await client.send_message(message.channel, "Here you go!", embed=e)
						pass
					pass
				elif startswith(f"l$levels"):
					ret = ""
					user_rank = 0
					tmp = []
					result = sqlread(f"""
					SELECT member, tier-1, rank
					FROM levels
					WHERE ((tier - 1) * 100) + rank > 0
					AND server = '{message.server.id}'
					ORDER BY ((tier - 1) * 100) + rank DESC, xp DESC;
					""".replace("\t", ""))
					for i in range(0, len(result)):
						if result[i][0] == message.author.id: user_rank = i + 1
						user = await client.get_user_info(result[i][0])
						ret += f"{user} : {(result[i][1]*100)+result[i][2]}\n"
						pass
					ret = ret.split("\n")
					for i in range(0, len(ret)):
						if i % 5 == 0: tmp.append(ret[i] + '\n')
						else: tmp[len(tmp) - 1] += ret[i] + "\n"
						pass
					for item in tmp: await client.send_message(message.channel, f"```{item}```")
					await client.send_message(message.channel, f"```You are ranked: #{user_rank}```")
					pass
				elif startswith(f"l$place"):
					leaderboard = sqlread(f"""
					SELECT member, ((tier - 1) * 100), rank
					FROM levels
					WHERE ((tier-1)*100) + rank > 0
					AND server='{message.server.id}'
					ORDER BY ((tier - 1) * 100) + rank DESC, xp DESC;
					""".replace("\t", ""))
					if len(message.mentions) > 0:
						users = message.mentions
						for user in users:
							is_ranked = False
							for i in range(0, len(leaderboard)):
								if leaderboard[i][0] == user.id:
									is_ranked = True
									break
									pass
								pass
							if is_ranked: await client.send_message(message.channel, f"```{user} is ranked #{i+1}```")
							else: await client.send_message(message.channel, f"```{user} is not ranked.```")
							pass
						pass
					else:
						is_ranked = False
						for i in range(0, len(leaderboard)):
							if leaderboard[i][0] == message.author.id:
								is_ranked = True
								break
								pass
							pass
						if is_ranked: await client.send_message(message.channel, f"```{message.author} is ranked #{i+1}```")
						else: await client.send_message(message.channel, f"```{message.author} is not ranked.```")
						pass
					pass
				elif startswith(f"l$buy "):
					content = message.content.replace(f"l$buy ", "").split(" ")
					if content[0].lower() == "mul" or content[0].lower() == "multiplier":
						if len(content) > 1:
							if sqlread(f"""
							SELECT credits
							FROM levels
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace("\t", ""))[0][0] >= floor(250 * int(content[1])):
								sqlexecute(f"""
								UPDATE levels
								SET multiplier=multiplier+(0.1*{int(content[1])})
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace("\t", ""))
								sqlexecute(f"""
								UPDATE levels
								SET credits=credits-{floor(250*int(content[1]))}
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace("\t", ""))
								await client.send_message(message.channel, f"```Bought {parse_num(int(content[1]))} multipliers, spending {parse_num(250*int(content[1]))} credits.```")
								pass
							elif sqlread(f"""
							SELECT credits
							FROM levels
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace("\t", ""))[0][0] >= 250:
								num = floor(sqlread(f"""
							SELECT credits
							FROM levels
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace("\t", ""))[0][0] / 250)
								sqlexecute(f"""
								UPDATE levels
								SET multiplier=multiplier+(0.1*{num})
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace("\t", ""))
								sqlexecute(f"""
								UPDATE levels
								SET credits=credits-{floor(250*num)}
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace("\t", ""))
								await client.send_message(message.channel, f"```Bought {parse_num(num)} multipliers, spending {parse_num(floor(num*250))} credits.```")
								pass
							else:
								await client.send_message(message.channel, "```You do not have enough credits to purchase this. Earn more by leveling up.```")
								pass
							pass
						else:
							num = floor(sqlread(f"""
							SELECT credits
							FROM levels
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace("\t", ""))[0][0] / 250)
							sqlexecute(f"""
							UPDATE levels
							SET multiplier=multiplier+(0.1*{num})
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace("\t", ""))
							sqlexecute(f"""
							UPDATE levels
							SET credits=credits-{floor(250*num)}
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace("\t", ""))
							await client.send_message(message.channel, f"```Bought {parse_num(num)} multipliers, spending {parse_num(floor(num*250))} credits.```")
							pass
						pass
					elif content[0].lower() == "cpm":
						if len(content) > 1:
							if sqlread(f"""
							SELECT credits
							FROM levels
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace("\t", ""))[0][0] >= floor(1000 * int(content[1])):
								sqlexecute(f"""
								UPDATE levels
								SET cpm=cpm+(5*{int(content[1])})
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace("\t", ""))
								sqlexecute(f"""
								UPDATE levels
								SET credits=credits-{floor(1000*int(content[1]))}
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace("\t", ""))
								await client.send_message(message.channel, f"```Bought {parse_num(int(content[1])*5)} CPM, spending {parse_num(1000*int(content[1]))} credits.```")
								pass
							elif sqlread(f"""
							SELECT credits
							FROM levels
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace("\t", ""))[0][0] >= 1000:
								num = floor(sqlread(f"""
								SELECT credits
								FROM levels
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace("\t", ""))[0][0] / 1000)
								sqlexecute(f"""
								UPDATE levels
								SET cpm=cpm+(5*{num})
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace("\t", ""))
								sqlexecute(f"""
								UPDATE levels
								SET credits=credits-{floor(1000*num)}
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace("\t", ""))
								await client.send_message(message.channel, f"```Bought {parse_num(num*5)} CPM, spending {parse_num(floor(num*1000))} credits.```")
								pass
							else:
								await client.send_message(message.channel, "```You do not have enough credits to purchase this. Earn more by leveling up.```")
								pass
							pass
						else:
							num = floor(sqlread(f"""
							SELECT credits
							FROM levels
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace("\t", ""))[0][0] / 1000)
							sqlexecute(f"""
							UPDATE levels
							SET cpm=cpm+(5*{num})
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace("\t", ""))
							sqlexecute(f"""
							UPDATE levels
							SET credits=credits-{floor(1000*num)}
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace("\t", ""))
							await client.send_message(message.channel, f"```Bought {parse_num(num*5)} CPM, spending {parse_num(floor(num*1000))} credits.```")
							pass
						pass
					elif content[0].lower() == "tier":
						if len(content) > 1:
							if sqlread(f"""
							SELECT credits
							FROM levels
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace("\t", ""))[0][0] >= floor(10000 * int(content[1])) and sqlread(f"""
							SELECT rank
							FROM levels
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace("\t", ""))[0][0] >= floor(100 * int(content[1])):
								num = int(content[1])
								sqlexecute(f"""
								UPDATE levels
								SET tier=tier+num
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace("\t", ""))
								sqlexecute(f"""
								UPDATE levels
								SET credits=credits-{floor(num*10000)}
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace("\t", ""))
								sqlexecute(f"""
								UPDATE levels
								SET rank=rank-{floor(num*100)}
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace("\t", ""))
								sqlexecute(f"""
								UPDATE levels
								SET xp=0
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace("\t", ""))
								sqlexecute(f"""
								UPDATE levels
								SET cpm=0
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace("\t", ""))
								sqlexecute(f"""
								UPDATE levels
								SET multiplier=1.0*tier
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace("\t", ""))
								if not message.author == bot:
									do_dm = sqlread(f"""
									SELECT dm, tier
									FROM levels
									WHERE server='{message.server.id}'
									AND member='{message.author.id}';
									""".replace("\t", ""))[0]
									if do_dm[0].lower() == 'true':
										await client.send_message(message.author, f"You have tiered up, {message.author}. You are now Tier {do_dm[1]}!")
										print(f"{Fore.GREEN}{message.author} has tiered up to {do_dm[1]} in {message.server}!{Fore.RESET}")
										pass
									else:
										await client.send_message(message.channel, f"You have tiered up, {message.author}. You are now Tier {do_dm[1]}!")
										print(f"{Fore.GREEN}{message.author} has tiered up to {do_dm[1]} in {message.server}!{Fore.RESET}")
										pass
									pass
								await client.send_message(message.channel, f"```Bought {parse_num(num)} Tiers, spending {parse_num(floor(num*10000))} credits and {parse_num(floor(num*100))} ranks.```")
								pass
							elif sqlread(f"""
							SELECT credits
							FROM levels
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace("\t", ""))[0][0] >= 10000 and sqlread(f"""
							SELECT rank
							FROM levels
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace("\t", ""))[0][0] >= 100:
								creds = floor(sqlread(f"""
							SELECT credits
							FROM levels
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace("\t", ""))[0][0] / 10000)
								ranks = floor(sqlread(f"""
							SELECT rank
							FROM levels
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace("\t", ""))[0][0] / 100)
								num = creds if creds <= ranks else ranks
								sqlexecute(f"""
								UPDATE levels
								SET tier=tier+{num}
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace("\t", ""))
								sqlexecute(f"""
								UPDATE levels
								SET credits=credits-{floor(num*10000)}
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace("\t", ""))
								sqlexecute(f"""
								UPDATE levels
								SET rank=rank-{floor(num*100)}
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace("\t", ""))
								sqlexecute(f"""
								UPDATE levels
								SET xp=0
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace("\t", ""))
								sqlexecute(f"""
								UPDATE levels
								SET cpm=0
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace("\t", ""))
								sqlexecute(f"""
								UPDATE levels
								SET multiplier=1.0*tier
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace("\t", ""))
								if not message.author == bot:
									do_dm = sqlread(f"""
									SELECT dm, tier
									FROM levels
									WHERE server='{message.server.id}'
									AND member='{message.author.id}';
									""".replace("\t", ""))[0]
									if do_dm[0].lower() == "true":
										await client.send_message(message.author, f"You have tiered up, {message.author}. You are now Tier {do_dm[1]}!")
										print(f"{Fore.GREEN}{message.author} has tiered up to {do_dm[1]} in {message.server}!{Fore.RESET}")
										pass
									else:
										await client.send_message(message.channel, f"You have tiered up, {message.author}. You are now Tier {do_dm[1]}!")
										print(f"{Fore.GREEN}{message.author} has tiered up to {do_dm[1]} in {message.server}!{Fore.RESET}")
										pass
									pass
								await client.send_message(message.channel, f"```Bought {parse_num(num)} Tiers, spending {parse_num(floor(num*10000))} credits and {parse_num(floor(num*100))} ranks.```")
								pass
							else: await client.send_message(message.channel, "```You do not have enough credits/ranks to purchase this. Earn more by leveling up.")
							pass
						else:
							creds = floor(sqlread(f"""
							SELECT credits
							FROM levels
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace("\t", ""))[0][0] / 10000)
							ranks = floor(sqlread(f"""
							SELECT rank
							FROM levels
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace("\t", ""))[0][0] / 100)
							num = creds if creds <= ranks else ranks
							sqlexecute(f"""
							UPDATE levels
							SET tier=tier+{num}
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace("\t", ""))
							sqlexecute(f"""
							UPDATE levels
							SET credits=credits-{floor(num*10000)}
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace("\t", ""))
							sqlexecute(f"""
							UPDATE levels
							SET rank=rank-{floor(num*100)}
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace("\t", ""))
							sqlexecute(f"""
							UPDATE levels
							SET xp=0
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace("\t", ""))
							sqlexecute(f"""
							UPDATE levels
							SET cpm=0
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace("\t", ""))
							sqlexecute(f"""
							UPDATE levels
							SET multiplier=1.0*tier
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace("\t", ""))
							if not message.author == bot:
								do_dm = sqlread(f"""
								SELECT dm, tier
								FROM levels
								WHERE server='{message.server.id}'
								AND member='{message.author.id}';
								""".replace("\t", ""))[0]
								if do_dm[0].lower() == "true":
									await client.send_message(message.author, f"You have tiered up, {message.author}. You are now Tier {do_dm[1]}!")
									print(f"{Fore.GREEN}{message.author} has tiered up to {do_dm[1]} in {message.server}!{Fore.RESET}")
									pass
								else:
									await client.send_message(message.channel, f"You have tiered up, {message.author}. You are now Tier {do_dm[1]}!")
									print(f"{Fore.GREEN}{message.author} has tiered up to {do_dm[1]} in {message.server}!{Fore.RESET}")
									pass
								pass
							await client.send_message(message.channel, f"```Bought {parse_num(num)} Tiers, spending {parse_num(floor(num*10000))} credits and {parse_num(floor(num*100))} ranks.```")
							pass
						pass
					pass
				elif startswith(f"l$shop"):
					udat = sqlread(f"""
					SELECT credits, rank
					FROM levels
					WHERE server='{message.server.id}'
					AND member='{message.author.id}';
					""".replace("\t", ""))[0]
					creds = floor(udat[0] / 100000)
					ranks = floor(udat[1] / 100)
					buy_tier = creds if creds < ranks else ranks

					string = f"""```
					Items:
					mul • Multiplier +0.1 - 250 credits ~ Buyable: {parse_num(floor(udat[0] / 250))}
					cpm • Credits Per Message +5 - 1,000 credits ~ Buyable: {parse_num(floor(udat[0] / 1000))}
					tier • Tier +1 - 10,000 credits + 100 ranks ~ Buyable: {parse_num(buy_tier)}
					```
					""".replace("\t", "")
					await client.send_message(message.channel, string)
					pass
				elif startswith(f"l$gift "):
					content = message.content.replace(f"l$gift ", "").split(" ")
					gift = float(content[1])
					user = message.mentions[0]
					_type = content[0]
					if _type == "xp":
						if sqlread(f"""
						SELECT xp
						FROM levels
						WHERE server='{message.server.id}'
						AND member='{message.author.id}';
						""".replace("\t", ""))[0][0] >= gift:
							sqlexecute(f"""
							UPDATE levels
							SET xp=xp+{gift}
							WHERE server='{message.server.id}'
							AND member='{user.id}';
							""".replace("\t", ""))
							sqlexecute(f"""
							UPDATE levels
							SET xp=xp-{gift}
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace("\t", ""))
							await client.send_message(message.channel, f"```Gifted {user} with {parse_num(str(gift).split('.')[0]) + str(gift).split('.')[1]} XP!```")
							pass
						else: await client.send_message(message.channel, f"```You do not have enough XP for that!```")
						pass
					elif _type == "cred":
						if sqlread(f"""SELECT credits FROM levels WHERE server='{message.server.id}' AND member='{message.author.id}';""")[0][0] >= gift:
							sqlexecute(f"""
							UPDATE levels
							SET credits=credits+{gift}
							WHERE server='{message.server.id}'
							AND member='{user.id}';
							""".replace("\t", ""))
							sqlexecute(f"""
							UPDATE levels
							SET credits=credits-{gift}
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace("\t", ""))
							await client.send_message(message.channel, f"```Gifted {user} with {parse_num(str(gift).split('.')[0]) + str(gift).split('.')[1]} credits!```")
							pass
						else: await client.send_message(message.channel, f"```You do not have enough credits to do that!```")
						pass
					elif _type == "cpm":
						if sqlread(f"""
						SELECT cpm
						FROM levels
						WHERE server='{message.server.id}'
						AND member='{message.author.id}';
						""".replace("\t", ""))[0][0] >= gift:
							sqlexecute(f"""
							UPDATE levels
							SET cpm=cpm+{gift}
							WHERE server='{message.server.id}'
							AND member='{user.id}';
							""".replace("\t", ""))
							sqlexecute(f"""
							UPDATE levels
							SET cpm=cpm-{gift}
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace("\t", ""))
							await client.send_message(message.channel, f"```Gifted {user} with {parse_num(str(gift).split('.')[0]) + str(gift).split('.')[1]} CPM!```")
							pass
						else: await client.send_message(message.channel, f"```You do not have enough CPM to do that!```")
						pass
					elif _type == "mul":
						if sqlread(f"""
						SELECT multiplier
						FROM levels
						WHERE server='{message.server.id}'
						AND member='{message.author.id}';
						""".replace("\t", ""))[0][0] >= gift:
							sqlexecute(f"""
							UPDATE levels
							SET multiplier=multiplier+{gift}
							WHERE server='{message.server.id}'
							AND member='{user.id}';
							""".replace("\t", ""))
							sqlexecute(f"""
							UPDATE levels
							UPDATE levels
							SET multiplier=multiplier+{gift}
							WHERE server='{message.server.id}'
							AND member='{message.author.id}';
							""".replace("\t", ""))
							await client.send_message(message.channel, f"```Gifted {user} with {parse_num(str(gift).split('.')[0]) + str(gift).split('.')[1]} multipliers!```")
							pass
						else: await client.send_message(message.channel, f"```You do not have enough credits to do that!```")
						pass
					pass
				elif startswith(f"l$award "):
					if admin_role in message.author.roles or message.author.id == owner_id:
						content = message.content.replace(f"l$award ", "")
						content = content.split(" ")
						selection = None
						_type = content[0].lower()
						gift = int(content[1]) if not len(content[1]) > 16 else int("9999999999999999")
						user = message.mentions
						role = message.role_mentions
						if len(role) == 0 and len(user) == 0: role.append(message.server.default_role)
						if _type == "cred":
							_type = "credits"
							if len(role) >= 1:
								for member in message.server.members:
									for r in role:
										if r in member.roles: sqlexecute(f"""
									UPDATE levels
									SET credits=credits+{gift}
									WHERE server='{message.server.id}'
									AND member='{member.id}';
									""".replace("\t", ""))
										pass
									pass
								selection = ', '.join([str(r) for r in role])
								pass
							else:
								if isinstance(user, list):
									for uobj in user:
										sqlexecute(f"""
										UPDATE levels
										SET credits=credits+{gift}
										WHERE server='{message.server.id}'
										AND member='{uobj.id}';
										""".replace("\t", ""))
										pass
									selection = ', '.join([str(u) for u in user])
									pass
								else:
									sqlexecute(f"""
									UPDATE levels
									SET credits=credits+{gift}
									WHERE server='{message.server.id}'
									AND member='{message.author.id}'
									""".replace("\t", ""))
									selection = user
									pass
								pass
							pass
						elif _type == "cpm":
							_type = "CPM"
							if len(role) >= 1:
								for member in message.server.members:
									for r in role:
										if r in member.roles: sqlexecute(f"""
											UPDATE levels
											SET cpm=cpm+{gift}
											WHERE server='{message.server.id}'
											AND member='{member.id}';
											""".replace("\t", ""))
									pass
								if isinstance(role, list): selection = ', '.join([str(r) for r in role])
								else: selection = str(role)
								pass
							else:
								if isinstance(user, list):
									for u in user: sqlexecute(f"""
										UPDATE levels
										SET cpm=cpm+{gift}
										WHERE server='{message.server.id}'
										AND member='{u.id}';
										""".replace("\t", ""))
									selection = ', '.join([str(u) for u in user])
									pass
								else:
									sqlexecute(f"""
									UPDATE levels
									SET cpm=cpm+{gift}
									WHERE server='{message.server.id}'
									AND member='{user.id}';
									""".replace("\t", ""))
									selection = user
									pass
								pass
							pass
						elif _type == "xp":
							_type = "experience"
							if len(role) >= 1:
								for member in message.server.members:
									for r in role:
										if r in member.roles: sqlexecute(f"""
										UPDATE levels
										SET xp=xp+{gift}
										WHERE server='{message.server.id}'
										AND member='{member.id}';
										""".replace("\t", ""))
										pass
									pass
								if isinstance(role, list): selection = ', '.join([str(r) for r in role])
								else: selection = role.name
								pass
							else:
								if isinstance(user, list):
									for u in user: sqlexecute(f"""UPDATE levels SET xp=xp+{gift} WHERE server='{message.server.id}' AND member='{u.id}';""".replace("\t", ""))
									selection = user[0]
									pass
								else:
									sqlexecute(f"""
									UPDATE levels
									SET xp=xp+{gift}
									WHERE server='{message.server.id}'
									AND member='{user.id}';
									""".replace("\t", ""))
									selection = user
									pass
								pass
							pass
						elif _type == "rank":
							_type = "ranks"
							if len(role) >= 1:
								for member in message.server.members:
									for r in role:
										if r in member.roles:
											sqlexecute(f"""
											UPDATE levels
											SET rank=rank+{gift}
											WHERE server='{message.server.id}'
											AND member='{member.id}';
											""".replace("\t", ""))
											pass
										pass
									pass
								if isinstance(role, list): selection = ', '.join([str(r) for r in role])
								else: selection = role.name
								pass
							else:
								if isinstance(user, list):
									for u in user: sqlexecute(f"""
										UPDATE levels
										SET rank=rank+{gift}
										WHERE server='{message.server.id}'
										AND member='{u.id}';
										""".replace("\t", ""))
									selection = ', '.join([str(u) for u in user])
									pass
								else:
									sqlexecute(f"""
									UPDATE levels
									SET rank=rank+{gift}
									WHERE server='{message.server.id}'
									AND member='{user.id}';
									""".replace("\t", ""))
									selection = user
									pass
								pass
							pass
						elif _type == "mul":
							_type = "multipliers"
							if len(role) >= 1:
								for member in message.server.members:
									for r in role:
										if r in member.roles:
											sqlexecute(f"""
											UPDATE levels
											SET multiplier=multiplier+{gift}
											WHERE server='{message.server.id}'
											AND member='{member.id}';
											""".replace("\t", ""))
											pass
										pass
									pass
								if isinstance(role, list): selection = ', '.join([str(r) for r in role])
								else: selection = role.name
								pass
							else:
								if isinstance(user, list):
									for u in user:
										sqlexecute(f"""
										UPDATE levels
										SET multiplier=multiplier+{gift}
										WHERE server='{message.server.id}'
										AND member='{u.id}';
										""".replace("\t", ""))
										pass
									selection = ', '.join([str(u) for u in user])
									pass
								if isinstance(user, list):
									sqlexecute(f"""
									UPDATE levels
									SET multiplier=multiplier+{gift}
									WHERE server='{message.server.id}'
									AND member='{u.id}';
									""".replace("\t", ""))
									selection = str(user)
									pass
								pass
							pass

						save(message.server.id)
						await client.send_message(message.channel, f"```Awarded {selection} with {parse_num(gift)} {_type}!```")
						pass
					else: await client.send_message(message.channel, "```Only admins can award users!```")
					pass
				elif startswith(f"l$estimate "):
					content = message.content.replace(f"l$estimate ", "")
					content = content.split("->")
					try:
						total = 0
						for i in range(int(content[0]), int(content[1]) + 1):
							total += round(base * (multi ** int(i)))
							pass
						await client.send_message(message.channel, f"{content[0]}->{content[1]}\n{parse_num(total)} xp needed.")
						pass
					except:
						await client.send_message(message.channel, f"Could not estimate the value of {content[0]}->{content[1]}")
						pass
					pass
				pass
			pass
		if startswith(f"$update", "logbot.levels.update"):
			if message.author.id == owner_id: do_update = True
			else:
				await client.send_message(message.channel, "```You do not have permission to use this command.```")
				print(f"{Fore.LIGHTGREEN_EX}{str(message.author)} attempted to use a command.{Fore.RESET}")
				pass
			pass
		elif startswith("logbot.levels.exit"):
			if message.author.id == owner_id: await client.logout()
			else:
				await client.send_message(message.channel, "```You do not have permission to use this command.```")
				print(f"{Fore.LIGHTGREEN_EX}{str(message.author)} attempted to use a command.{Fore.RESET}")
				pass
			pass
		elif startswith(f"$ping"):
			tm = datetime.now() - message.timestamp
			await client.send_message(message.channel, f"```LogBot Levels Online ~ {round(tm.microseconds / 1000)}```")
			pass
		elif startswith(f"l$disabled"):
			await client.send_message(message.channel, f"```{disabled}```")
			pass
		elif startswith(f"l$disable"):
			if admin_role in message.author.roles or message.author.id == owner_id:
				disabled = True
				await client.send_message(message.channel, "```Disabled levels plugin for this server.```")
				pass
			else:
				await client.send_message(message.channel, "```You do not have permission to use this command.```")
				print(f"{Fore.LIGHTGREEN_EX}{str(message.author)} attempted to use a command.{Fore.RESET}")
				pass
			pass
		elif startswith(f"l$enable"):
			if admin_role in message.author.roles or message.author.id == owner_id:
				disabled = False
				await client.send_message(message.channel, "```Enabled levels plugin for this server.```")
				pass
			else:
				await client.send_message(message.channel, "```You do not have permission to use this command.```")
				print(f"{Fore.LIGHTGREEN_EX}{str(message.author)} attempted to use a command.{Fore.RESET}")
				pass
			pass
		elif startswith(f"l$execute\n", "```sql\n--execute"):
			if message.author.id == owner_id:
				sqlexecute(message.content.replace("l$execute\n", "").replace("```sql\n--execute", "").replace("```", "").replace("{sid}", message.server.id).replace("{uid}", message.author.id))
				await client.send_message(message.channel, "```Execution Successful.```")
				pass
			else:
				await client.send_message(message.channel, "```You do not have permission to use this command.```")
				print(f"{Fore.LIGHTGREEN_EX}{str(message.author)} attempted to use a command.{Fore.RESET}")
				pass
			pass
		elif startswith(f"l$get\n", "```sql\n--get\n"):
			if message.author.id == owner_id:
				try:
					res = sqlread(message.content.replace("l$get\n", "").replace("```sql\n--get\n", "").replace("```", "").replace("{sid}", message.server.id).replace("{uid}", message.author.id))
					_res = str(res)
					if startswith("```sql\n--get\n--format_id\n"):
						for server in client.servers: _res = _res.replace(server.id, str(server))
						for member in client.get_all_members(): _res = _res.replace(member.id, str(member))
						pass
					ret = format_message(f"Execution Successful. Result:\n{_res}")
					for retu in ret: await client.send_message(message.channel, retu)
					pass
				except:
					for i in format_message(traceback.format_exc().replace("```", "`")):
						await client.send_message(message.channel, i)
						pass
					pass
				pass
			else:
				await client.send_message(message.channel, "```You do not have permission to use this command.```")
				print(f"{Fore.LIGHTGREEN_EX}{str(message.author)} attempted to use a command.{Fore.RESET}")
				pass
			pass
		elif startswith(f"l$dm "):
			content = message.content.replace("l$dm ", "")
			if "t" in content.lower(): sqlexecute(f"""
				UPDATE levels
				SET dm='TRUE'
				WHERE server='{message.server.id}'
				AND member='{message.author.id}';
				""".replace("\t", ""))
			else: sqlexecute(f"""
				UPDATE levels
				SET dm='FALSE'
				WHERE server='{message.server.id}'
				AND member='{message.author.id}';
				""".replace("\t", ""))
			await client.send_message(message.channel, "```Updated DM Channel.```")
			pass
		elif startswith(f"l$alert "):
			cnt = message.content.replace("l$alert ", "")
			if cnt.capitalize() == "None": new_alert = None
			else: new_alert = discord.utils.find(lambda c: c.id == cnt or c.name == cnt or str(c) == cnt or c.mention == cnt, message.server.channels)
			if isinstance(new_alert, discord.Channel): new_alert = new_alert.id
			sqlexecute(f"""
			UPDATE levels
			SET alert_channel="{new_alert}"
			WHERE server="{message.server.id}"
			AND member="{message.author.id}";
			""".replace("\t", ""))
			await client.send_message(message.channel, f"```Updated Alert Channel```")
			pass

		save(message.server.id if not message.server is None else message.channel.id)
		if do_update:
			print(f"{Fore.LIGHTCYAN_EX}Updating...{Fore.RESET}")
			await client.close()
			subprocess.Popen(f"python {os.getcwd()}\\levels.py", False)
			exit(0)
			pass
		pass
	pass

@client.event
async def on_ready():
	if not os.path.exists(_data): os.makedirs(_data)
	if not os.path.exists(_disables): os.makedirs(_disables)
	os.system("cls")
	print(f"{Fore.MAGENTA}Ready!!!{Fore.RESET}")
	try: sqlexecute(f"""
	CREATE TABLE levels (server VARCHAR(50), member VARCHAR(50), tier LONG, rank INTEGER(3), xp LONG, xp_limit LONG, multiplier DECIMAL(50,1), credits LONG, cpm LONG, dm BOOLEAN);
	""".replace("\t", ""))
	except: pass
	try: sqlexecute(f"""
		CREATE INDEX i
		ON levels (server, member, tier, rank, xp, xp_limit, multiplier, credits, cpm, dm);
		""".replace("\t", ""))
	except: pass
	try: sqlexecute(f"""
	CREATE TABLE disables (server VARCHAR(50), disabled INTEGER);
	""".replace("\t", ""))
	except: pass
	try: sqlexecute(f"""
	CREATE INDEX di
	ON disables (server, disabled);
	""".replace("\t", ""))
	except: pass
	pass

client.run(token)
