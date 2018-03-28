"""
The Verse/Bible Module.
"""
import ast
import asyncio
import math
import os
import random
import re
import sqlite3
import subprocess
import traceback
from datetime import datetime

import discord
from colorama import Fore, init

import sql_data
import symbols
from logbot_data import owner_id, token

AKJV_BOOKS = [
	"1 Samuel",
	"2 Samuel",
	"1 Kings",
	"2 Kings",
	"1 Chronicles",
	"2 Chronicles",
	"1 Corinthians",
	"2 Corinthians",
	"1 Thessalonians",
	"2 Thessalonians",
	"1 Timothy",
	"2 Timothy",
	"1 Peter",
	"2 Peter",
	"1 John",
	"2 John",
	"3 John",
	"Genesis",
	"Exodus",
	"Leviticus",
	"Numbers",
	"Deuteronomy",
	"Joshua",
	"Judges",
	"Ruth",
	"Ezra",
	"Nehemiah",
	"Esther",
	"Job",
	"Psalms",
	"Proverbs",
	"Ecclesiastes",
	"Songs",
	"Isaiah",
	"Jeremiah",
	"Lamentations",
	"Ezekiel",
	"Daniel",
	"Hosea",
	"Joel",
	"Amos",
	"Obadiah",
	"Jonah",
	"Micah",
	"Nahum",
	"Habakkuk",
	"Zephaniah",
	"Haggai",
	"Zechariah",
	"Malachi",
	"Matthew",
	"Mark",
	"Luke",
	"John",
	"Acts",
	"Romans",
	"Galatians",
	"Ephesians",
	"Philippians",
	"Colossians",
	"Titus",
	"Philemon",
	"Hebrews",
	"James",
	"Jude",
	"Revelation"
]
# <editor-fold desc="Clients">
CLIENT = discord.Client( )
init( )
EXITING = False
# </editor-fold>
# <editor-fold desc="Variables">
VERSE_DISABLE_LIST = [ ]
BIBLE_VERSIONS = { }
BIBLE_TYPES = { }
DEFAULT_CHANNEL = { }
LAST_DAY = 0
VOTD = ""
TOP_VERSES = [
	"Psalms 23:4", "Psalms 34:8", "Psalms 34:19", "Psalms 37:4", "Psalms 55:22",
	"Psalms 90:17", "Psalms 103:2-6", "Psalms 119:105", "Psalms 121:1-2", "Psalms 9:9",
	"Psalms 16:8", "Psalms 16:8", "Psalms 27:4", "Psalms 27:14", "Psalms 30:6-7",
	"Psalms 31:3", "Psalms 32:8", "Psalms 34:22", "Psalms 42:5-6", "Psalms 46:1-3",
	"Psalms 118:14", "Psalms 119:114-115", "Psalms 119:25", "Psalms 119:50", "Psalms 120:1",
	"Psalms 121:7-8", "Psalms 145:18-19", "Proverbs 3:5-6", "Proverbs 16:3", "Proverbs 18:10",
	"Proverbs 2:7", "Proverbs 11:25", "Proverbs 17:17", "Isaiah 40:31", "Jeremiah 29:11",
	"Matthew 11:28", "Romans 8:28", "Philippians 4:6-7", "Hebrews 2:18", "1 Peter 5:7",
	"1 John 4:4", "Deuteronomy 7:9", "Deuteronomy 31:6", "Deuteronomy 31:8", "Joshua 1:9",
	"Joshua 10:25", "Isaiah 26:3", "Isaiah 30:19", "Isaiah 41:13", "Isaiah 41:10",
	"Isaiah 43:1", "Isaiah 54:17", "Isaiah 58:11", "Lamentations 3:25", "Nahum 1:7",
	"Zephaniah 3:17", "Matthew 6:33", "Matthew 7:7-8", "Luke 10:19", "Luke 11:9-10",
	"John 3:16", "John 6:47", "John 14:27", "John 15:4", "John 15:13",
	"John 16:33", "Ephesians 3:20-21", "Philippians 4:8", "Philippians 4:4", "Philippians 4:13",
	"1 Corinthians 10:13", "1 Corinthians 15:57", "1 Corinthians 16:13", "2 Corinthians 2:14", "2 Corinthians 4:8-9",
	"2 Corinthians 4:16-18", "2 Corinthians 5:7", "2 Corinthians 5:17", "Romans 8:6", "Romans 8:28",
	"Romans 8:31", "Romans 8:38-39", "Romans 15:4", "Ephesians 3:17-19", "Ephesians 3:20-21",
	"Ephesians 6:10-11", "Philippians 3:7-9", "Philippians 4:19", "Colossians 3:15", "2 Thessalonians 3:3",
	"2 Timothy 1:7", "2 Timothy 3:16-17", "2 Timothy 4:18", "Hebrews 2:18", "Hebrews 3:6",
	"Hebrews 4:12", "Hebrews 10:19-23", "Hebrews 13:5", "James 1:2-4", "James 1:12-15",
	"James 4:7-8", "1 Peter 5:7", "1 John 4:4", "1 John 4:18", "1 John 5:14-15", "Revelation 14:12"
]
DISABLED_CHANNELS = [ ]
DISABLED_USERS = [ ]
# </editor-fold>
# <editor-fold desc="Paths">
DISCORD_SETTINGS_PATH = f"{os.getcwd()}\\Discord Logs\\SETTINGS"
VERSE_DISABLES_PATH = f"{DISCORD_SETTINGS_PATH}\\verse_disable_list.txt"
BIBLE_VERSIONS_PATH = f"{DISCORD_SETTINGS_PATH}\\bible_version.txt"
BIBLE_TYPES_PATH = f"{DISCORD_SETTINGS_PATH}\\bible_types.txt"
CHANNEL_LIST_PATH = f"{DISCORD_SETTINGS_PATH}\\DEFAULT_CHANNEL.txt"
LAST_DAY_PATH = f"{DISCORD_SETTINGS_PATH}\\last_day.txt"
VOTD_PATH = f"{DISCORD_SETTINGS_PATH}\\votd.txt"
DISABLED_CHANNELS_PATH = f"{DISCORD_SETTINGS_PATH}\\bible_plugin\\Disabled Channels\\"
DISABLED_USERS_PATH = f"{DISCORD_SETTINGS_PATH}\\bible_plugin\\Disabled Users\\"
# </editor-fold>
# <editor-fold desc="Databases">
SQLD = sql_data.AKJVSQL( )
SQLKJV = sql_data.KJVSQL( )
SQLWEB = sql_data.WEBSQL( )
SQLNIV = sql_data.NIVSQL( )
SQL = sqlite3.connect( f"{DISCORD_SETTINGS_PATH}\\logbot.db" )
CURSOR = SQL.cursor( )

# </editor-fold>

