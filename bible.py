import ast
import asyncio
import math
import os
import random
import re
import subprocess
from datetime import datetime
from sys import exit

import discord
from colorama import Fore, init

import sql_data
import symbols
from logbot_data import token

client = discord.Client()
init()

akjv_books = ["1 Samuel",
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
              "Revelation"]

verse_disable_list = []
bible_versions = {}
bible_types = {}
default_channel = {}
last_day = 0
votd = ""
top_verses = ["Psalms 23:4", "Psalms 34:8", "Psalms 34:19", "Psalms 37:4", "Psalms 55:22",
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
              "James 4:7-8", "1 Peter 5:7", "1 John 4:4", "1 John 4:18", "1 John 5:14-15", "Revelation 14:12"]
disabled_channels = []

discord_settings = f"{os.getcwd()}\\Discord Logs\\SETTINGS"
verse_disables = f"{discord_settings}\\verse_disable_list.txt"
version_list = f"{discord_settings}\\bible_version.txt"
type_list = f"{discord_settings}\\bible_types.txt"
c_list = f"{discord_settings}\\default_channel.txt"
d_last_day = f"{discord_settings}\\last_day.txt"
votd_d = f"{discord_settings}\\votd.txt"
_disabled_channels = f"{discord_settings}\\bible_plugin\\Disabled Channels\\"

sqld = sql_data.sql_data(akjv_books)
sqlkjv = sql_data.kjv_sql(akjv_books)
sqlweb = sql_data.web_sql(akjv_books)

