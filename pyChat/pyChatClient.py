import socket
import time
import io
import threading
import sys
import select
import pickle
import telnetlib
from pyChatMessageClass import dMessage, gMessage
from  multiprocessing import Process, JoinableQueue
from io import BytesIO


class Client(Process, object):

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def sendMsg(self, data):
		try:
			self.sock.sendall(data)
		except:
			print(str(sys.exc_info()[0]) + " SEND_MSG_CLIENT_CHAT")


	def recvMsg(self):
		try:
			while True:
				data = self.sock.recv(4096)
				if not data:
					break
				message = dMessage.makeMessage(data)
				self.queue1.put(message)
		except:
			print(str(sys.exc_info()[0]) + " RECV_MSG_CLIENT_CHAT")

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
		#ret_data = self.tel_connect.read_eager()
		#self.queue1.put(dMessage(0, "", 0, 0, 0, "lol"))
		

	def end_tellie(self):
		self.readThread.stop()
		self.tel_connect.close()
		
	def __init__(self, address, target, queue1):
		Process.__init__(self)
		self.queue1 = queue1
		self.sock.connect((address, 9000))
		self.sock.sendall(dMessage(1, "UBUNTU!", 0, 0, 0, "UBUNTU!").makePickle())
		"""print(str(self.sock.recv(1024)))
		while(str(self.sock.recv(1024)) != "Send"):
			pass
		self.sock.sendall(target.encode('utf-8')) """
		print("Begin Chatting...")
		rThread = threading.Thread(target=self.recvMsg)
		rThread.daemon = True
		rThread.start()


if __name__ == '__main__':
	client = Client(sys.argv[1], sys.argv[2])

