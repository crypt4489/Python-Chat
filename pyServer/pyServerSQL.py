import sqlite3
import os

db_name = "chat_database.db"
path = "./"


def resolve_name_to_addr(name):
	try:	
		conn = sqlite3.connect(path+db_name)
		cursor = conn.cursor()
		params = (name,)
		cursor.execute("SELECT * FROM users WHERE name=?", params)
		addr = ""
		row = cursor.fetchone()
		if (row != None):
			addr = row[0]
		conn.close()
		return str(addr)
	except sqlite3.Error as e:
		print e.args[0]

def check_if_db_exists():
	os.chdir(path)
	if os.path.isfile(db_name):
		return True
	else:
		create_database()

def get_all_names():
	try:	
		conn = sqlite3.connect(path+db_name)
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM users")
		names = []
		rows = cursor.fetchall()
		if (rows != None):
			for row in rows:
				names.append(str(row[1]))
		conn.close()
		return names
	except sqlite3.Error as e:
		print e.args[0]



def validate_token(token):
	try:
		result = False
		conn = sqlite3.connect(path+db_name)
		cursor = conn.cursor()
		params = (token,)
		cursor.execute("SELECT * FROM tokens WHERE token=?", params)
		if (cursor.fetchone() != None):
			result = True
		conn.close()
		return result
	except sqlite3.Error as e:
		print e.args[0]

def validate_pwd(name, pwd):
	try:
		result = False
		conn = sqlite3.connect(path+db_name)
		cursor = conn.cursor()
		params = (name, pwd)
		cursor.execute("SELECT * FROM users WHERE name=? AND pwd_encrypt=?", params)
		if (cursor.fetchone() != None):
			result = True
		conn.close()
		return result
	except sqlite3.Error as e:
		print e.args[0]


def create_user(addr, name, pwd):
	try:
		result = None
		conn = sqlite3.connect(path+db_name)
		cursor = conn.cursor()
		params = (name,)
		cursor.execute("SELECT * FROM users WHERE name=?", params)
		if (cursor.fetchone() == None):
			params = (addr, name, pwd)
			cursor.execute("INSERT INTO users VALUES(?, ?, ?)", params)
			conn.commit()
			result = "SQL_INSERT"
		else:
			params = (addr, name)
			cursor.execute("UPDATE users SET ip = ? WHERE name = ?", params)
			conn.commit()
			result = "SQL_UPDATE"
		conn.close()
		return result
	except sqlite3.Error as e:
		print e.args[0]



def create_database():
	try:
		conn = sqlite3.connect(path+db_name)
		cursor = conn.cursor()
		cursor.execute('''CREATE TABLE users (ip text,
 name text UNIQUE, pwd_encrypt text)''')
		cursor.execute('''CREATE TABLE tokens (token_id INTEGER PRIMARY KEY, token text UNIQUE)''')
		conn.commit()
		conn.close()
	except sqlite3.Error as e:
		print e.args[0]

