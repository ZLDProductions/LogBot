import os
import subprocess
from datetime import datetime

import discord
from colorama import Fore, init

from logbot_data import token

client = discord.Client()
init()

key = """
[] - optional parameter
{} - required parameter
{name: [choices]} - required parameter with possible choices.
[name: [choices]} - optional parameter with possible choices.
"""

infos = dict({
	"_exclude"       :{
		"Info"               :"Used to exclude a single message from the logs this bot creates.",
		"Usage"              :"$exclude {message}\n$ex {message}",
		"Required Permission":"LogBot Admin",
		"Type"               :"Logging"
	},
	"_excludechannel":{
		"Info"               :"Excludes all messages in the mentioned channel(s) from the logs.",
		"Usage"              :"$excludechannel {channel_mention(s)}\n$exc {channel_mention(s)}",
		"Required Permission":"LogBot Admin",
		"Type"               :"Logging"
	},
	"_includechannel":{
		"Info"               :"Used to remove the exclusion of mention channel(s) from the logs.",
		"Usage"              :"$includechannel {channel_mention(s)}\n$inc {channel_mention(s)}",
		"Required Permission":"LogBot Admin",
		"Type"               :"Logging"
	},
	"_mark"          :{
		"Info"                :"Used to set aside logs for the mentioned channel(s).",
		"Usage"               :"$mark a {channel-mention(s)}\n$mark r {channel_mention(s)}",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Logging"
	},
	"_admin"         :{
		"Info"                :"Used to add, remove, or show the admins for this bot.\nServer owners are _\\*always\\*_ an admin.",
		"Usage"               :"$admin a {mention(s)}\n$admin r {mention(s)}\n$admin s",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Moderation"
	},
	"_showlist"      :{
		"Info"                :"Shows the list of excluded channels.",
		"Usage"               :"$showlist",
		"Required Permissions":"LogBot Member",
		"Type"                :"Logging"
	},
	"_showmarks"     :{
		"Info"                :"Shows the list of marked channels.",
		"Usage"               :"$showmarks",
		"Required Permissions":"LogBot Member",
		"Type"                :"Logging"
	},
	"_help"          :{
		"Info"                :"Shows the help dialog for a specific command (this), or, if no [command] was stated, shows a list of commands.",
		"Usage"               :"$help [command]",
		"Required Permissions":"LogBot Member",
		"Type"                :"Help"
	},
	"_version"       :{
		"Info"                :"Shows the current bot version, and what programming language it was written in.",
		"Usage"               :"$version",
		"Required Permissions":"LogBot Member",
		"Type"                :"Stats"
	},
	"_channel"       :{
		"Info"                :"Creates a channel, edits a channel, shows a list of channels created by the bot, or deletes a bot-created channel.",
		"Usage"               :"$channel new {type: [text/voice]} {name} {permission level: [admin/member/everyone]}\n$channel del {channel mention or name}\n$channel edit {new permission level: [admin/member/everyone]} {channel mention or name}\n$channel show",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Utility"
	},
	"_updates"       :{
		"Info"                :"Shows what is new with the bot.",
		"Usage"               :"$updates",
		"Required Permissions":"LogBot Member",
		"Type"                :"Stats"
	},
	"_say"           :{
		"Info"                :"Sends a message in the specified channel.",
		"Usage"               :"$say {text}|{channel_mention}|{tts [True/False]}",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Fun"
	},
	"_member"        :{
		"Info"                :"Adds, removes, or shows the members of this bot.",
		"Usage"               :"$member a {mention(s)}\n$member r {mention(s)}\n$member s",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Moderation"
	},
	"_planned"       :{
		"Info"                :"Shows what may come next in the bot.",
		"Usage"               :"$planned",
		"Required Permissions":"LogBot Member",
		"Type"                :"Stats"
	},
	"_cmd"           :{
		"Info"                :"Creates, removes, or shows a list of the custom commands.",
		"Usage"               :"$cmd a {key}|{value}\n$cmd r {key}\n$cmd s",
		"Required Permissions":"LogBot Member",
		"Type"                :"Fun"
	},
	"_query"         :{
		"Info"                :"Fetches information from Wolfram|Alpha",
		"Usage"               :"$query {query}",
		"Required Permissions":"LogBot Member",
		"Type"                :"Fun"
	},
	"_wiki"          :{
		"Info"                :"Fetches information from Wikipedia.",
		"Usage"               :"$wiki {input}",
		"Required Permissions":"LogBot Member",
		"Type"                :"Fun"
	},
	"_verse"         :{
		"Info"                :"Fetches information from the Bible.",
		"Usage"               :"$verse info {book}\n$verse random\n$verse help\n$verse search {query}",
		"Required Permissions":"LogBot Member",
		"Type"                :"Fun"
	},
	"_disable"       :{
		"Info"                :"Disables a command.",
		"Usage"               :"$disable {command}",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Moderation"
	},
	"_enable"        :{
		"Info"                :"Enables a command.",
		"Usage"               :"$enable {command}",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Moderation"
	},
	"_disables"      :{
		"Info"                :"Shows the disabled commands.",
		"Usage"               :"$disables",
		"Required Permissions":"LogBot Member",
		"Type"                :"Moderation"
	},
	"_prunes"        :{
		"Info"                :"Estimates the number of members who will be kicked by $prune {days}.",
		"Usage"               :"$prunes {days}",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Moderation"
	},
	"_prune"         :{
		"Info"                :"Kicks members who have been offline for {days}.",
		"Usage"               :"$prune {days}",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Moderation"
	},
	"_suggest"       :{
		"Info"                :"Saves a suggestion for me.",
		"Usage"               :"$suggest {suggestion}",
		"Required Permissions":"LogBot Member",
		"Type"                :"Feedback"
	},
	"_suggestions"   :{
		"Info"                :"Shows suggestions received so far, unless they have been completed (and therefore removed).",
		"Usage"               :"$suggestions",
		"Required Permissions":"Owner",
		"Type"                :"Feedback"
	},
	"_decide"        :{
		"Info"                :"Chooses a random value between the options given.",
		"Usage"               :"$decide {option1|option2|...}",
		"Required Permissions":"LogBot Member",
		"Type"                :"Fun"
	},
	"_welcome"       :{
		"Info"                :"Either sets the current welcome message, or shows it.",
		"Usage"               :"$welcome [msg]",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Utility"
	},
	"_goodbye"       :{
		"Info"                :"Either sets the current goodbye message, or shows it.",
		"Usage"               :"$goodbye [msg]",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Utility"
	},
	"_user"          :{
		"Info"                :"Shows public information about a user.",
		"Usage"               :"$user {mention}",
		"Required Permissions":"LogBot Member",
		"Type"                :"Fun"
	},
	"_invite"        :{
		"Info"                :"Gives you an invite link.",
		"Usage"               :"$invite",
		"Required Permissions":"None",
		"Type"                :"Utility"
	},
	"_purge"         :{
		"Info"                :"Purges messages from the channel it is sent through. Restraint through the switches.",
		"Usage"               :"$purge [switches]",
		"Required Permissions":"LogBot Admin",
		"Switches"            :"{limit=[num]}, {contains=[text]}, {from=[mention]}, {attached=[True/False]}, {embedded=[True/False]}, {pinned=[True/False]}, {mentions=[mention]}, {mentions_channel=[channel_mention]}, {mentions_role=[role_mention]}",
		"Type"                :"Moderation"
	},
	"_kick"          :{
		"Info"                :"Kicks the mentioned user(s)",
		"Usage"               :"$kick {mention(s)}",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Moderation"
	},
	"_ban"           :{
		"Info"                :"Bans the mentioned user(s) from the server.",
		"Usage"               :"$ban {mention(s)}",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Moderation"
	},
	"_permissions"   :{
		"Info"                :"Shows the permissions of the user that sent it or the mentioned user, in the specified channel, if mentioned, or in the entire server.",
		"Usage"               :"$permissions [channel-mention] [user-mention]",
		"Required Permissions":"LogBot Member",
		"Type"                :"Fun"
	},
	"_translate.get" :{
		"Info"                :"Shows the list of language codes.",
		"Usage"               :"$translate.get",
		"Required Permissions":"LogBot Member",
		"Type"                :"Fun"
	},
	"_translate"     :{
		"Info"                :"Translates {text} from {from} to {to}",
		"Usage"               :"$translate {from}|{to}|{text}",
		"Required Permissions":"LogBot Member",
		"Type"                :"Fun"
	},
	"_dm"            :{
		"Info"                :"Starts a DM channel.",
		"Usage"               :"$dm",
		"Required Permissions":"LogBot Member",
		"Type"                :"Utility"
	},
	"_filter"        :{
		"Info"                :"Adds, removes, or shows banned words for this server.",
		"Usage"               :"$filter a {word}\n$filter r {word}\n$filter c\n$filter s",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Moderation"
	},
	"_convert"       :{
		"Info"                :"Converts a string to the encoded equivalent.",
		"Usage"               :"$convert {codec: [unicode/ascii/oem/utf-8]} {string}",
		"Required Permissions":"LogBot Member",
		"Type"                :"Fun"
	},
	"_mute"          :{
		"Info"                :"Mutes a person, deleting any and all messages sent by them in the channel the command was sent in.",
		"Usage"               :"$mute {mention(s)}",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Moderation"
	},
	"_unmute"        :{
		"Info"                :"Unmutes a person, allowing them to send a message in the channel the command was sent in.",
		"Usage"               :"$unmute {mention(s)}",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Moderation"
	},
	"_mutes"         :{
		"Info"                :"Shows the people muted in the channel.",
		"Usage"               :"$mutes",
		"Required Permissions":"LogBot Member",
		"Type"                :"Moderation"
	},
	"_setchannel"    :{
		"Info"                :"Sets the default channel for the daily verse.",
		"Usage"               :"$setchannel [channel-mention]",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Fun"
	},
	"_getchannel"    :{
		"Info"                :"Gets the default channel for the daily verse.",
		"Usage"               :"$getchannel",
		"Required Permissions":"None",
		"Type"                :"Fun"
	},
	"_votd"          :{
		"Info"                :"Shows the verse of the day.",
		"Usage"               :"$votd",
		"Required Permissions":"None",
		"Type"                :"Fun"
	},
	"logbot.info"    :{
		"Info"                :"Shows information on the current running instance of LogBot.",
		"Usage"               :"logbot.info",
		"Required Permissions":"LogBot Member",
		"Type"                :"Stats"
	},
	"l_rank"         :{
		"Info"                :"Shows the rank of the sender, or mentioned person.",
		"Usage"               :"l$rank [mention]",
		"Required Permissions":"None",
		"Type"                :"Fun"
	},
	"l_levels"       :{
		"Info"                :"Shows a list of everyone in the server, sorted by their ranks. Users with rank 0 are not listed.",
		"Usage"               :"l$levels",
		"Required Permissions":"None",
		"Type"                :"Fun"
	},
	"l_place"        :{
		"Info"                :"Shows your server rank.",
		"Usage"               :"l$place [mention]",
		"Required Permissions":"None",
		"Type"                :"Fun"
	},
	"l_buy"          :{
		"Info"                :"Purchases an item with the bot credits.",
		"Usage"               :"l$buy {item} [amount]",
		"Required Permissions":"None",
		"Type"                :"Fun"
	},
	"l_shop"         :{
		"Info"                :"Shows a list of items you can buy.",
		"Usage"               :"l$shop",
		"Required Permissions":"None",
		"Type"                :"Fun"
	},
	"l_gift"         :{
		"Info"                :"Sends some of your chosen {gift} to the chosen user.",
		"Usage"               :"l$gift {gift: [cred/xp/cpm/mul]} {amount} {mention}",
		"Required Permissions":"None",
		"Type"                :"Fun"
	},
	"l_award"        :{
		"Info"                :"Generates an award for the chosen user.",
		"Usage"               :"l$award {award: [cred/rank/xp/cpm/tier]} {amount} {mention}",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Fun"
	},
	"_ping"          :{
		"Info"                :"Checks which modules, if any, are working properly.",
		"Usage"               :"$ping",
		"Required Permissions":"None",
		"Type"                :"Utility"
	},
	"l_disabled"     :{
		"Info"                :"Shows if the Levels system is disabled.",
		"Usage"               :"l$disabled",
		"Required Permissions":"None",
		"Type"                :"Moderation"
	},
	"l_disable"      :{
		"Info"                :"Disables the Levels system, until you wish to re-enable it.",
		"Usage"               :"l$disable",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Moderation"
	},
	"l_enable"       :{
		"Info"                :"Enables the Levels system.",
		"Usage"               :"l$enable",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Moderation"
	},
	"v_disable"      :{
		"Info"                :"Disables verse recognition for the channel(s). If no channel is mentioned, it disables this feature for the channel in which the message was sent.",
		"Usage"               :"v$disable [channel_mentions(s)]",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Moderation"
	},
	"v_enable"       :{
		"Info"                :"Enables verse recognition for the channel(s). If no channel is mentioned, it enables this feature for the channel in which the message was sent.",
		"Usage"               :"v$enable [channel_mention(s)]",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Moderation"
	},
	"v_disables"     :{
		"Info"                :"Shows a list of the channels in this server where verse recognition is disabled.",
		"Usage"               :"v$disables",
		"Required Permissions":"None",
		"Type"                :"Moderation"
	},
	"g_rps"          :{
		"Info"                :"Plays a game of rock paper scissors.",
		"Usage"               :"g$rps {choice: [rock/paper/scissors]}",
		"Required Permissions":"None",
		"Type"                :"Fun"
	},
	"g_rpsls"        :{
		"Info"                :"Plays a game of rock paper scissors lizard Spock.",
		"Usage"               :"g$rpsls {choice: [rock/paper/scissors/lizard/Spock]}",
		"Required Permissions":"None",
		"Type"                :"Fun"
	},
	"g_rules"        :{
		"Info"                :"Shows rules for a game.",
		"Usage"               :"g$rules {game: [rps/rpsls/scramble]}",
		"Required Permissions":"None",
		"Type"                :"Fun"
	},
	"p_start"        :{
		"Info"                :"Starts a vote and returns the vote_index.",
		"Usage"               :"p$start {vote_name}|{choices: [1]|[2]|[3]|[4]|[...]}",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Feedback"
	},
	"p_end"          :{
		"Info"                :"Ends a vote and returns the results.",
		"Usage"               :"p$end {vote_index}",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Feedback"
	},
	"p_status"       :{
		"Info"                :"Shows the status of a vote.",
		"Usage"               :"p$status {vote_index}",
		"Required Permissions":"None",
		"Type"                :"Feedback"
	},
	"p_vote"         :{
		"Info"                :"Votes for a choice.",
		"Usage"               :"p$vote {vote_index} {choice_index}",
		"Required Permissions":"None",
		"Type"                :"Feedback"
	},
	"p_polls"        :{
		"Info"                :"Shows existing votes and their indices.",
		"Usage"               :"p$polls",
		"Required Permissions":"None",
		"Type"                :"Feedback"
	},
	"p_save"         :{
		"Info"                :"Saves a poll for later use.",
		"Usage"               :"p$save {topic_index}",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Feedback"
	},
	"p_view"         :{
		"Info"                :"Views a specific saved poll.",
		"Usage"               :"p$view {poll_index}",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Feedback"
	},
	"p_remove"       :{
		"Info"                :"Removes a saved poll from the database.",
		"Usage"               :"p$remove {poll_index}",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Feedback"
	},
	"p_saved"        :{
		"Info"                :"Shows saved polls.",
		"Usage"               :"p$saved",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Feedback"
	},
	"l_dm"           :{
		"Info"                :"Sets whether or not to send level/tier up notifications in DM or server channel.",
		"Usage"               :"l$dm {val: [t/f]}",
		"Required Permissions":"None",
		"Type"                :"Fun"
	},
	"_setversion"    :{
		"Info"                :"Set the bible version.",
		"Usage"               :"$setversion {version: [kjv/akjv/web]}",
		"Required Permissions":"None",
		"Type"                :"Fun"
	},
	"_settype"       :{
		"Info"                :"Sets the type of bible verses.",
		"Usage"               :"$settype {type: [embed/text]}",
		"Required Permissions":"None",
		"Type"                :"Fun"
	},
	"a_clear"        :{
		"Info"                :"Deletes all messages (in this instance of the bot) sent in the same channel as the command message.",
		"Usage"               :"a$clear",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Moderation"
	},
	"_hq"            :{
		"Info"                :"Sends the LogBot HQ Instant Invite Link through chat.",
		"Usage"               :"$hq",
		"Required Permissions":"None",
		"Type"                :"Utility"
	},
	"_fetch"         :{
		"Info"                :"Fetches the logs for a channel in a server.",
		"Usage"               :"$fetch {channel-name}\n$fetch event",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Logging"
	},
	"h_prefix"       :{
		"Info"                :"Much like $help, this command will either show a list of prefixes (if no prefix parameter is present), or the plugin for the provided prefix.",
		"Usage"               :"h$prefix [prefix]",
		"Required Permissions":"None",
		"Type"                :"Help"
	},
	"_joinrole"      :{
		"Info"                :"Gets or sets the join role.",
		"Usage"               :"$joinrole [role]",
		"Required Permissions":"LogBot Admin/Member",
		"Type"                :"Moderation"
	},
	"_git"           :{
		"Info"                :"Shows a link to the GitHub repo for this bot.",
		"Usage"               :"$git",
		"Required Permissions":"None",
		"Type"                :"Utility"
	},
	"_guess"         :{
		"Info"                :"Take a guess at what the scrambled word is.",
		"Usage"               :"$guess {word}",
		"Required Permissions":"None",
		"Type"                :"Fun"
	},
	"_scramble"      :{
		"Info"                :"Adds a word, removes a word, searches for a word, lists all words, or starts a word scramble (respectively).",
		"Usage"               :"$scramble add {word}\n$scramble rem {word}\n$scramble find {word}\n$scramble list\n$scramble",
		"Required Permissions":"LogBot Member",
		"Type"                :"Fun"
	},
	"_giveup"        :{
		"Info"                :"Gives up a word scramble.",
		"Usage"               :"$giveup",
		"Required Permissions":"None",
		"Type"                :"Fun"
	},
	"l_alert"        :{
		"Info"                :"Sets which channel you will be alerted in when DM is OFF.",
		"Usage"               :"l$alert {channel}",
		"Required Permissions":"None",
		"Type"                :"Fun"
	},
	"_logchannel"    :{
		"Info"                :"Gets or sets the logchannel for the server.",
		"Usage"               :"$logchannel [channel-mention]",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Logging"
	},
	"_roll"          :{
		"Info"                :"Rolls a random number between 1 and 6.",
		"$roll"               :"$roll",
		"Required Permissions":"None",
		"Type"                :"Fun"
	},
	"_channels"      :{
		"Info"                :"Shows a list of all voice and text channels in a server.",
		"Usage"               :"$channels",
		"Required Permissions":"LogBot Member",
		"Type"                :"Fun"
	},
	"_devotional"    :{
		"Error":"Since the help content is too large to display properly, please use the documentation on github (use `$git`)",
	},
	"l_milestone"    :{
		"Info"                :"Adds to, removes from, or shows the milestones in the levels system.",
		"Usage"               :"l$milestone a {item: [tier/rank]} {limit} {role_mention}\nl$milestone r {item: [tier/rank]} {limit} {role_mention}\nl$milestone s",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Utility"
	},
	"l$slots"        :{
		"Info"                :"Plays slots or shows the slots rules.",
		"Usage"               :"l$slots {bid}\nl$slots",
		"Required Permissions":"None",
		"Type"                :"Fun"
	}
})
prefixes = {
	"a$":"Admin Plugin",
	"v$":"Bible Plugin",
	"g$":"Games Plugin",
	"l$":"Levels Plugin",
	"$" :"Main",
	"p$":"Polling Plugin",
	"h$":"Help Plugin"
}

