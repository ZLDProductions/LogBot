import os
import subprocess
from asyncio import sleep

import discord
from colorama import Fore, init

import argparser

client = discord.Client(max_messages=1000000)
init()

token = "MjU1Mzc5NzQ4ODI4NjEwNTYx.CycwfQ.c6n0jvVrV5lGbbke68dHdlYMRX0"
owner_id = "239500860336373761"
purge_parser = argparser.ArgParser("&&", "=")

class Commands:
	class Admin:
		@staticmethod
		async def a_clear(message: discord.Message):
			messages = list(client.messages)
			mtd = [m for m in messages if m.channel == message.channel]
			[await client.delete_message(m) for m in mtd]
			del messages
			del mtd
			pass
		@staticmethod
		async def at_clear(message: discord.Message):
			cnt = message.content.split(" ")
			try: _limit = int(cnt[1])
			except: _limit = 100
			logs = client.logs_from(message.channel, limit=_limit).iterate
			count = 0
			while True:
				try:
					item = await logs()
					await client.delete_message(item)
					count += 1
					pass
				except: break
				pass
			m = await client.send_message(message.channel, f"Deleted {count} messages.")
			await sleep(3)
			await client.delete_message(m)
			del cnt
			del count
			del m
			del _limit
			del logs
			pass
		pass
	class Owner:
		pass
	pass

@client.event
async def on_message(message):
	do_update = False
	def startswith(*args: str, val: str = message.content) -> bool:
		for arg in args:
			if val.startswith(arg): return True
			pass
		return False
		pass
	if not message.channel.is_private:
		admin_role = discord.utils.find(lambda r:r.name == "LogBot Admin", message.server.roles)
		if startswith("a$clear"):
			if admin_role in message.author.roles or message.author.id == owner_id: await Commands.Admin.a_clear(message)
			pass
		elif startswith("a$purge"):
			if admin_role in message.author.roles or message.author.id == owner_id: await Commands.Admin.at_clear(message)
			pass
		pass

	if startswith("a$update", "logbot.admin.update", "$update"):
		if message.author.id == owner_id: do_update = True
		pass
	elif startswith("a$exit", "logbot.admin.exit"):
		if message.author.id == owner_id: client.logout()
		pass

	if do_update is True:
		print(f"{Fore.LIGHTCYAN_EX}Updating...{Fore.RESET}")
		subprocess.Popen(f"python {os.getcwd()}\\bible.py")
		exit(0)
		pass
	pass

@client.event
async def on_ready():
	print(f"{Fore.MAGENTA}Ready!!!{Fore.RESET}")
	pass

client.run(token)