class BI:
	"""
	BibleInfo class, remade.
	"""
	def __init__ ( self ):
		"""
		Initialization
		"""
		self.placeholder = ""
		self.data = {
			"Genesis"        :{
				"Author"  :"Moses",
				"Chapters":50,
				"Summary" :"Genesis answers two big questions: \"How did God's relationship with the world begin?\" and \"Where did the nation of Israel come from?\""
			},
			"Exodus"         :{
				"Author"  :"Moses",
				"Chapters":40,
				"Summary" :"God saves Israel from slavery in Egypt, and then enters into a special relationship with them."
			},
			"Leviticus"      :{
				"Author"  :"Moses",
				"Chapters":27,
				"Summary" :"God gives Israel instructions for how to worship Him."
			},
			"Numbers"        :{
				"Author"  :"Moses",
				"Chapters":36,
				"Summary" :"Israel fails to trust and obey God, and wanders in the wilderness for 40 years."
			},
			"Deuteronomy"    :{
				"Author"  :"Moses",
				"Chapters":34,
				"Summary" :"Moses gives Israel instructions (in some ways, a recap of the laws in Exodus-Numbers) for how to love and obey God in the Promised Land."
			},
			"Joshua"         :{
				"Author"  :"Joshua",
				"Chapters":24,
				"Summary" :"Joshua (Israel's new leader) leads Israel to conquer the Promised Land, then parcels out territories to the twelve tribes of Israel."
			},
			"Judges"         :{
				"Author"  :"Samuel",
				"Chapters":21,
				"Summary" :"Israel enters a cycle of turning from God, falling captive to oppressive nations, calling out to God, and being rescued by leaders God sends their way (called \"judges\")."
			},
			"Ruth"           :{
				"Author"  :"Samuel",
				"Chapters":4,
				"Summary" :"Two widows lose everything, and find hope in Israel-which leads to the birth of the future King David."
			},
			"1 Samuel"       :{
				"Author"  :"Samuel",
				"Chapters":31,
				"Summary" :"Israel demands a king, who turns out to be quite a disappointment."
			},
			"2 Samuel"       :{
				"Author"  :"Samuel",
				"Chapters":24,
				"Summary" :"David, a man after God's own heart, becomes king of Israel."
			},
			"1 Kings"        :{
				"Author"  :"Jeremiah",
				"Chapters":22,
				"Summary" :"The kingdom of Israel has a time of peace and prosperity under King Solomon, but afterward splits, and the two lines of kings turn away from God."
			},
			"2 Kings"        :{
				"Author"  :"Jeremiah",
				"Chapters":25,
				"Summary" :"Both kingdoms ignore God and his prophets, until they both fall captive to other world empires."
			},
			"1 Chronicles"   :{
				"Author"  :"Ezra",
				"Chapters":29,
				"Summary" :"This is a brief history of Israel from Adam to David, culminating with David commissioning the temple of God in Jerusalem."
			},
			"2 Chronicles"   :{
				"Author"  :"Ezra",
				"Chapters":36,
				"Summary" :"David's son Solomon builds the temple, but after centuries of rejecting God, the Babylonians take the southern Israelites captive and destroy the temple."
			},
			"Ezra"           :{
				"Author"  :"Ezra",
				"Chapters":10,
				"Summary" :"The Israelites rebuild the temple in Jerusalem, and a scribe named Ezra teaches the people to once again obey God's laws."
			},
			"Nehemiah"       :{
				"Author"  :"Ezra",
				"Chapters":13,
				"Summary" :"The city of Jerusalem is in bad shape, so Nehemiah rebuilds the wall around the city."
			},
			"Esther"         :{
				"Author"  :"Mordechai",
				"Chapters":10,
				"Summary" :"Someone hatches a genocidal plot to bring about Israel's extinction, and Esther must face the emperor to ask for help."
			},
			"Job"            :{
				"Author"  :"Possibly Job, Elihu, or Solomon",
				"Chapters":42,
				"Summary" :"Satan attacks a righteous man named Job, and Job and his friends argue about why terrible things are happening to him."
			},
			"Psalms"         :{
				"Author"  :"King David",
				"Chapters":150,
				"Summary" :"A collection of 150 songs that Israel sang to God (and to each other)-kind of like a hymnal for the ancient Israelites."
			},
			"Proverbs"       :{
				"Author"  :"Solomon",
				"Chapters":31,
				"Summary" :"A collection of sayings written to help people make wise decisions that bring about justice."
			},
			"Ecclesiastes"   :{
				"Author"  :"Solomon",
				"Chapters":12,
				"Summary" :"A philosophical exploration of the meaning of life-with a surprisingly nihilistic tone for the Bible."
			},
			"Song of Solomon":{
				"Author"  :"Solomon",
				"Chapters":8,
				"Summary" :"A love song (or collection of love songs) celebrating love, desire, and marriage."
			},
			"Isaiah"         :{
				"Author"  :"Isaiah",
				"Chapters":66,
				"Summary" :"God sends the prophet Isaiah to warn Israel of future judgment-but also to tell them about a coming king and servant who will \"bear the sins of many.\""
			},
			"Jeremiah"       :{
				"Author"  :"Jeremiah",
				"Chapters":52,
				"Summary" :"God sends a prophet to warn Israel about the coming Babylonian captivity, but the people don't take the news very well."
			},
			"Lamentations"   :{
				"Author"  :"Jeremiah",
				"Chapters":5,
				"Summary" :"A collection of dirges lamenting the fall of Jerusalem after the Babylonian attacks."
			},
			"Ezekiel"        :{
				"Author"  :"Ezekiel",
				"Chapters":47,
				"Summary" :"God chooses a man to speak for Him to Israel, to tell them the error of their ways and teach them justice: Ezekiel."
			},
			"Daniel"         :{
				"Author"  :"Daniel",
				"Chapters":11,
				"Summary" :"Daniel becomes a high-ranking wise man in the Babylonian and Persian empires, and has prophetic visions concerning Israel's future."
			},
			"Hosea"          :{
				"Author"  :"Hosea",
				"Chapters":13,
				"Summary" :"Hosea is told to marry a prostitute who leaves him, and he must bring her back: a picture of God's relationship with Israel."
			},
			"Joel"           :{
				"Author"  :"Joel",
				"Chapters":2,
				"Summary" :"God sends a plague of locusts to Judge Israel, but his judgment on the surrounding nations is coming, too."
			},
			"Amos"           :{
				"Author"  :"Amos",
				"Chapters":8,
				"Summary" :"A shepherd named Amos preaches against the injustice of the Northern Kingdom of Israel."
			},
			"Obadiah"        :{
				"Author"  :"Obadiah",
				"Chapters":1,
				"Summary" :"Obadiah warns the neighboring nation of Edom that they will be judged for plundering Jerusalem."
			},
			"Jonah"          :{
				"Author"  :"Jonah",
				"Chapters":4,
				"Summary" :"A disobedient prophet runs from God, is swallowed by a great fish, and then preaches God's message to the city of Ninevah."
			},
			"Micah"          :{
				"Author"  :"Micah",
				"Chapters":7,
				"Summary" :"Micah confronts the leaders of Israel and Judah regarding their injustice, and prophecies that one day the Lord himself will rule in perfect justice."
			},
			"Nahum"          :{
				"Author"  :"Nahum",
				"Chapters":3,
				"Summary" :"Nahum foretells of God's judgment on Nineveh, the capital of Assyria."
			},
			"Habakkuk"       :{
				"Author"  :"Habakkuk",
				"Chapters":3,
				"Summary" :"Habakkuk pleads with God to stop the injustice and violence in Judah, but is surprised to find that God will use the even more violent Babylonians to do so."
			},
			"Zephaniah"      :{
				"Author"  :"Zephaniah",
				"Chapters":3,
				"Summary" :"God warns that he will judge Israel and the surrounding nations, but also that he will restore them in peace and justice."
			},
			"Haggai"         :{
				"Author"  :"Haggai",
				"Chapters":2,
				"Summary" :"The people have abandoned the work of restoring God's temple in Jerusalem, and so Haggai takes them to task."
			},
			"Zechariah"      :{
				"Author"  :"Zechariah",
				"Chapters":14,
				"Summary" :"The prophet Zechariah calls Israel to return to God, and records prophetic visions that show what's happening behind the scenes."
			},
			"Malachi"        :{
				"Author"  :"Malachi",
				"Chapters":4,
				"Summary" :"God has been faithful to Israel, but they continue to live disconnected from him-so God sends Malachi to call them out."
			},
			"Matthew"        :{
				"Author"  :"Matthew",
				"Chapters":28,
				"Summary" :"This is an account of Jesus' life, death, and resurrection, focusing on Jesus' role as the true king of the Jews."
			},
			"Mark"           :{
				"Author"  :"Mark",
				"Chapters":16,
				"Summary" :"This brief account of Jesus' earthly ministry highlights Jesus' authority and servanthood."
			},
			"Luke"           :{
				"Author"  :"Luke",
				"Chapters":24,
				"Summary" :"Luke writes the most thorough account of Jesus' life, pulling together eyewitness testimonies to tell the full story of Jesus."
			},
			"John"           :{
				"Author"  :"John",
				"Chapters":21,
				"Summary" :"John lists stories of signs and miracles with the hope that readers will believe in Jesus."
			},
			"Acts"           :{
				"Author"  :"Luke",
				"Chapters":28,
				"Summary" :"Jesus returns to the Father, the Holy Spirit comes to the church, and the gospel of Jesus spreads throughout the world."
			},
			"Romans"         :{
				"Author"  :"Paul",
				"Chapters":16,
				"Summary" :"Paul summarizes how the gospel of Jesus works in a letter to the churches at Rome, where he plans to visit."
			},
			"1 Corinthians"  :{
				"Author"  :"Paul",
				"Chapters":15,
				"Summary" :"Paul writes a disciplinary letter to a fractured church in Corinth, and answers some questions that they've had about how Christians should behave."
			},
			"2 Corinthians"  :{
				"Author"  :"Paul",
				"Chapters":12,
				"Summary" :"Paul writes a letter of reconcilation to the church at Corinth, and clears up some concerns that they have."
			},
			"Galatians"      :{
				"Author"  :"Paul",
				"Chapters":5,
				"Summary" :"Paul hears that the Galatian churches have been lead to think that salvation comes from the law of Moses, and writes a (rather heated) letter telling them where the false teachers have it wrong."
			},
			"Ephesians"      :{
				"Author"  :"Paul",
				"Chapters":5,
				"Summary" :"Paul writes to the church at Ephesus about how to walk in grace, peace, and love."
			},
			"Philippians"    :{
				"Author"  :"Paul",
				"Chapters":3,
				"Summary" :"An encouraging letter to the church of Philippi from Paul, telling them how to have joy in Christ."
			},
			"Colossians"     :{
				"Author"  :"Paul",
				"Chapters":3,
				"Summary" :"Paul writes the church at Colossae a letter about who they are in Christ, and how to walk in Christ."
			},
			"1 Thessalonians":{
				"Author"  :"Paul",
				"Chapters":4,
				"Summary" :"Paul has heard a good report on the church at Thessalonica, and encourages them to \"excel still more\" in faith, hope, and love."
			},
			"2 Thessalonians":{
				"Author"  :"Paul",
				"Chapters":2,
				"Summary" :"Paul instructs the Thessalonians on how to stand firm until the coming of Jesus."
			},
			"1 Timothy"      :{
				"Author"  :"Paul",
				"Chapters":5,
				"Summary" :"Paul gives his protege Timothy instructions on how to lead a church with sound teaching and a godly example."
			},
			"2 Timothy"      :{
				"Author"  :"Paul",
				"Chapters":3,
				"Summary" :"Paul is nearing the end of his life, and encourages Timothy to continue preaching the word."
			},
			"Titus"          :{
				"Author"  :"Paul",
				"Chapters":2,
				"Summary" :"Paul advises Titus on how to lead orderly, counter-cultural churches on the island of Crete."
			},
			"Philemon"       :{
				"Author"  :"Philemon",
				"Chapters":1,
				"Summary" :"Paul strongly recommends that Philemon accept his runaway slave as a brother, not a slave."
			},
			"Hebrews"        :{
				"Author"  :"Unknown",
				"Chapters":12,
				"Summary" :"A letter encouraging Christians to cling to Christ despite persecution, because he is greater."
			},
			"James"          :{
				"Author"  :"James",
				"Chapters":4,
				"Summary" :"A letter telling Christians to live in ways that demonstrate their faith in action."
			},
			"1 Peter"        :{
				"Author"  :"Peter",
				"Chapters":4,
				"Summary" :"Peter writes to Christians who are being prosecuted, encouraging them to testify to the truth and live accordingly."
			},
			"2 Peter"        :{
				"Author"  :"Peter",
				"Chapters":2,
				"Summary" :"Peter writes a letter reminding Christians about the truth of Jesus, and warning them that false teachers will come."
			},
			"1 John"         :{
				"Author"  :"John",
				"Chapters":4,
				"Summary" :"John writes a letter to Christians about keeping Jesus' commands, loving one another, and important things they should know."
			},
			"2 John"         :{
				"Author"  :"John",
				"Chapters":1,
				"Summary" :"A very brief letter about walking in truth, love, and obedience."
			},
			"3 John"         :{
				"Author"  :"John",
				"Chapters":1,
				"Summary" :"An even shorter letter about Christian fellowship."
			},
			"Jude"           :{
				"Author"  :"Jude",
				"Chapters":1,
				"Summary" :
					"A letter encouraging Christians to content for the faith," +
					"even though ungodly persons have crept in unnoticed."
			},
			"Revelation"     :{
				"Author"  :"John",
				"Chapters":21,
				"Summary" :
					"John sees visions of things that have been, things that are, and things that are yet to come."
			}
		}
	def get_info ( self, book: str ) -> dict:
		"""
		Returns data on a book.
		:param book: The book.
		:return: The results.
		"""
		return self.data.get( book )

# <editor-fold desc="File Readers">
try:
	READER = open(
		VERSE_DISABLES_PATH,
		'r'
	)
	VERSE_DISABLE_LIST = ast.literal_eval( READER.read( ) )
	READER.close( )
	del READER
except Exception:
	pass

try:
	READER = open(
		BIBLE_VERSIONS_PATH,
		'r'
	)
	BIBLE_VERSIONS = ast.literal_eval( READER.read( ) )
	READER.close( )
	del READER
except Exception:
	pass

try:
	READER = open(
		BIBLE_TYPES_PATH,
		'r'
	)
	BIBLE_TYPES = ast.literal_eval( READER.read( ) )
	READER.close( )
	del READER
except Exception:
	pass

try:
	READER = open(
		CHANNEL_LIST_PATH,
		'r'
	)
	DEFAULT_CHANNEL = ast.literal_eval( READER.read( ) )
	READER.close( )
	del READER
except Exception:
	pass

try:
	READER = open(
		LAST_DAY_PATH,
		'r'
	)
	LAST_DAY = int( READER.read( ) )
	READER.close( )
	del READER
except Exception:
	pass