class BibleInfo:
	def __init__(self):
		self.placeholder = ""
		pass
	@staticmethod
	def getGenesisAuthor():
		return "Moses"
	@staticmethod
	def getGenesisChapters():
		return 50
	@staticmethod
	def getGenesisSummary():
		return "Genesis answers two big questions: \"How did God's relationship with the world begin?\" and \"Where did the nation of Israel come from?\""
	@staticmethod
	def getExodusAuthor():
		return "Moses"
	@staticmethod
	def getExodusChapters():
		return 40
	@staticmethod
	def getExodusSummary():
		return "God saves Israel from slavery in Egypt, and then enters into a special relationship with them."
	@staticmethod
	def getLeviticusAuthor():
		return "Moses"
	@staticmethod
	def getLeviticusChapters():
		return 27
	@staticmethod
	def getLeviticusSummary():
		return "God gives Israel instructions for how to worship Him."
	@staticmethod
	def getNumbersAuthor():
		return "Moses"
	@staticmethod
	def getNumbersChapters():
		return 36
	@staticmethod
	def getNumbersSummary():
		return "Israel fails to trust and obey God, and wanders in the wilderness for 40 years."
	@staticmethod
	def getDeuteronomyAuthor():
		return "Moses"
	@staticmethod
	def getDeuteronomyChapters():
		return 34
	@staticmethod
	def getDeuteronomySummary():
		return "Moses gives Israel instructions (in some ways, a recap of the laws in Exodus-Numbers) for how to love and obey God in the Promised Land."
	@staticmethod
	def getJoshuaAuthor():
		return "Joshua"
	@staticmethod
	def getJoshuaChapters():
		return 24
	@staticmethod
	def getJoshuaSummary():
		return "Joshua (Israel's new leader) leads Israel to conquer the Promised Land, then parcels out territories to the twelve tribes of Israel."
	@staticmethod
	def getJudgesAuthor():
		return "Samuel"
	@staticmethod
	def getJudgesChapters():
		return 21
	@staticmethod
	def getJudgesSummary():
		return "Israel enters a cycle of turning from God, falling captive to oppressive nations, calling out to God, and being rescued by leaders God sends their way (called \"judges\")."
	@staticmethod
	def getRuthAuthor():
		return "Samuel"
	@staticmethod
	def getRuthChapters():
		return 4
	@staticmethod
	def getRuthSummary():
		return "Two widows lose everything, and find hope in Israel-which leads to the birth of the future King David."
	@staticmethod
	def get1SamuelAuthor():
		return "Samuel"
	@staticmethod
	def get1SamuelChapters():
		return 31
	@staticmethod
	def get1SamuelSummary():
		return "Israel demands a king, who turns out to be quite a disappointment."
	@staticmethod
	def get2SamuelAuthor():
		return "Samuel"
	@staticmethod
	def get2SamuelChapters():
		return 24
	@staticmethod
	def get2SamuelSummary():
		return "David, a man after God's own heart, becomes king of Israel."
	@staticmethod
	def get1KingsAuthor():
		return "Jeremiah"
	@staticmethod
	def get1KingsChapters():
		return 22
	@staticmethod
	def get1KingsSummary():
		return "The kingdom of Israel has a time of peace and prosperity under King Solomon, but afterward splits, and the two lines of kings turn away from God."
	@staticmethod
	def get2KingsAuthor():
		return "Jeremiah"
	@staticmethod
	def get2KingsChapters():
		return 25
	@staticmethod
	def get2KingsSummary():
		return "Both kingdoms ignore God and his prophets, until they both fall captive to other world empires."
	@staticmethod
	def get1ChroniclesAuthor():
		return "Ezra"
	@staticmethod
	def get1ChroniclesChapters():
		return 29
	@staticmethod
	def get1ChroniclesSummary():
		return "This is a brief history of Israel from Adam to David, culminating with David commissioning the temple of God in Jerusalem."
	@staticmethod
	def get2ChroniclesAuthor():
		return "Ezra"
	@staticmethod
	def get2ChroniclesChapters():
		return 36
	@staticmethod
	def get2ChroniclesSummary():
		return "David's son Solomon builds the temple, but after centuries of rejecting God, the Babylonians take the southern Israelites captive and destroy the temple."
	@staticmethod
	def getEzraAuthor():
		return "Ezra"
	@staticmethod
	def getEzraChapters():
		return 10
	@staticmethod
	def getEzraSummary():
		return "The Israelites rebuild the temple in Jerusalem, and a scribe named Ezra teaches the people to once again obey God's laws."
	@staticmethod
	def getNehemiahAuthor():
		return "Ezra"
	@staticmethod
	def getNehemiahChapters():
		return 13
	@staticmethod
	def getNehemiahSummary():
		return "The city of Jerusalem is in bad shape, so Nehemiah rebuilds the wall around the city."
	@staticmethod
	def getEstherAuthor():
		return "Mordechai"
	@staticmethod
	def getEstherChapters():
		return 10
	@staticmethod
	def getEstherSummary():
		return "Someone hatches a genocidal plot to bring about Israel's extinction, and Esther must face the emperor to ask for help."
	@staticmethod
	def getJobAuthor():
		return "Possibly Job, ELihu, or Solomon"
	@staticmethod
	def getJobChapters():
		return 42
	@staticmethod
	def getJobSummary():
		return "Satan attacks a righteous man named Job, and Job and his friends argue about why terrible things are happening to him."
	@staticmethod
	def getPsalmsAuthor():
		return "King David"
	@staticmethod
	def getPsalmsChapters():
		return 150
	@staticmethod
	def getPsalmsSummary():
		return "A collection of 150 songs that Israel sang to God (and to each other)-kind of like a hymnal for the ancient Israelites."
	@staticmethod
	def getProverbsAuthor():
		return "Solomon"
	@staticmethod
	def getProverbsChapters():
		return 31
	@staticmethod
	def getProverbsSummary():
		return "A collection of sayings written to help peole make wise decisions that bring about justice."
	@staticmethod
	def getEcclesiastesAuthor():
		return "Solomon"
	@staticmethod
	def getEcclesiastesChapters():
		return 12
	@staticmethod
	def getEcclesiastesSummary():
		return "A philosophical exploration of the meaning of life-with a surprisingly nihilistic tone for the Bible."
	@staticmethod
	def getSongOfSolomonAuthor():
		return "Solomon"
	@staticmethod
	def getSongOfSolomonChapters():
		return 8
	@staticmethod
	def getSongOfSolomonSummary():
		return "A love song (or collection of love songs) celebrating love, desire, and marriage."
	@staticmethod
	def getIsaiahAuthor():
		return "Isaiah"
	@staticmethod
	def getIsaiahChapters():
		return 66
	@staticmethod
	def getIsaiahSummary():
		return "God sends the prophet Isaiah to warn Israel of future judgment-but also to tell them about a coming king and servant who will \"bear the sins of many.\""
	@staticmethod
	def getJeremiahAuthor():
		return "Jeremiah"
	@staticmethod
	def getJeremiahChapters():
		return 52
	@staticmethod
	def getJeremiahSummary():
		return "God sends a prophet to warn Israel about the coming Babylonian captivity, but the people don't take the news very well."
	@staticmethod
	def getLamentationsAuthor():
		return "Jeremiah"
	@staticmethod
	def getLamentationsChapters():
		return 5
	@staticmethod
	def getLamentationsSummary():
		return "A collection of dirges lamenting the fall of Jerusalem after the Babylonian attacks."
	@staticmethod
	def getEzekielAuthor():
		return "Ezekiel"
	@staticmethod
	def getEzekielChapters():
		return 47
	@staticmethod
	def getEzekielSummary():
		return "God chooses a man to speak for Him to Israel, to tell them the error of their ways and teach them justice: Ezekiel."
	@staticmethod
	def getDanielAuthor():
		return "Daniel"
	@staticmethod
	def getDanielChapters():
		return 11
	@staticmethod
	def getDanielSummary():
		return "Daniel becomes a high-ranking wise man in the Babylonian and Persian empires, and has prophetic visions concerning Israel's future."
	@staticmethod
	def getHoseaAuthor():
		return "Hosea"
	@staticmethod
	def getHoseaChapters():
		return 13
	@staticmethod
	def getHoseaSummary():
		return "Hosea is told to marry a prostitute who leaves him, and he must bring her back: a picture of God's relationship with Israel."
	@staticmethod
	def getJoelAuthor():
		return "Joel"
	@staticmethod
	def getJoelChapters():
		return 2
	@staticmethod
	def getJoelSummary():
		return "God sends a plague of locusts to Judge Israel, but his judgment on the surrounding nations is coming, too."
	@staticmethod
	def getAmosAuthor():
		return "Amos"
	@staticmethod
	def getAmosChapters():
		return 8
	@staticmethod
	def getAmosSummary():
		return "A shepherd named Amos preaches against the injustice of the Northern Kingdom of Israel."
	@staticmethod
	def getObadiahAuthor():
		return "Obadiah"
	@staticmethod
	def getObadiahChapters():
		return 1
	@staticmethod
	def getObadiahSummary():
		return "Obadiah warns the neighboring nation of Edom that they will be judged for plundering Jerusalem."
	@staticmethod
	def getJonahAuthor():
		return "Jonah"
	@staticmethod
	def getJonahChapters():
		return 4
	@staticmethod
	def getJonahSummary():
		return "A disobedient prophet runs from God, is swallowed by a great fish, and then preaches God's message to the city of Ninevah."
	@staticmethod
	def getMicahAuthor():
		return "Micah"
	@staticmethod
	def getMicahChapters():
		return 7
	@staticmethod
	def getMicahSummary():
		return "Micah confronts the leaders of Israel and Judah regarding their injustice, and prophecies that one day the Lord himself will rule in perfect justice."
	@staticmethod
	def getNahumAuthor():
		return "Nahum"
	@staticmethod
	def getNahumChapters():
		return 3
	@staticmethod
	def getNahumSummary():
		return "Nahum foretells of God's judgment on Nineveh, the capital of Assyria."
	@staticmethod
	def getHabakkukAuthor():
		return "Habakkuk"
	@staticmethod
	def getHabakkukChapters():
		return 3
	@staticmethod
	def getHabakkukSummary():
		return "Habakkuk pleads with God to stop the injustice and violence in Judah, but is surprised to find that God will use the even more violent Babylonians to do so."
	@staticmethod
	def getZephaniahAuthor():
		return "Zephaniah"
	@staticmethod
	def getZephaniahChapters():
		return 3
	@staticmethod
	def getZephaniahSummary():
		return "God warns that he will judge Israel and the surrounding nations, but also that he will restore them in peace and justice."
	@staticmethod
	def getHaggaiAuthor():
		return "Haggai"
	@staticmethod
	def getHaggaiChapters():
		return 2
	@staticmethod
	def getHaggaiSummary():
		return "The people have abandoned the work of restoring God's temple in Jerusalem, and so Haggai takes them to task."
	@staticmethod
	def getZechariahAuthor():
		return "Zechariah"
	@staticmethod
	def getZechariahChapters():
		return 14
	@staticmethod
	def getZechariahSummary():
		return "The prophet Zechariah calls Israel to return to God, and records prophetic visions that show what's happening behind the scenes."
	@staticmethod
	def getMalachiAuthor():
		return "Malachi"
	@staticmethod
	def getMalachiChapters():
		return 4
	@staticmethod
	def getMalachiSummary():
		return "God has been faithful to Israel, but they continue to live disconnected from him-so God sends Malachi to call them out."
	@staticmethod
	def getMatthewAuthor():
		return "Matthew"
	@staticmethod
	def getMatthewChapters():
		return 28
	@staticmethod
	def getMatthewSummary():
		return "This is an account of Jesus' life, death, and resurrection, focusing on Jesus' role as the true king of the Jews."
	@staticmethod
	def getMarkAuthor():
		return "Mark"
	@staticmethod
	def getMarkChapters():
		return 16
	@staticmethod
	def getMarkSummary():
		return "This brief account of Jesus' earthly ministry highlights Jesus' authority and servanthood."
	@staticmethod
	def getLukeAuthor():
		return "Luke"
	@staticmethod
	def getLukeChapters():
		return 24
	@staticmethod
	def getLukeSummary():
		return "Luke writes the most thorough account of Jesus' life, pulling together eyewitness testimonies to tell the full story of Jesus."
	@staticmethod
	def getJohnAuthor():
		return "John"
	@staticmethod
	def getJohnChapters():
		return 21
	@staticmethod
	def getJohnSummary():
		return "John lists stories of signs and miracles with the hope that readers will believe in Jesus."
	@staticmethod
	def getActsAuthor():
		return "Luke"
	@staticmethod
	def getActsChapters():
		return 28
	@staticmethod
	def getActsSummary():
		return "Jesus returns to the Father, the Holy Spirit comes to the church, and the gospel of Jesus spreads throughout the world."
	@staticmethod
	def getRomansAuthor():
		return "Paul"
	@staticmethod
	def getRomansChapters():
		return 16
	@staticmethod
	def getRomansSummary():
		return "Paul summarizes how the gospel of Jesus works in a letter to the churches at Rome, where he plans to visit."
	@staticmethod
	def get1CorinthiansAuthor():
		return "Paul"
	@staticmethod
	def get1CorinthiansChapters():
		return 15
	@staticmethod
	def get1CorinthiansSummary():
		return "Paul writes a disciplinary letter to a fractured church in Corinth, and answers some questions that they've had about how Christians should behave."
	@staticmethod
	def get2CorinthiansAuthor():
		return "Paul"
	@staticmethod
	def get2CorinthiansChapters():
		return 12
	@staticmethod
	def get2CorinthiansSummary():
		return "Paul writes a letter of reconcilation to the church at Corinth, and clears up some concerns that they have."
	@staticmethod
	def getGalatiansAuthor():
		return "Paul"
	@staticmethod
	def getGalatiansChapters():
		return 5
	@staticmethod
	def getGalatiansSummary():
		return "Paul hears that the Galatian churches have been lead to think that salvation comes from the law of Moses, and writes a (rather heated) letter telling them where the false teachers have it wrong."
	@staticmethod
	def getEphesiansAuthor():
		return "Paul"
	@staticmethod
	def getEphesiansChapters():
		return 5
	@staticmethod
	def getEphesiansSummary():
		return "Paul writes to the church at Ephesus about how to walk in grace, peace, and love."
	@staticmethod
	def getPhilippiansAuthor():
		return "Paul"
	@staticmethod
	def getPhilippiansChapters():
		return 3
	@staticmethod
	def getPhilippiansSummary():
		return "An encouragin letter to the church of Philippi from Paul, telling them how to have joy in Christ."
	@staticmethod
	def getColossiansAuthor():
		return "Paul"
	@staticmethod
	def getColossiansChapters():
		return 3
	@staticmethod
	def getColossiansSummary():
		return "Paul writes the church at Colossae a letter about who they are in Christ, and how to walk in Christ."
	@staticmethod
	def get1ThessaloniansAuthor():
		return "Paul"
	@staticmethod
	def get1ThessaloniansChapters():
		return 4
	@staticmethod
	def get1ThessaloniansSummary():
		return "Paul has heard a good report on the church at Thessalonica, and encourages them to \"excel still more\" in faith, hope, and love."
	@staticmethod
	def get2ThessaloniansAuthor():
		return "Paul"
	@staticmethod
	def get2ThessaloniansChapters():
		return 2
	@staticmethod
	def get2ThessaloniansSummary():
		return "Paul instructs the Thessalonians on how to stand firm until the coming of Jesus."
	@staticmethod
	def get1TimothyAuthor():
		return "Paul"
	@staticmethod
	def get1TimothyChapters():
		return 5
	@staticmethod
	def get1TimothySummary():
		return "Paul gives his protege Timothy instruction on how to lead a church with sound teaching and a godly example."
	@staticmethod
	def get2TimothyAuthor():
		return "Paul"
	@staticmethod
	def get2TimothyChapters():
		return 3
	@staticmethod
	def get2TimothySummary():
		return "Paul is nearing the end of his life, and encourages Timothy to continue preaching the word."
	@staticmethod
	def getTitusAuthor():
		return "Paul"
	@staticmethod
	def getTitusChapters():
		return 2
	@staticmethod
	def getTitusSummary():
		return "Paul advises Titus on how to lead orderly, counter-cultural churches on the island of Crete."
	@staticmethod
	def getPhilemonAuthor():
		return "Philemon"
	@staticmethod
	def getPhilemonChapters():
		return 1
	@staticmethod
	def getPhilemonSummary():
		return "Paul strongly recommends that Philemon accept his runaway slave as a brother, not a slave."
	@staticmethod
	def getHebrewsAuthor():
		return "Unkown"
	@staticmethod
	def getHebrewsChapters():
		return 12
	@staticmethod
	def getHebrewsSummary():
		return "A letter encouraging Christians to cling to Christ despite persecution, because he is greater."
	@staticmethod
	def getJamesAuthor():
		return "James"
	@staticmethod
	def getJamesChapters():
		return 4
	@staticmethod
	def getJamesSummary():
		return "A letter telling Christians to live in ways that demonstrate their faith in action."
	@staticmethod
	def get1PeterAuthor():
		return "Peter"
	@staticmethod
	def get1PeterChapters():
		return 4
	@staticmethod
	def get1PeterSummary():
		return "Peter writes to Christians who are being prosecuted, encouraging them to testify to the truth and live accordingly."
	@staticmethod
	def get2PeterAuthor():
		return "Peter"
	@staticmethod
	def get2PeterChapters():
		return 2
	@staticmethod
	def get2PeterSummary():
		return "Peter writes a letter reminding Christians about the truth of Jesus, and warning them that false teachers will come."
	@staticmethod
	def get1JohnAuthor():
		return "John"
	@staticmethod
	def get1JohnChapters():
		return 4
	@staticmethod
	def get1JohnSummary():
		return "John writes a letter to Christians about keeping Jesus' commands, loving one another, and important things they should know."
	@staticmethod
	def get2JohnAuthor():
		return "John"
	@staticmethod
	def get2JohnChapters():
		return 1
	@staticmethod
	def get2JohnSummary():
		return "A very brief letter about walking in truth, love, and obedience."
	@staticmethod
	def get3JohnAuthor():
		return "John"
	@staticmethod
	def get3JohnChapters():
		return 1
	@staticmethod
	def get3JohnSummary():
		return "An even shorter letter about Christian fellowship."
	@staticmethod
	def getJudeAuthor():
		return "Jude"
	@staticmethod
	def getJudeChapters():
		return 1
	@staticmethod
	def getJudeSummary():
		return "A letter encouraging Christians to content for the faith, even though ungodly persons have crept in unnoticed."
	@staticmethod
	def getRevelationAuthor():
		return "John"
	@staticmethod
	def getRevelationChapters():
		return 21
	@staticmethod
	def getRevelationSummary():
		return "John sees visions of things that have been, things that are, and things that are yet to come."
	pass

