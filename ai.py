import asyncio
import discord
from colorama import Fore, init
import os

client = discord.Client()
# noinspection SpellCheckingInspection
token = 'MjU1Mzc5NzQ4ODI4NjEwNTYx.CycwfQ.c6n0jvVrV5lGbbke68dHdlYMRX0'
init()

@asyncio.coroutine
async def _send():
	"""
	Sends a message as the bot.
	"""
	os.system("cls")
	channel = input(f"{Fore.RED}Channel:{Fore.LIGHTGREEN_EX} ")
	message = input(f"{Fore.RED}Message:{Fore.LIGHTGREEN_EX} ")

	if not ">" in channel:
		channel = client.get_channel(channel)
		pass
	elif "DM:" in channel:
		channel = await client.get_user_info(channel.replace("DM:", ""))
		pass
	else:
		tmp = channel.split(">")
		server = discord.utils.find(lambda s:s.name == tmp[0], client.servers)
		channel = discord.utils.find(lambda c:c.name == tmp[1], server.channels)
		pass
	await client.send_message(channel, message)
	return

@asyncio.coroutine
async def _presence():
	"""
	Changes the presence of the bot.
	"""
	os.system("cls")
	game = input(f"{Fore.RED}Game:{Fore.LIGHTGREEN_EX} ")
	print(Fore.RESET)
	if game == 'None':
		game = None
		pass
	if not game is None:
		await client.change_presence(status="online", game=discord.Game(name=game), afk=False)
		pass
	else:
		await client.change_presence(status="online", game=None)
		pass
	return

@asyncio.coroutine
async def _exit():
	"""
	Logs out of the bot account.
	"""
	await client.close()
	return

@client.event
async def on_ready():
	os.system("cls")
	print(f"{Fore.MAGENTA}Ready!!!{Fore.RESET}")
	while not client.is_closed:
		os.system("cls")
		oper = input(f"{Fore.YELLOW}Operation:{Fore.RESET} ")
		if oper == 'send':
			await _send()
			pass
		elif oper == 'pres':
			await _presence()
			pass
		elif oper == 'exit':
			await _exit()
			pass
		pass
	pass

client.run(token)
