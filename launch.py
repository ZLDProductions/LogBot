import os

my_str = """0. logbot.py
1. bible.py
2. admin.py
3. levels.py
4. polling.py
5. help.py
6. ai.py
7. games.py
8. swearing_filter.py
9. swearing_filter_v2.py"""
programs = {
	"0":"logbot.py",
	"1":"bible.py",
	"2":"admin.py",
	"3":"levels.py",
	"4":"polling.py",
	"5":"help.py",
	"6":"ai.py",
	"7":"games.py",
	"8":"swearing_filter.py",
	"9":"swearing_filter_v2.py"
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
	"8":"Swearing Filter Plugin",
	"9":"Swearing Filter V2 Plugin"
}

def main():
	print(my_str)
	files = input("Programs to launch: ")
	for c in files:
		os.system(f"start \"{titles[c.lower()]}\" /MAX /HIGH python {os.getcwd()}\\{programs[c.lower()]}")
		pass
	pass

main()