try:
	if LAST_DAY == datetime.now( ).day:
		READER = open(
			VOTD_PATH,
			'r'
		)
		VOTD = READER.read( )
		READER.close( )
		del READER
except Exception:
	pass

# </editor-fold>

def sqlread ( cmd: str ):
	"""
	Reads from SQL.
	:param cmd: The SQL Read command.
	:return: The data.
	"""
	CURSOR.execute( cmd )
	return CURSOR.fetchall( )

def parse_num ( num: int ) -> str:
	"""
	Parses a number to a more easily readable string.
	:param num: A number.
	:return: A string representation of the number.
	"""
	_num = str( num )
	_num = _num[ ::-1 ]
	_num = ','.join( [
		_num[ i:i + 3 ]
		for i in range(
			0,
			len( _num ),
			3
		)
	] )[ ::-1 ]
	return str( _num )

def is_ascii ( msg: str ):
	"""
	Checks for non-ascii characters in msg.
	:param msg: A string.
	:return: True/False
	"""
	return all(
		[
			ord( C ) < 128
			for C in msg
		 ]
	)

def check ( *msgs: str ):
	"""
	Checks for non-ascii characters in each string in the parameters.
	:param msgs:
	:return: The first instance of non-ascii string, or the last if none is found.
	"""
	for msg in msgs:
		if is_ascii( msg ):
			return msg
	return msgs[ len( msgs ) - 1 ]

def save ( sid: str ):
	"""
	Saves plugin data.
	:param sid: The server id.
	"""
	# <editor-fold desc="version_list">
	writer = open(
		BIBLE_VERSIONS_PATH,
		'w'
	)
	writer.write(
		str(
			BIBLE_VERSIONS
		)
	)
	writer.close( )
	# </editor-fold>
	# <editor-fold desc="type_list">
	writer = open(
		BIBLE_TYPES_PATH,
		'w'
	)
	writer.write(
		str(
			BIBLE_TYPES
		)
	)
	writer.close( )
	# </editor-fold>
	# <editor-fold desc="verse_disables">
	writer = open( VERSE_DISABLES_PATH, 'w' )
	writer.write( str( VERSE_DISABLE_LIST ) )
	writer.close( )
	# </editor-fold>
	# <editor-fold desc="c_list">
	writer = open( CHANNEL_LIST_PATH, 'w' )
	writer.write( str( DEFAULT_CHANNEL ) )
	writer.close( )
	# </editor-fold>
	# <editor-fold desc="d_last_day">
	writer = open( LAST_DAY_PATH, 'w' )
	writer.write( str( LAST_DAY ) )
	writer.close( )
	# </editor-fold>
	# <editor-fold desc="votd_d">
	writer = open( VOTD_PATH, 'w' )
	writer.write( VOTD )
	writer.close( )
	# </editor-fold>

	# <editor-fold desc="PATH CHECK: _disabled_channels">
	if not os.path.exists( DISABLED_CHANNELS_PATH ):
		os.makedirs( DISABLED_CHANNELS_PATH )
	# </editor-fold>
	# <editor-fold desc="PATH CHECK: _disabled_users">
	if not os.path.exists( DISABLED_USERS_PATH ):
		os.makedirs( DISABLED_USERS_PATH )
	# </editor-fold>

	# <editor-fold desc="_disabled_channels">
	writer = open( f"{DISABLED_CHANNELS_PATH}{sid}.txt", 'w' )
	writer.write( str( DISABLED_CHANNELS ) )
	writer.close( )
	# </editor-fold>
	# <editor-fold desc="_disabled_users">
	writer = open( f"{DISABLED_USERS_PATH}{sid}.txt", 'w' )
	writer.write( str( DISABLED_USERS ) )
	writer.close( )
	# </editor-fold>
	del writer

def abbr ( _msg: str ) -> str:
	"""
	Checks for book abbreviations in `ret`, and replaces them with the entire book title.
	:param _msg: A string.
	:return: The new string.
	"""
	books = {
		"Gen "  :"Genesis ",
		"Ex "   :"Exodus ",
		"Lev "  :"Leviticus ",
		"Num "  :"Numbers ",
		"Dt "   :"Deuteronomy ",
		"Josh " :"Joshua ",
		"Jdg "  :"Judges ",
		"Rth "  :"Ruth ",
		"1 Sam ":"1 Samuel ",
		"2 Sam ":"2 Samuel ",
		"1 Kin ":"1 Kings ",
		"2 Kin ":"2 Kings ",
		"1 Chr ":"1 Chronicles ",
		"2 Chr ":"2 Chronicles ",
		"Neh "  :"Nehemiah ",
		"Est "  :"Esther ",
		"Psa "  :"Psalms ",
		"Pro "  :"Proverbs ",
		"Ecc "  :"Ecclesiastes ",
		"Sos "  :"Songs ",
		"Isa "  :"Isaiah ",
		"Jer "  :"Jeremiah ",
		"Lam "  :"Lamentations ",
		"Eze "  :"Ezekiel ",
		"Dan "  :"Daniel ",
		"Hos "  :"Hosea ",
		"Oba "  :"Obadiah ",
		"Jon "  :"Jonah ",
		"Mic "  :"Micah ",
		"Nah "  :"Nahum ",
		"Hab "  :"Habakkuk ",
		"Zeph " :"Zephaniah ",
		"Hag "  :"Haggai ",
		"Zech " :"Zechariah ",
		"Mal "  :"Malachi ",
		"Mt "   :"Matthew ",
		"Mr "   :"Mark ",
		"Lk "   :"Luke ",
		"Jn "   :"John ",
		"Rom "  :"Romans ",
		"1 Cor ":"1 Corinthians ",
		"2 Cor ":"2 Corinthians ",
		"Gal "  :"Galations ",
		"Eph "  :"Ephesians ",
		"Phi "  :"Philippians ",
		"Col "  :"Colossians ",
		"1 The ":"1 Thessalonians ",
		"2 The ":"2 Thessalonians ",
		"1 Tim ":"1 Timothy ",
		"2 Tim ":"2 Timothy ",
		"Phil " :"Philemon ",
		"Heb "  :"Hebrews ",
		"Jam "  :"James ",
		"1 Pet ":"1 Peter ",
		"2 Pet ":"2 Peter ",
		"1 Jn " :"1 John ",
		"2 Jn " :"2 John ",
		"3 Jn " :"3 John ",
		"Rev "  :"Revelation "
	}
	for item in list( books.keys( ) ):
		_msg = _msg.lower( ).replace( item.lower( ), books[ item ] )
	for item in _msg.split( " " ):
		_msg = _msg.replace( item, item.capitalize( ) )
	del books
	return _msg

# noinspection PyUnusedLocal
def get_kjv_verse ( key: str, include_header: bool = True ) -> str:
	"""
	Fetch a verse from the King James Version of the Bible.
	:param key: A key to search for a verse with.
	:param include_header: Whether or not to include `key` at the beginning of the message.
	:return: A KJV Verse
	"""
	try:
		data = key.split( " " )
		book = ""
		chapter = ""
		verse = ""
		if len( data ) == 3:
			book = data[ 0 ] + " " + data[ 1 ]
			chapter = data[ 2 ].split( ":" )[ 0 ]
			verse = data[ 2 ].split( ":" )[ 1 ]
		else:
			book = data[ 0 ]
			chapter = data[ 1 ].split( ":" )[ 0 ]
			verse = data[ 1 ].split( ":" )[ 1 ]
		ret = ""
		if include_header is True:
			ret = f"**{key} ~ KJV**\n"
		ret += SQLKJV.read( book, chapter, verse )
		del data
		del book
		del chapter
		del verse
		return ret
	except Exception:
		return "No such verse!"

# noinspection PyUnusedLocal
def get_kjv_passage ( key: str, include_header: bool = True ) -> str:
	"""
	Fetches a passage from the KJV Bible.
	:param key: The verses to fetch.
	:param include_header: Whether or not to include `key` at the beginning of the reference.
	:return: The passage referred to by `key`
	"""
	stuffs = key.split( ":" )
	start = int( stuffs[ 1 ].split( "-" )[ 0 ] )
	end = int( stuffs[ 1 ].split( "-" )[ 1 ] )
	retpre = f"**{key} ~ KJV**\n"
	ret = ""
	data = key.split( " " )
	query = [ "", "", "" ]
	if len( data ) == 3:
		query = [ data[ 0 ] + " " + data[ 1 ], data[ 2 ].split( ":" )[ 0 ], data[ 2 ].split( ":" )[ 1 ] ]
	else:
		query = [ data[ 0 ], data[ 1 ].split( ":" )[ 0 ], data[ 1 ].split( ":" )[ 1 ] ]
	for i in range( start, end + 1 ):
		tmp = list( str( i ) )
		for index, item in enumerate( tmp ):
			tmp[ index ] = symbols.SYMBOLS[ "^" + item ]
		tmp = ''.join( tmp )
		ret += "{} {}\n".format(
			tmp,
			get_kjv_verse(
				query[ 0 ] + " " + query[ 1 ] + ":" + str( i ),
				include_header=False
			)
		)
		del tmp
	del stuffs
	del start
	del end
	del data
	del query
	return retpre + ret if include_header else ret

def get_niv_verse ( key: str, include_header: bool = True ) -> str:
	"""
	Fetch a verse from the King James Version of the Bible.
	:param key: A key to search for a verse with.
	:param include_header: Whether or not to include `key` at the beginning of the message.
	:return: A KJV Verse
	"""
	try:
		data = key.split( " " )
		if len( data ) == 3:
			book = data[ 0 ] + " " + data[ 1 ]
			chapter = data[ 2 ].split( ":" )[ 0 ]
			verse = data[ 2 ].split( ":" )[ 1 ]
		else:
			book = data[ 0 ]
			chapter = data[ 1 ].split( ":" )[ 0 ]
			verse = data[ 1 ].split( ":" )[ 1 ]
		ret = ""
		if include_header is True:
			ret = f"**{key} ~ KJV**\n"
		ret += SQLNIV.read( book, chapter, verse )
		del data
		del book
		del chapter
		del verse
		return ret
	except Exception:
		return "No such verse!"

# noinspection PyUnusedLocal
def get_niv_passage ( key: str, include_header: bool = True ) -> str:
	"""
	Fetches a passage from the KJV Bible.
	:param key: The verses to fetch.
	:param include_header: Whether or not to include `key` at the beginning of the reference.
	:return: The passage referred to by `key`
	"""
	stuffs = key.split( ":" )
	start = int( stuffs[ 1 ].split( "-" )[ 0 ] )
	end = int( stuffs[ 1 ].split( "-" )[ 1 ] )
	retpre = f"**{key} ~ NIV**\n"
	ret = ""
	data = key.split( " " )
	query = [ "", "", "" ]
	if len( data ) == 3:
		query = [ data[ 0 ] + " " + data[ 1 ], data[ 2 ].split( ":" )[ 0 ], data[ 2 ].split( ":" )[ 1 ] ]
	else:
		query = [ data[ 0 ], data[ 1 ].split( ":" )[ 0 ], data[ 1 ].split( ":" )[ 1 ] ]
	for i in range( start, end + 1 ):
		tmp = list( str( i ) )
		for index, item in enumerate( tmp ):
			tmp[ index ] = symbols.SYMBOLS[ "^" + item ]
		tmp = ''.join( tmp )
		ret += "{} {}\n".format(
			tmp,
			get_niv_verse(
				query[ 0 ] + " " + query[ 1 ] + ":" + str( i ),
				include_header=False
			)
		)
		del tmp
	del stuffs
	del start
	del end
	del data
	del query
	return retpre + ret if include_header else ret

