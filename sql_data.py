import sqlite3
import os
from colorama import Fore, Back, init

# noinspection PyUnusedLocal
class kjv_sql(object):
	def __init__(self, books: list):
		"""
		:param books: A string list of the books of the Bible.
		"""
		self.settings = os.path.expanduser("~\\Documents\\Discord Logs\\SETTINGS")
		self.has_initialized = False
		self.data = "{}\\bible.txt".format(self.settings)
		self.connection = sqlite3.connect("{}\\kjv.db".format(self.settings))
		self.cursor = self.connection.cursor()
		init()

		try:
			reader = open("{}\\has_kjv_initialized.txt".format(self.settings), 'r')
			self.has_initialized = True if reader.read() == "True" else False
			reader.close()
			pass
		except:
			self.has_initialized = False
			pass

		if not self.has_initialized:
			self.__create()
			reader = open(self.data, 'r')
			bible = reader.read()
			reader.close()
			lines = bible.split("\n")
			for line in lines:
				try:
					l = line.split("	")
					key = l[0]
					self.cursor.execute("""INSERT INTO kjv (key, value)
						VALUES ("{}", "{}");""".format(key, l[1]))
					print(f"{Back.LIGHTWHITE_EX}{Fore.BLACK}Loading line {lines.index(line)} of {len(lines)}{Fore.RESET}{Back.RESET}")
					pass
				except: pass
				pass
			print("{}Committing data...{}".format(Back.LIGHTWHITE_EX + Fore.BLACK, Fore.RESET + Back.RESET))
			self.connection.commit()
			self.has_initialized = True

			writer = open("{}\\has_kjv_initialized.txt".format(self.settings), 'w+')
			writer.write(str(self.has_initialized))
			writer.close()
			pass
		pass
	def __create(self):
		cmd = """CREATE TABLE kjv (key VARCHAR(30), value VARCHAR(10000));"""
		try:
			self.cursor.execute(cmd)
		except:
			pass
		self.connection.commit()
		pass
	def __write(self, key, value):
		cmd = """INSERT INTO kjv (key, value)
			VALUES ("{}", "{}");""".format(key, value)
		self.cursor.execute(cmd)
		self.connection.commit()
		pass
	def read(self, book: str, chapter: str, verse: str) -> str:
		"""
		Fetches a verse from the Bible.
		:param book: The book name. Should be capitalized.
		:param chapter: The chapter number.
		:param verse: The verse number.
		:return: The verse.
		"""
		self.cursor.execute(f"SELECT * FROM kjv WHERE key IN ('{book} {chapter}:{verse}');")
		result = self.cursor.fetchall()
		return result[0][1]
	def execute(self, cmd):
		self.cursor.execute(cmd)
		return self.cursor.fetchall()
	def close(self):
		"""
		Closes the SQL connection.
		"""
		self.connection.close()
		pass