@client.event
async def on_ready():
	await client.change_presence(game=None)
	os.system("cls")
	print(f"{Fore.MAGENTA}Ready!!!{Fore.RESET}")
	pass

@client.event
async def on_message(message):
	# noinspection PyUnusedLocal
	def replace(*args, val=message.content):
		_replace = val.replace
		for reg, rep in args: val = _replace(reg, rep)
		return val
	def startswith(*args, val=message.content):
		for arg in args:
			if val.startswith(arg): return True
			pass
		return False
		pass
	owner_id = "239500860336373761"
	do_update = False

	if startswith(f"$help "):
		content = message.content.replace(f"$help ", "", 1)
		myembed = discord.Embed(title=content, description=f"Command Information for {content}\n{key}", colour=discord.Colour.dark_gold())
		items = {}
		for item in infos.keys():
			if item.replace("_", "") == content.replace("$", ""): items = infos[item]
			pass
		for item in list(items.keys()): myembed.add_field(name=item, value=items[item])
		if not len(items.keys()) == 0: await client.send_message(message.channel, "Here you go!", embed=myembed)
		else: await client.send_message(message.channel, f"```There is no command for {content} at this time.```")
		del content
		del myembed
		del items
		pass
	elif startswith(f"$help"):
		all_commands = list(infos.keys())
		all_commands.sort()
		all_commands = ', '.join(all_commands).replace("_", "$")
		await client.send_message(message.channel, f"```Commands:\n{all_commands}```")
		pass
	elif startswith(f"h$prefix "):
		prefix = message.content.replace("h$prefix ", "")
		data = prefixes.get(prefix)
		if data is None:
			await client.send_message(message.channel, f"```There is no prefix \"{prefix}\"")
			pass
		else:
			e = discord.Embed(title=prefix, description=f"Prefix Information for {prefix}", colour=discord.Colour.dark_gold()) \
				.add_field(name="Plugin", value=data)
			await client.send_message(message.channel, "Here you go!", embed=e)
			del e
			pass
		del prefix
		del data
		pass
	elif startswith(f"h$prefix"):
		prefs = list(prefixes.keys())
		prefs.sort()
		await client.send_message(message.channel, f"```{', '.join(prefs)}```")
		del prefs
		pass
	elif startswith(f"$update", "logbot.help.update"):
		if message.author.id == owner_id: do_update = True
		pass
	elif startswith("logbot.settings exit", "logbot.help.exit"):
		if message.author.id == owner_id: exit(0)
		pass
	elif startswith(f"$ping"):
		tm = datetime.now() - message.timestamp
		await client.send_message(message.channel, f"```LogBot Help Online ~ {round(tm.microseconds / 1000)}```")
		pass

	if do_update:
		print(f"{Fore.LIGHTCYAN_EX}Updating...{Fore.RESET}")
		await client.close()
		subprocess.Popen(f"python {os.getcwd()}\\help.py", False)
		exit(0)
		pass
	pass

client.run(token)
