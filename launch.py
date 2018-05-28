"""
Launch the bot.
"""
import os
import sqlite3
import subprocess
import traceback

SQL = sqlite3.connect( "launch.db" )
CURSOR = SQL.cursor( )

MY_STR = """0. logbot.py
1. bible.py
2. admin.py
3. levels.py
4. polling.py
5. help.py
6. ai.py
7. games.py
8. custom.py
9. swearing_filter_v2.py
A. dev.py
B. security.py
C. moderation.py
D. musiclaunch.py
E. reminders.py"""
PROGRAMS = {
	"0":"logbot.py",
	"1":"bible.py",
	"2":"admin.py",
	"3":"levels.py",
	"4":"polling.py",
	"5":"help.py",
	"6":"ai.py",
	"7":"games.py",
	"8":"custom.py",
	"9":"swearing_filter_v2.py",
	"A":"dev.py",
	"B":"security.py",
	"C":"moderation.py",
	"D":"musiclaunch.py",
	"E":"reminders.py"
}
TITLES = {
	"0":"LogBot Main",
	"1":"Bible Plugin",
	"2":"Admin Plugin",
	"3":"Levels Plugin",
	"4":"Polling Plugin",
	"5":"Help Plugin",
	"6":"AI Plugin",
	"7":"Games Plugin",
	"8":"Custom Commands Plugin",
	"9":"Swearing Filter V2 Plugin",
	"A":"Dev Plugin",
	"B":"Security Plugin",
	"C":"Moderation Plugin",
	"D":"Music Plugin",
	"E":"Reminders Plugin"
}

EXT_LAUNCH = False

# <editor-fold desc="Standard initialization">
try:
	CURSOR.execute( f"""
	CREATE TABLE packages (name VARCHAR(50), sequence VARCHAR(50));
	""".replace( "\t", "" ) )
except Exception:
	pass
try:
	CURSOR.execute( f"""
	CREATE INDEX pkg_index
	ON packages (name, sequence);
	""".replace( "\t", "" ) )
except Exception:
	pass

# </editor-fold>

def get_run_packages ( ):
	"""
	Package runner.
	"""
	CURSOR.execute( f"""
	SELECT *
	FROM packages;
	""".replace( "\t", "" ) )
	res = CURSOR.fetchall( )
	for pkg in res:
		print( f"{res.index(pkg)}. {pkg[0]} - {pkg[1]}" )
	seq = res[ int( input( "Sequence to run: " ) ) ][ 1 ]
	os.system( "cls" )
	if EXT_LAUNCH:
		for character in seq:
			os.system(
				f"start \"{TITLES[character]}\" /MAX /HIGH python \"{os.getcwd()}\\{PROGRAMS[character]}\""
			)
	else:
		for character in seq:
			subprocess.Popen( f"python \"{os.getcwd()}\\{PROGRAMS[character]}\"" )

def main ( ):
	"""
	Main Menu
	"""
	global EXT_LAUNCH
	print( "T. Launch LogBot Externally\nF. Launch LogBot Internally" )
	tmp = input( f"Choice: " )
	EXT_LAUNCH = (tmp.lower( ) == "t")

	print( "1. Run sequence\n2. Run package\n3. Create package\n4. Edit package\n5. Remove package." )
	choice = int( input( "Operation: " ) )
	if choice == 1:
		print( MY_STR )
		files = input( "Programs to launch: " )
		os.system( "cls" )
		if EXT_LAUNCH:
			for character in files:
				os.system(
					f"start \"{TITLES[character]}\" /MAX /HIGH python \"{os.getcwd()}\\{PROGRAMS[character]}\""
				)
		else:
			for character in files:
				subprocess.Popen( f"python \"{os.getcwd()}\\{PROGRAMS[character]}\"" )
	elif choice == 2:
		get_run_packages( )
	elif choice == 3:
		name = input( "Package name: " )
		sequence = input( "Package sequence: " )
		CURSOR.execute( f"""
		SELECT *
		FROM packages
		WHERE name="{name}"
		OR sequence="{sequence}";
		""".replace( "\t", "" ) )
		res = CURSOR.fetchall( )
		if len( res ) >= 1:
			print( "That package already exists." )
		else:
			CURSOR.execute( f"""
			INSERT INTO packages (name, sequence)
			VALUES ("{name}", "{sequence}");
			""".replace( "\t", "" ) )
			print( "Created the package." )
		main( )
	elif choice == 4:
		CURSOR.execute( f"""
			SELECT *
			FROM packages;
			""".replace( "\t", "" ) )
		res = CURSOR.fetchall( )
		for pkg in res:
			print( f"{res.index(pkg)}. {pkg[0]} - {pkg[1]}" )
		name = input( "Package name to edit: " )
		seq = input( "New Sequence: " )

		try:
			CURSOR.execute( f"""
			UPDATE packages
			SET sequence="{seq}"
			WHERE name="{name}";
			""".replace( "\t", "" ) )
			SQL.commit( )
			print( "Updated the package." )
			input( "" )
		except Exception:
			print( "Could not update the package." )
			print( traceback.format_exc( ) )
			input( "" )
		main( )
	elif choice == 5:
		CURSOR.execute( f"""
		SELECT *
		FROM packages;
		""".replace( "\t", "" ) )
		res = CURSOR.fetchall( )
		for pkg in res:
			print( f"{pkg[0]} - {pkg[1]}" )
		name = input( "Package name: " )
		try:
			CURSOR.execute( f"""
			DELETE FROM packages
			WHERE name="{name}";
			""".replace( "\t", "" ) )
			SQL.commit( )
			print( "Removed the package." )
			input( "" )
		except Exception:
			print( "Could not remove the package." )
			print( traceback.format_exc( ) )
			input( "" )
		main( )

main( )
SQL.commit( )
