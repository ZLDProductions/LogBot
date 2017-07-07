# LogBot

## Developer Discord ID:
    JVOD#6496

[Invite the Bot!](https://discordapp.com/oauth2/authorize?client_id=255379748828610561&scope=bot&permissions=2146958463)

Have questions? Ask them here: [LogBot HQ](https://discord.gg/82DYM3T)

## Commands
Use `$help` to view a list of all documented commands, and use `$help [command]` for more specific documentation.

Key:

* {} - required parameter.
* [] - optional parameter.
* {param: [choice/choice/...]} - required parameter with specific choices.
* [param: [choice/choice/...]] - optional parameter with specific choices.

Command documentation is as follows:

#### $exclude
**Info**  
Used to exclude a single message from the logs this bot creates.

**Usage**

    $exclude {message}
    $ex {message}
`message` is the normal message you would have sent.

**Required Permissions**  
LogBot Admin

---

#### $excludechannel
**Info**  
Excludes all messages in the mentioned channel(s) from the logs.

**Usage**

    $excludechannel {channels}
    $exc {channels}
`channels` is one or more channel mentions (#channel-name).

**Required Permissions**  
LogBot Admin

---

#### $includechannel
**Info**  
Used to remove the exclusion of mention channel(s) from the logs.

**Usage**

    $includechannel {channels}
    $inc {channels}
`channels` is one or more channel mentions (#channel-name).

**Required Permissions**  
LogBot Admin

---

#### $mark
**Info**  
Used to set aside logs for the mentioned channel(s).

**Usage**

    $mark a {channels}
    $mark r {channels}
`channels` is one or more channel mentions.

**Required Permissions**      
LogBot Admin

---

#### $admin
**Info**  
Used to add, remove, or show the admins for this bot.  
Server owners are always an admin.

**Usage**

    $admin a {users}
    $admin r {users}
    $admin s
`users` is one or more user mentions (@user#0000)

**Required Permissions**  
LogBot Admin

---

#### $showlist
**Info**  
Shows the list of excluded channels.

**Usage**

    $showlist

**Required Permissions**  
LogBot Member

---

#### $showmarks
**Info**  
Shows the list of marked channels.

**Usage**

    $showmarks
    
**Required Permissions**  
LogBot Member

---

#### $help
**Info**  
Shows the help dialog for a specific command, or, if no command was stated, shows a list of commands.

**Usage**

    $help [command]
`command` is a command for the bot.
    
**Required Permissions**  
LogBot Member.

---

#### $version
**Info**  
Shows the current bot version, and what programming language it was written in.

**Usage**

    $version
    
**Required Permissions**  
LogBot Member

---

#### $channel
**Info**  
Creates a channel, edits a channel, shows a list of channels created by the bot, or deletes a bot-created channel.

**Usage**

    $channel new {type: [text/voice]} {name} {permission level: [admin/member/everyone]
    $channel del {channels}
    $channel edit {permission level: [admin/member/everyone]} {channel}
    $channel show
`type` is the type of the channel.  
`name` is the name of the channel.  
`permission level` is the permission level for the channel , regarding the bot.  
`channels` is a channel mention (#channel-name) or the name of the channel.

**Required Permissions**  
LogBot Admin

---

#### $updates
**Info**  
Shows what is new with the bot.

**Usage**  

    $updates
    
**Required Permissions**  
LogBot Member

---

#### $say
**Info**  
Sends a message in the specific channel.

**Usage**

    $say {text}|{channel}|{tts: [True/False]}
`text` is the text to say.  
`channel` is a channel mention (#channel).  
`tts` is a boolean (True or False) value, and describes whether the message is spoken through Discord's voice synthesis.

**Required Permissions**  
LogBot Admin

---

#### $member
**Info**  
Adds, removes, or shows the members of this bot.

**Usage**

    $member a {user}
    $member r {user}
    $member s
`user` is one or more user mentions (@user#0000).

**Required Permissions**  
LogBot Admin

---

#### $planned
**Info**  
Shows what may come next in the bot.

**Usage**

    $planned

**Required Permissions**  
LogBot Member

---

#### $cmd
**Info**  
Creates, removes, or shows a list of the custom commands.

**Usage**

    $cmd a {key}|{value}
    $cmd r {key}
    $cmd s
`key` is the command name. Include the prefix at the beginning.  
`value` is the message that is sent once the command is triggered.

**Required Permissions**  
LogBot Member

---

#### $query
**Info**  
Fetches information from Wolfram|Alpha.

**Usage**

    $query {query}
`query` is the statement searched on Wolfram|Alpha.

**Required Permissions** 
LogBot Member

---

#### $wiki
**Info**  
Fetches information from Wikipedia.

**Usage**

    $wiki {input}
`input` is the topic for the wikipedia search.

**Required Permissions**  
LogBot Member

---

#### $verse
**Info**  
Fetches information from the Bible.

**Usage**

    $verse info {book}
    $verse random
    $verse help
    $verse search {query}
`book` is a book of the bible.  
`query` is the search key.

**Required Permissions**  
LogBot Member

---

#### $disable
**Info**  
Disables a command.

**Usage**

    $disable {command}
`command` is one of the bot commands listed below.

**Commands**  
* $exclude
* $excludechannel
* $includechannel
* $mark
* $showlist
* $showmarks
* $channel
* $cmd
* $query
* $wiki
* $say
* welcome
* goodbye
* $decide
* $prune
* $purge
* $user
* $translate
* filter

**Required Permissions**  
LogBot Admin

---

#### $enable
**Info**  
Enables a disabled command.  
All commands that work with disabled also work with this one.

**Usage**

    $enable {command}
`command` is one of the bot commands listed in $disable.

**Required Permissions**  
LogBot Admin

---

#### $disables
**Info**  
Shows the disabled commands.

**Usage**

    $disables

**Required Permissions**  
LogBot Member

---

#### $prunes
**Info**  
Estimates the number of members who will be kicked by `$prune {days}`.

**Usage**

    $prunes {days}
`days` is the number of minimum offline days a member has to have in order to qualify for the prune.

**Required Permissions**  
LogBot Admin

---

#### $prune
**Info**  
Kicks members who have been offline for {days}.

**Usage**

    $prune {days}
`days` is the minimum number of days a member has to be offline in order to qualify for the prune.

**Required Permissions**  
LogBot Admin

---

#### $suggest
**Info**  
Saves a suggestion for the developer.

**Usage**

    $suggest {suggestion}
`suggestion` is your suggestion for an addition or a change in the bot's features.

**Required Permissions**  
LogBot Member

---

#### $suggestions
**Info**  
Shows suggestions received so far unless they have been completed (and therefore removed).

**Usage**

    $suggestions

**Required Permissions**  
LogBot Member

---

#### $decide
**Info**  
Chooses a random value between the options given.

**Usage**

    $decide {options}
`options` is a list of options, separated by | (vertical bar), like this: `Yes|No`

**Required Permissions**  
LogBot Member

---

#### $welcome
**Info**  
Either sets the current welcome message (if [msg] is present), or shows it.

**Usage**

    $welcome [msg]
`msg` is the new welcome message.

**Required Permissions**  
LogBot Admin

---

#### $goodbye
**Info**  
Either sets the current goodbye message, or shows it.

**Usage**

    $goodbye [msg]
`msg` is the new goodbye message.

**Required Permissions**  
LogBot Admin

---

#### $user
**Info**  
Shows public information about a user.

**Usage**

    $user {user}
`user` is a user mention (@user#0000) or the name of the user.

**Required Permissions**  
LogBot Member

---

#### $invite
**Info**  
Gives you an invite link.

**Usage**

    $invite

**Required Permissions**  
None

---

#### $purge
**Info**  
Purges messages from the channel it is sent through.  
It is restrained through the switches (listed below).  
It can only delete messages if they are under 2 weeks old.

**Usage**

    $purge [switches]
`switches` is one or more (separated by &&) of the switches listed below.

**Switches**

    limit={num}
    contains={text}
    from={mention}
    attached={boolean}
    embedded={boolean}
    pinned={boolean}
    mentions={mention}
    mentions_channel={channel_mention}
    mentions_role={role_mention}
`num` represents a number.  
`text` represents a sequence of characters.  
`mention` represents a user mention.  
`channel_mention` represents a channel mention.  
`role_mention` represents a role mention.  
`boolean` represents a True or False (case-sensitive) value.

**Required Permissions**  
LogBot Admin

---

#### $kick
**Info**  
Kicks the mentioned user(s).

**Usage**

    $kick {users}
`users` is one or more mentions of users (@user#0000).

**Required Permissions**  
LogBot Admin

---

#### $ban
**Info**  
Bans the mentioned user(s) from the server.

**Usage**

    $ban {users}
`users` is one or more user mentions.

**Required Permissions**  
LogBot Admin

---

#### $permissions
**Info**  
Shows the permissions of the user that sent it or the mentioned user, in the specified channel (if present) or in the entire server.

**Usage**

    $permissions [channel] [user]
`channel` is a channel mention.  
`user` is a user mention.

**Required Permissions**  
LogBot Member

---

#### $translate.get
**Info**  
Shows the list of language codes.

**Usage**

    $translate.get

**Required Permissions**  
LogBot Member

---

#### $translate
**Info**  
Translates text.

**Usage**

    $translate {from}|{to}|{text}
`from` is the language code `text` is written in.  
`to` is the language code `text` will be translated to.  
`text` is the text that will be translated.

**Required Permissions**  
LogBot Member

---

#### $dm
**Info**  
Starts a DM channel.

**Usage**

    $dm

**Required Permissions**  
LogBot Member

---

#### $filter
**Info**  
Adds, removes, or shows banned words for the server.

**Usage**

    $filter a {word}
    $filter r {word}
    $filter c
    $filter s
`word` is a word.

**Required Permissions**  
LogBot Admin

---

#### $convert
**Info**  
Converts a string to the encoded equivalent.

**Usage**

    $convert {codec: [unicode/ascii/eom/utf-8]} {string}
`codec` is the conversion codec to use. Unicode is used most often.  
`string` is a sequence of characters.

**Required Permissions**  
LogBot Member

---

#### $mute
**Info**  
Mutes a person, deleting any and all messages sent by them in the channel the command was sent in.

**Usage**

    $mute {users}
`users` is one or more user mentions.

**Required Permissions**  
LogBot Admin

---

#### $unmute
**Info**  
Unmutes a person, allowing them to send a message in the channel the command was sent in.

**Usage**

    $unmute {users}
`users` is one or more user mentions.

**Required Permissions**  
LogBot Admin

---

#### $mutes
**Info**  
Shows the people muted in the server.

**Usage**

    $mutes

**Required Permissions**  
LogBot Member

---

#### $setchannel
**Info**  
Sets the default channel for the daily verse.

**Usage**

    $setchannel {channel}
`channel` is a channel mention.

**Required Permissions**  
LogBot Admin

---

#### $getchannel
**Info**  
Gets the default channel for the daily verse.

**Usage**

    $getchannel

**Required Permissions**  
None

---

#### $votd
**Info**  
Shows the verse of the day.

**Usage**

    $votd

**Required Permissions**  
None

---

#### logbot.info
**Info**  
Shows information on the current running instance of LogBot.

**Usage**

    logbot.info

**Required Permissions**  
LogBot Member

---

#### l$rank
**Info**  
Shows the rank of the sender, or mentioned person.

**Usage**

    l$rank [user]
`user` is a user mention.

**Required Permissions**  
None

---

#### l$levels
**Info**  
Shows a list of everyone in the server, sorted by their ranks. Users with rank 0 are not listed.

**Usage**

    l$levels

**Required Permissions**  
None

---

#### l$place
**Info**  
Shows your server rank.

**Usage**

    l$place [user]
`user` is a user mention.

**Required Permissions**  
None

---

#### l$buy
**Info**  
Purchases an item from the shop with credits earned in the bot.  
`{item}` is an item from the shop.

**Usage**

    l$buy {item} [amount]
`item` is the item to buy. This matches up with the first column provided when using `l$shop`.  
`amount` is the amount to buy.

**Required Permissions**  
None

---

#### l$shop
**Info**  
Shows a list of items you can buy.

**Usage**

    l$shop

**Required Permissions**  
None

---

#### l$gift
**Info**  
Sends some of your chosen `{gift}` to the chosen user.

**Usage**

    l$gift {gift: [cred/xp/cpm/mul]} {amount} {user}
`gift` is the item to give to `user`.  
`amount` is the amount to give.  
`user` is the user to give `gift` to.

**Required Permissions**  
None

---

#### l$award
**Info**  
Generates an award for the chosen user.

**Usage**

    l$award {award: [cred/rank/xp/cpm/tier]} {amount} {user}
`award` is the item to award `user`.  
`amount` is the amount of `award` to award.
`user` is the user to award `award` to.

**Required Permissions**  
LogBot Admin

---

## Features
* Bible
  * Verse Recognition for three versions.
  * Daily verse selection, and auto-send.
* Swearing Filter
  * Relatively fast.
  * Filters out symbols.
* Chat Moderation
  * Purge/clear out chat.
  * Mute members.
  * Command restrictions (Admin/Member/everyone).
  * Ban-hammer.
  * Kick users.
  * Disable commands.
  * Channel creation.
  * Prune users.
* Event Logging
  * Logs everything, including:
    * New message.
    * Deleted message.
    * Edited message.
    * Server name change.
    * Member name/nick/game/status change.
    * Channel name/bitrate/max members/topic/etc... change.
    * And More!
* Polling
  * Allows for several polls at one time.
  * Can save the polls for later use.
* Leveling
  * Relatively easy.
  * Near-infinite levels.
* Games
  * Rock, paper, scissors(, lizard, Spock)
  * Word scramble.
* Web-services
  * Wikipedia
  * Wolfram|Alpha
  * Translator
  * Dictionary

## Self-Run Instances
    Currently, you cannot run the bot locally on your computer.
    I am working on 24/7 up-time, but it may take quite a while.

## Contributions
    I will accept contributions from users who have tested the bot in it's server, and ONLY from those who are familiar with Python.
    If you meet these standards, and wish to participate, contact me through Discord, and ask if you can.
    Currently, I am looking for performance improvements, security improvements, and new features to add.