try:
	reader = open(verse_disables, 'r')
	verse_disable_list = ast.literal_eval(reader.read())
	reader.close()
	del reader
	pass
except: pass

try:
	reader = open(version_list, 'r')
	bible_versions = ast.literal_eval(reader.read())
	reader.close()
	del reader
	pass
except: pass

try:
	reader = open(type_list, 'r')
	bible_types = ast.literal_eval(reader.read())
	reader.close()
	del reader
	pass
except: pass

try:
	reader = open(c_list, 'r')
	default_channel = ast.literal_eval(reader.read())
	reader.close()
	del reader
	pass
except: pass

try:
	reader = open(d_last_day, 'r')
	last_day = int(reader.read())
	reader.close()
	del reader
	pass
except: pass

try:
	if last_day == datetime.now().day:
		reader = open(votd_d, 'r')
		votd = reader.read()
		reader.close()
		del reader
		pass
	pass
except: pass

def parse_num(num: int) -> str:
	_num = str(num)
	_num = _num[::-1]
	_num = ','.join([_num[i:i + 3] for i in range(0, len(_num), 3)])[::-1]
	return str(_num)
	pass

def is_ascii(msg: str):
	"""
	Checks for non-ascii characters in msg.
	:param msg: A string.
	:return: True/False
	"""
	return all(ord(C) < 128 for C in msg)

def check(*msgs: str):
	"""
	Checks for non-ascii characters in each string in the parameters.
	:param msgs: 
	:return: The first instance of non-ascii string, or the last if none is found.
	"""
	for M in msgs:
		if is_ascii(M): return M
		pass
	return msgs[len(msgs) - 1]

def save(sid: str):
	"""
	Saves plugin data.
	:param sid: The server id.
	"""
	# <editor-fold desc="version_list">
	writer = open(version_list, 'w')
	writer.write(str(bible_versions))
	writer.close()
	# </editor-fold>
	# <editor-fold desc="type_list">
	writer = open(type_list, 'w')
	writer.write(str(bible_types))
	writer.close()
	# </editor-fold>
	# <editor-fold desc="verse_disables">
	writer = open(verse_disables, 'w')
	writer.write(str(verse_disable_list))
	writer.close()
	# </editor-fold>
	# <editor-fold desc="c_list">
	writer = open(c_list, 'w')
	writer.write(str(default_channel))
	writer.close()
	# </editor-fold>
	# <editor-fold desc="d_last_day">
	writer = open(d_last_day, 'w')
	writer.write(str(last_day))
	writer.close()
	# </editor-fold>
	# <editor-fold desc="votd_d">
	writer = open(votd_d, 'w')
	writer.write(votd)
	writer.close()
	# </editor-fold>

	# <editor-fold desc="PATH CHECK: _disabled_channels">
	if not os.path.exists(_disabled_channels):
		os.makedirs(_disabled_channels)
		pass
	# </editor-fold>

	# <editor-fold desc="_disabled_channels">
	writer = open(f"{_disabled_channels}{sid}.txt", 'w')
	writer.write(str(disabled_channels))
	writer.close()
	# </editor-fold>
	del writer
	pass

def abbr(_msg: str) -> str:
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
		"Est "  :"Esther",
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
	for item in list(books.keys()): _msg = _msg.lower().replace(item.lower(), books[item])
	for item in _msg.split(" "): _msg = _msg.replace(item, item.capitalize())
	return _msg

# noinspection PyUnusedLocal
def getVerse(key: str, ih: bool = True) -> str:
	"""
	Fetch a verse from the King James Version of the Bible.
	:param key: A key to search for a verse with.
	:param ih: Whether or not to include `key` at the beginning of the message.
	:return: A KJV Verse
	"""
	try:
		d = key.split(" ")
		book = ""
		chapter = ""
		verse = ""
		if len(d) == 3:
			book = d[0] + " " + d[1]
			chapter = d[2].split(":")[0]
			verse = d[2].split(":")[1]
			pass
		else:
			book = d[0]
			chapter = d[1].split(":")[0]
			verse = d[1].split(":")[1]
			pass
		ret = ""
		if ih is True: ret = f"**{key} ~ KJV**\n"
		ret += sqlkjv.read(book, chapter, verse)
		return ret
		pass
	except:
		return "No such verse!"
		pass
	pass

# noinspection PyUnusedLocal
def getPassage(key: str, ih: bool = True) -> str:
	"""
	Fetches a passage from the KJV Bible.
	:param key: The verses to fetch.
	:param ih: Whether or not to include `key` at the beginning of the reference.
	:return: The passage referred to by `key`
	"""
	stuffs = key.split(":")
	start = int(stuffs[1].split("-")[0])
	end = int(stuffs[1].split("-")[1])
	retpre = f"**{key} ~ KJV**\n"
	ret = ""
	d = key.split(" ")
	qu = ["", "", ""]
	if len(d) == 3:
		qu = [d[0] + " " + d[1], d[2].split(":")[0], d[2].split(":")[1]]
		pass
	else:
		qu = [d[0], d[1].split(":")[0], d[1].split(":")[1]]
		pass
	for i in range(start, end + 1):
		tmp = list(str(i))
		for j in range(0, len(tmp)):
			tmp[j] = symbols.symbols["^" + tmp[j]]
			pass
		tmp = ''.join(tmp)
		ret += "{} {}".format(tmp, getVerse(qu[0] + " " + qu[1] + ":" + str(i), ih=False)) + "\n"
		pass
	if ih: return retpre + ret
	else: return ret
	pass

# noinspection PyUnusedLocal
def getAKJVVerse(key: str, ih: bool = True) -> str:
	"""
	Fetch a verse from the AKJV Bible.
	:param key: The verse to fetch.
	:param ih: Whether or not to include `key` at the beginning of the reference.
	:return: The verse `key` refers to.
	"""
	try:
		d = key.split(" ")
		book = ""
		chapter = ""
		verse = ""
		if len(d) == 3:
			book = d[0] + " " + d[1]
			chapter = d[2].split(":")[0]
			verse = d[2].split(":")[1]
			pass
		else:
			book = d[0]
			chapter = d[1].split(":")[0]
			verse = d[1].split(":")[1]
			pass
		ret = ""
		if ih:
			ret = f"**{key} ~ AKJV**\n"
			pass
		ret += sqld.read(book, chapter, verse)
		return ret
		pass
	except:
		return "No such verse!"
		pass

# noinspection PyUnusedLocal
def getAKJVPassage(key: str, ih: bool = True) -> str:
	"""
	Fetch a passage from the AKJV Bible.
	:param key: The passage to fetch.
	:param ih: Whether or not to include `key` at the beginning of the reference.
	:return: The passage `key` refers to.
	"""
	stuffs = key.split(":")
	start = int(stuffs[1].split("-")[0])
	end = int(stuffs[1].split("-")[1])
	retpre = f"**{key} ~ AKJV**\n"
	ret = ""
	d = key.split(" ")
	qu = ["", "", ""]
	if len(d) == 3:
		qu = [d[0] + " " + d[1], d[2].split(":")[0], d[2].split(":")[1]]
		pass
	else:
		qu = [d[0], d[1].split(":")[0], d[1].split(":")[1]]
		pass
	for i in range(start, end + 1):
		tmp = list(str(i))
		for j in range(0, len(tmp)):
			tmp[j] = symbols.symbols["^" + tmp[j]]
			pass
		tmp = ''.join(tmp)
		ret += "{} {}".format(tmp, getAKJVVerse(qu[0] + " " + qu[1] + ":" + str(i), ih=False)) + "\n"
		pass
	if ih:
		return retpre + ret
	else:
		return ret
	pass

# noinspection PyUnusedLocal
def getWEBVerse(key: str, ih: bool = True) -> str:
	"""
	Fetch a verse from the WEB Bible.
	:param key: The verse to fetch.
	:param ih: Whether or not to include `key` in the reference.
	:return: The referred verse.
	"""
	try:
		d = key.split(" ")
		book = ""
		chapter = ""
		verse = ""
		if len(d) == 3:
			book = d[0] + " " + d[1]
			chapter = d[2].split(":")[0]
			verse = d[2].split(":")[1]
			pass
		else:
			book = d[0]
			chapter = d[1].split(":")[0]
			verse = d[1].split(":")[1]
			pass
		ret = ""
		if ih:
			ret = f"**{key} ~ WEB**\n"
			pass
		ret += sqlweb.read(book, chapter, verse)
		return ret
		pass
	except:
		return "No such verse!"
		pass

