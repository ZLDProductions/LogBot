"""
ArgParser Tool
"""
class ArgParser( object ):
	"""
	Used to parse strings.
	"""
	def __init__ ( self, switch: str = "-", sep: str = "=" ):
		"""
		:param switch: The switch character. Defaults to '-'.
		:param sep: The separator between key and value. Defaults to '='.
		"""
		self.switch = switch
		self.sep = sep
	def parse ( self, cmd: str ):
		"""
		:param cmd: The command to parse. Uses switch and sep to parse the command.
		:return A dictionary of arguments: [switch]:[arg].
		"""
		try:
			args = { }
			for arg in cmd.split( self.switch ):
				tmp = arg.split( self.sep )
				key = tmp[ 0 ]
				tmp.remove( tmp[ 0 ] )
				tmp_arg = ' '.join( tmp )
				args[ key ] = tmp_arg
				del tmp
				del key
				del tmp_arg
			return args
		except Exception:
			return None
