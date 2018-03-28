"""
SQL Data Tool
"""
import sqlite3
import os
from colorama import Fore, Back, init

# noinspection PyUnusedLocal
class KJVSQL( object ):
	"""
	KJVSQL class
	"""
	def __init__ ( self ):
		"""
		"""
		# self.settings = os.path.expanduser( "~\\Documents\\Discord Logs\\SETTINGS" )
		self.settings = f"{os.getcwd( )}\\Discord Logs\\SETTINGS"
		self.has_initialized = False
		self.data = f"{self.settings}\\bible.txt"
		self.connection = sqlite3.connect( f"{self.settings}\\kjv.db" )
		self.cursor = self.connection.cursor( )
		init( )

		try:
			reader = open( f"{self.settings}\\has_kjv_initialized.txt", 'r' )
			self.has_initialized = True if reader.read( ) == "True" else False
			reader.close( )
			del reader
		except Exception:
			self.has_initialized = False

		if not self.has_initialized:
			self.__create( )
			reader = open( self.data, 'r' )
			bible = reader.read( )
			reader.close( )
			lines = bible.split( "\n" )
			for line in lines:
				try:
					line_part = line.split( "	" )
					key = line_part[ 0 ]
					self.cursor.execute( f"""INSERT INTO kjv (key, value)
						VALUES ("{key}", "{line_part[1]}");""" )
					print( f"{Back.LIGHTWHITE_EX}{Fore.BLACK}Loading line {lines.index(line)} of {len(lines)}{Fore.RESET}{Back.RESET}" )
					del line_part
					del key
				except Exception:
					pass
			print( f"{Back.LIGHTWHITE_EX + Fore.BLACK}Committing data...{Fore.RESET + Back.RESET}" )
			self.connection.commit( )
			self.has_initialized = True

			writer = open( f"{self.settings}\\has_kjv_initialized.txt", 'w+' )
			writer.write( str( self.has_initialized ) )
			writer.close( )
			del writer
			del reader
			del bible
			del lines
	def __create ( self ):
		cmd = """CREATE TABLE kjv (key VARCHAR(30), value VARCHAR(10000));"""
		try:
			self.cursor.execute( cmd )
		except Exception:
			pass
		self.connection.commit( )
		del cmd
	def __write ( self, key, value ):
		cmd = f"""INSERT INTO kjv (key, value)
			VALUES ("{key}", "{value}");"""
		self.cursor.execute( cmd )
		self.connection.commit( )
		del cmd
	def read ( self, book: str, chapter: str, verse: str ) -> str:
		"""
		Fetches a verse from the Bible.
		:param book: The book name. Should be capitalized.
		:param chapter: The chapter number.
		:param verse: The verse number.
		:return: The verse.
		"""
		self.cursor.execute( f"SELECT * FROM kjv WHERE key IN ('{book} {chapter}:{verse}');" )
		result = self.cursor.fetchall( )
		return result[ 0 ][ 1 ]
	def execute ( self, cmd ):
		"""
		Executes a command.
		:param cmd: The command.
		:return: The resulting data.
		"""
		self.cursor.execute( cmd )
		return self.cursor.fetchall( )
	def close ( self ):
		"""
		Closes the SQL connection.
		"""
		self.connection.close( )

