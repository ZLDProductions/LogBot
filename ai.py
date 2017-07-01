import asyncio
import discord
from colorama import Fore, init
import os
from logbot_data import token

client = discord.Client()
# noinspection SpellCheckingInspection
init()

@asyncio.coroutine
async def _send():
	"""
	Sends a message as the bot.
	"""
	os.system("cls")
	print("\n".join([f"{server} [{server.id}]" for server in client.servers]))
	server = input(f"{Fore.RED}Server:{Fore.LIGHTGREEN_EX} ")
	server = discord.utils.find(lambda s: s.name == server or s.id == server, client.servers)
	if not server is None:
		print("\n".join([f"{channel} [{channel.id}]" for channel in server.channels]))
		channel = input(f"{Fore.RED}Channel:{Fore.LIGHTGREEN_EX} ")
		channel = discord.utils.find(lambda c: c.name == channel or c.id == channel or c.mention == channel or f"#{str(c)}" == channel, server.channels)
		pass
	else:
		print('\n'.join([f"{channel} [{channel.id}]" for channel in client.get_all_members()]))
		channel = input(f"{Fore.RED}Channel:{Fore.LIGHTGREEN_EX} ")
		channel = discord.utils.find(lambda c: c.name == channel or c.id == channel or c.mention == channel or f"{str(c)}" == channel, client.get_all_members())
		pass
	message = input(f"{Fore.RED}Message:{Fore.LIGHTGREEN_EX} ")

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
