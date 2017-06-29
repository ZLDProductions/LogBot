import os
import subprocess
from datetime import datetime

import discord
from colorama import Fore, init

# noinspection SpellCheckingInspection
token = 'MjU1Mzc5NzQ4ODI4NjEwNTYx.CycwfQ.c6n0jvVrV5lGbbke68dHdlYMRX0'
client = discord.Client()
init()

infos = dict({
	"_exclude"       :{
		"Info" :"Used to exclude a single message from the logs this bot creates.",
		"Usage":"$exclude \\*message\\*", "Required Permission":"LogBot Admin",
		"Alias":"$ex \\*message\\*"
	},
	"_excludechannel":{
		"Info" :"Excludes all messages in the mentioned channel(s) from the logs.",
		"Usage":"$excludechannel \\*channel_mention(s)\\*", "Required Permission":"LogBot Admin",
		"Alias":"$exc \\*channel_mention(s)\\*"
	},
	"_includechannel":{
		"Info" :"Used to remove the exclusion of mention channel(s) from the logs.",
		"Usage":"$includechannel \\*channel_mention(s)\\*", "Required Permission":"LogBot Admin",
		"Alias":"$inc \\*channel_mention(s)\\*"
	},
	"_mark"          :{
		"Info"                :"Used to set aside logs for the mentioned channel(s).",
		"Usage"               :"$mark \\*switch\\* \\*channel-mention(s)\\*",
		"Required Permissions":"LogBot Admin", "Switches":"\\*a\\* or \\*r\\*"
	},
	"_admin"         :{
		"Info"    :"Used to add, remove, or show the admins for this bot.\nServer owners are _\\*always\\*_ an admin.",
		"Usage"   :"$admin \\*switch\\* \\*mention(s)\\*", "Required Permissions":"LogBot Admin",
		"Switches":"\\*a\\*, \\*r\\*, \\*s\\*"
	},
	"_showlist"      :{
		"Info"                :"Shows the list of excluded channels.", "Usage":"$showlist",
		"Required Permissions":"LogBot Member"
	},
	"_showmarks"     :{
		"Info"                :"Shows the list of marked channels.", "Usage":"$showmarks",
		"Required Permissions":"LogBot Member"
	},
	"_help"          :{
		"Info" :"Shows the help dialog for a specific command (this), or, if no \\*command\\* was stated, shows a list of commands.",
		"Usage":"$help \\*OPTIONAL command\\*", "Required Permissions":"LogBot Member"
	},
	"_version"       :{
		"Info" :"Shows the current bot version, and what programming language it was written in.",
		"Usage":"$version", "Required Permissions":"LogBot Member"
	},
	"_channel"       :{
		"Info"                :"Creates ", "Usage":"$channel \\*switch args\\*",
		"Required Permissions":"LogBot Admin",
		"Switches"            :"new \\*type (text|voice)\\* \\*name\\* \\*permission-level (admin|member|everyone)\ndel \\*channel-mention\\*\nedit \\*new-permission-level (admin|member|everyone) \\*channel-mention\\*\nshow"
	},
	"_updates"       :{
		"Info"                :"Shows what is new with the bot.", "Usage":"$updates",
		"Required Permissions":"LogBot Member"
	},
	"_say"           :{
		"Info"                :"Sends a message in the specified channel.",
		"Usage"               :"$say \\*text\\*|\\*channel_mention\\*|\\*tts (true/false)\\*",
		"Required Permissions":"LogBot Admin"
	},
	"_member"        :{
		"Info"                :"Adds, removes, or shows the members of this bot.",
		"Usage"               :"$member \\*switch\\* \\*mention(s)\\*",
		"Required Permissions":"LogBot Admin",
		"Switches"            :"\\*a\\*, \\*r\\*, or \\*s\\*\n\\*mention(s)\\* is not required for \\*s\\*"
	},
	"_planned"       :{
		"Info"                :"Shows what may come next in the bot.", "Usage":"$planned",
		"Required Permissions":"LogBot Member"
	},
	"_cmd"           :{
		"Info"    :"Creates, removes, or shows a list of the custom commands.",
		"Usage"   :"$cmd \\*switch\\* \\*key\\*|\\*value\\*", "Required Permissions":"LogBot Member",
		"Switches":"\\*a\\*, \\*r\\*, or \\*s\\*"
	},
	"_query"         :{
		"Info"                :"Fetches information from Wolfram|Alpha", "Usage":"$query \\*query\\*",
		"Required Permissions":"LogBot Member"
	},
	"_wiki"          :{
		"Info"                :"Fetches information from Wikipedia.", "Usage":"$wiki \\*input\\*",
		"Required Permissions":"LogBot Member"
	},
	"_verse"         :{
		"Info"                :"Fetches information from the Bible.",
		"Usage"               :"$verse \\*switch OPTIONAL params\\*",
		"Required Permissions":"LogBot Member",
		"Switches"            :"\\*info [book]\\*\n\\*random\\*\n\\*help\\*\n\\*search [query]\\*"
	},
	"_disable"       :{
		"Info"                :"Disables a command.", "Usage":"$disable \\*command\\*",
		"Required Permissions":"LogBot Admin"
	},
	"_enable"        :{
		"Info"                :"Enables a command.", "Usage":"$enable \\*command\\*",
		"Required Permissions":"LogBot Admin"
	},
	"_disables"      :{
		"Info"                :"Shows the disabled commands.", "Usage":"$disables",
		"Required Permissions":"LogBot Member"
	},
	"_prunes"        :{
		"Info" :"Estimates the number of members who will be kicked by $prune \\*days\\*.",
		"Usage":"$prunes \\*number-of-days\\*", "Required Permissions":"LogBot Admin"
	},
	"_prune"         :{
		"Info" :"Kicks members who have been offline for \\*days\\*.",
		"Usage":"$prune \\*days\\*", "Required Permissions":"LogBot Admin"
	},
	"_suggest"       :{
		"Info" :"Saves a suggestion for something to change/add/fix",
		"Usage":"$suggest \\*suggestion\\*", "Required Permissions":"LogBot Member"
	},
	"_suggestions"   :{
		"Info" :"Shows suggestions received so far, unless they have been completed (and therefore removed).",
		"Usage":"$suggestions", "Required Permissions":"LogBot Member"
	},
	"_decide"        :{
		"Info"                :"Chooses a random value between the options given.",
		"Usage"               :"$decide \\*option1|option2|...\\*",
		"Required Permissions":"LogBot Member"
	},
	"_welcome"       :{
		"Info" :"Either sets the current welcome message, or shows it.",
		"Usage":"$welcome [OPTIONAL msg]", "Required Permissions":"LogBot Admin"
	},
	"_goodbye"       :{
		"Info" :"Either sets the current goodbye message, or shows it.",
		"Usage":"$goodbye [OPTIONAL msg]", "Required Permissions":"LogBot Admin"
	},
	"_user"          :{
		"Info"                :"Shows public information about a user.", "Usage":"$user \\*mention\\*",
		"Required Permissions":"LogBot Member"
	},
	"_invite"        :{
		"Info"                :"Gives you an invite link.", "Usage":"$invite",
		"Required Permissions":"None"
	},
	"_purge"         :{
		"Info"    :"Purges messages from the channel it is sent through. Restraint through \\*switch(es)\\*",
		"Usage"   :"$purge \\*OPTIONAL switch(es)\\*", "Required Permissions":"LogBot Admin",
		"Switches":"\\*limit=[num]\\*, \\*contains=[text]\\*, \\*from=[mention]\\*, \\*attached=[True/False]\\*, \\*embedded=[True/False]\\*, \\*pinned=[True/False]\\*, \\*mentions=[mention]\\*, \\*mentions_channel=[channel_mention]\\*, \\*mentions_role=[role_mention]\\*"
	},
	"_kick"          :{
		"Info"                :"Kicks the mentioned user(s)", "Usage":"$kick \\*mention(s)\\*",
		"Required Permissions":"LogBot Admin"
	},
	"_ban"           :{
		"Info" :"Bans the mentioned user(s) from the server.",
		"Usage":"$ban \\*mention(s)\\*", "Required Permissions":"LogBot Admin"
	},
	"_permissions"   :{
		"Info"                :"Shows the permissions of the user that sent it or the mentioned user, in the specified channel, if mentioned, or in the entire server.",
		"Usage"               :"$permissions \\*OPTIONAL channel-mention\\* \\*OPTIONAL user-mention\\*",
		"Required Permissions":"LogBot Member"
	},
	"_translate.get" :{
		"Info"                :"Shows the list of language codes.", "Usage":"$translate.get",
		"Required Permissions":"LogBot Member"
	},
	"_translate"     :{
		"Info"                :"Translates \\*text\\* from \\*from\\* to \\*to",
		"Usage"               :"$translate \\*from\\*|\\*to\\*|\\*text\\*",
		"Required Permissions":"LogBot Member"
	},
	"_dm"            :{
		"Info"                :"Starts a DM channel.", "Usage":"$dm",
		"Required Permissions":"LogBot Member"
	},
	"_filter"        :{
		"Info"                :"Adds, removes, or shows banned words for this server.",
		"Usage"               :"$filter \\*switch\\* \\*DEPENDENT word\\*",
		"Required Permissions":"LogBot Admin",
		"Switches"            :"\\*a \\\*word\\\*\\*\n\\*r \\\*word\\\*\\*\n\\*c\\*\n\\*s\\*"
	},
	"_convert"       :{
		"Info"    :"Converts a string to the encoded equivalent.",
		"Usage"   :"$convert \\*codec\\* [string]", "Required Permissions":"LogBot Member",
		"Switches":"\\*codec\\* can be \\*unicode\\*, \\*ascii\\*, \\*oem\\*, or \\*utf-8\\*"
	},
	"_mute"          :{
		"Info"                :"Mutes a person, deleting any and all messages sent by them in the channel the command was sent in.",
		"Usage"               :"$mute \\*mention(s)\\*",
		"Required Permissions":"LogBot Member"
	},
	"_unmute"        :{
		"Info"                :"Unmutes a person, allowing them to send a message in the channel the command was sent in.",
		"Usage"               :"$unmute \\*mention(s)\\*",
		"Required Permissions":"LogBot Member"
	},
	"_mutes"         :{
		"Info"                :"Shows the people muted in the channel.",
		"Usage"               :"$mutes",
		"Required Permissions":"LogBot Member"
	},
	"_setchannel"    :{
		"Info"                :"Sets the default channel for the daily verse.",
		"Usage"               :"$setchannel \\*channel-mention\\*",
		"Required Permissions":"LogBot Admin"
	},
	"_getchannel"    :{
		"Info"                :"Gets the default channel for the daily verse.",
		"Usage"               :"$getchannel",
		"Required Permissions":"None"
	},
	"_votd"          :{
		"Info"                :"Shows the verse of the day.",
		"Usage"               :"$votd",
		"Required Permissions":"None"
	},
	"logbot.info"    :{
		"Info"                :"Shows information on the current running instance of LogBot.",
		"Usage"               :"logbot.info",
		"Required Permissions":"LogBot Member"
	},
	"l_rank"         :{
		"Info"                :"Shows the rank of the sender, or mentioned person.",
		"Usage"               :"l$rank \\*OPTIONAL mention\\*",
		"Required Permissions":"None"
	},
	"l_levels"       :{
		"Info"                :"Shows a list of everyone in the server, sorted by their ranks. Users with rank 0 are not listed.",
		"Usage"               :"l$levels",
		"Required Permissions":"None"
	},
	"l_place"        :{
		"Info"                :"Shows your server rank.",
		"Usage"               :"l$place \\*Optional mention\\*",
		"Required Permissions":"None"
	},
	"l_buy"          :{
		"Info"                :"Purchases an item with the bot credits.",
		"Usage"               :"l$buy \\*item\\* \\*amount\\*",
		"Required Permissions":"None"
	},
	"l_shop"         :{
		"Info"                :"Shows a list of items you can buy.",
		"Usage"               :"l$shop",
		"Required Permissions":"None"
	},
	"l_gift"         :{
		"Info"                :"Sends some of your chosen \\*gift\\* to the chosen user.",
		"Usage"               :"l$gift \\*gift\\* \\*amount\\* \\*mention\\*",
		"Switches"            :"\\*gift\\* can be \\*cred\\*, \\*xp\\*, or \\*cpm\\*.",
		"Required Permissions":"None"
	},
	"l_award"        :{
		"Info"                :"Generates an award for the chosen user.",
		"Usage"               :"l$award \\*award\\* \\*amount\\* \\*mention\\*",
		"Switches"            :"\\*award\\* can be \\*cred\\*, \\*rank\\*, \\*xp\\*, or \\*cpm\\*.",
		"Required Permissions":"LogBot Admin"
	},
	"l_clear"        :{
		"Info"                :"Clears data about the user. Only do this if you are glitching out VERY badly (have too much XP, credits, etc.",
		"Usage"               :"l$clear",
		"Required Permissions":"None"
	},
	"_ping"          :{
		"Info"                :"Checks which modules, if any, are working properly.",
		"Usage"               :"$ping",
		"Required Permissions":"None"
	},
	"l_disabled"     :{
		"Info"                :"Shows if the Levels system is disabled.",
		"Usage"               :"l$disabled",
		"Required Permissions":"None"
	},
	"l_disable"      :{
		"Info"                :"Disables the Levels system, until you wish to re-enable it.",
		"Usage"               :"l$disable",
		"Required Permissions":"LogBot Admin"
	},
	"l_enable"       :{
		"Info"                :"Enables the Levels system.",
		"Usage"               :"l$enable",
		"Required Permissions":"LogBot Admin"
	},
	"v_disable"      :{
		"Info"                :"Disables verse recognition for the channel(s). If no channel is mentioned, it disables this feature for the channel in which the message was sent.",
		"Usage"               :"v$disable \\*OPTIONAL channel_mentions(s)\\*",
		"Required Permissions":"LogBot Admin"
	},
	"v_enable"       :{
		"Info"                :"Enables verse recognition for the channel(s). If no channel is mentioned, it enables this feature for the channel in which the message was sent.",
		"Usage"               :"v$enable \\*OPTIONAL channel_mention(s)\\*",
		"Required Permissions":"LogBot Admin"
	},
	"v_disables"     :{
		"Info"                :"Shows a list of the channels in this server where verse recognition is disabled.",
		"Usage"               :"v$disables",
		"Required Permissions":"None"
	},
	"g_rps"          :{
		"Info"                :"Plays a game of rock paper scissors.",
		"Usage"               :"g$rps \\*choice\\*",
		"Required Permissions":"None"
	},
	"g_rpsls"        :{
		"Info"                :"Plays a game of rock paper scissors lizard Spock.",
		"Usage"               :"g$rpsls \\*choice\\*",
		"Required Permissions":"None"
	},
	"g_rules"        :{
		"Info"                :"Shows rules for a game.",
		"Usage"               :"g$rpsls \\*game\\*",
		"Games"               :"Currently, only set up for \\*rps\\* and \\*rpsls\\*.",
		"Required Permissions":"None"
	},
	"p_start"        :{
		"Info"                :"Starts a vote and returns the vote_index.",
		"Usage"               :"p$start \\*vote_name\\*|\\*choice1\\*|\\*choice2\\*|\\*choice3\\*|...",
		"Required Permissions":"LogBot Admin"
	},
	"p_end"          :{
		"Info"                :"Ends a vote and returns the results.",
		"Usage"               :"p$end \\*vote_index\\*",
		"Required Permissions":"LogBot Admin"
	},
	"p_status"       :{
		"Info"                :"Shows the status of a vote.",
		"Usage"               :"p$status \\*vote_index\\*",
		"Required Permissions":"None"
	},
	"p_vote"         :{
		"Info"                :"Votes for a choice.",
		"Usage"               :"p$vote \\*vote_index\\* \\*choice_index\\*",
		"Required Permissions":"None"
	},
	"p_polls"        :{
		"Info"                :"Shows existing votes and their indices.",
		"Usage"               :"p$polls",
		"Required Permissions":"None"
	},
	"p_save"         :{
		"Info"                :"Saves a poll for later use.",
		"Usage"               :"p$save \\*topic_index\\*",
		"Required Permissions":"LogBot Admin"
	},
	"p_view"         :{
		"Info"                :"Views a specific saved poll.",
		"Usage"               :"p$view \\*poll_index\\*",
		"Required Permissions":"LogBot Admin"
	},
	"p_remove"       :{
		"Info"                :"Removes a saved poll from the database.",
		"Usage"               :"p$remove \\*poll_index\\*",
		"Required Permissions":"LogBot Admin"
	},
	"p_saved"        :{
		"Info"                :"Shows saved polls.",
		"Usage"               :"p$saved",
		"Required Permissions":"LogBot Admin"
	},
	"l_dm"           :{
		"Info"                :"Sets whether or not to send level/tier up notifications in DM or server channel.",
		"Usage"               :"l$dm \\*t/f\\*",
		"Required Permissions":"None"
	},
	"_setversion"    :{
		"Info"                :"Set the bible version.",
		"Usage"               :"$setversion \\*version\\*",
		"Versions"            :"\\*kjv\\*, \\*akjv\\*, \\*web\\*",
		"Required Permissions":"None"
	},
	"_settype"       :{
		"Info"                :"Sets the type of bible verses.",
		"Usage"               :"$settype \\*embed/text\\*",
		"Required Permissions":"None"
	},
	"a_clear"        :{
		"Info"                :"Deletes all messages (in this instance of the bot) sent in the same channel as the command message.",
		"Usage"               :"a$clear",
		"Required Permissions":"LogBot Admin"
	},
	"_hq"            :{
		"Info"                :"Sends the LogBot HQ Instant Invite Link through chat.",
		"Usage"               :"$hq",
		"Required Permissions":"None"
	},
	"_fetch"         :{
		"Info"                :"Fetches the logs for a channel in a server.",
		"Usage"               :"$fetch \\*channel-name\\*\n$fetch event",
		"Required Permissions":"LogBot Admin"
	},
	"h_prefix"       :{
		"Info"                :"Much like $help, this command will either show a list of prefixes (if no prefix parameter is present), or the plugin for the provided prefix.",
		"Usage"               :"h$prefix\nh$prefix \\*prefix\\*",
		"Required Permissions":"None"
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
		myembed = discord.Embed(title=content, description=f"Command Information for {content}", colour=discord.Colour.dark_gold())
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