# noinspection PyUnusedLocal
class AKJVSQL( object ):
	"""
	AKJVSQL class
	"""
	def __init__ ( self):
		self.settings = f"{os.getcwd( )}\\Discord Logs\\SETTINGS"
		self.has_initialized = False
		self.data = f"{self.settings}\\akjv.txt"
		self.connection = sqlite3.connect( f"{self.settings}\\akjv.db" )
		self.cursor = self.connection.cursor( )
		init( )

		try:
			reader = open( f"{self.settings}\\has_initialized.txt", 'r' )
			self.has_initialized = True if reader.read( ) == "True" else False
			reader.close( )
			del reader
		except Exception:
			self.has_initialized = False

		if not self.has_initialized:
			self.__create( )
			reader = open( self.data, 'r' )
			bible = reader.read( )
			reader.close( )
			lines = bible.split( "\n" )
			for line in lines:
				try:
					line_part = line.split( "	" )
					key = line_part[ 0 ]
					self.cursor.execute( f"""INSERT INTO akjv (key, value)
						VALUES ("{key}", "{line_part[1]}");""")
					print( f"{Back.LIGHTWHITE_EX + Fore.BLACK}Loading line {lines.index(line)} of {len(lines)}{Fore.RESET + Back.RESET}" )
					del line_part
					del key
				except Exception:
					pass
			print( f"{Back.LIGHTWHITE_EX}{Fore.BLACK}Committing data...{Fore.RESET}{Back.RESET}" )
			self.connection.commit( )
			self.has_initialized = True

			writer = open( f"{self.settings}\\has_initialized.txt", 'w+' )
			writer.write( str( self.has_initialized ) )
			writer.close( )
			del reader
			del bible
			del lines
			del writer
	def __create ( self ):
		cmd = """CREATE TABLE akjv (key VARCHAR(30), value VARCHAR(10000));"""
		try:
			self.cursor.execute( cmd )
		except Exception:
			pass
		self.connection.commit( )
		del cmd
	def __write ( self, key, value ):
		cmd = f"""INSERT INTO akjv (key, value)
			VALUES ("{key}", "{value}");"""
		self.cursor.execute( cmd )
		self.connection.commit( )
		del cmd
	def read ( self, book: str, chapter: str, verse: str ):
		"""
		Fetches a verse from the Bible.
		:param book: The book name. Should be capitalized.
		:param chapter: The chapter number.
		:param verse: The verse number.
		:return: The verse.
		"""
		self.cursor.execute( f"SELECT * FROM akjv WHERE key IN ('{book} {chapter}:{verse}');" )
		result = self.cursor.fetchall( )
		return result[ 0 ][ 1 ]
	def execute ( self, cmd ):
		"""
		Executes a command.
		:param cmd: The command.
		:return: The resulting data.
		"""
		self.cursor.execute( cmd )
		return self.cursor.fetchall( )
	def close ( self ):
		"""
		Closes the SQL connection.
		"""
		self.connection.close( )

# noinspection PyUnusedLocal
class WEBSQL( object ):
	"""
	WEBSQL class.
	"""
	def __init__ ( self):
		"""
		"""
		# self.settings = os.path.expanduser( "~\\Documents\\Discord Logs\\SETTINGS" )
		self.settings = f"{os.getcwd()}\\Discord Logs\\SETTINGS"
		self.has_initialized = False
		self.data = f"{self.settings}\\web.txt"
		self.connection = sqlite3.connect( f"{self.settings}\\web.db" )
		self.cursor = self.connection.cursor( )
		init( )

		try:
			reader = open( f"{self.settings}\\has_web_initialized.txt", 'r' )
			self.has_initialized = True if reader.read( ) == "True" else False
			reader.close( )
			del reader
		except Exception:
			self.has_initialized = False

		if not self.has_initialized:
			self.__create( )
			reader = open( self.data, 'r' )
			bible = reader.read( )
			reader.close( )
			lines = bible.split( '\n' )
			for line in lines:
				try:
					line_part = line.split( "	" )
					key = line_part[ 0 ]
					self.cursor.execute( f"""INSERT INTO web (key, value)
						VALUES ("{key}", "{line_part[1]}");""" )
					print( f"{Back.LIGHTWHITE_EX}{Fore.BLACK}Loading line {lines.index(line)} of {len(lines)}{Fore.RESET}{Back.RESET}" )
					del line_part
					del key
				except Exception:
					pass
			print( f"{Back.LIGHTWHITE_EX}{Fore.BLACK}Committing data...{Fore.RESET}{Back.RESET}" )
			self.connection.commit( )
			self.has_initialized = True

			writer = open( f"{self.settings}\\has_web_initialized.txt", 'w+' )
			writer.write( str( self.has_initialized ) )
			writer.close( )
			del writer
			del reader
			del bible
			del lines
	def __create ( self ):
		cmd = """CREATE TABLE web (key VARCHAR(30), value VARCHAR(10000));"""
		try:
			self.cursor.execute( cmd )
		except Exception:
			pass
		self.connection.commit( )
		del cmd
	def __write ( self, key, value ):
		cmd = """INSERT INTO web (key, value)
			VALUES ("{}", "{}");""".format( key, value )
		self.cursor.execute( cmd )
		self.connection.commit( )
		del cmd
	def read ( self, book: str, chapter: str, verse: str ) -> str:
		"""
		Fetch a verse from the Bible.
		:param book: The book name. Should be capitalized.
		:param chapter: The chapter number.
		:param verse: The verse number.
		:return: The verse fetched.
		"""
		self.cursor.execute( f"SELECT * FROM web WHERE key IN ('{book} {chapter}:{verse}');" )
		result = self.cursor.fetchall( )
		return result[ 0 ][ 1 ]
	def execute ( self, cmd ):
		"""
		Executes a command.
		:param cmd: The command.
		:return: The resulting information.
		"""
		self.cursor.execute( cmd )
		return self.cursor.fetchall( )
	def close ( self ):
		"""
		Closes the SQL connection.
		"""
		self.connection.close( )

