import pickle

class messageMethods(object):

	def makePickle(self):
		with open("/root/pyServer/servMsg.txt", "wb") as f:
			pickle.dump(self, f, 2)
		with open("/root/pyServer/servMsg.txt", "rb") as f:
			db = f.read()
		f.close()
		return db


	@staticmethod
	def makeMessage(self):
		with open("/root/pyServer/in_msg.txt", "wb") as f:
			f.write(self)
		with open("/root/pyServer/in_msg.txt", "rb") as f:
			mess = pickle.load(f)
		f.close()
		return mess


class dMessage(messageMethods, object):

	messageType = "srv_msg"

	def __init__  (self, conn, target, end, sendMsg, data):

		self.header = {"conn": conn, "end": end, "chat": sendMsg}
		self.data = data
		self.target = target


class gMessage(messageMethods, object):

	messageType = "gui_msg"

	def __init__(self, quit, dataMsg, data):

		self.quit = quit
		self.dataMsg = dataMsg
		self.data = data

