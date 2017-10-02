from datetime import datetime, timezone
from typing import Union
from PyQt5.Qt import QSystemTrayIcon

def startswith ( *msgs: str, val: str = "" ) -> bool:
	"""
	Checks if `val` starts with any string in `msgs`.
	:param msgs: One or more strings.
	:param val: The value to check through.
	:return: True if `val` starts with one or more of the `msgs`, else False.
	"""
	for msg in msgs:
		if val.startswith( msg ): return True
		pass
	return False

def format_message ( message: str, length: int = 1000, code_block: bool = True ) -> list:
	"""
	Splits a string into several strings and returns a list.
	:param message: The string.
	:param length: The length of each string in the list. Defaults to 1,000 characters.
	:param code_block: Useful for Discord messages, True will surround the messages in ```, and False will return the message itself. Defaults to True.
	:return: A list of strings.
	"""
	if len( message ) > length: return [ (f"```{item}```" if code_block else f"{item}") for item in [ message[ i:i + length ] for i in range( 0, len( message ), length ) ] ]
	else: return [ f"```{message}```" if code_block else f"{message}" ]
	pass

def is_ascii ( message: str ) -> bool:
	"""
	Checks to see if a string has any unicode characters.
	:param message: The string to check.
	:return: True if no unicode characters exist, otherwise False
	"""
	return all( ord( c ) < 128 for c in message )

def format_time ( time_stamp: datetime ) -> datetime:
	"""
	Converts a time to your local time zone.
	:param time_stamp: datetime object
	:return: datetime object
	"""
	return time_stamp.replace( tzinfo=timezone.utc ).astimezone( tz=None )

def parse_num ( num: Union[ str, int ] ) -> str:
	"""
	Adds commas to split every three places of a number. 1000 would be 1,000.
	:param num:
	:type num:
	:return:
	:rtype:
	"""
	_num = str( num )
	_num = _num[ ::-1 ]
	_num = ','.join( [ _num[ i:i + 3 ] for i in range( 0, len( _num ), 3 ) ] )[ ::-1 ]
	return str( _num )
	pass

def replace ( message: str, *repls: tuple ) -> str:
	"""
	Replaces values in a string.
	:param message: The string.
	:param repls: One or more tuple arguments where the order is (old, new)
	:return: The new string.
	"""
	for repl in repls: message = message.replace( repl[ 0 ], repl[ 1 ] )
	return message
	pass

def notify ( header: str, body: str, sti: QSystemTrayIcon ):
	sti.showMessage( header, body )
	pass