# noinspection PyUnusedLocal
def getWEBPassage(key: str, ih: bool = True) -> str:
	"""
	Fetch a passage from the WEB Bible.
	:param key: The passage to fetch.
	:param ih: Whether or not to include `key` in the reference.
	:return: The referred passage. 
	"""
	stuffs = key.split(":")
	start = int(stuffs[1].split("-")[0])
	end = int(stuffs[1].split("-")[1])
	retpre = f"**{key} ~ WEB**\n"
	ret = ""
	d = key.split(" ")
	qu = ["", "", ""]
	if len(d) == 3:
		qu = [d[0] + " " + d[1], d[2].split(":")[0], d[2].split(":")[1]]
		pass
	else:
		qu = [d[0], d[1].split(":")[0], d[1].split(":")[1]]
		pass
	for i in range(start, end + 1):
		tmp = list(str(i))
		for j in range(0, len(tmp)):
			tmp[j] = symbols.symbols["^" + tmp[j]]
			pass
		tmp = ''.join(tmp)
		ret += "{} {}".format(tmp, getWEBVerse(qu[0] + " " + qu[1] + ":" + str(i), ih=False)) + "\n"
		pass
	if ih:
		return retpre + ret
	else:
		return ret
	pass

def getChapter(key: str, version: str) -> str:
	"""
	Fetch a chapter from the Bible. Deprecated due to errors.
	:param key: The reference.
	:param version: The bible version.
	:return: The chapter text.
	"""
	ret = "{}\n".format(key)
	res = ""
	if version == "kjv":
		res = sqlkjv.execute("SELECT * FROM kjv WHERE key LIKE '{}:%';".format(key))
		pass
	elif version == "akjv":
		res = sqld.execute("SELECT * FROM akjv WHERE key LIKE '{}:%';".format(key))
		pass
	elif version == "web":
		res = sqlweb.execute("SELECT * FROM web WHERE key LIKE '{}:%';".format(key))
		pass
	for r in res:
		v = r[0].split(":")[1]
		ret += "[{}] {}".format(v, r[1]) + "\n"
		pass
	return ret

def getRandomVerse(version: str) -> str:
	"""
	Fetches a random verse from `version`
	:param version: The version to use.
	:return: A random verse in `version`
	"""
	book = random.choice(akjv_books)
	res = ""
	if version == "kjv":
		res = sqlkjv.execute("SELECT * FROM kjv WHERE key LIKE '{}%'".format(book))
		pass
	elif version == "akjv":
		res = sqld.execute("SELECT * FROM akjv WHERE key LIKE '{}%'".format(book))
		pass
	elif version == "web":
		res = sqld.execute("SELECT * FROM web WHERE key LIKE '{}%'".format(book))
		pass
	s = random.choice(res)
	ret = "{}\n{}".format(s[0], s[1])
	return ret

def searchForVerse(key: str, p: int = 0, v: str = "kjv") -> str:
	"""
	Fetch search results for `key` in the Bible
	:param key: The key to search for.
	:param p: The page number. Default to 0 (first 10 results).
	:param v: The version. Always a string.
	:return: The search results.
	"""
	res = ""
	if v == "kjv":
		res = sqlkjv.execute(f"SELECT * FROM kjv WHERE value LIKE '%{key}%'")
		pass
	elif v == "akjv":
		res = sqld.execute(f"SELECT * FROM akjv WHERE value LIKE '%{key}%'")
		pass
	elif v == "web":
		res = sqlweb.execute(f"SELECT * FROM web WHERE value LIKE '%{key}%'")
		pass

	ret = "```"
	total = 0
	if len(res) > p * 10 + 10:
		for i in range(p * 10, p * 10 + 10): ret += "{}\n".format(res[i][0])
	elif len(res) > 0:
		for i in range(0, len(res)): ret += "{}\n".format(res[i][0])

	for item in res: total += len(re.findall(key, item[1], flags=2))
	ret += f"{parse_num(total)} occurences found, {parse_num(int(math.ceil(total / 10)))} pages overall!```"
	return ret

def format_message(cont: str) -> list:
	"""
	Format a message to use with discord, splitting it into sections each 2000 characters long, including ``` on each side.
	:param cont: The string to format. 
	:return: A list of strings with each section of text.
	"""
	if len(cont) > 1994: return [f"{item}" for item in [cont[i:i + 1000] for i in range(0, len(cont), 1000)]]
	else: return [f"```{cont}```"]
	pass

def read(sid: str):
	"""
	Read plugin data.
	:param sid: The id of the server to read data from.
	"""
	global disabled_channels
	try:
		# noinspection PyShadowingNames
		reader = open(f"{_disabled_channels}{sid}.txt", 'r')
		disabled_channels = ast.literal_eval(reader.read())
		reader.close()
		del reader
		pass
	except:
		disabled_channels = []
		pass

	if not os.path.exists(f"{discord_settings}\\SERVER SETTINGS\\{sid}\\"): os.makedirs(f"{discord_settings}\\SERVER SETTINGS\\{sid}\\")

	pass

# noinspection PyUnresolvedReferences
class formatting:
	BOLD = "**"
	ITALIC = "*"
	UNDERLINE = "__"
	STRIKETHROUGH = "~~"
	CODE_BLOCK = "```"
	INLINE_CODE = "`"
	def __init__(self):
		self.placeholder = ""
		pass
	@staticmethod
	def apply_formatting(string: str, indices: list, types: list) -> str:
		""" 
		:param string: The string to format.
		:param indices: A list of indexes at which to apply the formatting. Will push any items to the right. To have this work properly, items have to be listed in numerical order. 
		:param types: A list of the format types to use. Use BOLD, ITALIC, UNDERLINE, STRIKETHROUGH, CODE_BLOCK, or INLINE_CODE for the formatting types. Each item can be combined.
		:return: The string, with formatting applied.
		"""

		repl = ""

		# Converts data given to a dictionary of index:type
		items = dict()
		for i in range(0, len(indices)):
			items[str(indices[i])] = types[i]
			pass

		# For each item in items, apply formatting appropriately.
		keys = items.keys()
		for i in range(0, len(keys)):
			format_code = items[keys[i]]
			if i != 0: repl += string[int(keys[i - 1]):int(keys[i])]
			else: repl += string[0:int(keys[i])]
			repl += format_code
			pass

		return repl
		pass
	pass