# noinspection PyUnusedLocal
class sql_data(object):
	def __init__(self, books: list):
		"""
		:param books: A string array of the books of the Bible. Not required.
		"""
		self.settings = os.path.expanduser("~\\Documents\\Discord Logs\\SETTINGS")  # @UndefinedVariable
		self.has_initialized = False
		self.data = "{}\\akjv.txt".format(self.settings)
		self.connection = sqlite3.connect("{}\\akjv.db".format(self.settings))
		self.cursor = self.connection.cursor()
		init()

		try:
			reader = open("{}\\has_initialized.txt".format(self.settings), 'r')
			self.has_initialized = True if reader.read() == "True" else False
			reader.close()
			pass
		except:
			self.has_initialized = False
			pass

		if not self.has_initialized:
			self.__create()
			reader = open(self.data, 'r')
			bible = reader.read()
			reader.close()
			lines = bible.split("\n")
			for line in lines:
				try:
					l = line.split("	")
					key = l[0]
					self.cursor.execute("""INSERT INTO akjv (key, value)
						VALUES ("{}", "{}");""".format(key, l[1]))
					print("{}Loading line {} of {}{}".format(Back.LIGHTWHITE_EX + Fore.BLACK, lines.index(line), len(lines), Fore.RESET + Back.RESET))
					# if lines.index(line) % 1000 == 0:self.connection.commit()
					pass
				except:
					pass
			print("{}Committing data...{}".format(Back.LIGHTWHITE_EX + Fore.BLACK, Fore.RESET + Back.RESET))
			self.connection.commit()
			self.has_initialized = True

			writer = open("{}\\has_initialized.txt".format(self.settings), 'w+')
			writer.write(str(self.has_initialized))
			writer.close()
			pass
		pass
	def __create(self):
		cmd = """CREATE TABLE akjv (key VARCHAR(30), value VARCHAR(10000));"""
		try:
			self.cursor.execute(cmd)
		except:
			pass
		self.connection.commit()
		pass
	def __write(self, key, value):
		cmd = """INSERT INTO akjv (key, value)
			VALUES ("{}", "{}");""".format(key, value)
		self.cursor.execute(cmd)
		self.connection.commit()
		pass
	def read(self, book: str, chapter: str, verse: str):
		"""
		Fetches a verse from the Bible.
		:param book: The book name. Should be capitalized.
		:param chapter: The chapter number.
		:param verse: The verse number.
		:return: The verse.
		"""
		self.cursor.execute(f"SELECT * FROM akjv WHERE key IN ('{book} {chapter}:{verse}');")
		result = self.cursor.fetchall()
		return result[0][1]
		pass
	def execute(self, cmd):
		self.cursor.execute(cmd)
		return self.cursor.fetchall()
		pass
	def close(self):
		"""
		Closes the SQL connection.
		"""
		self.connection.close()
		pass
	pass

# noinspection PyUnusedLocal
class web_sql(object):
	def __init__(self, books: list):
		"""
		:param books: A list of book names. Not required.
		"""
		self.settings = os.path.expanduser("~\\Documents\\Discord Logs\\SETTINGS")
		self.has_initialized = False
		self.data = "{}\\web.txt".format(self.settings)
		self.connection = sqlite3.connect("{}\\web.db".format(self.settings))
		self.cursor = self.connection.cursor()
		init()

		try:
			reader = open("{}\\has_web_initialized.txt".format(self.settings), 'r')
			self.has_initialized = True if reader.read() == "True" else False
			reader.close()
			pass
		except:
			self.has_initialized = False
			pass

		if not self.has_initialized:
			self.__create()
			reader = open(self.data, 'r')
			bible = reader.read()
			reader.close()
			lines = bible.split('\n')
			for line in lines:
				try:
					l = line.split("	")
					key = l[0]
					self.cursor.execute("""INSERT INTO web (key, value)
						VALUES ("{}", "{}");""".format(key, l[1]))
					print("{}Loading line {} of {}{}".format(Back.LIGHTWHITE_EX + Fore.BLACK, lines.index(line), len(lines), Fore.RESET + Back.RESET))
					pass
				except:
					pass
				pass
			print("{}Committing data...{}".format(Back.LIGHTWHITE_EX + Fore.BLACK, Fore.RESET + Back.RESET))
			self.connection.commit()
			self.has_initialized = True

			writer = open("{}\\has_web_initialized.txt".format(self.settings), 'w+')
			writer.write(str(self.has_initialized))
			writer.close()
			pass
		pass
	def __create(self):
		cmd = """CREATE TABLE web (key VARCHAR(30), value VARCHAR(10000));"""
		try:
			self.cursor.execute(cmd)
		except:
			pass
		self.connection.commit()
		pass
	def __write(self, key, value):
		cmd = """INSERT INTO web (key, value)
			VALUES ("{}", "{}");""".format(key, value)
		self.cursor.execute(cmd)
		self.connection.commit()
		pass
	def read(self, book: str, chapter: str, verse: str) -> str:
		"""
		Fetch a verse from the Bible.
		:param book: The book name. Should be capitalized.
		:param chapter: The chapter number.
		:param verse: The verse number.
		:return: The verse fetched.
		"""
		self.cursor.execute(f"SELECT * FROM web WHERE key IN ('{book} {chapter}:{verse}');")
		result = self.cursor.fetchall()
		return result[0][1]
		pass
	def execute(self, cmd):
		self.cursor.execute(cmd)
		return self.cursor.fetchall()
		pass
	def close(self):
		"""
		Closes the SQL connection.
		"""
		self.connection.close()
		pass
	pass
