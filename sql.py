"""
SQL tool.
"""
import sqlite3
import os
import random

class SQL:
	"""
	SQL class.
	"""
	def __init__ ( self, file: str = "logbot" ):
		self.settings = f"{os.getcwd()}\\Discord Logs\\SETTINGS"
		self.connection = sqlite3.connect( f"{self.settings}\\{file}.db" )
		self.cursor = self.connection.cursor( )
	def create ( self, table_name: str, *key_names: str ):
		"""
		Create an SQL Table if it does not already exist.
		:param table_name: The name of the table to create.
		:param key_names: The names of the keys. 1+ arguments required.
		"""
		vals = ""
		for k in key_names:
			vals += str( f", " + str( k ) + " VARCHAR(100000)" )
		vals = vals[ 2: ]
		cmd = f"""CREATE TABLE {table_name} ({vals});"""
		try:
			self.cursor.execute( cmd )
		except Exception:
			pass
		self.connection.commit( )
		del vals
		del cmd
	def write ( self, table: str, *values: dict ):
		"""
		Write data to a table.
		:param table: The table to write to.
		:param values: The keys of the table, with their respective values.
		"""
		tmp1 = ""
		tmp2 = ""
		vals = values[ 0 ]
		for val in list( vals.keys( ) ):
			tmp1 += f", '{val}'"
			tmp2 += f", '{vals[val]}'"
		tmp1 = tmp1[ 2: ]
		tmp2 = tmp2[ 2: ]
		cmd = f"""INSERT INTO {table} ({tmp1})
			VALUES ({tmp2});"""
		self.cursor.execute( cmd )
		self.connection.commit( )
		del tmp1
		del tmp2
		del vals
		del cmd
	def read ( self, table: str, server: str, arg: str = 'server' ) -> str:
		"""
		Read SQL data.
		:param table: Table name
		:param server: Server id
		:param arg: constraint
		:return: data retrieved.
		"""
		self.cursor.execute( f"SELECT * FROM {table} WHERE {arg}='{server}';" )
		result = self.cursor.fetchall( )
		return result[ 0 ][ 1 ]
	def update ( self, table: str, key: str, val: str, server: str ):
		"""
		Update an item in a table.
		:param table: Table name.
		:param key: Key to update
		:param val: New value of the key.
		:param server: The server id
		"""
		cmd = f"""UPDATE {table}
		SET {key}='{val}'
		WHERE server='{server}'"""
		self.cursor.execute( cmd )
		self.connection.commit( )
		del cmd
	def fmany ( self, cmd: str, num: int = 3 ) -> list:
		"""
		Returns a random result of `cmd`
		:param cmd: The command to use.
		:param num: The number of items to fetch at one time.
		:return: A random selection from 'cmd'
		"""
		self.cursor.execute( cmd )
		done = False
		results = [ ]
		while not done:
			arr = self.cursor.fetchmany( num )
			results.append( arr )
			del arr
		del done
		return random.choice( results )
	def execute ( self, cmd: str ) -> list:
		"""
		Executes a command and returns values of that command.
		:param cmd: The command to execute.
		:return: Any possible values selected in the SQL table.
		"""
		self.cursor.execute( cmd )
		return self.cursor.fetchall( )
	def close ( self ):
		"""
		Closes the SQL connection.
		"""
		self.connection.close( )
