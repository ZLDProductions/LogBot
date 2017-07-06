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

**Required Permissions**  
LogBot Admin

---

#### $excludechannel
**Info**  
Excludes all messages in the mentioned channel(s) from the logs.

**Usage**

    $excludechannel {channel_mention(s)}
    $exc {channel_mention(s)}

**Required Permissions**  
LogBot Admin

---

#### $includechannel
**Info**  
Used to remove the exclusion of mention channel(s) from the logs.

**Usage**

    $includechannel {channel_mention(s)}
    $inc {channel_mention(s)}

**Required Permissions**  
LogBot Admin

---

#### $mark
**Info**  
Used to set aside logs for the mentioned channel(s).

**Usage**

    $mark a {channel_mention(s)}
    $mark r {channel_mention(s)}
    
**Required Permissions**      
LogBot Admin

---

#### $admin
**Info**  
Used to add, remove, or show the admins for this bot.  
Server owners are always an admin.

**Usage**

    $admin a {mention(s)}
    $admin r {mention(s)}
    $admin s
    
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
    $channel del {channel mention or name}
    $channel edit {new permission level: [admin/member/everyone]} {channel mention or name}
    $channel show
    
**Required Permissions**  
LogBot Admin

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

    $say {text}|{channel_mention}|{tts [True/False]}
    
**Required Permissions**  
LogBot Admin

---

#### $member
**Info**  
Adds, removes, or shows the members of this bot.

**Usage**

    $member a {mention(s)}
    $member r {mention(s)}
    $member s

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

**Required Permissions**  
LogBot Member

---

#### $query
**Info**  
Fetches information from Wolfram|Alpha.

**Usage**

    $query {query}

**Required Permissions** 
LogBot Member

---

#### $wiki
**Info**  
Fetches information from Wikipedia.

**Usage**

    $wiki {input}

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

**Required Permissions**  
LogBot Member

---

#### $disable
**Info**  
Disables a command.

**Usage**

    $disable {command}

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

**Required Permissions**  
LogBot Admin

---

#### $prune
**Info**  
Kicks members who have been offline for {days}.

**Usage**

    $prune {days}

**Required Permissions**  
LogBot Admin

---

#### $suggest
**Info**  
Saves a suggestion for the developer.

**Usage**

    $suggest {suggestion}

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

    $decide {option1|option2|...}

**Required Permissions**  
LogBot Member

---

#### $welcome
**Info**  
Either sets the current welcome message (if [msg] is present), or shows it.

**Usage**

    $welcome [msg]

**Required Permissions**  
LogBot Admin

---

#### $goodbye
**Info**  
Either sets the current goodbye message, or shows it.

**Usage**

    $goodbye [msg]

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