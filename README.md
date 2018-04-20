# LogBot

## Developer Discord ID:
    JVOD#6496

[Invite the Bot!](https://discordapp.com/oauth2/authorize?client_id=255379748828610561&scope=bot&permissions=2146958463)

Have questions? Ask them here: [LogBot HQ](https://discord.gg/82DYM3T)

---

## Logging Notice
I originally created LogBot to log events, such as message editing, deletion, etc.
Because the log channel is optional, the logs are stored locally (but not checked by me, whatsoever). The logs contain events such as status change, server updates, channel updates, messages, etc.  
Using `$excludechannel all` will cause the bot to ignore logging events.

The bot also stores data (level data, polling data, etc.). This data is not checked in any way (it's not even easily readable).

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

**Required Level**  
LogBot Admin

---

#### $excludechannel
**Info**  
Excludes all messages in the mentioned channel(s) from the logs.

**Usage**

    $excludechannel {channels}
    $exc {channels}
`channels` is one or more channel mentions (#channel-name).

**Required Level**  
LogBot Admin

---

#### $includechannel
**Info**  
Used to remove the exclusion of mention channel(s) from the logs.

**Usage**

    $includechannel {channels}
    $inc {channels}
`channels` is one or more channel mentions (#channel-name).

**Required Level**  
LogBot Admin

---

#### $mark
**Info**  
Used to set aside logs for the mentioned channel(s).

**Usage**

    $mark a {channels}
    $mark r {channels}
`channels` is one or more channel mentions.

**Required Level**      
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

**Required Level**  
LogBot Admin

---

#### $showlist
**Info**  
Shows the list of excluded channels.

**Usage**

    $showlist

**Required Level**  
None

---

#### $showmarks
**Info**  
Shows the list of marked channels.

**Usage**

    $showmarks
    
**Required Level**  
None

---

#### $help
**Info**  
Shows the help dialog for a specific command, or, if no command was stated, shows a list of commands. Adding GroupBy modifiers changes the format of the command list. Adding multiple modifiers gives GroupByPlugin preference.

**Usage**

    $help [command]
    $help&{modifier}
`command` is a command for the bot.
`modifier` is either `GroupByPlugin` or `GroupByType`.
    
**Required Level**  
None

---

#### $version
**Info**  
Shows the current bot version, and what programming language it was written in.

**Usage**

    $version
    
**Required Level**  
None

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

**Required Level**  
LogBot Admin

---

#### $updates
**Info**  
Shows what is new with the bot.

**Usage**  

    $updates
    
**Required Level**  
None

---

#### $say
**Info**  
Sends a message in the specific channel.

**Usage**

    $say {channel}|{text}
`text` is the text to say.  
`channel` is one or more channel mentions (#channel).  

**Required Level**  
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

**Required Level**  
LogBot Admin

---

#### $planned
**Info**  
Shows what may come next in the bot.

**Usage**

    $planned

**Required Level**  
None

---

#### $query
**Info**  
Fetches information from Wolfram|Alpha.

**Usage**

    $query {query}
`query` is the statement searched on Wolfram|Alpha.

**Required Level** 
None

---

#### $wiki
**Info**  
Fetches information from Wikipedia.

**Usage**

    $wiki {input}
`input` is the topic for the wikipedia search.

**Required Level**  
None

---

#### $verse
**Info**  
Fetches information from the Bible.

**Usage**

    $verse info:book {book}
    $verse info:chapter {book} {chapter}
    $verse info:verse {book} {chapter}:{verse}
    $verse random
    $verse help
    $verse search {query}
`book` is a book of the bible.  
`chapter` is a number describing the chapter of the `book`.  
`verse` is a number describing the verse of the `chapter` of the `book`.  
`query` is the search key.

**Required Level**  
None

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

**Required Level**  
LogBot Admin

---

#### $enable
**Info**  
Enables a disabled command.  
All commands that work with disabled also work with this one.

**Usage**

    $enable {command}
`command` is one of the bot commands listed in $disable.

**Required Level**  
LogBot Admin

---

#### $disables
**Info**  
Shows the disabled commands.

**Usage**

    $disables

**Required Level**  
None

---

#### $prunes
**Info**  
Estimates the number of members who will be kicked by `$prune {days}`.

**Usage**

    $prunes {days}
`days` is the number of minimum offline days a member has to have in order to qualify for the prune.

**Required Level**  
LogBot Admin

---

#### $prune
**Info**  
Kicks members who have been offline for {days}.

**Usage**

    $prune {days}
`days` is the minimum number of days a member has to be offline in order to qualify for the prune.

**Required Level**  
LogBot Admin

---

#### $suggest
**Info**  
Saves a suggestion for the developer.

**Usage**

    $suggest {suggestion}
`suggestion` is your suggestion for an addition or a change in the bot's features.

**Required Level**  
None

---

#### $suggestions
**Info**  
Shows suggestions received so far unless they have been completed (and therefore removed).

**Usage**

    $suggestions

**Required Level**  
None

---

#### $decide
**Info**  
Chooses a random value between the options given.

**Usage**

    $decide {options}
`options` is a list of options, separated by | (vertical bar), like this: `Yes|No`

**Required Level**  
None

---

#### $welcome
**Info**  
Either sets the current welcome message (if [msg] is present), or shows it.

**Usage**

    $welcome [msg]
`msg` is the new welcome message.

**Required Level**  
LogBot Admin

---

#### $goodbye
**Info**  
Either sets the current goodbye message, or shows it.

**Usage**

    $goodbye [msg]
`msg` is the new goodbye message.

**Required Level**  
LogBot Admin

---

#### $user
**Info**  
Shows public information about a user.

**Usage**

    $user[:field] {user}
`user` is a user mention (@user#0000) or the name of the user.
`:field` is optional. Include : in your message. Fields are: `name`, `nick`, `id`, `date`, `default`, `avatar`, `status`, `type`

**Required Level**  
None

---

#### $invite
**Info**  
Gives you an invite link.

**Usage**

    $invite

**Required Level**  
None

---

#### $purge
**Info**  
Purges messages from the channel it is sent through.  
It is restrained through the switches (listed below).  
It can only delete messages if they are under 2 weeks old.

**Usage**

    $purge [switches]
`switches` is one or more (separated by &&) of the switches listed below. `limit=[num]` is required if you use switches.

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

**Required Level**  
LogBot Admin

---

#### $kick
**Info**  
Kicks the mentioned user(s).

**Usage**

    $kick {users}
`users` is one or more mentions of users (@user#0000).

**Required Level**  
LogBot Admin

---

#### $ban
**Info**  
Bans the mentioned user(s) from the server.

**Usage**

    $ban {users}
`users` is one or more user mentions.

**Required Level**  
LogBot Admin

---

#### $permissions
**Info**  
Shows the permissions of the user that sent it or the mentioned user, in the specified channel (if present) or in the entire server.

**Usage**

    $permissions [channel] [user]
`channel` is a channel mention.  
`user` is a user mention.

**Required Level**  
None

---

#### $translate.get
**Info**  
Shows the list of language codes.

**Usage**

    $translate.get

**Required Level**  
None

---

#### $translate
**Info**  
Translates text.

**Usage**

    $translate {from}|{to}|{text}
`from` is the language code `text` is written in.  
`to` is the language code `text` will be translated to.  
`text` is the text that will be translated.

**Required Level**  
None

---

#### $dm
**Info**  
Starts a DM channel.

**Usage**

    $dm

**Required Level**  
None

---

#### $filter
**Info**  
Alters or shows the filter settings.

**Usage**

    $filter settype {type: [edit/delete]}
    $filter
`type` is the new filter type. This is for setting whether or not the bot should replace filtered messages with their censored versions.

**Required Level**  
LogBot Admin

---

#### $convert
**Info**  
Converts a string to the encoded equivalent.

**Usage**

    $convert {codec: [unicode/ascii/eom/utf-8]} {string}
`codec` is the conversion codec to use. Unicode is used most often.  
`string` is a sequence of characters.

**Required Level**  
None

---

#### $mute
**Info**  
Mutes a person, deleting any and all messages sent by them in the channel the command was sent in.

**Usage**

    $mute {users}
`users` is one or more user mentions.

**Required Level**  
LogBot Admin

---

#### $unmute
**Info**  
Unmutes a person, allowing them to send a message in the channel the command was sent in.

**Usage**

    $unmute {users}
`users` is one or more user mentions.

**Required Level**  
LogBot Admin

---

#### $mutes
**Info**  
Shows the people muted in the server.

**Usage**

    $mutes

**Required Level**  
None

---

#### $setchannel
**Info**  
Sets the default channel for the daily verse.

**Usage**

    $setchannel {channel}
`channel` is a channel mention.

**Required Level**  
LogBot Admin

---

#### $getchannel
**Info**  
Gets the default channel for the daily verse.

**Usage**

    $getchannel

**Required Level**  
None

---

#### $votd
**Info**  
Shows the verse of the day.

**Usage**

    $votd

**Required Level**  
None

---

#### logbot.info
**Info**  
Shows information on the current running instance of LogBot.

**Usage**

    logbot.info

**Required Level**  
None

---

#### l$rank
**Info**  
Shows the rank of the sender, or mentioned person.

**Usage**

    l$rank [user]
`user` is a user mention.

**Required Level**  
None

---

#### l$levels
**Info**  
Shows a list of everyone in the server, sorted by their ranks. Users with rank 0 are not listed.

**Usage**

    l$levels

**Required Level**  
None

---

#### l$place
**Info**  
Shows your server rank.

**Usage**

    l$place [user]
`user` is a user mention.

**Required Level**  
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

**Required Level**  
None

---

#### l$shop
**Info**  
Shows a list of items you can buy.

**Usage**

    l$shop

**Required Level**  
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

**Required Level**  
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

**Required Level**  
LogBot Admin

---

#### $ping
**Info**  
Checks which modules, if any, are working properly.

**Usage**

    $ping

**Required Level**  
None

---

#### l$disabled
**Info**  
Shows if the levels module is disabled.

**Usage**

    l$disabled

**Required Level**  
None

---

#### l$disable
**Info**  
Disables the levels module for the server, until it is is re-enabled.

**Usage**

    l$disable

**Required Level**  
LogBot Admin

---

#### l$enable
**Info**  
Enables the levels system.

**Usage**

    l$enable

**Required Level**  
LogBot Admin

---

#### v$disable
**Info**  
Disables verse recognition for individual channels, if some were mentioned. If not, it disables VR for the channel the message was sent in.

**Usage**

    v$disable {channel}
`channel` is one or more channel mentions.

**Required Level**  
LogBot Admin

---

#### v$enable
**Info**  
Enables verse recognition for the channel(s) mentioned. If none were mentioned, then it enables VR for the channel the message was sent in.

**Usage**

    v$enable {channel}
`channel` is one or more channel mentions.

**Required Level**  
LogBot Admin

---

#### v$disables
**Info**  
Shows a list of the channels in this server where verse recognition is disabled.

**Usage**

    v$disables

**Required Level**  
None

---

#### g$rps
**Info**  
Plays a game of rock paper scissors.  
Traditionally, the rules are:  
rock beats scissors  
scissors beats paper  
paper beats rock

**Usage**

    g$rps {choice: [rock/paper/scissors]}
`choice` is your choice between rock, paper, and scissors.

**Required Level**  
None

---

#### g$rpsls
**Info**  
Plays a game of rock, paper, scissors, lizard, Spock.  
Traditionally, the rules are:  
Rock crushes scissors and bludgeons lizard  
Paper covers rock and blinds Spock  
scissors cuts paper and decapitates lizard  
lizard eats paper and poisons Spock  
Spock destroys rock and disintegrates scissors

**Usage**

    g$rpsls {choice: [rock/paper/scissors/lizard/Spock]}
`choice` is your choice between rock, paper, scissors, lizard, and Spock.

**Required Level**  
None

---

#### g$rules
**Info**  
Shows rules for a game.

**Usage**

    g$rules {game: [rps/rpsls/scramble]}
`game` is the game you want rules for.

**Required Level**  
None

---

#### p$start
**Info**  
Starts a vote and returns the index of the vote.

**Usage**

    p$start {prompt}|{choices: [1]|[2]|[3]|...}
`prompt` is the topic of the vote.  
`choices` is one or more choices for the users to choose from. Each one is separated by a vertical bar.

**Required Level**  
LogBot Admin

---

#### p$end
**Info**  
Ends a vote and returns the results.

**Usage**

    p$end {index}
`index` is the vote index. This can be retrieved by using the `p$polls` command.

**Required Level**  
LogBot Admin

---

#### p$status
**Info**  
Shows the status of a poll.

**Usage**

    p$status {index}
`index` is the poll index. This can be retrieved by using the `p$polls` command.

**Required Level**  
None

---

#### p$vote
**Info**  
Votes for a choice.

**Usage**

    p$vote

**Required Level**  
None

---

#### p$polls
**Info**  
Shows existing votes and their indices.

**Usage**

    p$polls

**Required Level**  
None

---

#### p$save
**Info**  
Saves a poll for later use.

**Usage**

    p$save {index}
`index` is the poll index, which can be fetched by using `p$polls`.

**Required Level**  
LogBot Admin

---

#### p$view
**Info**  
Views a specific saved poll.

**Usage**

    p$view {index}
`index` is the poll index, which can be found by using `p$saved`.

**Required Level**  
LogBot Admin

---

#### p$remove
**Info**  
Removes a saved poll from the database.

**Usage**

    p$remove {index}
`index` is the poll index, which can be fetched by using `p$saved`.

**Required Level**  
LogBot Admin

---

#### p$saved
**Info**  
Shows the saved polls.

**Usage**

    p$saved

**Required Level**  
LogBot Admin

---

#### l$dm
**Info**  
Sets whether or not to send level/tier up notifications in DM or a server channel.

**Usage**

    l$dm {val: [t/f]}
`val` is a boolean (True or False) value.

**Required Level**  
None

---

#### $setversion
**Info**  
Sets your preferred bible version.

**Usage**

    $setversion [version: [kjv/akjv/web]}
`version` is the bible version you want to set yours to. Currently only supports 3 versions.

**Required Level**  
None

---

#### $settype
**Info**  
Sets the type of the bible verses.

**Usage**

    $settype {type: [embed/text]}
`type` is the return format you wish to receive references in.

**Required Level**  
None

---

#### $hq
**Info**  
Sends the LogBot HQ Instant Invite Link through chat.

**Usage**

    $hq

**Required Level**  
None

---

#### $fetch
**Info**  
Fetches the logs for a channel in a server.

**Usage**

    $fetch {channel}
    $fetch event
`channel` is the name (not a mention) of a channel.

**Required Level**  
LogBot Admin

---

#### h$prefix
**Info**  
Much like $help, this command will either show a list of prefixes (if no prefix parameter is present), or the plugin for the provided prefix.

**Usage**

    h$prefix [prefix]
`prefix` is the prefix that you wish to view.

**Required Level**  
None

---

#### $joinrole
**Info**  
Gets or sets the join role.

**Usage**

    $joinrole [role]
`role` is a role mention.

**Required Level**  
LogBot Admin/Member

---

#### $git
**Info**  
Shows a link to the GitHub repository for this bot.

**Usage**

    $git

**Required Level**  
None

---

#### $guess
**Info**  
Take a guess at what the scrambled word is.

**Usage**

    $guess {word}
`word` is the un-scrambled word that you are guessing.

**Required Level**  
None

---

#### $scramble
**Info**  
Adds a word, removes a word, searches for a word, lists all words, or starts word scramble.

**Usage**

    $scramble add {word}
    $scramble rem {word}
    $scramble find {word}
    $scrambl list
    $scramble
`word` is the word you wish to add/remove/find.

**Required Level**  
None

---

#### $giveup
**Info**  
Gives up a word scramble.

**Usage**

    $giveup

**Required Level**  
None

---

#### l$alert
**Info**  
Sets which channel you will be alerted in when DM is OFF.

**Usage**

    l$alert {channel}
`channel` is a channel mention, `self`, or `None` (case-sensitive).

**Required Level**  
None

---

#### $logchannel
**Info**  
Gets or sets the logchannel for the server.

**Usage**

    $logchannel [channel]
`channel` is a channel mention.

**Required Level**  
LogBot Admin

---

#### $roll
**Info**  
Rolls a random number between 1 and 6.

**Usage**  

    $roll

**Required Level**  
None

---

#### $channels
**Info**  
Shows all of the voice and text channels in a server.

**Usage**  

    $channels

**Required Level**  
None

---

#### $devotional
**Info**  
Allows the user to create an embed with more personalized attributes.

**Usage**  
multi-line:  

    $devotional
    &title=[title]
    &description=[description]
    &thumbnail=[image-url]
    &footer=[text]
    &text=[text]
    &passage=[ref]
    &keyword=[word]
`title` is the title of the embed. This line is required and can only be used once.  
`description` is the description of the embed. This line is optional and can only be used once.  
`image-url` is the url of an image. This line is optional, and can only be used once.  
`text` describes text. `&footer` is an optional, one-use line. `&text` can be added at any point, is optional, and can be used as many times as needed.  
`ref` is a verse reference. This line is optional, and can be used as many times as is necessary.  
`word` is a word or phrase.

**Required Level**  
None

---

#### l$milestone
**Info**  
Adds, removes, or shows all milestones within the levels system.

**Usage**  

    l$milestone a {type: [tier/rank]} {limit} {role}
    l$milestone r {type: [tier/rank]} {limit} {role}
    l$milestone s
`type` is the type of the milestone. Once the users reaches `limit` of the type, they get the role.  
`limit` is the number needed to complete the milestone.  
`role` is a role mention.

**Required Level**  
LogBot Admin

---

#### l$slots
**Info**  
Plays slots, or shows the rules for slots.

**Usage**  

    l$slots {bid}
    l$slots
`bid` is how many credits you bet.


**Required Level**  
None

---

#### l$default
**Info**  
Sets the DM or AlertChannel default values for the server.

**Usage**

    l$default DM {val: [on/true/1/off/false/0]}
    l$default AlertChannel {channel}
`val` is the value for the DM value. Must be either on/true/1 or off/false/0. False is default.  
`channel` is a channel mention.

**Required Level**  
LogBot Admin

---

#### l$defaults
**Info**  
Gets the default values for the server.

**Usage**  

    l$defaults

**Required Level**  
None

---

#### l$defaultchannel
**Info**  
Gets or sets the server's default welcoming channel.

**Usage**

    l$defaultchannel [channel]
`channel` is a channel mention.

**Required Level**  
LogBot Admin

---

#### $report
**Info**  
Reports a bug with the bot.

**Usage**  

    $report {bug}
`message` is your bug report. Please try to include as detailed a description as possible.

**Required Level**  
None

---

#### $reports
**Info**  
Shows the bug reports with the bot.

**Usage**  

    $reports

**Required Level**  
None

---

#### m$strikes
**Info**  
Views the strikes on a person.

**Usage**  

    m$strikes [user]
`user` is a mention. If not included, the bot will consider you as the user.

**Required Level**  
LogBot Admin

---

#### m$strike
**Info**  
Strikes a person.

**Usage**  

    m$strike {user}|{reason}
`user` is a user mention.  
`reason` is the reason you struck this user.

**Required Level**  
LogBot Admin

---

#### m$destrike
**Info**  
Removes a strike from a person.

**Usage**  

    m$destrike {code}
`code` is the strike code. It can be retrieved by viewing a user's strikes.

**Required Level**  
LogBot Admin

---

#### v$settings
**Info**  
Shows the Verse Module's settings for the server and you.

**Usage**  

    v$settings

**Required Level**  
None

---

#### $changeprefix
**Info**  
Changes the server's prefix.

**Usage**

    $changeprefix {prefix}
`prefix` is the new prefix.

**Required Level**  
LogBot Admin

---

#### $prefix
**Info**  
Shows the server's prefix. Works with both the default ($) prefix as well as the server's original prefix.

**Usage**  

    $prefix

**Required Level**  
None

---

#### $role
**Info**  
Shows information about a role.

**Usage**  

    $role {role}
`role` can be a role's name, id, or mention.

**Required Level**  
None

---

#### $urban
**Info**  
Shows information about a role.

**Usage**  

    $urban {word}
`word` is the word you would like to look up.

**Required Level**  
None

---

#### $dict
**Info**  
Shows the definitions, antonyms, or synonyms of a word.

**Usage**  

    $dict def {word}
    $dict ant {word}
    $dict syn {word}
`word` is the word you want information on.

**Required Level**  
None

---

#### $files
**Info**  
Shows the server's log files.

**Usage**

    $files

**Required Level**  
LogBot Admin

---

#### c$show
**Info**  
Shows the server's log files.

**Usage**  

    c$show

**Required Level**  
None

---

#### c$add
**Info**  
Adds a custom command to the list.

**Usage**

    c$add {trigger}||{response}

**Required Level**  
None

---

#### c$remove
**Info**  
Removes a custom command from the list.

**Usage**  

    c$remove {trigger}

**Required Level**  
None

---

#### $gif
**Info**  
Fetches GIF images from Giphy.

**Usage**  

    $gif [tag]
`tag` is the image tag.

**Required Level**  
None

---

#### $sf
**Info**  
Calculates the number of significant figures in a number.

**Usage**

    $sf {n}
`n` is a number. It can be a decimal.

**Required Level**  
None

---

#### g$prob
**Info**  
Calculates probabilities with numbers, and gives the results of trials back to you.

**Usage**  

    g$prob {parts}|{trials}
`parts` is the number of choices the bot can choose from (like the choices on a spinner). For lag, memory, and message issues, must be equal to or below 100.  
`trials` is the number of trials to perform. For lag, memory, and message issues, must be equal to or below 1,000,000.

**Required Level**  
None

---

#### mu$playing
**Info**  
Shows if the bot is playing a song in your server.

**Usage**  

    mu$playing

**Required Level**  
None

---

#### mu$join
**Info**  
Joins a voice channel.

**Usage**  

    mu$join {channel}
`channel` is a channel name.

**Required Level**  
None

---

#### mu$summon
**Info**  
Joins the voice channel you are currently in.

**Usage**  

    mu$summon

**Required Level**  
None

---

#### mu$play
**Info**  
Plays a song.

**Usage**  

    mu$play {song}
`song` is the name of a song or youtube video.

**Required Level**  
None

---

#### mu$volume
**Info**  
Sets the player volume.

**Usage**  

    mu$volume {level}
`volume` is a number.

**Required Level**  
None

---

#### mu$resume
**Info**  
Resumes the player.

**Usage**  

    mu$resume

**Required Level**  
None

---

#### mu$stop
**Info**  
Stops the player, clears the queue, and disconnects from the voice channel.

**Usage**  

    mu$stop

**Required Level**  
None

---

#### mu$skip
**Info**  
Votes to skip the song. The song's requestor can automatically skip.

**Usage**  

    mu$skip

**Required Level**  
None

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

---

## Self-Run Instances
    Currently, you cannot run the bot locally on your computer.
    I am working on 24/7 up-time, but it may take quite a while.

---

## Contributions
    I will accept contributions from users who have tested the bot in it's server, and ONLY from those who are familiar with Python.
    If you meet these standards, and wish to participate, contact me through Discord, and ask if you can.
    Currently, I am looking for performance improvements, security improvements, and new features to add.

---