class Commands:
	class Member:
		@staticmethod
		async def ping(message: discord.Message):
			tm = datetime.now() - message.timestamp
			await client.send_message(message.channel, f"```LogBot Bible Online ~ {round(tm.microseconds / 1000)}```")
			pass
		@staticmethod
		async def verse_search(message: discord.Message):
			await client.send_typing(message.channel)
			c = message.content.replace("$verse search", "")
			page = 0
			if c.startswith("."): page = int(c.split(" ")[0].replace(".", ""))
			key = c.replace(f".{page} ", "")
			for item in format_message(searchForVerse(key, p=page, v=bible_versions[message.author.id])): await client.send_message(message.channel, item)
			del c
			del page
			del key
			pass
		@staticmethod
		async def verse_random(message: discord.Message):
			await client.send_typing(message.channel)
			verse = getRandomVerse(bible_versions[message.author.id])
			if bible_types[message.author.id] == "text":
				for item in format_message(verse): await client.send_message(message.channel, item)
				pass
			else:
				stuffs = verse.split("\n")
				e = discord.Embed(title=bible_versions[message.author.id], colour=discord.Colour.green()) \
					.add_field(name=stuffs[0], value=stuffs[1])
				await client.send_message(message.channel, "Here you go!", embed=e)
				del e
				del stuffs
				pass
			del verse
			pass
		@staticmethod
		async def verse_info(message: discord.Message, bi: BibleInfo):
			content = message.content.split(" ")
			content.remove(f"$verse")
			content.remove("info")
			cont = ' '.join(content)
			ret = ""
			if not " " in cont:
				if cont == "Genesis":
					ret += f"Genesis\nAuthor: {bi.getGenesisAuthor()}\nChapters: {bi.getGenesisChapters()}\n{bi.getGenesisSummary()}"
					pass
				elif cont == "Exodus":
					ret += f"Exodus\nAuthor: {bi.getExodusAuthor()}\nChapters: {bi.getExodusChapters()}\n{bi.getExodusSummary()}"
					pass
				elif cont == "Leviticus":
					ret += "Leviticus\nAuthor: {}\nChapters: {}\n{}".format(bi.getLeviticusAuthor(), bi.getLeviticusChapters(), bi.getLeviticusSummary())
					pass
				elif cont == "Numbers":
					ret += "Numbers\nAuthor: {}\nChapers: {}\n{}".format(bi.getNumbersAuthor(), bi.getNumbersChapters(), bi.getNumbersSummary())
					pass
				elif cont == "Deuteronomy":
					ret += "Deuteronomy\nAuthor: {}\nChapters: {}\n{}".format(bi.getDeuteronomyAuthor(), bi.getDeuteronomyChapters(), bi.getDeuteronomySummary())
					pass
				elif cont == "Joshua":
					ret += "Joshua\nAuthor: {}\nChapters: {}\n{}".format(bi.getJoshuaAuthor(), bi.getJoshuaChapters(), bi.getJoshuaSummary())
					pass
				elif cont == "Judges":
					ret += "Judges\nAuthor: {}\nChapters: {}\n{}".format(bi.getJudgesAuthor(), bi.getJudgesChapters(), bi.getJudgesSummary())
					pass
				elif cont == "Ruth":
					ret += "Ruth\nAuthor: {}\nChapters: {}\n{}".format(bi.getRuthAuthor(), bi.getRuthChapters(), bi.getRuthSummary())
					pass
				elif cont == "1 Samuel ":
					ret = "1 Samuel\nAuthor: {}\nChapters: {}\n{}".format(bi.get1SamuelAuthor(), bi.get1SamuelChapters(), bi.get1SamuelSummary())
					pass
				elif cont == "2 Samuel":
					ret = "2 Samuel\nAuthor: {}\nChapers: {}\n{}".format(bi.get2SamuelAuthor(), bi.get2SamuelChapters(), bi.get2SamuelSummary())
					pass
				elif cont == "1 Kings":
					ret = "1 Kings\nAuthor: {}\nChapters: {}\n{}".format(bi.get1KingsAuthor(), bi.get1KingsChapters(), bi.get1KingsSummary())
					pass
				elif cont == "2 Kings":
					ret = "2 Kings\nAuthor: {}\nChapters: {}\n{}".format(bi.get2KingsAuthor(), bi.get2KingsChapters(), bi.get2KingsSummary())
					pass
				elif cont == "1 Chronicles":
					ret = "1 Chronicles\nAuthor: {}\nChapters: {}\n{}".format(bi.get1ChroniclesAuthor(), bi.get1ChroniclesChapters(), bi.get1ChroniclesSummary())
					pass
				elif cont == "2 Chronicles":
					ret = "2 Chronicles\nAuthor: {}\nChapters: {}\n{}".format(bi.get2ChroniclesAuthor(), bi.get2ChroniclesChapters(), bi.get2ChroniclesSummary())
					pass
				elif cont == "Ezra":
					ret = "Ezra\nAuthor: {}\nChapters: {}\n{}".format(bi.getEzraAuthor(), bi.getEzraChapters(), bi.getEzraSummary())
					pass
				elif cont == "Nehemiah":
					ret = "Nehemiah\nAuthor: {}\nChapters: {}\n{}".format(bi.getNehemiahAuthor(), bi.getNehemiahChapters(), bi.getNehemiahSummary())
					pass
				elif cont == "Esther":
					ret = "Esther\nAuthor: {}\nChapters: {}\n{}".format(bi.getEstherAuthor(), bi.getEstherChapters(), bi.getEstherSummary())
					pass
				elif cont == "Job":
					ret = "Job\nAuthor: {}\nChapters: {}\n{}".format(bi.getJobAuthor(), bi.getJobChapters(), bi.getJobSummary())
					pass
				elif cont == "Psalms":
					ret = "Psalms\nAuthor: {}\nChapters: {}\n{}".format(bi.getPsalmsAuthor(), bi.getPsalmsChapters(), bi.getPsalmsSummary())
					pass
				elif cont == "Proverbs":
					ret = "Proverbs\nAuthor: {}\nChapters: {}\n{}".format(bi.getProverbsAuthor(), bi.getProverbsChapters(), bi.getProverbsSummary())
					pass
				elif cont == "Ecclesiastes":
					ret = "Ecclesiastes\nAuthor: {}\nChapters: {}\n{}".format(bi.getEcclesiastesAuthor(), bi.getEcclesiastesChapters(), bi.getEcclesiastesSummary())
					pass
				elif cont == "Songs":
					ret = "Songs\nAuthor: {}\nChapters: {}\n{}".format(bi.getSongOfSolomonAuthor(), bi.getSongOfSolomonChapters(), bi.getSongOfSolomonSummary())
					pass
				elif cont == "Isaiah":
					ret = "Isaiah\nAuthor: {}\nChapters: {}\n{}".format(bi.getIsaiahAuthor(), bi.getIsaiahChapters(), bi.getIsaiahSummary())
					pass
				elif cont == "Jeremiah":
					ret = "Jeremiah\nAuthor: {}\nChapters: {}\n{}".format(bi.getJeremiahAuthor(), bi.getJeremiahChapters(), bi.getJeremiahSummary())
					pass
				elif cont == "Lamentations":
					ret = "Lamentations\nAuthor: {}\nChapters: {}\n{}".format(bi.getLamentationsAuthor(), bi.getLamentationsChapters(), bi.getLamentationsSummary())
					pass
				elif cont == "Ezekiel":
					ret = "Ezekiel\nAuthor: {}\nChapters: {}\n{}".format(bi.getEzekielAuthor(), bi.getEzekielChapters(), bi.getEzekielSummary())
					pass
				elif cont == "Daniel":
					ret = "Daniel\nAuthor: {}\nChapters: {}\n{}".format(bi.getDanielAuthor(), bi.getDanielChapters(), bi.getDanielSummary())
					pass
				elif cont == "Hosea":
					ret = "Hosea\nAuthor: {}\nChapters: {}\n{}".format(bi.getHoseaAuthor(), bi.getHoseaChapters(), bi.getHoseaSummary())
					pass
				elif cont == "Joel":
					ret = "Joel\nAuthor: {}\nChapters: {}\n{}".format(bi.getJoelAuthor(), bi.getJoelChapters(), bi.getJoelSummary())
					pass
				elif cont == "Amos":
					ret = "Amos\nAuthor: {}\nChapters: {}\n{}".format(bi.getAmosAuthor(), bi.getAmosChapters(), bi.getAmosSummary())
					pass
				elif cont == "Obadiah":
					ret = "Obadiah\nAuthor: {}\nChapters: {}\n{}".format(bi.getObadiahAuthor(), bi.getObadiahChapters(), bi.getObadiahSummary())
					pass
				elif cont == "Jonah":
					ret = "Jonah\nAuthor: {}\nChapters: {}\n{}".format(bi.getJonahAuthor(), bi.getJonahChapters(), bi.getJonahSummary())
					pass
				elif cont == "Micah":
					ret = "Micah\nAuthor: {}\nChapters: {}\n{}".format(bi.getMicahAuthor(), bi.getMicahChapters(), bi.getMicahSummary())
					pass
				elif cont == "Nahum":
					ret = "Nahum\nAuthor: {}\nChapters: {}\n{}".format(bi.getNahumAuthor(), bi.getNahumChapters(), bi.getNahumSummary())
					pass
				elif cont == "Habakkuk":
					ret = "Habakkuk\nAuthor: {}\nChapters: {}\n{}".format(bi.getHabakkukAuthor(), bi.getHabakkukChapters(), bi.getHabakkukSummary())
					pass
				elif cont == "Zephaniah":
					ret = "Zephaniah\nAuthor: {}\nChapters: {}\n{}".format(bi.getZephaniahAuthor(), bi.getZephaniahChapters(), bi.getZephaniahSummary())
					pass
				elif cont == "Haggai":
					ret = "Haggai\nAuthor: {}\nChapters: {}\n{}".format(bi.getHaggaiAuthor(), bi.getHaggaiChapters(), bi.getHaggaiSummary())
					pass
				elif cont == "Zechariah":
					ret = "Zechariah\nAuthor: {}\nChapters: {}\n{}".format(bi.getZechariahAuthor(), bi.getZechariahChapters(), bi.getZechariahSummary())
					pass
				elif cont == "Malachi":
					ret = "Malachi\nAuthor: {}\nChapters: {}\n{}".format(bi.getMalachiAuthor(), bi.getMalachiChapters(), bi.getMalachiSummary())
					pass
				elif cont == "Matthew":
					ret = "Matthew\nAuthor: {}\nChapters: {}\n{}".format(bi.getMatthewAuthor(), bi.getMatthewChapters(), bi.getMatthewSummary())
					pass
				elif cont == "Mark":
					ret = "Mark\nAuthor: {}\nChapters: {}\n{}".format(bi.getMarkAuthor(), bi.getMarkChapters(), bi.getMarkSummary())
					pass
				elif cont == "Luke":
					ret = "Luke\nAuthor: {}\nChapters: {}\n{}".format(bi.getLukeAuthor(), bi.getLukeChapters(), bi.getLukeSummary())
					pass
				elif cont == "John":
					ret = "John\nAuthor: {}\nChapters: {}\n{}".format(bi.getJohnAuthor(), bi.getJohnChapters(), bi.getJohnSummary())
					pass
				elif cont == "Acts":
					ret = "Acts\nAuthor: {}\nChapters: {}\n{}".format(bi.getActsAuthor(), bi.getActsChapters(), bi.getActsSummary())
					pass
				elif cont == "Romans":
					ret = "Romans\nAuthor: {}\nChapters: {}\n{}".format(bi.getRomansAuthor(), bi.getRomansChapters(), bi.getRomansSummary())
					pass
				elif cont == "1 Corinthians":
					ret = "1 Corinthians\nAuthor: {}\nChapters: {}\n{}".format(bi.get1CorinthiansAuthor(), bi.get1CorinthiansChapters(), bi.get1CorinthiansSummary())
					pass
				elif cont == "2 Corinthians":
					ret = "2 Corinthians\nAuthor: {}\nChapters: {}\n{}".format(bi.get2CorinthiansAuthor(), bi.get2CorinthiansChapters(), bi.get2CorinthiansSummary())
					pass
				elif cont == "Galatians":
					ret = "Galatians\nAuthor: {}\nChapters: {}\n{}".format(bi.getGalatiansAuthor(), bi.getGalatiansChapters(), bi.getGalatiansSummary())
					pass
				elif cont == "Ephesians":
					ret = "Ephesians\nAuthor: {}\nChapters: {}\n{}".format(bi.getEphesiansAuthor(), bi.getEphesiansChapters(), bi.getEphesiansSummary())
					pass
				elif cont == "Philippians":
					ret = "Philippians\nAuthor: {}\nChapters: {}\n{}".format(bi.getPhilippiansAuthor(), bi.getPhilippiansChapters(), bi.getPhilippiansSummary())
					pass
				elif cont == "Colossians":
					ret = "Colossians\nAuthor: {}\nChapters: {}\n{}".format(bi.getColossiansAuthor(), bi.getColossiansChapters(), bi.getColossiansSummary())
					pass
				elif cont == "1 Thessalonians":
					ret = "1 Thessalonians\nAuthor: {}\nChapters: {}\n{}".format(bi.get1ThessaloniansAuthor(), bi.get1ThessaloniansChapters(), bi.get1ThessaloniansSummary())
					pass
				elif cont == "2 Thessalonians":
					ret = "2 Thessalonians\nAuthor: {}\nChapters: {}\n{}".format(bi.get2ThessaloniansAuthor(), bi.get2ThessaloniansChapters(), bi.get2ThessaloniansSummary())
					pass
				elif cont == "1 Timothy":
					ret = "1 Timothy\nAuthor: {}\nChapters: {}\n{}".format(bi.get1TimothyAuthor(), bi.get1TimothyChapters(), bi.get1TimothySummary())
					pass
				elif cont == "2 Timothy":
					ret = "2 Timothy\nAuthor: {}\nChapters: {}\n{}".format(bi.get2TimothyAuthor(), bi.get2TimothyChapters(), bi.get2TimothySummary())
					pass
				elif cont == "Titus":
					ret = "Titus\nAuthor: {}\nChapters: {}\n{}".format(bi.getTitusAuthor(), bi.getTitusChapters(), bi.getTitusSummary())
					pass
				elif cont == "Philemon":
					ret = "Philemon\nAuthor: {}\nChapters: {}\n{}".format(bi.getPhilemonAuthor(), bi.getPhilemonChapters(), bi.getPhilemonSummary())
					pass
				elif cont == "Hebrews":
					ret = "Hebrews\nAuthor: {}\nChapters: {}\n{}".format(bi.getHebrewsAuthor(), bi.getHebrewsChapters(), bi.getHebrewsSummary())
					pass
				elif cont == "James":
					ret = "James\nAuthor: {}\nChapters: {}\n{}".format(bi.getJamesAuthor(), bi.getJamesChapters(), bi.getJamesSummary())
					pass
				elif cont == "1 Peter":
					ret = "1 Peter\nAuthor: {}\nChapters: {}\n{}".format(bi.get1PeterAuthor(), bi.get1PeterChapters(), bi.get1PeterSummary())
					pass
				elif cont == "2 Peter":
					ret = "2 Peter\nAuthor: {}\nChapters: {}\n{}".format(bi.get2PeterAuthor(), bi.get2PeterChapters(), bi.get2PeterSummary())
					pass
				elif cont == "1 John":
					ret = "1 John\nAuthor: {}\nChapters: {}\n{}".format(bi.get1JohnAuthor(), bi.get1JohnChapters(), bi.get1JohnSummary())
					pass
				elif cont == "2 John":
					ret = "2 John\nAuthor: {}\nChapters: {}\n{}".format(bi.get2JohnAuthor(), bi.get2JohnChapters(), bi.get2JohnSummary())
					pass
				elif cont == "3 John":
					ret = "3 John\nAuthor: {}\nChapters: {}\n{}".format(bi.get3JohnAuthor(), bi.get3JohnChapters(), bi.get3JohnSummary())
					pass
				elif cont == "Jude":
					ret = "Jude\nAuthor: {}\nChapters: {}\n{}".format(bi.getJudeAuthor(), bi.getJudeChapters(), bi.getJudeSummary())
					pass
				elif cont == "Revelation":
					ret = "Revelation\nAuthor: {}\nChapters: {}\n{}".format(bi.getRevelationAuthor(), bi.getRevelationChapters(), bi.getRevelationSummary())
					pass
				pass
			for item in format_message(ret): await client.send_message(message.channel, item)
			del content
			del cont
			del ret
			pass
		@staticmethod
		async def verse_help(message: discord.Message):
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
			ret += '\n'.join([f"{books[item]} ~ {item}" for item in books.keys()]) + "```"
			await client.send_message(message.channel, ret)
			del ret
			del books
			pass
		@staticmethod
		async def verse_compare(message: discord.Message):
			content = message.content.replace(f"$verse compare ", "")
			if bible_types[message.author.id] == "text":
				await client.send_message(message.channel, "```" + content + "```")
				if "-" in content:
					stuffs = [getPassage(content, ih=False), getAKJVPassage(content, ih=False), getWEBPassage(content, ih=False)]
					for item in stuffs:
						for m in format_message(item): await client.send_message(message.channel, m)
						pass
					del stuffs
					pass
				else:
					stuffs = [getVerse(content, ih=False), getAKJVVerse(content, ih=False), getWEBVerse(content, ih=False)]
					for item in stuffs: await client.send_message(message.content, f"```{item}```")
					del stuffs
					pass
				pass
			else:
				if "-" in content:
					stuffs = [getPassage(content, ih=False), getAKJVPassage(content, ih=False), getWEBPassage(content, ih=False)]
					e = discord.Embed(title="Verse Compare", description=f"Comparison of {content}", colour=discord.Colour.teal()) \
						.add_field(name="KJV", value=stuffs[0]) \
						.add_field(name="AKJV", value=stuffs[1]) \
						.add_field(name="WEB", value=stuffs[2])
					await client.send_message(message.channel, "Here you go!", embed=e)
					del stuffs
					del e
					pass
				else:
					stuffs = [getVerse(content, ih=False), getAKJVVerse(content, ih=False), getWEBVerse(content, ih=False)]
					e = discord.Embed(title="Verse Compare", description=f"Comparation of {content}", colour=discord.Colour.teal()) \
						.add_field(name="KJV", value=stuffs[0]) \
						.add_field(name="AKJV", value=stuffs[1]) \
						.add_field(name="WEB", value=stuffs[2])
					await client.send_message(message.channel, "Here you go!", embed=e)
					del stuffs
					del e
					pass
				pass
			del content
			pass
		@staticmethod
		async def send_votd(message: discord.Message):
			e = discord.Embed(title="Verse of the Day", description="Version: akjv", colour=discord.Colour.dark_blue())
			if "-" in votd: e.add_field(name=votd, value=getAKJVPassage(votd, ih=False))
			else: e.add_field(name=votd, value=getAKJVVerse(votd, ih=False))
			await client.send_message(message.channel, "", embed=e)
			del e
			pass
		@staticmethod
		async def setversion(message: discord.Message):
			c = message.content.replace(f"$setversion ", "")
			if c == "kjv" or c == "akjv" or c == "web": bible_versions[message.author.id] = c
			await client.send_message(message.channel, f"Set version to {c}")
			del c
			pass
		@staticmethod
		async def settype(message: discord.Message):
			c = message.content.replace(f"$settype ", "").lower()
			if c == "text" or c == "embed": bible_types[message.author.id] = c
			await client.send_message(message.channel, f"```Set the type to: {c}```")
			del c
			pass
		@staticmethod
		async def disables(message: discord.Message):
			ret = [str(client.get_channel(_id)) if client.get_channel(_id).server == message.server else None for _id in disabled_channels]
			remove = ret.remove
			while None in ret: remove(None)
			ret = ', '.join(ret)
			try: await client.send_message(message.channel, ret)
			except: await client.send_message(message.channel, "```No channels have been disabled!```")
			del remove
			del ret
			pass
		pass
	class Admin:
		@staticmethod
		async def setchannel(message: discord.Message):
			if "None" in message.content:
				del default_channel[message.server.id]
				await client.send_message(message.channel, "Set the default channel to None.")
				pass
			else:
				default_channel[message.server.id] = message.channel_mentions[0].id
				await client.send_message(message.channel, f"Set the default channel to {message.channel_mentions[0].mention}")
				pass
			pass
		@staticmethod
		async def disable(message: discord.Message):
			verse_disable_list.append(message.server.id)
			pass
		@staticmethod
		async def enable(message: discord.Message):
			verse_disable_list.remove(message.server.id)
			pass
		@staticmethod
		async def v_disable(message: discord.Message):
			ret = []
			if len(message.channel_mentions) > 0:
				for c in message.channel_mentions:
					ret.append(str(c))
					disabled_channels.append(c.id)
					pass
				ret = f"```Disabled {', '.join(ret)}```"
				pass
			else:
				disabled_channels.append(message.channel.id)
				ret = f"```Disabled {str(message.channel)}```"
				pass
			save(message.server.id)
			await client.send_message(message.channel, ret)
			del ret
			pass
		@staticmethod
		async def v_enable(message: discord.Message):
			ret = ""
			if len(message.channel_mentions) > 0:
				for c in message.channel_mentions:
					ret += ", " + str(c)
					disabled_channels.remove(c.id)
					pass
				ret = "```Enabled " + ret[2:] + "```"
				pass
			else:
				disabled_channels.remove(message.channel.id)
				ret = f"```Enabled {str(message.channel)}```"
				pass
			save(message.server.id)
			await client.send_message(message.channel, ret)
			pass
		pass
	class Owner:
		@staticmethod
		async def exit():
			await client.logout()
			exit(0)
			pass
		pass
	pass

