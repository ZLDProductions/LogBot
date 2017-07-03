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

Command documentation is as follows:

#### $exclude
##### Info
###### Used to exclude a single message from the logs this bot creates.
##### Usage
###### $exclude {message}
###### $ex {message}
##### Required Permissions
###### LogBot Admin

#### $excludechannel
##### Info
###### Excludes all messages in the mentioned channel(s) from the logs.
##### Usage
###### $excludechannel {channel_mention(s)}
###### $exc {channel_mention(s)}
##### Required Permissions
###### LogBot Admin

#### $includechannel
##### Info
###### Used to remove the exclusion of mention channel(s) from the logs.
##### Usage
###### $includechannel {channel_mention(s)}
###### $inc {channel_mention(s)}
##### Required Permissions
###### LogBot Admin

#### $mark
##### Info
###### Used to set aside logs for the mentioned channel(s).
#### Usage
###### $mark a {channel_mention(s)}
###### $mark r {channel_mention(s)}
##### Required Permissions
###### LogBot Admin

#### $admin
##### Info
###### Used to add, remove, or show the admins for this bot.
###### Server owners are always an admin.
##### Usage
###### $admin a {mention(s)}
###### $admin r {mention(s)}
###### $admin s
##### LogBot Admin

#### $showlist
##### Info
###### Shows the list of excluded channels.
##### Usage
###### $showlist
##### Required Permissions
###### LogBot Member

#### $showmarks
##### Info
###### Shows the list of marked channels.
##### Usage
###### $showmarks
##### Required Permissions
###### LogBot Member

#### $help
##### Info
###### Shows the help dialog for a specific command, or, if no command was stated, shows a list of commands.
##### Usage
###### $help [command]
##### Required Permissions
###### LogBot Member.

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