# noinspection PyUnusedLocal
def get_akjv_verse ( key: str, include_header: bool = True ) -> str:
	"""
	Fetch a verse from the AKJV Bible.
	:param key: The verse to fetch.
	:param include_header: Whether or not to include `key` at the beginning of the reference.
	:return: The verse `key` refers to.
	"""
	try:
		data = key.split( " " )
		book = ""
		chapter = ""
		verse = ""
		if len( data ) == 3:
			book = data[ 0 ] + " " + data[ 1 ]
			chapter = data[ 2 ].split( ":" )[ 0 ]
			verse = data[ 2 ].split( ":" )[ 1 ]
		else:
			book = data[ 0 ]
			chapter = data[ 1 ].split( ":" )[ 0 ]
			verse = data[ 1 ].split( ":" )[ 1 ]
		ret = ""
		if include_header:
			ret = f"**{key} ~ AKJV**\n"
		ret += SQLD.read( book, chapter, verse )
		del data
		del book
		del chapter
		del verse
		return ret
	except Exception:
		return "No such verse!"

# noinspection PyUnusedLocal
def get_akjv_passage ( key: str, include_header: bool = True ) -> str:
	"""
	Fetch a passage from the AKJV Bible.
	:param key: The passage to fetch.
	:param include_header: Whether or not to include `key` at the beginning of the reference.
	:return: The passage `key` refers to.
	"""
	stuffs = key.split( ":" )
	start = int( stuffs[ 1 ].split( "-" )[ 0 ] )
	end = int( stuffs[ 1 ].split( "-" )[ 1 ] )
	retpre = f"**{key} ~ AKJV**\n"
	ret = ""
	data = key.split( " " )
	query = [ "", "", "" ]
	if len( data ) == 3:
		query = [ data[ 0 ] + " " + data[ 1 ], data[ 2 ].split( ":" )[ 0 ], data[ 2 ].split( ":" )[ 1 ] ]
	else:
		query = [ data[ 0 ], data[ 1 ].split( ":" )[ 0 ], data[ 1 ].split( ":" )[ 1 ] ]
	for i in range( start, end + 1 ):
		tmp = list( str( i ) )
		for index, item in enumerate( tmp ):
			tmp[ index ] = symbols.SYMBOLS[ "^" + item ]
		tmp = ''.join( tmp )
		ret += "{} {}\n".format(
			tmp,
			get_akjv_verse(
				query[ 0 ] + " " + query[ 1 ] + ":" + str( i ),
				include_header=False
			)
		)
		del tmp
	del stuffs
	del start
	del end
	del data
	del query
	return retpre + ret if include_header else ret

# noinspection PyUnusedLocal
def get_web_verse ( key: str, include_header: bool = True ) -> str:
	"""
	Fetch a verse from the WEB Bible.
	:param key: The verse to fetch.
	:param include_header: Whether or not to include `key` in the reference.
	:return: The referred verse.
	"""
	try:
		data = key.split( " " )
		book = ""
		chapter = ""
		verse = ""
		if len( data ) == 3:
			book = data[ 0 ] + " " + data[ 1 ]
			chapter = data[ 2 ].split( ":" )[ 0 ]
			verse = data[ 2 ].split( ":" )[ 1 ]
		else:
			book = data[ 0 ]
			chapter = data[ 1 ].split( ":" )[ 0 ]
			verse = data[ 1 ].split( ":" )[ 1 ]
		ret = ""
		if include_header:
			ret = f"**{key} ~ WEB**\n"
		ret += SQLWEB.read( book, chapter, verse )
		del data
		del book
		del chapter
		del verse
		return ret
	except Exception:
		return "No such verse!"

# noinspection PyUnusedLocal
def get_web_passage ( key: str, include_header: bool = True ) -> str:
	"""
	Fetch a passage from the WEB Bible.
	:param key: The passage to fetch.
	:param include_header: Whether or not to include `key` in the reference.
	:return: The referred passage.
	"""
	stuffs = key.split( ":" )
	start = int( stuffs[ 1 ].split( "-" )[ 0 ] )
	end = int( stuffs[ 1 ].split( "-" )[ 1 ] )
	retpre = f"**{key} ~ WEB**\n"
	ret = ""
	data = key.split( " " )
	query = [ "", "", "" ]
	if len( data ) == 3:
		query = [ data[ 0 ] + " " + data[ 1 ], data[ 2 ].split( ":" )[ 0 ], data[ 2 ].split( ":" )[ 1 ] ]
	else:
		query = [ data[ 0 ], data[ 1 ].split( ":" )[ 0 ], data[ 1 ].split( ":" )[ 1 ] ]
	for i in range( start, end + 1 ):
		tmp = list( str( i ) )
		for index, item in enumerate( tmp ):
			tmp[ index ] = symbols.SYMBOLS[ "^" + item ]
		tmp = ''.join( tmp )
		ret += "{} {}\n".format(
			tmp,
			get_web_verse(
				query[ 0 ] + " " + query[ 1 ] + ":" + str( i ),
				include_header=False
			)
		)
		del tmp
	del stuffs
	del start
	del end
	del data
	del query
	return retpre + ret if include_header else ret

# noinspection PyShadowingNames
def get_chapter ( key: str, version: str ) -> str:
	"""
	Fetch a chapter from the Bible. Deprecated due to errors.
	:param key: The reference.
	:param version: The bible version.
	:return: The chapter text.
	"""
	ret = "{}\n".format( key )
	res = ""
	if version == "kjv":
		res = SQLKJV.execute( "SELECT * FROM kjv WHERE key LIKE '{}:%';".format( key ) )
	elif version == "akjv":
		res = SQLD.execute( "SELECT * FROM akjv WHERE key LIKE '{}:%';".format( key ) )
	elif version == "web":
		res = SQLWEB.execute( "SELECT * FROM web WHERE key LIKE '{}:%';".format( key ) )
	for result in res:
		verse = result[ 0 ].split( ":" )[ 1 ]
		ret += f"[{verse}] {result[1]}\n"
		del verse
	del res
	return ret

# noinspection PyShadowingNames
def get_random_verse ( version: str ) -> str:
	"""
	Fetches a random verse from `version`
	:param version: The version to use.
	:return: A random verse in `version`
	"""
	book = random.choice( AKJV_BOOKS )
	res = ""
	if version == "kjv":
		res = SQLKJV.execute( "SELECT * FROM kjv WHERE key LIKE '{}%'".format( book ) )
	elif version == "akjv":
		res = SQLD.execute( "SELECT * FROM akjv WHERE key LIKE '{}%'".format( book ) )
	elif version == "web":
		res = SQLWEB.execute( "SELECT * FROM web WHERE key LIKE '{}%'".format( book ) )
	elif version == "niv":
		res = SQLNIV.execute( "SELECT * FROM niv WHERE key LIKE '{}%".format( book ) )
	selected_verse = random.choice( res )
	ret = f"{selected_verse[0]}\n{selected_verse[1]}"
	del selected_verse
	del book
	del res
	return ret

def search_for_verse ( key: str, page: int = 0, version: str = "kjv" ) -> str:
	"""
	Fetch search results for `key` in the Bible
	:param key: The key to search for.
	:param page: The page number. Default to 0 (first 10 results).
	:param version: The version. Always a string.
	:return: The search results.
	"""
	res = ""
	if version == "kjv":
		res = SQLKJV.execute( f"SELECT * FROM kjv WHERE value LIKE '%{key}%'" )
	elif version == "akjv":
		res = SQLD.execute( f"SELECT * FROM akjv WHERE value LIKE '%{key}%'" )
	elif version == "web":
		res = SQLWEB.execute( f"SELECT * FROM web WHERE value LIKE '%{key}%'" )
	elif version == "niv":
		res = SQLNIV.execute( f"SELECT * FROM niv WHERE value LIKE '%{key}%'" )

	ret = "```"
	total = 0
	if len( res ) > page * 10 + 10:
		for i in range( page * 10, page * 10 + 10 ):
			ret += "{}\n".format( res[ i ][ 0 ] )
	elif res:
		for item in res:
			ret += f"{item[0]}\n"

	for item in res:
		total += len( re.findall( key, item[ 1 ], flags=2 ) )
	pages = parse_num( int( math.ceil( total / 10 ) ) )
	ret += f"{parse_num(total)} occurences found, {pages} pages overall!```"
	del res
	del total
	del pages
	return ret

def format_message ( cont: str ) -> list:
	"""
	Format a message to use with discord (2000 characters long) including ``` on each side.
	:param cont: The string to format.
	:return: A list of strings with each section of text.
	"""
	return [
		f"{item}"
		for item in [
			cont[ i:i + 1000 ]
			for i in range( 0, len( cont ), 1000 )
		]
	] if len( cont ) > 1994 else [
		f"```{cont}```"
	]

def read ( sid: str ):
	"""
	Read plugin data.
	:param sid: The id of the server to read data from.
	"""
	global DISABLED_CHANNELS, DISABLED_USERS
	try:
		# noinspection PyShadowingNames
		reader_obj = open( f"{DISABLED_CHANNELS_PATH}{sid}.txt", 'r' )
		DISABLED_CHANNELS = ast.literal_eval( reader_obj.read( ) )
		reader_obj.close( )
		del reader_obj
	except Exception:
		DISABLED_CHANNELS = [ ]
	try:
		# noinspection PyShadowingNames
		reader_obj = open( f"{DISABLED_USERS_PATH}{sid}.txt", 'r' )
		DISABLED_USERS = ast.literal_eval( reader_obj.read( ) )
		reader_obj.close( )
		del reader_obj
	except Exception:
		DISABLED_USERS = [ ]

	if not os.path.exists( f"{DISCORD_SETTINGS_PATH}\\SERVER SETTINGS\\{sid}\\" ):
		os.makedirs( f"{DISCORD_SETTINGS_PATH}\\SERVER SETTINGS\\{sid}\\" )

def cap_all_words ( text: str ):
	"""
	Capitalizes every word in a string.
	:param text: The text to capitalize.
	"""
	ret = [ ]
	for seq in text.split( " " ):
		ret.append( seq.capitalize( ) )
	return ' '.join( ret )

