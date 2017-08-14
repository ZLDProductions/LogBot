import os
import subprocess
from asyncio import sleep

from discord import Client, Message
from discord.utils import find
from colorama import Fore, init

import argparser
from logbot_data import token, owner_id

client = Client(max_messages=1000000)
init()
purge_parser = argparser.ArgParser("&&", "=")

class Commands:
	class Admin:
		@staticmethod
		async def a_clear(message: Message):
			messages = list(client.messages)
			mtd = [m for m in messages if m.channel == message.channel]
			[await client.delete_message(m) for m in mtd]
			del messages
			del mtd
			pass
		@staticmethod
		async def at_clear(message: Message):
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
			print(count)
			await sleep(3)
			await client.delete_message(m)
			del cnt
			del count
			del m
			del _limit
			del logs
			pass
		@staticmethod
		async def a_count(message: Message):
			count = 0
			logs = client.logs_from(message.channel, limit=1000000000).iterate
			while True:
				try:
					await logs()
					count += 1
					pass
				except: break
				pass
			await client.send_message(message.channel, f"```{count} messages found!```")
			pass
		@staticmethod
		async def a_total(message: Message):
			count = 0
			for channel in message.server.channels:
				logs = client.logs_from(channel, limit=1000000000).iterate
				while True:
					try:
						await logs()
						count += 1
						pass
					except: break
					pass
				pass
			await client.send_message(message.channel, f"```{count} messages found!```")
			pass
		# noinspection PyShadowingNames
		@staticmethod
		async def a_count_param(message: Message):
			_cnt = message.content.replace("a$count ", "").split(" ")
			_type = _cnt[0].lower()
			_param = _cnt[1]
			user = find(lambda m:m.id == _param or m.name == _param or str(m) == _param or m.mention == _param, message.server.members)

			msgs = list()
			count = 0
			logs = client.logs_from(message.channel, limit=1000000000).iterate
			app = msgs.append
			while True:
				try: item = await logs(); app(item)
				except: break
				pass
			for m in msgs:
				if isinstance(m, Message):
					if _type == "&text":
						if _param in m.content: count += 1
						pass
					elif _type == "&from":
						if m.author.id == user.id: count += 1
						pass
					pass
				pass
			await client.send_message(message.channel, f"```{count} messages found!```")
			pass
		pass
	class Owner:
		@staticmethod
		async def a_server_clear(message: Message):
			count = 0
			for channel in message.server.channels:
				logs = client.logs_from(channel, limit=1000000).iterate
				while True:
					try:
						await client.delete_message(await logs())
						count += 1
						pass
					except: break
					pass
				pass
			m = await client.send_message(message.channel, f"```Deleted {count} messages.```")
			await sleep(3)
			await client.delete_message(m)
			del m
			del count
			pass
		pass
	pass

@client.event
async def on_message(message: Message):
	do_update = False
	def startswith(*args: str, val: str = message.content) -> bool:
		for arg in args:
			if val.startswith(arg): return True
			pass
		return False
	if not message.channel.is_private:
		admin_role = find(lambda r:r.name == "LogBot Admin", message.server.roles)
		if startswith("a$clear"):
			if message.author == message.server.owner or message.author.id == owner_id: await Commands.Admin.a_clear(message)
			pass
		elif startswith("a$purge"):
			if message.author == message.server.owner or message.author.id == owner_id: await Commands.Admin.at_clear(message)
			pass
		elif startswith("a$clsserver"):
			if message.author == message.server.owner or message.author.id == owner_id: await Commands.Owner.a_server_clear(message)
			pass
		elif startswith("a$count "):
			if admin_role in message.author.roles or message.author.id == owner_id: await Commands.Admin.a_count_param(message)
			pass
		elif startswith("a$count"):
			if admin_role in message.author.roles or message.author.id == owner_id: await Commands.Admin.a_count(message)
			pass
		elif startswith("a$total"):
			if admin_role in message.author.roles or message.author.id == owner_id: await Commands.Admin.a_total(message)
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
		subprocess.Popen(f"python {os.getcwd()}\\admin.py")
		exit(0)
		pass
	pass

@client.event
async def on_ready():
	os.system("cls")
	print(f"{Fore.MAGENTA}Ready!!!{Fore.RESET}")
	pass

client.run(token)