class NIVSQL( object ):
	"""
	NIVSQL class
	"""
	def __init__ ( self ):
		self.settings = f"{os.getcwd()}\\Discord Logs\\SETTINGS"
		self.has_initialized = False
		self.data = f"{self.settings}\\NIV_TEXT.txt"
		self.connection = sqlite3.connect( f"{self.settings}\\niv.db" )
		self.cursor = self.connection.cursor( )
		init( )

		try:
			reader = open( f"{self.settings}\\has_niv_initialized.txt", 'r' )
			self.has_initialized = True if reader.read( ) == "True" else False
			reader.close( )
			del reader
		except Exception:
			self.has_initialized = False

		if not self.has_initialized:
			self.__create( )
			reader = open( self.data, 'r' )
			bible = reader.read( )
			reader.close( )
			lines = bible.split( '\n' )
			for line in lines:
				try:
					line_part = line.split( "	" )
					key = line_part[ 0 ]
					self.cursor.execute( f"""INSERT INTO niv (key, value)
						VALUES ("{key}", "{line_part[1]}");""" )
					print( f"{Back.LIGHTWHITE_EX}{Fore.BLACK}Loading line {lines.index(line)} of {len(lines)}{Fore.RESET}{Back.RESET}" )
					del line_part
					del key
				except Exception:
					pass
			print( f"{Back.LIGHTWHITE_EX}{Fore.BLACK}Committing data...{Fore.RESET}{Back.RESET}" )
			self.connection.commit( )
			self.has_initialized = True

			writer = open( f"{self.settings}\\has_niv_initialized.txt", 'w+' )
			writer.write( str( self.has_initialized ) )
			writer.close( )
			del writer
			del reader
			del bible
			del lines
	def __create ( self ):
		cmd = """CREATE TABLE niv (key VARCHAR(30), value VARCHAR(10000));"""
		try:
			self.cursor.execute( cmd )
		except Exception:
			pass
		self.connection.commit( )
		del cmd
	def __write ( self, key, value ):
		cmd = """INSERT INTO niv (key, value)
			VALUES ("{}", "{}");""".format( key, value )
		self.cursor.execute( cmd )
		self.connection.commit( )
		del cmd
	def read ( self, book: str, chapter: str, verse: str ) -> str:
		"""
		Fetch a verse from the Bible.
		:param book: The book name. Should be capitalized.
		:param chapter: The chapter number.
		:param verse: The verse number.
		:return: The verse fetched.
		"""
		self.cursor.execute( f"SELECT * FROM niv WHERE key IN ('{book} {chapter}:{verse}');" )
		result = self.cursor.fetchall( )
		return result[ 0 ][ 1 ]
	def execute ( self, cmd ):
		"""
		Executes `cmd`
		:param cmd: The command.
		:return: the results.
		"""
		self.cursor.execute( cmd )
		return self.cursor.fetchall( )
	def close ( self ):
		"""
		Closes the SQL connection.
		"""
		self.connection.close( )