# noinspection PyUnresolvedReferences
class Formatting:
	"""
	Applies Discord Markup formatting to a message.
	"""
	BOLD = "**"
	ITALIC = "*"
	UNDERLINE = "__"
	STRIKETHROUGH = "~~"
	CODE_BLOCK = "```"
	INLINE_CODE = "`"
	def __init__ ( self ):
		self.placeholder = ""
	@staticmethod
	def apply_formatting ( string: str, indices: list, types: list ) -> str:
		"""
		:param string: The string to format.
		:param indices: A list of indexes at which to apply the formatting.
		:param types: A list of the format types to use. Each item can be combined.
		:return: The string, with formatting applied.
		"""

		repl = ""

		# Converts data given to a dictionary of index:type
		items = dict( )
		for index, item in enumerate( indices ):
			items[ str( item ) ] = types[ index ]

		# For each item in items, apply formatting appropriately.
		keys = items.keys( )
		for index, item in enumerate( keys ):
			format_code = items[ item ]
			if index != 0:
				repl += string[ int( keys[ index - 1 ] ):int( item ) ]
			else:
				repl += string[ 0:int( item ) ]
			repl += format_code

		return repl

class Commands:
	"""
	Command methods for the Bible Module.
	"""
	class Member:
		"""
		For Everyone!
		"""
		@staticmethod
		async def ping ( message: discord.Message ):
			"""
			Pings the bot.
			:param message: A discord.Message object.
			"""
			timestamp = datetime.now( ) - message.timestamp
			await CLIENT.send_message(
				message.channel,
				f"```LogBot Bible Online ~ {round(timestamp.microseconds / 1000)}```"
			)
			del timestamp
		@staticmethod
		async def verse_search ( message: discord.Message, prefix: str ):
			"""
			Searches the Bible for a specific phrase.
			:param message: A discord.Message object.
			:param prefix: The server's prefix.
			"""
			await CLIENT.send_typing( message.channel )
			content = message.content.replace( f"{prefix}verse search", "" )
			page = 0
			if content.startswith( "." ):
				page = int( content.split( " " )[ 0 ].replace( ".", "" ) )
			key = content.replace( f".{page} ", "" )
			for item in format_message(
					search_for_verse(
						key,
						page=page,
						version=BIBLE_VERSIONS[
							message.author.id
						]
					)
			):
				await CLIENT.send_message( message.channel, item )
			del content
			del page
			del key
		@staticmethod
		async def verse_random ( message: discord.Message ):
			"""
			Sends a random verse.
			:param message: A discord.Message object.
			"""
			await CLIENT.send_typing( message.channel )
			verse = get_random_verse( BIBLE_VERSIONS[ message.author.id ] )
			if BIBLE_TYPES[ message.author.id ] == "text":
				for item in format_message( verse ):
					await CLIENT.send_message( message.channel, item )
			else:
				stuffs = verse.split( "\n" )
				embed_obj = discord.Embed(
					title=BIBLE_VERSIONS[
						message.author.id
					],
					colour=discord.Colour.green( )
				) \
					.add_field( name=stuffs[ 0 ], value=stuffs[ 1 ] )
				await CLIENT.send_message( message.channel, "Here you go!", embed=embed_obj )
				del embed_obj
				del stuffs
			del verse
		@staticmethod
		async def verse_info ( message: discord.Message, bible_info: BI, prefix: str ):
			"""
			Sends info on a specific book of the bible.
			:param message: A discord.Message object.
			:param bible_info: The BI() class.
			:param prefix: The server's prefix.
			"""
			if ":book" in message.content:
				cont = message.content.replace( f"{prefix}verse info:book ", "" )
				data = bible_info.get_info( cont.replace( "Songs", "Song of Solomon" ) )
				ret = f"""{cont}
				Author: {data['Author']}
				Chapters: {data['Chapters']}
				Summary: {data['Summary']}""".replace( "\t", "" )
				for item in format_message( ret ):
					await CLIENT.send_message( message.channel, item )
				del cont
				del ret
			elif ":chapter" in message.content:
				cont = message.content.replace( f"{prefix}verse info:chapter ", "" )
				ret = {
					"Verses"    :0,
					"Words"     :0,
					"Characters":0
				}
				stuffs = [ ]
				stapp = stuffs.append
				index = 0
				while True:
					index += 1
					try:
						stapp( SQLKJV.read( cont.split( " " )[ 0 ], cont.split( " " )[ 1 ], str( index ) ) )
					except Exception:
						break
				ret[ "Verses" ] = len( stuffs )
				# noinspection PyUnusedLocal
				for item in stuffs:
					ret[ "Words" ] += len( item.split( " " ) )
					ret[ "Characters" ] += len( item )
				await CLIENT.send_message(
					message.channel,
					f"```Info for {cont}\n"
					f"Verses: {ret['Verses']}\n"
					f"Words: {ret['Words']}\n"
					f"Characters: {ret['Characters']}```"
				)
				del cont
				del stuffs
				del ret
				del stapp
				del index
			elif ":verse" in message.content:
				cont = message.content.replace( f"{prefix}verse info:verse ", "" )
				verse_str = get_kjv_verse( cont, include_header=False )
				words = len( verse_str.split( " " ) )
				characters = len( verse_str )
				await CLIENT.send_message(
					message.channel,
					f"```Info for {cont}\nWords: {words}\nCharacters: {characters}```"
				)
				del cont
		@staticmethod
		async def verse_help ( message: discord.Message ):
			"""
			Sends a list of book abbreviations used by this bot.
			:param message: A discord.Message object.
			"""
			ret = "```Book Abbreviations:\n"
			books = {
				"Gen"  :"Genesis",
				"Ex"   :"Exodus",
				"Lev"  :"Leviticus",
				"Num"  :"Numbers",
				"Dt"   :"Deuteronomy",
				"Josh" :"Joshua",
				"Jdg"  :"Judges",
				"Rth"  :"Ruth",
				"Ezra" :"Ezra",
				"1 Sam":"1 Samuel",
				"2 Sam":"2 Samuel",
				"1 Kin":"1 Kings",
				"2 Kin":"2 Kings",
				"1 Chr":"1 Chronicles",
				"2 Chr":"2 Chronicles",
				"Neh"  :"Nehemiah",
				"Est"  :"Esther",
				"Job"  :"Job",
				"Psa"  :"Psalms",
				"Pro"  :"Proverbs",
				"Ecc"  :"Ecclesiastes",
				"Sos"  :"Songs",
				"Isa"  :"Isaiah",
				"Jer"  :"Jeremiah",
				"Lam"  :"Lamentations",
				"Eze"  :"Ezekiel",
				"Dan"  :"Daniel",
				"Hos"  :"Hosea",
				"Joel" :"Joel",
				"Amos" :"Amos",
				"Oba"  :"Obadiah",
				"Jon"  :"Jonah",
				"Mic"  :"Micah",
				"Nah"  :"Nahum",
				"Hab"  :"Habakkuk",
				"Zeph" :"Zephaniah",
				"Hag"  :"Haggai",
				"Zech" :"Zechariah",
				"Mal"  :"Malachi",
				"Mt"   :"Matthew",
				"Mr"   :"Mark",
				"Lk"   :"Luke",
				"Jn"   :"John",
				"Acts" :"Acts",
				"Rom"  :"Romans",
				"1 Cor":"1 Corinthians",
				"2 Cor":"2 Corinthians",
				"Gal"  :"Galations",
				"Eph"  :"Ephesians",
				"Phi"  :"Philippians",
				"Col"  :"Colossians",
				"1 The":"1 Thessalonians",
				"2 The":"2 Thessalonians",
				"1 Tim":"1 Timothy",
				"2 Tim":"2 Timothy",
				"Titus":"Titus",
				"Phil" :"Philemon",
				"Heb"  :"Hebrews",
				"Jam"  :"James",
				"1 Pet":"1 Peter",
				"2 Pet":"2 Peter",
				"1 Jn" :"1 John",
				"2 Jn" :"2 John",
				"3 Jn" :"3 John",
				"Jude" :"Jude",
				"Rev"  :"Revelation"
			}
			ret += '\n'.join( [
				f"{item} ~ {book}"
				for book, item in books.items( )
			] ) + "```"
			await CLIENT.send_message( message.channel, ret )
			del ret
			del books
		@staticmethod
		async def verse_compare ( message: discord.Message, prefix: str ):
			"""
			Compares verses from two different versions.
			:param message: A discord.Message object.
			:param prefix: The server's prefix.
			"""
			content = message.content.replace( f"{prefix}verse compare ", "" )
			if BIBLE_TYPES[ message.author.id ] == "text":
				await CLIENT.send_message( message.channel, "```" + content + "```" )
				if "-" in content:
					stuffs = [
						get_kjv_passage(
							content,
							include_header=False
						),
						get_akjv_passage(
							content,
							include_header=False
						),
						get_web_passage(
							content,
							include_header=False
						)
					]
					for item in stuffs:
						for msg in format_message( item ):
							await CLIENT.send_message( message.channel, msg )
					del stuffs
				else:
					stuffs = [
						get_kjv_verse(
							content,
							include_header=False
						),
						get_akjv_verse(
							content,
							include_header=False
						),
						get_web_verse(
							content,
							include_header=False
						)
					]
					for item in stuffs:
						await CLIENT.send_message( message.content, f"```{item}```" )
					del stuffs
			else:
				if "-" in content:
					stuffs = [
						get_kjv_passage(
							content,
							include_header=False
						),
						get_akjv_passage(
							content,
							include_header=False
						),
						get_web_passage(
							content,
							include_header=False
						)
					]
					embed_obj = discord.Embed(
						title="Verse Compare",
						description=f"Comparison of {content}",
						colour=discord.Colour.teal( )
					) \
						.add_field( name="KJV", value=stuffs[ 0 ] ) \
						.add_field( name="AKJV", value=stuffs[ 1 ] ) \
						.add_field( name="WEB", value=stuffs[ 2 ] )
					await CLIENT.send_message( message.channel, "Here you go!", embed=embed_obj )
					del stuffs
					del embed_obj
				else:
					stuffs = [
						get_kjv_verse(
							content,
							include_header=False
						),
						get_akjv_verse(
							content,
							include_header=False
						),
						get_web_verse(
							content,
							include_header=False
						)
					]
					embed_obj = discord.Embed(
						title="Verse Compare",
						description=f"Comparation of {content}",
						colour=discord.Colour.teal( )
					) \
						.add_field( name="KJV", value=stuffs[ 0 ] ) \
						.add_field( name="AKJV", value=stuffs[ 1 ] ) \
						.add_field( name="WEB", value=stuffs[ 2 ] )
					await CLIENT.send_message( message.channel, "Here you go!", embed=embed_obj )
					del stuffs
					del embed_obj
			del content
		@staticmethod
		async def send_votd ( message: discord.Message ):
			"""
			Sends the Verse of the Day through chat.
			:param message: A discord.Message object.
			"""
			embed_obj = discord.Embed(
				title="Verse of the Day",
				description="Version: akjv",
				colour=discord.Colour.dark_blue( )
			)
			if "-" in VOTD:
				embed_obj.add_field( name=VOTD, value=get_akjv_passage( VOTD, include_header=False ) )
			else:
				embed_obj.add_field( name=VOTD, value=get_akjv_verse( VOTD, include_header=False ) )
			await CLIENT.send_message( message.channel, "", embed=embed_obj )
			del embed_obj
		@staticmethod
		async def setversion ( message: discord.Message, prefix: str ):
			"""
			Sets the preferred bible version.
			:param message: A discord.Message object.
			:param prefix: The server's prefix.
			"""
			new_version = message.content.replace( f"{prefix}setversion ", "" )
			if new_version == "kjv" or new_version == "akjv" or new_version == "web" or new_version == "niv":
				BIBLE_VERSIONS[ message.author.id ] = new_version
			await CLIENT.send_message( message.channel, f"Set version to {new_version}" )
			del new_version
		@staticmethod
		async def settype ( message: discord.Message, prefix: str ):
			"""
			Sets the verse return type.
			:param message: A discord.Message object.
			:param prefix: The server's prefix.
			"""
			new_type = message.content.replace( f"{prefix}settype ", "" ).lower( )
			if new_type == "text" or new_type == "embed":
				BIBLE_TYPES[ message.author.id ] = new_type
			await CLIENT.send_message( message.channel, f"```Set the type to: {new_type}```" )
			del new_type
		@staticmethod
		async def disables ( message: discord.Message ):
			"""
			Sends a list of disabled commands.
			:param message: A discord.Message object.
			"""
			ret = [
				str( await CLIENT.get_channel( _id ) )
				for _id in DISABLED_CHANNELS
				if CLIENT.get_channel( _id ).server == message.server
			]
			ret = ', '.join( ret )
			try:
				await CLIENT.send_message( message.channel, ret )
			except Exception:
				await CLIENT.send_message( message.channel, "```No channels have been disabled!```" )
			del ret
			ret = [ ]
			for _id in DISABLED_USERS:
				try:
					# noinspection PyUnresolvedReferences
					tmp_user = await CLIENT.get_user_info( _id )
					if not discord.utils.find( lambda u:u.id == _id, message.server.members ) is None:
						ret.append( str( tmp_user ) )
				except Exception:
					traceback.format_exc( )
			ret = ', '.join( ret )
			try:
				await CLIENT.send_message( message.channel, ret )
			except Exception:
				await CLIENT.send_message( message.channel, "```No users have been disabled!```" )
			del ret
	class Admin:
		"""
		Commands for Admins only.
		"""
		@staticmethod
		async def setchannel ( message: discord.Message ):
			"""
			Sets the daily verse channel.
			:param message: A discord.Message object.
			"""
			if "None" in message.content:
				del DEFAULT_CHANNEL[ message.server.id ]
				await CLIENT.send_message( message.channel, "Set the default channel to None." )
			else:
				DEFAULT_CHANNEL[ message.server.id ] = message.channel_mentions[ 0 ].id
				await CLIENT.send_message(
					message.channel,
					f"Set the default channel to {message.channel_mentions[0].mention}"
				)
		@staticmethod
		async def disable ( message: discord.Message ):
			"""
			Disables verse recognition for the server.
			:param message: A discord.Message object.
			"""
			VERSE_DISABLE_LIST.append( message.server.id )
		@staticmethod
		async def enable ( message: discord.Message ):
			"""
			Enables verse recognition for the server.
			:param message: A discord.Message object.
			"""
			VERSE_DISABLE_LIST.remove( message.server.id )
		@staticmethod
		async def v_disable ( message: discord.Message ):
			"""
			Disabled commands.
			:param message: A discord.Message object.
			"""
			ret = [ ]
			if message.channel_mentions:
				for channel_obj in message.channel_mentions:
					ret.append( str( channel_obj ) )
					DISABLED_CHANNELS.append( channel_obj.id )
				ret = f"```Disabled {', '.join(ret)}```"
			elif message.mentions:
				for user_obj in message.mentions:
					ret.append( str( user_obj ) )
					DISABLED_USERS.append( user_obj.id )
				ret = f"```Disabled {', '.join(ret)}```"
			else:
				DISABLED_CHANNELS.append( message.channel.id )
				ret = f"```Disabled {str(message.channel)}```"
			save( message.server.id )
			await CLIENT.send_message( message.channel, ret )
			del ret
		@staticmethod
		async def v_enable ( message: discord.Message ):
			"""
			Enables commands.
			:param message: A discord.Message object.
			"""
			ret = ""
			if message.channel_mentions:
				for channel_obj in message.channel_mentions:
					ret += ", " + str( channel_obj )
					DISABLED_CHANNELS.remove( channel_obj.id )
				ret = "```Enabled " + ret[ 2: ] + "```"
			elif message.mentions:
				for user_obj in message.mentions:
					ret += ", " + str( user_obj )
					DISABLED_USERS.remove( user_obj.id )
				ret = f"```Enabled {ret[2:]}```"
			else:
				DISABLED_CHANNELS.remove( message.channel.id )
				ret = f"```Enabled {str(message.channel)}```"
			save( message.server.id )
			await CLIENT.send_message( message.channel, ret )
			del ret
	class Owner:
		"""
		Commands for Owner (me) only.
		"""
		@staticmethod
		async def exit ( ):
			"""
			Exits the bot.
			"""
			await CLIENT.logout( )
			exit( 0 )

