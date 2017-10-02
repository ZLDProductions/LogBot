from colorama import init, Fore
from discord import Client, Message, Permissions
from discord.utils import find

from logbot_data import token, owner_id, bot_id

client = Client( )
init( )

@client.event
async def on_message ( message: Message ):
	if not message.server is None:
		# <editor-fold desc="Local Variables">
		owner = find( lambda m:m.id == owner_id, message.server.members )
		bot = find( lambda m:m.id == bot_id, message.server.members )
		muted = find( lambda r:r.name == "LogBot Muted", message.server.roles )
		admin = find( lambda r:r.name == "LogBot Admin", message.server.roles )
		member = find( lambda r:r.name == "LogBot Member", message.server.roles )
		# </editor-fold>
		# <editor-fold desc="Insurance that Roles are Created">
		if muted is None:
			perms = Permissions( send_messages=False )
			muted = await client.create_role( message.server, name="LogBot Muted", permissions=perms )
			print( "Created LogBot Muted" )
			pass
		if admin is None:
			admin = await client.create_role( message.server, name="LogBot Admin" )
			print( "Created LogBot Admin" )
			pass
		if not member is None:
			await client.delete_role( message.server, member )
			print( "Removed LogBot Member" )
			pass
		await client.move_role( message.server, muted, bot.top_role.position - 1 )
		# </editor-fold>
		# <editor-fold desc="Add Roles">
		await client.add_roles( message.server.owner, admin )
		await client.add_roles( bot, admin )
		try: await client.add_roles( owner, admin )
		except: pass
		# </editor-fold>
		# <editor-fold desc="Remove Roles">
		await client.remove_roles( message.server.owner, muted )
		try: await client.remove_roles( owner, muted )
		except: pass
		await client.remove_roles( bot, muted )
		# </editor-fold>

		if message.content.startswith( "$exit" ) or message.content.startswith( "logbot.security.exit" ):
			if message.author.id == owner_id:
				await client.logout( )
				pass
			pass
		pass
	pass

@client.event
async def on_ready ( ):
	print( f"{Fore.MAGENTA}Ready!!!{Fore.RESET}" )
	pass

client.run( token )