@asyncio.coroutine
def trigger_votd():
	"""
	Sends the verse of the day in each channel set for each server.
	"""
	global last_day, votd
	if last_day != datetime.now().day:
		last_day = datetime.now().day
		key = random.choice(top_verses)
		votd = key
		e = discord.Embed(title="Verse of the Day", description="Version: akjv", colour=discord.Colour.dark_blue())
		if "-" in key: e.add_field(name=key, value=getAKJVPassage(key, ih=False))
		else: e.add_field(name=key, value=getAKJVVerse(key, ih=False))
		encountered = []
		for channel in client.get_all_channels():
			server = channel.server
			if server.id in list(default_channel.keys()) and not server.id in encountered:
				channel = client.get_channel(default_channel[server.id])
				yield from client.send_message(channel, "Here is the VotD! :calendar_spiral:", embed=e)
				encountered.append(server.id)
				pass
			pass
		pass
	pass

@client.event
async def sendNoPerm(message: discord.Message):
	"""
	Sends a `NO PERMISSION` message to a user.
	:param message: a discord.Message object from on_message.
	"""
	await client.send_message(message.channel, "```You do not have permission to use this command.```")
	print("{}{} attempted to use a command.{}".format(Fore.LIGHTGREEN_EX, check(message.author.nick, message.author.name, message.author.id), Fore.RESET))

@client.event
async def sendDisabled(message: discord.Message):
	"""
	Send a `DISABLED` message to a user.
	:param message: A discord.Message object from on_message.
	"""
	await client.send_message(message.channel, "```That command has been disabled!!!```")
	pass