def log_error ( error_text: str ):
	"""
	Logs errors in the bot.
	:param error_text: The error text.
	"""
	file = f"{os.getcwd()}\\error_log.txt"
	prev_text = ""
	try:
		# noinspection PyShadowingNames
		reader_tmp = open( file, 'r' )
		prev_text = reader_tmp.read( )
		reader_tmp.close( )
		del reader_tmp
	except Exception:
		pass
	writer = open( file, 'w' )
	writer.write( f"{datetime.now()} (bible.py) - {error_text}\n\n{prev_text}" )
	writer.close( )
	if "SystemExit" in error_text:
		exit( 0 )
	del writer
	del file
	del prev_text

@asyncio.coroutine
def trigger_votd ( ):
	"""
	Sends the verse of the day in each channel set for each server.
	"""
	global LAST_DAY, VOTD
	if LAST_DAY != datetime.now( ).day:
		LAST_DAY = datetime.now( ).day
		key = random.choice( TOP_VERSES )
		VOTD = key
		embed_obj = discord.Embed(
			title="Verse of the Day",
			description="Version: akjv",
			colour=discord.Colour.dark_blue( )
		)
		if "-" in key:
			embed_obj.add_field( name=key, value=get_akjv_passage( key, include_header=False ) )
		else:
			embed_obj.add_field( name=key, value=get_akjv_verse( key, include_header=False ) )
		encountered = [ ]
		for channel in CLIENT.get_all_channels( ):
			server = channel.server
			if server.id in list( DEFAULT_CHANNEL.keys( ) ) and not server.id in encountered:
				channel = CLIENT.get_channel( DEFAULT_CHANNEL[ server.id ] )
				yield from CLIENT.send_message(
					channel,
					"Here is the VotD! :calendar_spiral:",
					embed=embed_obj
				)
				encountered.append( server.id )
			del server
		del key
		del embed_obj
		del encountered

@CLIENT.event
async def send_no_perm ( message: discord.Message ):
	"""
	Sends a `NO PERMISSION` message to a user.
	:param message: a discord.Message object from on_message.
	"""
	await CLIENT.send_message(
		message.channel,
		"```You do not have permission to use this command.```"
	)
	print( "{}{} attempted to use a command.{}".format(
		Fore.LIGHTGREEN_EX,
		check(
			message.author.nick,
			message.author.name,
			message.author.id
		),
		Fore.RESET
	) )

@CLIENT.event
async def send_disabled ( message: discord.Message ):
	"""
	Send a `DISABLED` message to a user.
	:param message: A discord.Message object from on_message.
	"""
	await CLIENT.send_message( message.channel, "```That command has been disabled!!!```" )

