import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet


def check_for_key():
	data = None	
	with open("./.env", "r") as f:
		data = f.readlines()
	f.close()
	if (data[2] == "key=\n"):
		key = Fernet.generate_key()
		print(key)
		key_utf8 = key.decode("utf-8")			
		data[2] = "key="+key_utf8+"\n"
		print(data)
		with open("./.env", "w") as f:
			f.writelines(data)
		f.close()
	
def setup_environment():
	check_for_key()
	load_dotenv()
			
	
	
	
