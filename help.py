import os
import subprocess
from datetime import datetime

import discord
import sqlite3
from colorama import Fore, init

from logbot_data import token

client = discord.Client( )
init( )

key = """
[] - optional parameter
{} - required parameter
{name: [choices]} - required parameter with possible choices.
[name: [choices]} - optional parameter with possible choices.
"""

infos = dict( {
	"_exclude"       :{
		"Info"               :"Used to exclude a single message from the logs this bot creates.",
		"Usage"              :"$exclude {message}\n$ex {message}",
		"Required Permission":"LogBot Admin",
		"Type"               :"Logging",
		"Plugin"             :"Main"
	},
	"_excludechannel":{
		"Info"               :"Excludes all messages in the mentioned channel(s) from the logs.",
		"Usage"              :"$excludechannel {channel_mention(s)}\n$exc {channel_mention(s)}",
		"Required Permission":"LogBot Admin",
		"Type"               :"Logging",
		"Plugin"             :"Main"
	},
	"_includechannel":{
		"Info"               :"Used to remove the exclusion of mention channel(s) from the logs.",
		"Usage"              :"$includechannel {channel_mention(s)}\n$inc {channel_mention(s)}",
		"Required Permission":"LogBot Admin",
		"Type"               :"Logging",
		"Plugin"             :"Main"
	},
	"_mark"          :{
		"Info"                :"Used to set aside logs for the mentioned channel(s).",
		"Usage"               :"$mark a {channel-mention(s)}\n$mark r {channel_mention(s)}",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Logging",
		"Plugin"              :"Main"
	},
	"_admin"         :{
		"Info"                :"Used to add, remove, or show the admins for this bot.\nServer owners are _\\*always\\*_ an admin.",
		"Usage"               :"$admin a {mention(s)}\n$admin r {mention(s)}\n$admin s",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Moderation",
		"Plugin"              :"Main"
	},
	"_showlist"      :{
		"Info"                :"Shows the list of excluded channels.",
		"Usage"               :"$showlist",
		"Required Permissions":"LogBot Member",
		"Type"                :"Logging",
		"Plugin"              :"Main"
	},
	"_showmarks"     :{
		"Info"                :"Shows the list of marked channels.",
		"Usage"               :"$showmarks",
		"Required Permissions":"LogBot Member",
		"Type"                :"Logging",
		"Plugin"              :"Main"
	},
	"_help"          :{
		"Info"                :"Shows the help dialog for a specific command (this), or, if no [command] was stated, shows a list of commands. Adding `&GroupByType` or `&GroupByPlugin` changes the format of the command list.",
		"Usage"               :"$help[group: [&GroupByType/&GroupByPlugin]] [command]",
		"Required Permissions":"LogBot Member",
		"Type"                :"Help",
		"Plugin"              :"Help"
	},
	"_version"       :{
		"Info"                :"Shows the current bot version, and what programming language it was written in.",
		"Usage"               :"$version",
		"Required Permissions":"LogBot Member",
		"Type"                :"Stats",
		"Plugin"              :"Main"
	},
	"_channel"       :{
		"Info"                :"Creates a channel, edits a channel, shows a list of channels created by the bot, or deletes a bot-created channel.",
		"Usage"               :"$channel new {type: [text/voice]} {name} {permission level: [admin/member/everyone]}\n$channel del {channel mention or name}\n$channel edit {new permission level: [admin/member/everyone]} {channel mention or name}\n$channel show",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Utility",
		"Plugin"              :"Main"
	},
	"_updates"       :{
		"Info"                :"Shows what is new with the bot.",
		"Usage"               :"$updates",
		"Required Permissions":"LogBot Member",
		"Type"                :"Stats",
		"Plugin"              :"Main"
	},
	"_say"           :{
		"Info"                :"Sends a message in the specified channel.",
		"Usage"               :"$say {channel_mentions}|{text}",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Fun",
		"Plugin"              :"Main"
	},
	"_member"        :{
		"Info"                :"Adds, removes, or shows the members of this bot.",
		"Usage"               :"$member a {mention(s)}\n$member r {mention(s)}\n$member s",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Moderation",
		"Plugin"              :"Main"
	},
	"_planned"       :{
		"Info"                :"Shows what may come next in the bot.",
		"Usage"               :"$planned",
		"Required Permissions":"LogBot Member",
		"Type"                :"Stats",
		"Plugin"              :"Main"
	},
	"_cmd"           :{
		"Info"                :"Creates, removes, or shows a list of the custom commands.",
		"Usage"               :"$cmd a {key}|{value}\n$cmd r {key}\n$cmd s",
		"Required Permissions":"LogBot Member",
		"Type"                :"Fun",
		"Plugin"              :"Main"
	},
	"_query"         :{
		"Info"                :"Fetches information from Wolfram|Alpha",
		"Usage"               :"$query {query}",
		"Required Permissions":"LogBot Member",
		"Type"                :"Fun",
		"Plugin"              :"Main"
	},
	"_wiki"          :{
		"Info"                :"Fetches information from Wikipedia.",
		"Usage"               :"$wiki {input}",
		"Required Permissions":"LogBot Member",
		"Type"                :"Fun",
		"Plugin"              :"Main"
	},
	"_verse"         :{
		"Info"                :"Fetches information from the Bible.",
		"Usage"               :"$verse info:book {book}\n$verse info:chapter {book} {chapter}\n$verse info:verse {book} {chapter}:{verse}\n$verse random\n$verse help\n$verse search {query}",
		"Required Permissions":"LogBot Member",
		"Type"                :"Fun",
		"Plugin"              :"Bible"
	},
	"_disable"       :{
		"Info"                :"Disables a command.",
		"Usage"               :"$disable {command}",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Moderation",
		"Plugin"              :"Main"
	},
	"_enable"        :{
		"Info"                :"Enables a command.",
		"Usage"               :"$enable {command}",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Moderation",
		"Plugin"              :"Main"
	},
	"_disables"      :{
		"Info"                :"Shows the disabled commands.",
		"Usage"               :"$disables",
		"Required Permissions":"LogBot Member",
		"Type"                :"Moderation",
		"Plugin"              :"Main"
	},
	"_prunes"        :{
		"Info"                :"Estimates the number of members who will be kicked by $prune {days}.",
		"Usage"               :"$prunes {days}",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Moderation",
		"Plugin"              :"Main"
	},
	"_prune"         :{
		"Info"                :"Kicks members who have been offline for {days}.",
		"Usage"               :"$prune {days}",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Moderation",
		"Plugin"              :"Main"
	},
	"_suggest"       :{
		"Info"                :"Saves a suggestion for me.",
		"Usage"               :"$suggest {suggestion}",
		"Required Permissions":"LogBot Member",
		"Type"                :"Feedback",
		"Plugin"              :"Dev"
	},
	"_suggestions"   :{
		"Info"                :"Shows suggestions received so far, unless they have been completed (and therefore removed).",
		"Usage"               :"$suggestions",
		"Required Permissions":"Owner",
		"Type"                :"Feedback",
		"Plugin"              :"Dev"
	},
	"_decide"        :{
		"Info"                :"Chooses a random value between the options given.",
		"Usage"               :"$decide {option1|option2|...}",
		"Required Permissions":"LogBot Member",
		"Type"                :"Fun",
		"Plugin"              :"Main"
	},
	"_welcome"       :{
		"Info"                :"Either sets the current welcome message, or shows it.",
		"Usage"               :"$welcome [msg]",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Utility",
		"Plugin"              :"Main"
	},
	"_goodbye"       :{
		"Info"                :"Either sets the current goodbye message, or shows it.",
		"Usage"               :"$goodbye [msg]",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Utility",
		"Plugin"              :"Main"
	},
	"_user"          :{
		"Info"                :"Shows public information about a user.",
		"Usage"               :"$user {mention}",
		"Required Permissions":"LogBot Member",
		"Type"                :"Fun",
		"Plugin"              :"Main"
	},
	"_invite"        :{
		"Info"                :"Gives you an invite link.",
		"Usage"               :"$invite",
		"Required Permissions":"None",
		"Type"                :"Utility",
		"Plugin"              :"Main"
	},
	"_purge"         :{
		"Info"                :"Purges messages from the channel it is sent through. Restraint through the switches. If switches are present, and there is a problem, the bot will delete the trigger.",
		"Usage"               :"$purge limit=[num]&&contains=[text]&&from=[mention]&&attached=[True/False]&&embedded=[True/False]&&pinned=[True/False]&&mentions=[mention]&&mentions_channel=[channel_mention]&&mentions_role=[role_mention]",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Moderation",
		"Plugin"              :"Main"
	},
	"_kick"          :{
		"Info"                :"Kicks the mentioned user(s)",
		"Usage"               :"$kick {mention(s)}",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Moderation",
		"Plugin"              :"Main"
	},
	"_ban"           :{
		"Info"                :"Bans the mentioned user(s) from the server.",
		"Usage"               :"$ban {mention(s)}",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Moderation",
		"Plugin"              :"Main"
	},
	"_permissions"   :{
		"Info"                :"Shows the permissions of the user that sent it or the mentioned user, in the specified channel, if mentioned, or in the entire server.",
		"Usage"               :"$permissions [channel-mention] [user-mention]",
		"Required Permissions":"LogBot Member",
		"Type"                :"Fun",
		"Plugin"              :"Main"
	},
	"_translate.get" :{
		"Info"                :"Shows the list of language codes.",
		"Usage"               :"$translate.get",
		"Required Permissions":"LogBot Member",
		"Type"                :"Fun",
		"Plugin"              :"Main"
	},
	"_translate"     :{
		"Info"                :"Translates {text} from {from} to {to}",
		"Usage"               :"$translate {from}|{to}|{text}",
		"Required Permissions":"LogBot Member",
		"Type"                :"Fun",
		"Plugin"              :"Main"
	},
	"_dm"            :{
		"Info"                :"Starts a DM channel.",
		"Usage"               :"$dm",
		"Required Permissions":"LogBot Member",
		"Type"                :"Utility",
		"Plugin"              :"Main"
	},
	"_filter"        :{
		"Info"                :"Changes or shows the filter settings.",
		"Usage"               :"$filter settype {type: [edit/delete]}\n$filter",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Moderation",
		"Plugin"              :"Swearing Filter"
	},
	"_convert"       :{
		"Info"                :"Converts a string to the encoded equivalent.",
		"Usage"               :"$convert {codec: [unicode/ascii/oem/utf-8]} {string}",
		"Required Permissions":"LogBot Member",
		"Type"                :"Fun",
		"Plugin"              :"Main"
	},
	"_mute"          :{
		"Info"                :"Mutes a person, deleting any and all messages sent by them in the channel the command was sent in.",
		"Usage"               :"$mute {mention(s)}",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Moderation",
		"Plugin"              :"Main"
	},
	"_unmute"        :{
		"Info"                :"Unmutes a person, allowing them to send a message in the channel the command was sent in.",
		"Usage"               :"$unmute {mention(s)}",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Moderation",
		"Plugin"              :"Main"
	},
	"_mutes"         :{
		"Info"                :"Shows the people muted in the channel.",
		"Usage"               :"$mutes",
		"Required Permissions":"LogBot Member",
		"Type"                :"Moderation",
		"Plugin"              :"Main"
	},
	"_setchannel"    :{
		"Info"                :"Sets the default channel for the daily verse.",
		"Usage"               :"$setchannel [channel-mention]",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Fun",
		"Plugin"              :"Bible"
	},
	"_getchannel"    :{
		"Info"                :"Gets the default channel for the daily verse.",
		"Usage"               :"$getchannel",
		"Required Permissions":"None",
		"Type"                :"Fun",
		"Plugin"              :"Bible"
	},
	"_votd"          :{
		"Info"                :"Shows the verse of the day.",
		"Usage"               :"$votd",
		"Required Permissions":"None",
		"Type"                :"Fun",
		"Plugin"              :"Bible"
	},
	"logbot.info"    :{
		"Info"                :"Shows information on the current running instance of LogBot.",
		"Usage"               :"logbot.info",
		"Required Permissions":"LogBot Member",
		"Type"                :"Stats",
		"Plugin"              :"Main"
	},
	"l_rank"         :{
		"Info"                :"Shows the rank of the sender, or mentioned person.",
		"Usage"               :"l$rank [mention]",
		"Required Permissions":"None",
		"Type"                :"Fun",
		"Plugin"              :"Levels"
	},
	"l_levels"       :{
		"Info"                :"Shows a list of everyone in the server, sorted by their ranks. Users with rank 0 are not listed.",
		"Usage"               :"l$levels",
		"Required Permissions":"None",
		"Type"                :"Fun",
		"Plugin"              :"Levels"
	},
	"l_place"        :{
		"Info"                :"Shows your server rank.",
		"Usage"               :"l$place [mention]",
		"Required Permissions":"None",
		"Type"                :"Fun",
		"Plugin"              :"Levels"
	},
	"l_buy"          :{
		"Info"                :"Purchases an item with the bot credits.",
		"Usage"               :"l$buy {item} [amount]",
		"Required Permissions":"None",
		"Type"                :"Fun",
		"Plugin"              :"Levels"
	},
	"l_shop"         :{
		"Info"                :"Shows a list of items you can buy.",
		"Usage"               :"l$shop",
		"Required Permissions":"None",
		"Type"                :"Fun",
		"Plugin"              :"Levels"
	},
	"l_gift"         :{
		"Info"                :"Sends some of your chosen {gift} to the chosen user.",
		"Usage"               :"l$gift {gift: [cred/xp/cpm/mul]} {amount} {mention}",
		"Required Permissions":"None",
		"Type"                :"Fun",
		"Plugin"              :"Levels"
	},
	"l_award"        :{
		"Info"                :"Generates an award for the chosen user.",
		"Usage"               :"l$award {award: [cred/rank/xp/cpm/tier]} {amount} {mention}",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Fun",
		"Plugin"              :"Levels"
	},
	"_ping"          :{
		"Info"                :"Checks which modules, if any, are working properly.",
		"Usage"               :"$ping",
		"Required Permissions":"None",
		"Type"                :"Utility",
		"Plugin"              :"All"
	},
	"l_disabled"     :{
		"Info"                :"Shows if the Levels system is disabled.",
		"Usage"               :"l$disabled",
		"Required Permissions":"None",
		"Type"                :"Moderation",
		"Plugin"              :"Levels"
	},
	"l_disable"      :{
		"Info"                :"Disables the Levels system, until you wish to re-enable it.",
		"Usage"               :"l$disable",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Moderation",
		"Plugin"              :"Levels"
	},
	"l_enable"       :{
		"Info"                :"Enables the Levels system.",
		"Usage"               :"l$enable",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Moderation",
		"Plugin"              :"Levels"
	},
	"v_disable"      :{
		"Info"                :"Disables verse recognition for the channel(s). If no channel is mentioned, it disables this feature for the channel in which the message was sent.",
		"Usage"               :"v$disable [channel_mentions(s)]",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Moderation",
		"Plugin"              :"Bible"
	},
	"v_enable"       :{
		"Info"                :"Enables verse recognition for the channel(s). If no channel is mentioned, it enables this feature for the channel in which the message was sent.",
		"Usage"               :"v$enable [channel_mention(s)]",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Moderation",
		"Plugin"              :"Bible"
	},
	"v_disables"     :{
		"Info"                :"Shows a list of the channels in this server where verse recognition is disabled.",
		"Usage"               :"v$disables",
		"Required Permissions":"None",
		"Type"                :"Moderation",
		"Plugin"              :"Bible"
	},
	"g_rps"          :{
		"Info"                :"Plays a game of rock paper scissors.",
		"Usage"               :"g$rps {choice: [rock/paper/scissors]}",
		"Required Permissions":"None",
		"Type"                :"Fun",
		"Plugin"              :"Games"
	},
	"g_rpsls"        :{
		"Info"                :"Plays a game of rock paper scissors lizard Spock.",
		"Usage"               :"g$rpsls {choice: [rock/paper/scissors/lizard/Spock]}",
		"Required Permissions":"None",
		"Type"                :"Fun",
		"Plugin"              :"Games"
	},
	"g_rules"        :{
		"Info"                :"Shows rules for a game.",
		"Usage"               :"g$rules {game: [rps/rpsls/scramble]}",
		"Required Permissions":"None",
		"Type"                :"Fun",
		"Plugin"              :"Games"
	},
	"p_start"        :{
		"Info"                :"Starts a vote and returns the vote_index.",
		"Usage"               :"p$start {vote_name}|{choices: [1]|[2]|[3]|[4]|[...]}",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Feedback",
		"Plugin"              :"Polling"
	},
	"p_end"          :{
		"Info"                :"Ends a vote and returns the results.",
		"Usage"               :"p$end {vote_index}",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Feedback",
		"Plugin"              :"Polling"
	},
	"p_status"       :{
		"Info"                :"Shows the status of a vote.",
		"Usage"               :"p$status {vote_index}",
		"Required Permissions":"None",
		"Type"                :"Feedback",
		"Plugin"              :"Polling"
	},
	"p_vote"         :{
		"Info"                :"Votes for a choice.",
		"Usage"               :"p$vote {vote_index} {choice_index}",
		"Required Permissions":"None",
		"Type"                :"Feedback",
		"Plugin"              :"Polling"
	},
	"p_polls"        :{
		"Info"                :"Shows existing votes and their indices.",
		"Usage"               :"p$polls",
		"Required Permissions":"None",
		"Type"                :"Feedback",
		"Plugin"              :"Polling"
	},
	"p_save"         :{
		"Info"                :"Saves a poll for later use.",
		"Usage"               :"p$save {topic_index}",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Feedback",
		"Plugin"              :"Polling"
	},
	"p_view"         :{
		"Info"                :"Views a specific saved poll.",
		"Usage"               :"p$view {poll_index}",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Feedback",
		"Plugin"              :"Polling"
	},
	"p_remove"       :{
		"Info"                :"Removes a saved poll from the database.",
		"Usage"               :"p$remove {poll_index}",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Feedback",
		"Plugin"              :"Polling"
	},
	"p_saved"        :{
		"Info"                :"Shows saved polls.",
		"Usage"               :"p$saved",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Feedback",
		"Plugin"              :"Polling"
	},
	"l_dm"           :{
		"Info"                :"Sets whether or not to send level/tier up notifications in DM or server channel.",
		"Usage"               :"l$dm {val: [t/f]}",
		"Required Permissions":"None",
		"Type"                :"Fun",
		"Plugin"              :"Levels"
	},
	"_setversion"    :{
		"Info"                :"Set the bible version.",
		"Usage"               :"$setversion {version: [kjv/akjv/web]}",
		"Required Permissions":"None",
		"Type"                :"Fun",
		"Plugin"              :"Bible"
	},
	"_settype"       :{
		"Info"                :"Sets the type of bible verses.",
		"Usage"               :"$settype {type: [embed/text]}",
		"Required Permissions":"None",
		"Type"                :"Fun",
		"Plugin"              :"Bible"
	},
	"_hq"            :{
		"Info"                :"Sends the LogBot HQ Instant Invite Link through chat.",
		"Usage"               :"$hq",
		"Required Permissions":"None",
		"Type"                :"Utility",
		"Plugin"              :"Main"
	},
	"_fetch"         :{
		"Info"                :"Fetches the logs for a channel in a server.",
		"Usage"               :"$fetch {channel-name}\n$fetch event",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Logging",
		"Plugin"              :"Main"
	},
	"h_prefix"       :{
		"Info"                :"Much like $help, this command will either show a list of prefixes (if no prefix parameter is present), or the plugin for the provided prefix.",
		"Usage"               :"h$prefix [prefix]",
		"Required Permissions":"None",
		"Type"                :"Help",
		"Plugin"              :"Help"
	},
	"_joinrole"      :{
		"Info"                :"Gets or sets the join role.",
		"Usage"               :"$joinrole [role]",
		"Required Permissions":"LogBot Admin/Member",
		"Type"                :"Moderation",
		"Plugin"              :"Main"
	},
	"_git"           :{
		"Info"                :"Shows a link to the GitHub repo for this bot.",
		"Usage"               :"$git",
		"Required Permissions":"None",
		"Type"                :"Utility",
		"Plugin"              :"Main"
	},
	"_guess"         :{
		"Info"                :"Take a guess at what the scrambled word is.",
		"Usage"               :"$guess {word}",
		"Required Permissions":"None",
		"Type"                :"Fun",
		"Plugin"              :"Games"
	},
	"_scramble"      :{
		"Info"                :"Adds a word, removes a word, searches for a word, lists all words, or starts a word scramble (respectively).",
		"Usage"               :"$scramble add {word}\n$scramble rem {word}\n$scramble find {word}\n$scramble list\n$scramble",
		"Required Permissions":"LogBot Member",
		"Type"                :"Fun",
		"Plugin"              :"Games"
	},
	"_giveup"        :{
		"Info"                :"Gives up a word scramble.",
		"Usage"               :"$giveup",
		"Required Permissions":"None",
		"Type"                :"Fun",
		"Plugin"              :"Games"
	},
	"l_alert"        :{
		"Info"                :"Sets which channel you will be alerted in when DM is OFF.",
		"Usage"               :"l$alert {channel}",
		"Required Permissions":"None",
		"Type"                :"Fun",
		"Plugin"              :"Levels"
	},
	"_logchannel"    :{
		"Info"                :"Gets or sets the logchannel for the server.",
		"Usage"               :"$logchannel [channel-mention]",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Logging",
		"Plugin"              :"Main"
	},
	"_roll"          :{
		"Info"                :"Rolls a random number between 1 and 6.",
		"$roll"               :"$roll",
		"Required Permissions":"None",
		"Type"                :"Fun",
		"Plugin"              :"Main"
	},
	"_channels"      :{
		"Info"                :"Shows a list of all voice and text channels in a server.",
		"Usage"               :"$channels",
		"Required Permissions":"LogBot Member",
		"Type"                :"Fun",
		"Plugin"              :"Main"
	},
	"_devotional"    :{
		"Error" :"Since the help content is too large to display properly, please use the documentation on github (use `$git`)",
		"Type"  :"Fun",
		"Plugin":"Bible"
	},
	"l_milestone"    :{
		"Info"                :"Adds to, removes from, or shows the milestones in the levels system.",
		"Usage"               :"l$milestone a {item: [tier/rank]} {limit} {role_mention}\nl$milestone r {item: [tier/rank]} {limit} {role_mention}\nl$milestone s",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Utility",
		"Plugin"              :"Levels"
	},
	"l_slots"        :{
		"Info"                :"Plays slots or shows the slots rules.",
		"Usage"               :"l$slots {bid}\nl$slots",
		"Required Permissions":"None",
		"Type"                :"Fun",
		"Plugin"              :"Levels"
	},
	"l_default"      :{
		"Info"                :"Sets the default values for DM or Alert channel in the server.",
		"Usage"               :"l$default DM {val: [on/off]}\nl$default AlertChannel {channel-mention}",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Utility",
		"Plugin"              :"Levels"
	},
	"l_defaults"     :{
		"Info"                :"Shows the default settings for DM and AlertChannel in the server.",
		"Usage"               :"l$defaults",
		"Required Permissions":"None",
		"Type"                :"Utility",
		"Plugin"              :"Levels"
	},
	"_defaultchannel":{
		"Info"                :"Gets or sets the default welcome/goodbye channel in the server.",
		"Usage"               :"$defaultchannel [channel-mention]",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Utility",
		"Plugin"              :"Main"
	},
	"_report"        :{
		"Info"                :"Reports a bug with the bot. Please try to include as detailed a description as possible.",
		"Usage"               :"$report {bug}",
		"Required Permissions":"None",
		"Type"                :"Feedback",
		"Plugin"              :"Dev"
	},
	"_reports"       :{
		"Info"                :"Shows the bug reports made so far.",
		"Usage"               :"$reports",
		"Required Permissions":"None",
		"Type"                :"Feedback",
		"Plugin"              :"Dev"
	},
	"m_strikes"      :{
		"Info"                :"Shows a user's strikes.",
		"Usage"               :"m$strikes [user]",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Moderation",
		"Plugin"              :"Moderation"
	},
	"m_strike"       :{
		"Info"                :"Strikes a user.",
		"Usage"               :"m$strike {user}|{reason}",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Moderation",
		"Plugin"              :"Moderation"
	},
	"m_destrike"     :{
		"Info"                :"Removes a strike.",
		"Usage"               :"m$destrike {code}",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Moderation",
		"Plugin"              :"Moderation"
	},
	"v_settings"     :{
		"Info"                :"Shows the Verse Module's settings for the server and you.",
		"Usage"               :"v$settings",
		"Required Permissions":"None",
		"Type"                :"Fun",
		"Plugin"              :"Bible"
	},
	"_changeprefix"  :{
		"Info"                :"Changes the server's prefix.",
		"Usage"               :"$changeprefix {prefix}",
		"Required Permissions":"LogBot Admin",
		"Type"                :"Customization",
		"Plugin"              :"Main"
	},
	"_prefix"        :{
		"Info"                :"Shows the server's prefix. Always works with the default prefix.",
		"Usage"               :"$prefix",
		"Required Permissions":"None",
		"Type"                :"Customization",
		"Plugin"              :"Main"
	},
	"_role"          :{
		"Info"                :"Shows information about a role.",
		"Usage"               :"$role {name}\n$role {id}\n$role {mention}",
		"Required Permissions":"None",
		"Type"                :"Fun",
		"Plugin"              :"Main"
	},
	"_urban"         :{
		"Info"                :"Shows the UrbanDictionary definition, examples, upvotes, and downvotes of a word.",
		"Usage"               :"$urban {word}",
		"Required Permissions":"None",
		"Type"                :"Fun",
		"Plugin"              :"Main"
	},
	"_dict"          :{
		"Info"                :"Shows the definition, antonyms, or synonyms of a word.",
		"Usage"               :"$dict def {word}\n$dict ant {word}\n$dict syn {word}",
		"Required Permissions":"None",
		"Type"                :"Fun",
		"Plugin"              :"Main"
	},
	"_files"         :{
		"Info"                :"Shows the server's log files.",
		"Usage"               :"$files",
		"Required Permissions":"LogBot Admin",
		"Plugin"              :"Main",
		"Type"                :"Utility"
	}
} )
prefixes = {
	"a$":"Admin Plugin",
	"v$":"Bible Plugin",
	"g$":"Games Plugin",
	"l$":"Levels Plugin",
	"$" :"Main",
	"p$":"Polling Plugin",
	"h$":"Help Plugin"
}
url = "http://bit.ly/logbot_repo#"
web_url = "https://zldproductions.github.io/LogBot/Commands.html#"

