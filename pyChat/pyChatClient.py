import socket
import time
import io
import threading
import sys
import pickle
import telnetlib
from pyChatMessageClass import dMessage
from  multiprocessing import Process, JoinableQueue


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
				data = self.sock.recv(1024)
				self.queue1.put(dMessage.makeMessage(data))
		except:
			print(str(sys.exc_info()[0]) + " RECV_MSG_CLIENT_CHAT")

	def tellie(self, tel_info):
		try:
			self.tel_connect = telnetlib.Telnet(tel_info[0])
			self.tel_connect.read_until("Password: ")
			self.tel_connect.write(tel_info[2] + "\n\r")
			#self.tel_connect.close()
			print("Success with TELLIE")
			self.tel_connect.interact()
		except:
			print("Something wrong w/ tellie " + str(sys.exc_info()[0]) + "\n")

	def cmd_tel(self, cmd):
		self.tel_connect.write(cmd + "\n\r")
		self.tel_connect.write("exit\n\r")
		ret_data = self.tel_connect.read_all()
		print(ret_data)
		self.queue1.put(dMessage(0, "", 0, 0, ret_data))

	def end_tellie(self):
		self.tel_connect.close()
		

	def __init__(self, address, target, queue1):
		Process.__init__(self)
		self.queue1 = queue1
		self.sock.connect((address, 9000))
		self.sock.sendall(dMessage(1, "UBUNTU!", 0, 0, "UBUNTU!").makePickle())
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

