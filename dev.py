import os
import subprocess

import discord
from colorama import Fore, init

from logbot_data import owner_id, token

client = discord.Client()
init()

discord_settings = f"{os.getcwd()}\\Discord Logs\\SETTINGS"
suggestions = f"{discord_settings}\\suggestions.txt"
reports = f"{discord_settings}\\bugs.txt"

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
	else: ret = [msg[i:i + 2000] for i in range(0, len(msg), 2000)]
	return ret

@client.event
async def on_message(message: discord.Message):
	begins = message.content.startswith
	if message.author.id == owner_id:
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
		elif begins("d$update") or begins("logbot.dev.update"):
			print("{Fore.LIGHTCYAN_EX}Updating...{Fore.RESET}")
			await client.close()
			subprocess.Popen("python " + os.getcwd() + "\\dev.py", False)
			exit(0)
			pass
		pass

	if begins("$report "):
		cnt = "-" + message.content.replace('$report ', '').replace("```", "'''")
		try:
			reader = open(reports, 'r')
			text = reader.read()
			reader.close()
			pass
		except: text = ""
		if f"{cnt}\n" in text:
			await client.send_message(message.channel, f"```There is already a report for \"{cnt}\"```")
			pass
		else:
			writer = open(reports, 'a')
			writer.write(f"{cnt}\n")
			writer.close()
			await client.send_message(message.channel, f"```Thank you for your report.```")
			del writer
			pass
		del text
		del cnt
		pass
	elif begins("$reports"):
		reader = open(reports, 'r')
		text = reader.read()
		reader.close()
		if len(text) > 0:
			msgs = format_message(text, "```")
			for msg in msgs: await client.send_message(message.channel, msg)
			pass
		else:
			await client.send_message(message.channel, f"```There are no bug reports yet.```")
			pass
		del reader
		pass
	pass

@client.event
async def on_ready():
	os.system("cls")
	print(f"{Fore.MAGENTA}Ready!!!{Fore.RESET}")
	pass

client.run(token)