sql = sqlite3.connect( f"{os.getcwd()}\\Discord Logs\\SETTINGS\\logbot.db" )
cursor = sql.cursor( )

def sqlread ( cmd: str ):
	cursor.execute( cmd )
	return cursor.fetchall( )

@client.event
async def on_ready ( ):
	await client.change_presence( game=None )
	os.system( "cls" )
	print( f"{Fore.MAGENTA}Ready!!!{Fore.RESET}" )
	pass

@client.event
async def on_message ( message ):
	# noinspection PyUnusedLocal
	def replace ( *args, val=message.content ):
		_replace = val.replace
		for reg, rep in args: val = _replace( reg, rep )
		return val
	def startswith ( *args, val=message.content ):
		for arg in args:
			if val.startswith( arg ): return True
			pass
		return False
		pass
	owner_id = "239500860336373761"
	do_update = False

	prefix = sqlread( f"SELECT prefix FROM Prefixes WHERE server='{message.server.id}';" )[ 0 ][ 0 ]

	if startswith( f"{prefix}help " ):
		content = message.content.replace( f"{prefix}help ", "", 1 )
		myembed = discord.Embed( title=content, description=f"Command Information for {content}\n{key}", colour=discord.Colour.dark_gold( ) )
		items = { }
		for item in infos.keys( ):
			if item.replace( "_", "" ) == content.replace( prefix, "" ).replace( "$", "" ): items = infos[ item ]
			pass
		for item in list( items.keys( ) ): myembed.add_field( name=item, value=items[ item ].replace( "$", prefix ) )
		myembed.set_footer( text=f"GitHub URL: {url}{content.replace(prefix, '')}" )
		if not len( items.keys( ) ) == 0: await client.send_message( message.channel, f"Website URL: {web_url}{content.replace(prefix, '')}", embed=myembed )
		else: await client.send_message( message.channel, f"```There is no command for \"{content}\" at this time.```" )
		del content
		del myembed
		del items
		pass
	elif startswith( f"{prefix}help" ):
		_cnt = message.content.replace( f"{prefix}help", "" )
		_groupby = None
		if "&GroupByType" in _cnt: _groupby = "type"
		if "&GroupByPlugin" in _cnt: _groupby = "plugin"
		if _groupby == "type":
			all_commands = { }
			_str = ""
			for item in infos:
				if all_commands.get( infos[ item ][ "Type" ] ) is not None: all_commands[ infos[ item ][ "Type" ] ].append( item )
				else: all_commands[ infos[ item ][ "Type" ] ] = list( ); all_commands[ infos[ item ][ "Type" ] ].append( item )
				pass
			for item in all_commands:
				_str += f"{item}:\n{', '.join(all_commands[item])}\n\n"
				pass
			all_commands = _str
			pass
		elif _groupby == "plugin":
			all_commands = { }
			_str = ""
			for item in infos:
				if all_commands.get( infos[ item ][ "Plugin" ] ) is not None: all_commands[ infos[ item ][ "Plugin" ] ].append( item )
				else: all_commands[ infos[ item ][ "Plugin" ] ] = list( ); all_commands[ infos[ item ][ "Plugin" ] ].append( item )
				pass
			for item in all_commands:
				_str += f"{item}:\n{', '.join(all_commands[item])}\n\n"
				pass
			all_commands = _str
			pass
		else:
			all_commands = list( infos.keys( ) )
			all_commands.sort( )
			all_commands = ', '.join( all_commands ).replace( "_", prefix )
			pass
		await client.send_message( message.channel, f"```Use {prefix}help to get the list of commands.\nUse {prefix}help [command] to get more information on [command].\nUse {prefix}git to visit the GitHub Documentation.\nThe prefix is {prefix}```" )
		await client.send_message( message.channel, f"```Commands:\n{all_commands.replace('_', prefix)}```" )
		pass
	elif startswith( f"h{prefix}prefix " ):
		prefix = message.content.replace( "h{prefix}prefix ", "" )
		data = prefixes.get( prefix )
		if data is None:
			await client.send_message( message.channel, f"```There is no prefix \"{prefix}\"" )
			pass
		else:
			e = discord.Embed( title=prefix, description=f"Prefix Information for {prefix}", colour=discord.Colour.dark_gold( ) ) \
				.add_field( name="Plugin", value=data )
			await client.send_message( message.channel, "Here you go!", embed=e )
			del e
			pass
		del prefix
		del data
		pass
	elif startswith( f"h{prefix}prefix" ):
		prefs = list( prefixes.keys( ) )
		prefs.sort( )
		await client.send_message( message.channel, f"```{', '.join(prefs)}```" )
		del prefs
		pass
	elif startswith( f"$update", "logbot.help.update" ):
		if message.author.id == owner_id: do_update = True
		pass
	elif startswith( "$exit", "logbot.help.exit" ):
		if message.author.id == owner_id: exit( 0 )
		pass
	elif startswith( f"{prefix}ping" ):
		tm = datetime.now( ) - message.timestamp
		await client.send_message( message.channel, f"```LogBot Help Online ~ {round(tm.microseconds / 1000)}```" )
		pass

	if do_update:
		print( f"{Fore.LIGHTCYAN_EX}Updating...{Fore.RESET}" )
		await client.close( )
		subprocess.Popen( f"python {os.getcwd()}\\help.py", False )
		exit( 0 )
		pass
	pass

client.run( token )
