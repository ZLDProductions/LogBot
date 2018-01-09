import os
import sqlite3
import subprocess
import traceback

sql = sqlite3.connect( "launch.db" )
cursor = sql.cursor( )

my_str = """0. logbot.py
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
D. musiclaunch.py"""
programs = {
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
	"D":"musiclaunch.py"
}
titles = {
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
	"D":"Music Plugin"
}

ext_launch = False

# <editor-fold desc="Standard initialization">
try:
	cursor.execute( f"""
CREATE TABLE packages (name VARCHAR(50), sequence VARCHAR(50));
""".replace( "\t", "" ) )
except:
	pass
try:
	cursor.execute( f"""
CREATE INDEX pkg_index
ON packages (name, sequence);
""".replace( "\t", "" ) )
except:
	pass

# </editor-fold>

def getRunPackages ( ):
	cursor.execute( f"""
	SELECT *
	FROM packages;
	""".replace( "\t", "" ) )
	res = cursor.fetchall( )
	for pkg in res: print( f"{res.index(pkg)}. {pkg[0]} - {pkg[1]}" )
	seq = res[ int( input( "Sequence to run: " ) ) ][ 1 ]
	os.system( "cls" )
	if ext_launch:
		for c in seq:
			os.system( f"start \"{titles[c]}\" /MAX /HIGH python \"{os.getcwd()}\\{programs[c]}\"" )
			pass
		pass
	else:
		for c in seq:
			subprocess.Popen( f"python \"{os.getcwd()}\\{programs[c]}\"" )
			pass
		pass
	pass

def main ( ):
	global ext_launch
	print( "T. Launch LogBot Externally\nF. Launch LogBot Internally" )
	tmp = input( f"Choice: " )
	ext_launch = (tmp.lower( ) == "t")

	print( "1. Run sequence\n2. Run package\n3. Create package\n4. Edit package\n5. Remove package." )
	choice = int( input( "Operation: " ) )
	if choice == 1:
		print( my_str )
		files = input( "Programs to launch: " )
		os.system( "cls" )
		if ext_launch:
			for c in files:
				os.system( f"start \"{titles[c]}\" /MAX /HIGH python \"{os.getcwd()}\\{programs[c]}\"" )
				pass
			pass
		else:
			for c in files:
				subprocess.Popen( f"python \"{os.getcwd()}\\{programs[c]}\"" )
				pass
			pass
		pass
	elif choice == 2:
		getRunPackages( )
		pass
	elif choice == 3:
		name = input( "Package name: " )
		sequence = input( "Package sequence: " )
		cursor.execute( f"""
		SELECT *
		FROM packages
		WHERE name="{name}"
		OR sequence="{sequence}";
		""".replace( "\t", "" ) )
		res = cursor.fetchall( )
		if len( res ) >= 1:
			print( "That package already exists." )
		else:
			cursor.execute( f"""
			INSERT INTO packages (name, sequence)
			VALUES ("{name}", "{sequence}");
			""".replace( "\t", "" ) )
			print( "Created the package." )
			pass
		main( )
		pass
	elif choice == 4:
		cursor.execute( f"""
			SELECT *
			FROM packages;
			""".replace( "\t", "" ) )
		res = cursor.fetchall( )
		for pkg in res: print( f"{res.index(pkg)}. {pkg[0]} - {pkg[1]}" )
		name = input( "Package name to edit: " )
		seq = input( "New Sequence: " )

		try:
			cursor.execute( f"""
		UPDATE packages
		SET sequence="{seq}"
		WHERE name="{name}";
		""".replace( "\t", "" ) )
			sql.commit( )
			print( "Updated the package." )
			input( "" )
			pass
		except:
			print( "Could not update the package." )
			print( traceback.format_exc( ) )
			input( "" )
			pass
		main( )
		pass
	elif choice == 5:
		cursor.execute( f"""
		SELECT *
		FROM packages;
		""".replace( "\t", "" ) )
		res = cursor.fetchall( )
		for pkg in res: print( f"{pkg[0]} - {pkg[1]}" )
		name = input( "Package name: " )
		try:
			cursor.execute( f"""
			DELETE FROM packages
			WHERE name="{name}";
			""".replace( "\t", "" ) )
			sql.commit( )
			print( "Removed the package." )
			input( "" )
			pass
		except:
			print( "Could not remove the package." )
			print( traceback.format_exc( ) )
			input( "" )
			pass
		main( )
	pass

main( )
sql.commit( )
