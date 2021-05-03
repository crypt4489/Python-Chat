import socket
import time
import io
import threading
import os
import sys
import select
import pickle
import telnetlib
from pyChatMessageClass import dMessage, gMessage
from  multiprocessing import Process, JoinableQueue
from io import BytesIO
from cryptography.fernet import Fernet

class Client(Process, object):

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def sendMsg(self, data):
		try:
			print("send")
			self.sock.sendall(data)
		except:
			print(str(sys.exc_info()[0]) + " SEND_MSG_CLIENT_CHAT")


	def recvMsg(self):
		try:
			while self.recv_bool:
				data = self.sock.recv(4096)
				if not data:
					break
				message = dMessage.makeMessage(data)
				self.queue1.put(message)
		except:
			print(str(sys.exc_info()[0]) + " RECV_MSG_CLIENT_CHAT")

	def endConnection(self):
		self.recv_bool = False
		print("ending recv thread")

	def tellie(self, tel_info):
		try:
			self.tel_connect = telnetlib.Telnet(tel_info[0])
			self.tel_connect.read_until("Password: ")
			self.tel_connect.write(tel_info[2] + "\n\r")
			print("Success with TELLIE")
			
			
			self.readThread = threading.Thread(target=self.read_tel)
			self.readThread.daemon = True
			self.readThread.start()
		except:
			print("Something wrong w/ tellie " + str(sys.exc_info()[0]) + "\n")

	def read_tel(self):
		while True:
			rfd, wfd, xfd = select.select([self.tel_connect], [], [])
			try:
				if self.tel_connect in rfd:
					data = self.tel_connect.read_eager()
					if data:
						self.queue1.put(dMessage(0, "", 0, 0, 0, data))
			except EOFError:
				print("Something wrong w/ tellie receive " + str(sys.exc_info()[0]) + "\n")
				break;


	def cmd_tel(self, cmd):
		self.tel_connect.write(cmd + "\n\r")
		

	def end_tellie(self):
		self.readThread.stop()
		self.tel_connect.close()

	def encrypt_pwd(self, pwd):
		key = bytes(os.environ["key"], "utf-8").decode('unicode_escape')
		f = Fernet(key)
		return f.encrypt(pwd.encode())

	def connect(self, address):
		pwd = os.getenv("pwd")
		e_pwd = self.encrypt_pwd(pwd)
		self.sock.connect((address, 9000))
		data = "{uname} {pwd} {token}".format(
			uname= os.getenv("username"), 
			pwd = e_pwd.decode('utf-8'), 				
			token = os.getenv("token"))
		self.sock.sendall(dMessage(1, None, 0, 0, 0, data).makePickle())
		data = self.sock.recv(4096)	
		print("Begin Chatting...")
		self.recv_bool = True;
		rThread = threading.Thread(target=self.recvMsg)
		rThread.daemon = True
		rThread.start()



		
	def __init__(self, address, target, queue1):
		Process.__init__(self)
		self.queue1 = queue1

		self.connect(address)


if __name__ == '__main__':
	client = Client(sys.argv[1], sys.argv[2])

