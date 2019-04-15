import sqlite3
import os

db_name = "chat_database.db"
path = "/root/pyServer/database/"

def check_if_db_exists():
	os.chdir(path)
	if os.path.isfile(db_name):
		return True
	else:
		create_database()

def create_user(addr, name):
	try:
		conn = sqlite3.connect(path+db_name)
		cursor = conn.cursor()
		params = (addr,)
		cursor.execute("SELECT * FROM users WHERE ip=?", params)
		if (cursor.fetchone() == None):
			print("LET's go!")
			params = (addr, name)
			cursor.execute("INSERT INTO users VALUES(?, ?)", params)
			conn.commit()
		conn.close()
	except sqlite3.Error as e:
		print e.args[0]



def create_database():
	try:
		conn = sqlite3.connect(path+db_name)
		cursor = conn.cursor()
		cursor.execute('''CREATE TABLE users (ip text, name text)''')
		conn.commit()
		conn.close()
	except sqlite3.Error as e:
		print e.args[0]

