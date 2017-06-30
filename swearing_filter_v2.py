import ast
from datetime import datetime
import os
import subprocess
import re

from colorama import init, Fore
from discord import Client
import nltk
import requests
from logbot_data import token

client = Client()
init()
owner_id = "239500860336373761"

discord_settings = os.path.expanduser("~\\Documents\\Discord Logs\\SETTINGS")
filter_disables = f"{discord_settings}\\filter_disable_list.txt"
filter_disable_list = {}

try:
	reader = open(filter_disables, 'r')
	filter_disable_list = ast.literal_eval(reader.read())
	reader.close()
	del reader
	pass
except: pass

def check(*args: str) -> str:
	"""
	Compares each string to check which one is ascii.
	:param args: Several string parameters.
	:return: The first ascii instance, or "Unknown String." if none are ascii.
	"""
	for item in args:
		if item is not None and all(ord(c) for c in item): return item
		pass
	return "Unknown String."

def checkForSymbols(m: str) -> list:
	"""
	Filters disallowed symbols out of a message.
	:param m: The message content.
	:return: An enumeration of the filtered message and the symbols.
	"""
	symbols = ['+', '#', '&']
	repl = "\{i\}"
	for i in symbols: m = m.replace(i, repl.replace("i", str(symbols.index(i))))
	return [m, symbols]

def filter_message(msg: str) -> tuple:
	"""
	Filters `msg` and replaces banned words.
	:param msg: The message to filter.
	:return: `msg`, but with all banned words replaced in index 0, and with a list of the words replaced (in the order replaced) at index 1.
	"""
	base_words = """ass
	asses
	assface
	assfaces
	asshole
	assholes
	bastard
	bastards
	bitch
	bitches
	bitchy
	bullshit
	cocksucker
	cocksuckers
	cocksucking
	cunt
	cunts
	dickhead
	dickheads
	faggot
	faggots
	fuc
	fuck
	fucked
	fuckedup
	fucker
	fuckers
	fucking
	fuckoff
	fucks
	fuckup
	fuk
	fukker
	fukkers
	fuq
	goddamn
	goddamnit
	jackass
	jackasses
	motherfucker
	motherfuckers
	motherfucking
	nigger
	niggers
	pussy
	shit
	shithead
	shitheads
	shits
	shittier
	shittiest
	shitting
	shitty
	smartass
	smartasses
	tities
	tits
	titties
	wiseass
	wiseasses""".replace("\t", "").split("\n")
	res = ""
	repl_words = []
	for item in msg.split("\n"):
		message_words = nltk.tokenize.word_tokenize(item, preserve_line=True)
		repl_words = []
		for i in range(0, len(message_words)):
			for bw in base_words:
				if bw == message_words[i].lower().replace("$", "s").replace("@", "a"):
					repl_words.append(message_words[i]); r = "\\*"
					res += f" {repl_char * len(message_words[i])}"
					pass
				else: res += f" {message_words[i]}"
				pass
			pass
		pass
	return res, repl_words
	pass

@client.event
async def on_message(message):
	do_update = False
	ocont = message.content
	result = filter_message(ocont)
	ncont = result[0]
	print(f"\"{ocont}\" -> \"{ncont}\"")

	if f" {ocont}" != ncont:
		await client.delete_message(message)
		await client.send_message(message.channel, f"[{message.author.mention}] {ncont}")
		pass

	def startswith(*msgs, val=message.content):
		for m in msgs:
			if val.startswith(m): return True
			pass
		return False
	if startswith("$update", "logbot.filter.update"):
		if message.author.id == owner_id: do_update = True
		pass
	elif startswith("logbot.settings exit", "logbot.filter.exit"):
		if message.author.id == owner_id: exit(0)
		pass
	elif startswith("$ping"):
		tm = datetime.now() - message.timestamp
		await client.send_message(message.channel, f"```LogBot Swearing Filter Online ~ {round(tm.microseconds / 1000)}```")
		pass
	if do_update:
		print(f"{Fore.LIGHTCYAN_EX}Updating...{Fore.RESET}")
		await client.close()
		subprocess.Popen(f"python {os.getcwd()}\\swearing_filter_v2.py", False)
		exit(0)
		pass
	pass

@client.event
async def on_ready():
	print(f"{Fore.MAGENTA}Ready!!!{Fore.RESET}")
	pass

client.run(token)