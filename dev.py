import os

import discord
from colorama import Fore, init

from logbot_data import token, owner_id

client = discord.Client()
init()

discord_settings = os.path.expanduser("~\\Documents\\Discord Logs\\SETTINGS")
suggestions = f"{discord_settings}\\suggestions.txt"

def format_message(msg: str, _tag: str) -> list:
	"""
	:param msg: The string to format
	:param _tag: The tag to insert. Can be None. If not None, will insert tag at the beginning and end of each string in the result.
	:return: A list of strings from `msg`, where each string is no more than 2000 characters long.
	"""
	if not _tag is None:
		len_tag = len(_tag) * 2
		len_str = 2000 - len_tag
		ret = [f"{_tag}{msg[i:i+len_str]}{_tag}" for i in range(0, len(msg), len_str)]
		pass
	else: ret = [msg[i:i+2000] for i in range(0, len(msg), 2000)]
	return ret

@client.event
async def on_message(message: discord.Message):
	if message.author.id == owner_id:
		begins = message.content.startswith
		if begins("$suggestions"):
			# <editor-fold desc="READER: suggestions">
			# noinspection PyShadowingNames
			reader = open(suggestions, 'r')
			ret = f"Suggestions:{reader.read()}"
			reader.close()
			# </editor-fold>
			for item in format_message(ret, "```"): await client.send_message(message.channel, item)
			del ret
			del reader
			pass
		pass
	pass

@client.event
async def on_ready():
	os.system("cls")
	print(f"{Fore.MAGENTA}Ready!!!{Fore.RESET}")
	pass

client.run(token)