@client.event
async def on_message(message):
	await trigger_votd()
	read(message.server.id)
	bible_versions[message.author.id] = bible_versions[message.author.id] if not bible_versions.get(message.author.id) is None else "akjv"
	bible_types[message.author.id] = bible_types[message.author.id] if not bible_types.get(message.author.id) is None else "embed"
	if not message.server.id in verse_disable_list:
		if not message.author.bot:
			if not message.content.startswith(f"$verse ") and not message.content.startswith("$devotional\n"):
				if not message.channel.id in disabled_channels:
					for mcont in message.content.split("\n"):
						e = discord.Embed(title=bible_versions[message.author.id], colour=discord.Colour.purple())
						encountered = []
						tmp_content = mcont.replace(".", " ")\
							.replace("`", "")\
							.replace("*", "")\
							.replace("_", "")
						verse = []
						tmp_content = abbr(tmp_content)
						for i in range(0, 17): tmp_content = tmp_content.replace(akjv_books[i], akjv_books[i].replace(" ", "|"))
						mc = tmp_content.split(" ")
						append = verse.append
						for i in range(0, len(mc)): mc[i] = abbr(mc[i].replace("|", " ").capitalize())
						for b in akjv_books:
							while b in mc:
								index = mc.index(b)
								if not index == len(mc) - 1:
									if "," in mc[index + 1]:
										for item in mc[index + 1].split(":")[1].split(","): append(f"{mc[index]} {mc[index+1].split(':')[0]}:{item}")
										pass
									else: verse.append(f"{mc[index]} {mc[index+1]}")
									pass
								mc.remove(b)
								pass
							pass
						for v in verse:
							if bible_types[message.author.id] == "text":
								if "-" in v and not v in encountered:
									if bible_versions[message.author.id] == "kjv":
										for m in format_message(getPassage(v, ih=True)):
											m = m.replace("```", "").split('\n')
											m[1] = f"```{m[1]}"
											m = '\n'.join(m) + "```"
											await client.send_message(message.channel, m)
											pass
										pass
									elif bible_versions[message.author.id] == "akjv":
										for m in format_message(getAKJVPassage(v, ih=True)):
											m = m.replace("```", "").split('\n')
											m[1] = f"```{m[1]}"
											m = '\n'.join(m) + "```"
											await client.send_message(message.channel, m)
											pass
										pass
									elif bible_versions[message.author.id] == "web":
										for m in format_message(getWEBPassage(v, ih=True)):
											m = m.replace("```", "").split('\n')
											m[1] = f"```{m[1]}"
											m = '\n'.join(m) + "```"
											await client.send_message(message.channel, m)
											pass
										pass
									pass
								elif ":" in v and not v in encountered:
									if bible_versions[message.author.id] == "kjv":
										for m in format_message(getVerse(v, ih=True)):
											m = m.replace("```", "").split('\n')
											m[1] = f"```{m[1]}"
											m = '\n'.join(m) + "```"
											await client.send_message(message.channel, m)
											pass
										pass
									elif bible_versions[message.author.id] == "akjv":
										for m in format_message(getAKJVVerse(v, ih=True)):
											m = m.replace("```", "").split('\n')
											m[1] = f"```{m[1]}"
											m = '\n'.join(m) + "```"
											await client.send_message(message.channel, m)
											pass
										pass
									elif bible_versions[message.author.id] == "web":
										for m in format_message(getWEBVerse(v, ih=True)):
											m = m.replace("```", "").split('\n')
											m[1] = f"```{m[1]}"
											m = '\n'.join(m) + "```"
											await client.send_message(message.channel, m)
											pass
										pass
									pass
								pass
							else:
								if "-" in v and not v in encountered:
									if bible_versions[message.author.id] == "kjv": e.add_field(name=v, value=getPassage(v, ih=False))
									elif bible_versions[message.author.id] == "akjv": e.add_field(name=v, value=getAKJVPassage(v, ih=False))
									elif bible_versions[message.author.id] == "web": e.add_field(name=v, value=getWEBPassage(v, ih=False))
									pass
								elif ":" in v and not v in encountered:
									if bible_versions[message.author.id] == "kjv": e.add_field(name=v, value=getVerse(v, ih=False))
									elif bible_versions[message.author.id] == "akjv": e.add_field(name=v, value=getAKJVVerse(v, ih=False))
									elif bible_versions[message.author.id] == "web": e.add_field(name=v, value=getWEBVerse(v, ih=False))
									pass
								pass
							encountered.append(v)
							pass
						if bible_types[message.author.id] == "embed" and len(e.fields) >= 1:
							try:
								# <editor-fold desc="Fetching Title...">
								index = list(mcont).index('"')
								title = ""
								has_found = False
								for i in range(index+1, len(mcont)):
									if mcont[i] == "\"": has_found = True
									if not has_found: title += mcont[i]
									pass
								title=' '.join([t for t in title.split(" ")])
								# </editor-fold>
								e.title = title
								e.description = bible_versions[message.author.id]
								pass
							except: pass

							for i in range(0, len(e.fields)):
								if e.fields[i].value == "No such verse!": e.remove_field(i)
								pass

							tm = datetime.now() - message.timestamp
							# delay = int(divmod(tm.total_seconds(), 60)[1] * 1000)
							# delay = int((tm.total_seconds() % 60) * 1000)
							delay = int(tm.microseconds / 1000)
							if delay > 999: delay = str(delay / 1000)
							else: delay = f"0.{delay}"
							await client.send_message(message.channel, f"Response in {delay} seconds! :smile:", embed=e)
							print(f"Sending {', '.join(verse)} ~ Delay: {delay}s.")
							pass
						pass
					pass
				pass
			pass
		pass
	# if not message.server.id in verse_disable_list and not message.author.bot and not message.content.startswith(f"$verse ") and not message.channel.id in disabled_channels:
	# 	# try:
	# 	for mcont in message.content.split("\n"):
	# 		myembed = discord.Embed(title=bible_versions[message.author.id], colour=discord.Colour.purple())
	# 		encountered = []
	# 		tmp_content = mcont.replace(".", " ").replace("`", "").replace("*", "").replace("_", "")
	# 		verse = []
	# 		tmp_content = abbr(tmp_content)
	# 		for i in range(0, 17):
	# 			tmp_content = tmp_content.replace(akjv_books[i], akjv_books[i].replace(" ", "|"))
	# 			pass
	# 		mc = tmp_content.split(" ")
	# 		for i in range(0, len(mc)):
	# 			mc[i] = mc[i].replace("|", " ")
	# 			mc[i] = mc[i].capitalize()
	# 			mc[i] = abbr(mc[i])
	# 			pass
	# 		for b in akjv_books:
	# 			while b in mc:
	# 				if not mc.index(b) == len(mc) - 1:
	# 					index = mc.index(b)
	# 					if "," in mc[index + 1]:
	# 						for item in mc[index + 1].split(":")[1].split(","):
	# 							verse.append(mc[index] + " " + mc[index + 1].split(":")[0] + ":" + item)
	# 							pass
	# 						pass
	# 					else:
	# 						verse.append(mc[index] + " " + mc[index + 1])
	# 						pass
	# 					pass
	# 				mc.remove(b)
	# 				pass
	# 			pass
	# 		for v in verse:
	# 			if bible_types[message.author.id] == "text":
	# 				if "-" in v and not v in encountered:
	# 					if bible_versions[message.author.id] == "kjv":
	# 						for m in format_message(getPassage(v, ih=True)):
	# 							m = m.split("\n")
	# 							t = m[1]
	# 							m[1] = f"```{t}```"
	# 							m = '\n'.join(m)
	# 							await client.send_message(message.channel, m)
	# 							pass
	# 						pass
	# 					elif bible_versions[message.author.id] == "akjv":
	# 						for m in format_message(getAKJVPassage(v, ih=True)):
	# 							m = m.split("\n")
	# 							t = m[1]
	# 							m[1] = f"```{t}```"
	# 							m = '\n'.join(m)
	# 							await client.send_message(message.channel, m)
	# 							pass
	# 						pass
	# 					elif bible_versions[message.author.id] == "web":
	# 						for m in format_message(getWEBPassage(v, ih=True)):
	# 							m = m.split("\n")
	# 							t = m[1]
	# 							m[1] = f"```{t}```"
	# 							m = '\n'.join(m)
	# 							await client.send_message(message.channel, m)
	# 							pass
	# 						pass
	# 					pass
	# 				elif ":" in v and not v in encountered:
	# 					if bible_versions[message.author.id] == "kjv":
	# 						for m in format_message(getVerse(v, ih=True)):
	# 							m = m.split("\n")
	# 							t = m[1]
	# 							m[1] = f"```{t}```"
	# 							m = '\n'.join(m)
	# 							await client.send_message(message.channel, m)
	# 							pass
	# 						pass
	# 					elif bible_versions[message.author.id] == "akjv":
	# 						for m in format_message(getAKJVVerse(v, ih=True)):
	# 							m = m.split("\n")
	# 							t = m[1]
	# 							m[1] = f"```{t}```"
	# 							m = '\n'.join(m)
	# 							await client.send_message(message.channel, m)
	# 							pass
	# 						pass
	# 					elif bible_versions[message.author.id] == "web":
	# 						for m in format_message(getWEBVerse(v, ih=True)):
	# 							m = m.split("\n")
	# 							t = m[1]
	# 							m[1] = f"```{t}```"
	# 							m = '\n'.join(m)
	# 							await client.send_message(message.channel, m)
	# 							pass
	# 						pass
	# 					pass
	# 				pass
	# 			else:
	# 				if "-" in v and not v in encountered:
	# 					if bible_versions[message.author.id] == "kjv":
	# 						myembed.add_field(name=v, value=getPassage(v, ih=False))
	# 						pass
	# 					if bible_versions[message.author.id] == "akjv":
	# 						myembed.add_field(name=v, value=getAKJVPassage(v, ih=False))
	# 						pass
	# 					if bible_versions[message.author.id] == "web":
	# 						myembed.add_field(name=v, value=getWEBPassage(v, ih=False))
	# 						pass
	# 					pass
	# 				elif ":" in v and not v in encountered:
	# 					if bible_versions[message.author.id] == "kjv":
	# 						myembed.add_field(name=v, value=getVerse(v, ih=False))
	# 						pass
	# 					if bible_versions[message.author.id] == "akjv":
	# 						myembed.add_field(name=v, value=getAKJVVerse(v, ih=False))
	# 						pass
	# 					if bible_versions[message.author.id] == "web":
	# 						myembed.add_field(name=v, value=getWEBVerse(v, ih=False))
	# 						pass
	# 					pass
	# 				pass
	# 			encountered.append(v)
	# 			pass
	# 		if bible_types[message.author.id] == "embed" and len(myembed.fields) >= 1:
	# 			try:
	# 				# <editor-fold desc="Fetching Title...">
	# 				index = list(mcont).index('"')
	# 				title = ""
	# 				has_found = False
	# 				for i in range(index + 1, len(mcont)):
	# 					if mcont[i] == "\"": has_found = True
	# 					if not has_found: title += mcont[i]
	# 					pass
	# 				title = ' '.join([t for t in title.split(" ")])
	# 				# </editor-fold>
	# 				myembed.title = title
	# 				myembed.description = bible_versions[message.author.id]
	# 				pass
	# 			except:
	# 				pass
	#
	# 			tm = datetime.now() - message.timestamp
	# 			# delay = int(divmod(tm.total_seconds(), 60)[1] * 1000)
	# 			# delay = int((tm.total_seconds() % 60)*1000)
	# 			delay = int(tm.microseconds / 1000)
	# 			if delay > 999: delay = str(delay / 1000)
	# 			else: delay = "0." + str(delay)
	# 			await client.send_message(message.channel, f"Response in {delay} seconds! :smile:", embed=myembed)
	# 			print(f"sending {', '.join(verse)} ~ Delay: {delay}s")
	# 			pass
	# 		pass
	# 	pass
	# except:pass
	# pass

	do_update = False

	owner_id = "239500860336373761"

	admin_role = discord.utils.find(lambda r:r.name == "LogBot Admin", message.server.roles)
	def startswith(*msg, val=message.content):
		# noinspection PyShadowingNames
		for item in msg:
			if val.startswith(item): return True
		return False
	bi = BibleInfo()

	if startswith(f"$disable verse", f"$disable $verse"):
		if admin_role in message.author.roles or message.author.id == owner_id: await Commands.Admin.disable(message)
		else: sendNoPerm(message)
		pass
	elif startswith(f"$enable verse", f"$enable $verse"):
		if admin_role in message.author.roles or message.author.id == owner_id: await Commands.Admin.enable(message)
		else: sendNoPerm(message)
		pass
	elif startswith(f"$verse help"):
		if not message.server.id in verse_disable_list or message.author.id == owner_id: await Commands.Member.verse_help(message)
		elif message.server.id in verse_disable_list: sendDisabled(message)
		else: sendNoPerm(message)
		pass
	elif startswith(f"$verse info "):
		if not message.server.id in verse_disable_list or message.author.id == owner_id: await Commands.Member.verse_info(message, bi)
		elif message.server.id in verse_disable_list: sendDisabled(message)
		else: sendNoPerm(message)
		pass
	elif startswith(f"$verse random"):
		if not message.server.id in verse_disable_list or message.author.id == owner_id: await Commands.Member.verse_random(message)
		elif message.server.id in verse_disable_list: sendDisabled(message)
		else: sendNoPerm(message)
		pass
	elif startswith(f"$verse search"):
		if not message.server.id in verse_disable_list or message.author.id == owner_id: await Commands.Member.verse_search(message)
		elif message.server.id in verse_disable_list: sendDisabled(message)
		else: sendNoPerm(message)
		pass
	elif startswith(f"$verse compare "):
		if not message.server.id in verse_disable_list or message.author.id == owner_id: await Commands.Member.verse_compare(message)
		elif message.server.id in verse_disable_list: sendDisabled(message)
		else: sendNoPerm(message)
		pass
	elif startswith(f"$votd"): await Commands.Member.send_votd(message)
	elif startswith(f"$setversion "): await Commands.Member.setversion(message)
	elif startswith(f"$settype "): await Commands.Member.settype(message)
	elif startswith(f"$getversion", f"$setversion"):
		await client.send_message(message.channel, bible_versions[message.author.id])
		pass
	elif startswith(f"$gettype", f"$settype"):
		await client.send_message(message.channel, bible_types[message.author.id])
		pass
	elif startswith(f"$setchannel "):
		if admin_role in message.author.roles: await Commands.Admin.setchannel(message)
		else: sendNoPerm(message)
		pass
	elif startswith(f"$getchannel"):
		await client.send_message(message.channel, f"The default channel is <#{default_channel[message.server.id]}>")
		pass
	elif startswith(f"v$disables"): await Commands.Member.disables(message)
	elif startswith(f"v$disable"):
		if admin_role in message.author.roles or message.author.id == owner_id: await Commands.Admin.v_disable(message)
		else: sendNoPerm(message)
		pass
	elif startswith(f"v$enable"):
		if admin_role in message.author.roles or message.author.id == owner_id: await Commands.Admin.v_enable(message)
		else: sendNoPerm(message)
		pass
	elif startswith("logbot.settings exit", "logbot.bible.exit"):
		if message.author.id == owner_id: await Commands.Owner.exit()
		else: sendNoPerm(message)
		pass
	elif startswith(f"$update", "logbot.bible.update"):
		if message.author.id == owner_id: do_update = True
		else: sendNoPerm(message)
		pass
	elif startswith(f"$ping"): await Commands.Member.ping(message)
	elif startswith(f"$devotional\n"):
		lines = message.content.replace("$devotional\n", "").split("\n")
		e = discord.Embed(title="", description="", colour=discord.Colour.green())
		for line in lines:
			if line.startswith("&title="): e.title = line.replace("&title=", "")
			elif line.startswith("&description="): e.description = line.replace("&description=", "")
			elif line.startswith("&author=") or line.startswith("&footer="): e.set_footer(text=line.replace("&author=", "").replace("&footer=", ""))
			elif line.startswith("&thumbnail="): e.set_thumbnail(url=line.replace("&thumbnail=", ""))
			elif line.startswith("&passage="):
				def analyzeVerse(text, _version="kjv"):
					if _version == "kjv":
						if "-" in text: return [text, getPassage(text, ih=False)]
						else: return [text, getVerse(text, ih=False)]
						pass
					elif _version == "akjv":
						if "-" in text: return [text, getAKJVPassage(text, ih=False)]
						else: return [text, getAKJVVerse(text, ih=False)]
						pass
					elif _version == "web":
						if "-" in text: return [text, getWEBPassage(text, ih=False)]
						else: return [text, getWEBVerse(text, ih=False)]
						pass
					pass
				_text = line.replace("&passage=", "")
				version = bible_versions[message.author.id]
				ret = analyzeVerse(_text.capitalize(), _version=version)
				e.add_field(name=ret[0], value=ret[1], inline=False)
				pass
			elif line.startswith("&text="):
				if "|" in line: _title = line.replace("&text=", "").split("|")[0]; _text = line.replace("&text=", "").split("|")[1]
				else: _title = "` `"; _text = line.replace("&text=", "")
				e.add_field(name=_title, value=_text, inline=False)
				pass
			pass
		await client.send_message(message.channel, "", embed=e)
		pass
	elif startswith(f"$devotional"):
		_msgs = []
		lines = []
		mappend = _msgs.append
		lappend = lines.append
		cont = True
		_msg = await client.wait_for_message(author=message.author)
		mappend(_msg)
		lappend(_msg.content)
		while cont:
			_msg = await client.wait_for_message(author=message.author)
			if _msg.content == "&end": cont = False; mappend(_msg)
			else: lappend(_msg.content); mappend(_msg)
			pass
		mappend(message)
		e = discord.Embed(title="", description="", colour=discord.Colour.green())
		for line in lines:
			if line.startswith("&title="): e.title = line.replace("&title=", "")
			elif line.startswith("&description="): e.description = line.replace("&description=", "")
			elif line.startswith("&author=") or line.startswith("&footer="): e.set_footer(text=line.replace("&author=", "").replace("&footer=", ""))
			elif line.startswith("&thumbnail="): e.set_thumbnail(url=line.replace("&thumbnail=", ""))
			elif line.startswith("&passage="):
				def analyzeVerse(text, _version="kjv"):
					if _version == "kjv":
						if "-" in text: return [text, getPassage(text, ih=False)]
						else: return [text, getVerse(text, ih=False)]
						pass
					elif _version == "akjv":
						if "-" in text: return [text, getAKJVPassage(text, ih=False)]
						else: return [text, getAKJVVerse(text, ih=False)]
						pass
					elif _version == "web":
						if "-" in text: return [text, getWEBPassage(text, ih=False)]
						else: return [text, getWEBVerse(text, ih=False)]
						pass
					pass
				_text = line.replace("&passage=", "")
				version = bible_versions[message.author.id]
				ret = analyzeVerse(_text.capitalize(), _version=version)
				e.add_field(name=ret[0], value=ret[1], inline=False)
				pass
			elif line.startswith("&text="):
				if "|" in line: _title = line.replace("&text=", "").split("|")[0]; _text = line.replace("&text=", "").split("|")[1]
				else: _title = "` `"; _text = line.replace("&text=", "")
				e.add_field(name=_title, value=_text, inline=False)
				pass
			pass
		await client.send_message(message.channel, "", embed=e)
		for m in _msgs:
			await client.delete_message(m)
			pass
		pass

	save(message.server.id)
	if do_update:
		print(f"{Fore.LIGHTCYAN_EX}Updating...{Fore.RESET}")
		subprocess.Popen(f"python {os.getcwd()}\\bible.py")
		exit(0)
		pass
	pass

@client.event
async def on_ready():
	await client.change_presence(game=None)
	os.system("cls")
	print(f"{Fore.MAGENTA}Ready!!!{Fore.RESET}")
	pass

client.run(token)
