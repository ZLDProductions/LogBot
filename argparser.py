class ArgParser( object ):
	def __init__ ( self, switch: str = "-", sep: str = "=" ):
		"""
		:param switch: The switch character. Defaults to '-'.
		:param sep: The separator between key and value. Defaults to '='.
		"""
		self.switch = switch
		self.sep = sep
		pass
	def parse ( self, cmd: str ):
		"""
		:param cmd: The command to parse. Uses switch and sep to parse the command.
		:return A dictionary of arguments. [switch]:[arg]. If there is no switches in the command, returns None.
		"""
		try:
			args = { }
			for arg in cmd.split( self.switch ):
				tmp = arg.split( self.sep )
				key = tmp[ 0 ]
				tmp.remove( tmp[ 0 ] )
				tmp_arg = ' '.join( tmp )
				args[ key ] = tmp_arg
				pass
			return args
		except: return None
		pass