@CLIENT.event
async def on_message ( message ):
	"""
	Occurs when the bot receives a message.
	:param message: A discord.Message object.
	"""
	global EXITING

	try:
		prefix = sqlread( f"SELECT prefix FROM Prefixes WHERE server='{message.server.id}';" )[ 0 ][ 0 ]
		await trigger_votd( )
		read( message.server.id )
		BIBLE_VERSIONS[ message.author.id ] = BIBLE_VERSIONS[ message.author.id ] \
			if not BIBLE_VERSIONS.get( message.author.id ) is None \
			else "akjv"
		BIBLE_TYPES[ message.author.id ] = BIBLE_TYPES[ message.author.id ] \
			if not BIBLE_TYPES.get( message.author.id ) is None else "embed"
		if not message.server.id in VERSE_DISABLE_LIST:
			if not message.author.bot:
				if not message.content.startswith( f"{prefix}verse " ) \
						and not message.content.startswith( f"{prefix}devotional\n" ):
					if not message.channel.id in DISABLED_CHANNELS and not message.author.id in DISABLED_USERS:
						for mcont in message.content.split( "\n" ):
							embed_obj = discord.Embed( colour=discord.Colour.purple( ) )
							encountered = [ ]
							tmp_content = mcont.replace( ".", " " ) \
								.replace( "`", "" ) \
								.replace( "*", "" ) \
								.replace( "_", "" )
							verse = [ ]
							tmp_content = abbr( tmp_content )
							for i in range( 0, 17 ):
								tmp_content = tmp_content.replace( AKJV_BOOKS[ i ], AKJV_BOOKS[ i ].replace( " ", "|" ) )
							msg_cont = tmp_content.split( " " )
							append = verse.append
							for item in enumerate( msg_cont ):
								msg_cont[ item[ 0 ] ] = abbr( item[ 1 ].replace( "|", " " ).capitalize( ) )
							# for i in range( 0, len( msg_cont ) ):
							# 	msg_cont[ i ] = abbr( msg_cont[ i ].replace( "|", " " ).capitalize( ) )
							for book in AKJV_BOOKS:
								while book in msg_cont:
									index = msg_cont.index( book )
									if not index == len( msg_cont ) - 1:
										if "," in msg_cont[ index + 1 ]:
											for item in msg_cont[ index + 1 ].split( ":" )[ 1 ].split( "," ):
												append( f"{msg_cont[index]} {msg_cont[index+1].split(':')[0]}:{item}" )
										else:
											verse.append( f"{msg_cont[index]} {msg_cont[index+1]}" )
									msg_cont.remove( book )
							for verse_item in verse:
								if BIBLE_TYPES[ message.author.id ] == "text":
									if "-" in verse_item and not verse_item in encountered:
										if "AKJV" in message.content:
											for msg in format_message( get_akjv_passage( verse_item, include_header=True ) ):
												await CLIENT.send_message( message.channel, f"```{msg.replace('```','')}```" )
										elif "KJV" in message.content:
											for msg in format_message( get_kjv_passage( verse_item, include_header=True ) ):
												await CLIENT.send_message( message.channel, f"```{msg.replace('```','')}```" )
										elif "WEB" in message.content:
											for msg in format_message( get_web_passage( verse_item, include_header=True ) ):
												await CLIENT.send_message( message.channel, f"```{msg.replace('```','')}```" )
										elif "NIV" in message.content:
											for msg in format_message( get_niv_passage( verse_item, include_header=True ) ):
												await CLIENT.send_message( message.channel, f"```{msg.replace('```','')}```" )
										elif BIBLE_VERSIONS[ message.author.id ] == "kjv":
											for msg in format_message( get_kjv_passage( verse_item, include_header=True ) ):
												msg = msg.replace( "```", "" ).split( '\n' )
												msg[ 1 ] = f"```{msg[1]}"
												msg = '\n'.join( msg ) + "```"
												await CLIENT.send_message( message.channel, msg )
										elif BIBLE_VERSIONS[ message.author.id ] == "akjv":
											for msg in format_message( get_akjv_passage( verse_item, include_header=True ) ):
												msg = msg.replace( "```", "" ).split( '\n' )
												msg[ 1 ] = f"```{msg[1]}"
												msg = '\n'.join( msg ) + "```"
												await CLIENT.send_message( message.channel, msg )
										elif BIBLE_VERSIONS[ message.author.id ] == "web":
											for msg in format_message( get_web_passage( verse_item, include_header=True ) ):
												msg = msg.replace( "```", "" ).split( '\n' )
												msg[ 1 ] = f"```{msg[1]}"
												msg = '\n'.join( msg ) + "```"
												await CLIENT.send_message( message.channel, msg )
										elif BIBLE_VERSIONS[ message.author.id ] == "niv":
											for msg in format_message( get_niv_passage( verse_item, include_header=True ) ):
												msg = msg.replace( "```", "" ).split( '\n' )
												msg[ 1 ] = f"```{msg[1]}"
												msg = '\n'.join( msg ) + "```"
												await CLIENT.send_message( message.channel, msg )
									elif ":" in verse_item and not verse_item in encountered:
										if "AKJV" in message.content:
											for msg in format_message( get_akjv_verse( verse_item, include_header=True ) ):
												await CLIENT.send_message( message.channel, f"```{msg.replace('```','')}```" )
										elif "KJV" in message.content:
											for msg in format_message( get_kjv_verse( verse_item, include_header=True ) ):
												await CLIENT.send_message( message.channel, f"```{msg.replace('```','')}```" )
										elif "WEB" in message.content:
											for msg in format_message( get_web_verse( verse_item, include_header=True ) ):
												await CLIENT.send_message( message.channel, f"```{msg.replace('```','')}```" )
										elif "NIV" in message.content:
											for msg in format_message( get_niv_verse( verse_item, include_header=True ) ):
												await CLIENT.send_message( message.channel, f"```{msg.replace('```','')}```" )
										elif BIBLE_VERSIONS[ message.author.id ] == "kjv":
											for msg in format_message( get_kjv_verse( verse_item, include_header=True ) ):
												msg = msg.replace( "```", "" ).split( '\n' )
												msg[ 1 ] = f"```{msg[1]}"
												msg = '\n'.join( msg ) + "```"
												await CLIENT.send_message( message.channel, msg )
										elif BIBLE_VERSIONS[ message.author.id ] == "akjv":
											for msg in format_message( get_akjv_verse( verse_item, include_header=True ) ):
												msg = msg.replace( "```", "" ).split( '\n' )
												msg[ 1 ] = f"```{msg[1]}"
												msg = '\n'.join( msg ) + "```"
												await CLIENT.send_message( message.channel, msg )
										elif BIBLE_VERSIONS[ message.author.id ] == "web":
											for msg in format_message( get_web_verse( verse_item, include_header=True ) ):
												msg = msg.replace( "```", "" ).split( '\n' )
												msg[ 1 ] = f"```{msg[1]}"
												msg = '\n'.join( msg ) + "```"
												await CLIENT.send_message( message.channel, msg )
										elif BIBLE_VERSIONS[ message.author.id ] == "niv":
											for msg in format_message( get_niv_verse( verse_item, include_header=True ) ):
												msg = msg.replace( "```", "" ).split( '\n' )
												msg[ 1 ] = f"```{msg[1]}"
												msg = '\n'.join( msg ) + "```"
												await CLIENT.send_message( message.channel, msg )
								else:
									if "-" in verse_item and not verse_item in encountered:
										if "AKJV" in message.content:
											embed_obj.add_field(
												name=verse_item,
												value=get_akjv_passage(
													verse_item,
													include_header=False
												)
											)
										elif "KJV" in message.content:
											embed_obj.add_field(
												name=verse_item,
												value=get_kjv_passage(
													verse_item,
													include_header=False
												)
											)
										elif "WEB" in message.content:
											embed_obj.add_field(
												name=verse_item,
												value=get_web_passage(
													verse_item,
													include_header=False
												)
											)
										elif "NIV" in message.content:
											embed_obj.add_field(
												name=verse_item,
												value=get_niv_passage(
													verse_item,
													include_header=False
												)
											)
										elif BIBLE_VERSIONS[ message.author.id ] == "kjv":
											embed_obj.add_field(
												name=verse_item,
												value=get_kjv_passage(
													verse_item,
													include_header=False
												)
											)
										elif BIBLE_VERSIONS[ message.author.id ] == "akjv":
											embed_obj.add_field(
												name=verse_item,
												value=get_akjv_passage(
													verse_item,
													include_header=False
												)
											)
										elif BIBLE_VERSIONS[ message.author.id ] == "web":
											embed_obj.add_field(
												name=verse_item,
												value=get_web_passage(
													verse_item,
													include_header=False
												)
											)
										elif BIBLE_VERSIONS[ message.author.id ] == "niv":
											embed_obj.add_field(
												name=verse_item,
												value=get_niv_passage(
													verse_item,
													include_header=False
												)
											)
									elif ":" in verse_item and not verse_item in encountered:
										if "AKJV" in message.content:
											embed_obj.add_field(
												name=verse_item,
												value=get_akjv_verse(
													verse_item,
													include_header=False
												)
											)
										elif "KJV" in message.content:
											embed_obj.add_field(
												name=verse_item,
												value=get_kjv_verse(
													verse_item,
													include_header=False
												)
											)
										elif "WEB" in message.content:
											embed_obj.add_field(
												name=verse_item,
												value=get_web_verse(
													verse_item,
													include_header=False
												)
											)
										elif "NIV" in message.content:
											embed_obj.add_field(
												name=verse_item,
												value=get_niv_verse(
													verse_item,
													include_header=False
												)
											)
										elif BIBLE_VERSIONS[ message.author.id ] == "kjv":
											embed_obj.add_field(
												name=verse_item,
												value=get_kjv_verse(
													verse_item,
													include_header=False
												)
											)
										elif BIBLE_VERSIONS[ message.author.id ] == "akjv":
											embed_obj.add_field(
												name=verse_item,
												value=get_akjv_verse(
													verse_item,
													include_header=False
												)
											)
										elif BIBLE_VERSIONS[ message.author.id ] == "web":
											embed_obj.add_field(
												name=verse_item,
												value=get_web_verse(
													verse_item,
													include_header=False
												)
											)
										elif BIBLE_VERSIONS[ message.author.id ] == "niv":
											embed_obj.add_field(
												name=verse_item,
												value=get_niv_verse(
													verse_item,
													include_header=False
												)
											)
								encountered.append( verse_item )
							if BIBLE_TYPES[ message.author.id ] == "embed" and len( embed_obj.fields ) >= 1:
								try:
									# <editor-fold desc="Fetching Title...">
									index = list( mcont ).index( '"' )
									title = ""
									has_found = False
									for i in range( index + 1, len( mcont ) ):
										if mcont[ i ] == "\"":
											has_found = True
										if not has_found:
											title += mcont[ i ]
									# </editor-fold>
									embed_obj.title = title
									del index
									del title
									del has_found
								except Exception:
									pass
								try:
									# <editor-fold desc="Fetching Description">
									if "AKJV" in message.content:
										description = "akjv"
									elif "KJV" in message.content:
										description = "kjv"
									elif "WEB" in message.content:
										description = "web"
									elif "NIV" in message.content:
										description = "niv"
									else:
										description = BIBLE_VERSIONS[ message.author.id ]
									# </editor-fold>
									embed_obj.description = description.upper( )
									del description
								except Exception:
									pass

								for i in range( 0, len( embed_obj.fields ) ):
									if embed_obj.fields[ i ].value == "No such verse!":
										embed_obj.remove_field( i )

								timestamp = datetime.now( ) - message.timestamp
								delay = int( timestamp.microseconds / 1000 )
								if delay > 999:
									delay = str( delay / 1000 )
								else:
									delay = f"0.{delay}"
								await CLIENT.send_message(
									message.channel,
									f"Response in {delay} seconds! :smile:",
									embed=embed_obj
								)
								print( f"Sending {', '.join(verse)} ~ Delay: {delay}s." )
								del timestamp
								del delay
							del embed_obj
							del encountered
							del tmp_content
							del verse
							del msg_cont
							del append

		do_update = False

		admin_role = discord.utils.find( lambda r:r.name == "LogBot Admin", message.server.roles )
		def startswith ( *msgs, val=message.content ):
			"""
			Checks the string to see if any number of characters are at the beginning.
			:param msgs: The character sequences to check for.
			:param val: The string to check.
			:return: True or False
			"""
			# noinspection PyShadowingNames
			for item in msgs:
				if val.startswith( item ):
					return True
			return False
		# bi = BibleInfo( )
		bible_info = BI( )

		if startswith( f"{prefix}disable verse", f"{prefix}disable {prefix}verse" ):
			if admin_role in message.author.roles or message.author.id == owner_id:
				await Commands.Admin.disable( message )
			else:
				send_no_perm( message )
		elif startswith( f"{prefix}enable verse", f"{prefix}enable {prefix}verse" ):
			if admin_role in message.author.roles or message.author.id == owner_id:
				await Commands.Admin.enable( message )
			else:
				send_no_perm( message )
		elif startswith( f"{prefix}verse help" ):
			if not message.server.id in VERSE_DISABLE_LIST or message.author.id == owner_id:
				await Commands.Member.verse_help( message )
			elif message.server.id in VERSE_DISABLE_LIST:
				send_disabled( message )
			else:
				send_no_perm( message )
		elif startswith( f"{prefix}verse info" ):
			if not message.server.id in VERSE_DISABLE_LIST or message.author.id == owner_id:
				await Commands.Member.verse_info( message, bible_info, prefix )
			elif message.server.id in VERSE_DISABLE_LIST:
				send_disabled( message )
			else:
				send_no_perm( message )
		elif startswith( f"{prefix}verse random" ):
			if not message.server.id in VERSE_DISABLE_LIST or message.author.id == owner_id:
				await Commands.Member.verse_random( message )
			elif message.server.id in VERSE_DISABLE_LIST:
				send_disabled( message )
			else:
				send_no_perm( message )
		elif startswith( f"{prefix}verse search" ):
			if not message.server.id in VERSE_DISABLE_LIST or message.author.id == owner_id:
				await Commands.Member.verse_search( message, prefix )
			elif message.server.id in VERSE_DISABLE_LIST:
				send_disabled( message )
			else:
				send_no_perm( message )
		elif startswith( f"{prefix}verse compare " ):
			if not message.server.id in VERSE_DISABLE_LIST or message.author.id == owner_id:
				await Commands.Member.verse_compare( message, prefix )
			elif message.server.id in VERSE_DISABLE_LIST:
				send_disabled( message )
			else:
				send_no_perm( message )
		elif startswith( f"{prefix}votd" ):
			await Commands.Member.send_votd( message )
		elif startswith( f"{prefix}setversion " ):
			await Commands.Member.setversion( message, prefix )
		elif startswith( f"{prefix}settype " ):
			await Commands.Member.settype( message, prefix )
		elif startswith( f"{prefix}getversion", f"{prefix}setversion" ):
			await CLIENT.send_message( message.channel, BIBLE_VERSIONS[ message.author.id ] )
		elif startswith( f"{prefix}gettype", f"{prefix}settype" ):
			await CLIENT.send_message( message.channel, BIBLE_TYPES[ message.author.id ] )
		elif startswith( f"{prefix}setchannel " ):
			if admin_role in message.author.roles:
				await Commands.Admin.setchannel( message )
			else:
				send_no_perm( message )
		elif startswith( f"{prefix}getchannel" ):
			await CLIENT.send_message(
				message.channel,
				f"The default channel is <#{DEFAULT_CHANNEL[message.server.id]}>"
			)
		elif startswith( f"verse_item{prefix}disables" ):
			await Commands.Member.disables( message )
		elif startswith( f"verse_item{prefix}disable" ):
			if admin_role in message.author.roles or message.author.id == owner_id:
				await Commands.Admin.v_disable( message )
			else:
				send_no_perm( message )
		elif startswith( f"verse_item{prefix}enable" ):
			if admin_role in message.author.roles or message.author.id == owner_id:
				await Commands.Admin.v_enable( message )
			else:
				send_no_perm( message )
		elif startswith( "$exit", "logbot.bible.exit" ):
			if message.author.id == owner_id:
				EXITING = True
				await Commands.Owner.exit( )
			else:
				send_no_perm( message )
		elif startswith( f"$update", "logbot.bible.update" ):
			if message.author.id == owner_id:
				do_update = True
			else:
				send_no_perm( message )
		elif startswith( f"{prefix}ping" ):
			await Commands.Member.ping( message )
		elif startswith( f"{prefix}devotional\n" ):
			lines = message.content.replace( "{prefix}devotional\n", "" ).split( "\n" )
			embed_obj = discord.Embed( title="", description="", colour=discord.Colour.green( ) )
			text = ""
			for line in lines:
				if line.startswith( "&title=" ):
					embed_obj.title = line.replace( "&title=", "" )
				elif line.startswith( "&description=" ):
					embed_obj.description = line.replace( "&description=", "" )
				elif line.startswith( "&author=" ) or line.startswith( "&footer=" ):
					embed_obj.set_footer( text=line.replace( "&author=", "" ).replace( "&footer=", "" ) )
				elif line.startswith( "&thumbnail=" ):
					embed_obj.set_thumbnail( url=line.replace( "&thumbnail=", "" ) )
				elif line.startswith( "&passage=" ):
					def analyze_verse ( _text, _version="kjv" ):
						"""
						Fetches the verse associated with the reference.
						:param _text: A verse reference.
						:param _version: The Bible version.
						:return: [reference, verse]
						"""
						res = ""
						if _version == "kjv":
							res = get_kjv_passage(
								_text,
								include_header=False
							) if "-" in _text else get_kjv_verse(
								_text,
								include_header=False
							)
						elif _version == "akjv":
							res = get_akjv_passage(
								_text,
								include_header=False
							) if "-" in _text else get_akjv_verse(
								_text,
								include_header=False
							)
						elif _version == "web":
							res = get_web_passage(
								_text,
								include_header=False
							) if "-" in _text else get_web_verse(
								_text,
								include_header=False
							)
						elif _version == "niv":
							res = get_niv_passage(
								_text,
								include_header=False
							) if "-" in _text else get_niv_verse(
								_text,
								include_header=False
							)
						return [
							_text,
							res
						]
					_text = line.replace( "&passage=", "" )
					# noinspection PyShadowingNames
					version = BIBLE_VERSIONS[ message.author.id ]
					ret = analyze_verse( cap_all_words( _text ), _version=version )
					embed_obj.add_field( name=ret[ 0 ], value=ret[ 1 ], inline=False )
					del _text
					del version
					del ret
				elif line.startswith( "&text=" ):
					if "|" in line:
						_title = line.replace( "&text=", "" ).split( "|" )[ 0 ]
						_text = line.replace( "&text=", "" ).split( "|" )[ 1 ]
					else:
						_title = "` `"
						_text = line.replace( "&text=", "" )
					embed_obj.add_field( name=_title, value=_text, inline=False )
					del _title
					del _text
				elif line.startswith( "&keyword=" ):
					text = line.replace( "&keyword=", "" )
			if text == "":
				text = embed_obj.title
			await CLIENT.send_message( message.channel, text, embed=embed_obj )
			del lines
			del embed_obj
			del text
		elif startswith( f"{prefix}devotional" ):
			_msgs = [ ]
			lines = [ ]
			mappend = _msgs.append
			lappend = lines.append
			cont = True
			_msg = await CLIENT.wait_for_message( author=message.author )
			mappend( _msg )
			lappend( _msg.content )
			while cont:
				_msg = await CLIENT.wait_for_message( author=message.author )
				if _msg.content == "&end":
					cont = False
					mappend( _msg )
				else:
					lappend( _msg.content )
					mappend( _msg )
			mappend( message )
			text = ""
			embed_obj = discord.Embed( title="", description="", colour=discord.Colour.green( ) )
			for line in lines:
				if line.startswith( "&title=" ):
					embed_obj.title = line.replace( "&title=", "" )
				elif line.startswith( "&description=" ):
					embed_obj.description = line.replace( "&description=", "" )
				elif line.startswith( "&author=" ) or line.startswith( "&footer=" ):
					embed_obj.set_footer( text=line.replace( "&author=", "" ).replace( "&footer=", "" ) )
				elif line.startswith( "&thumbnail=" ):
					embed_obj.set_thumbnail( url=line.replace( "&thumbnail=", "" ) )
				elif line.startswith( "&passage=" ):
					def analyze_verse ( _text, _version="kjv" ):
						"""
						Fetches the verse associated with the reference.
						:param _text: A verse reference.
						:param _version: The Bible version.
						:return: [reference, verse]
						"""
						res = ""
						if _version == "kjv":
							res = get_kjv_passage(
								_text,
								include_header=False
							) if "-" in _text else get_kjv_verse(
								_text,
								include_header=False
							)
						elif _version == "akjv":
							res = get_akjv_passage(
								_text,
								include_header=False
							) if "-" in _text else get_akjv_verse(
								_text,
								include_header=False
							)
						elif _version == "web":
							res = get_web_passage(
								_text,
								include_header=False
							) if "-" in _text else get_web_verse(
								_text,
								include_header=False
							)
						elif _version == "niv":
							res = get_niv_passage(
								_text,
								include_header=False
							) if "-" in _text else get_niv_verse(
								_text,
								include_header=False
							)
						return [
							_text,
							res
						]
					_text = line.replace( "&passage=", "" )
					# noinspection PyShadowingNames
					version = BIBLE_VERSIONS[ message.author.id ]
					ret = analyze_verse( cap_all_words( _text ), _version=version )
					embed_obj.add_field( name=ret[ 0 ], value=ret[ 1 ], inline=False )
					del version
					del ret
					del _text
				elif line.startswith( "&text=" ):
					if "|" in line:
						_title = line.replace( "&text=", "" ).split( "|" )[ 0 ]
						_text = line.replace( "&text=", "" ).split( "|" )[ 1 ]
					else:
						_title = "` `"
						_text = line.replace( "&text=", "" )
					embed_obj.add_field( name=_title, value=_text, inline=False )
					del _title
					del _text
				elif line.startswith( "&keyword=" ):
					text = line.replace( "&keyword=", "" )
			if text == "":
				text = embed_obj.title
			await CLIENT.send_message( message.channel, text, embed=embed_obj )
			await CLIENT.delete_messages( _msgs )
			del _msgs
			del lines
			del mappend
			del lappend
			del cont
			del _msg
		elif startswith( f"verse_item{prefix}settings" ):
			channels = [
				str( CLIENT.get_channel( _id ) )
				if CLIENT.get_channel( _id ).server == message.server
				else None
				for _id in DISABLED_CHANNELS
			]
			crem = channels.remove
			while None in channels:
				crem( None )

			_def_channel = DEFAULT_CHANNEL.get( message.server.id )
			if _def_channel is None:
				_def_channel = "No default channel."

			_personal = discord.Embed(
				title="Personal",
				description="Verse Module Settings",
				colour=discord.Colour.dark_blue( )
			).add_field(
				name="Type",
				value=BIBLE_TYPES[ message.author.id ]
			).add_field(
				name="Version",
				value=BIBLE_VERSIONS[ message.author.id ]
			)
			_server = discord.Embed(
				title="Server",
				description="Verse Module Settings",
				colour=discord.Colour.dark_blue( )
			).add_field(
				name="Verse Channel",
				value=DEFAULT_CHANNEL.get( message.server.id )
			).add_field(
				name="Disabled Channels",
				value=''.join( channels ) if channels else "No disabled channels."
			)

			await CLIENT.send_message( message.channel, "", embed=_personal )
			await CLIENT.send_message( message.channel, "", embed=_server )
			del _def_channel
			del channels
			del crem
			del _personal
			del _server

		save( message.server.id )
		if do_update:
			print( f"{Fore.LIGHTCYAN_EX}Updating...{Fore.RESET}" )
			subprocess.Popen( f"python {os.getcwd()}\\bible.py" )
			exit( 0 )
	except Exception:
		log_error( traceback.format_exc( ) )

@CLIENT.event
async def on_ready ( ):
	"""
	Occurs when the bot logs in.
	"""
	await CLIENT.change_presence( game=None )
	# os.system( "cls" )
	print( f"{Fore.MAGENTA}Bible Ready!!!{Fore.RESET}" )

CLIENT.run( token )

if not EXITING:
	subprocess.Popen( f"python {os.getcwd()}\\bible.py" )
	exit( 0 )
