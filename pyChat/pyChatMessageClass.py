import pickle

class messageMethods(object):

	def makePickle(self):
		with open("./servMsg.txt", "wb+") as f:
			pickle.dump(self, f, 2)
		with open("./servMsg.txt", "rb+") as f:
			db = f.read()
		f.close()
		return db


	@staticmethod
	def makeMessage(self):
		with open("./in_msg.txt", "wb") as f:
			f.write(self)
		with open("./in_msg.txt", "rb") as f:
			mess = pickle.load(f)
		f.close()
		return mess


class dMessage(messageMethods, object):

	messageType = "srv_msg"

	def __init__  (self, conn, target, end, sendMsg, alert, friends_list, data):

		self.header = {"conn": conn, "end": end, "chat": sendMsg, "alert": alert, "friends_list": friends_list}
		self.data = data
		self.target = target


class gMessage(messageMethods, object):

	messageType = "gui_msg"

	def __init__(self, quit, dataMsg, telnet, cmd, data):

		self.quit = quit
		self.dataMsg = dataMsg
		self.telnet = telnet
		self.cmd = cmd
		self.data = data


class messageFormat():

	quickMess = { "DATA_MSG" : {"conn" : False, "target": None, "end" : False, "sendMsg" : True, "alert" : False, "friends_list": False, "data" : None}, 
			"NEW_CONN" : {"conn" : True, "target" : None, "end" : False, "sendMsg" : False, "alert" : False, "friends_list": False, "data" : None}, 
			"END_CONN" : {"conn" : False, "target" : None, "end" : True, "sendMsg" : False, "alert" : False, "friends_list": False, "data" : None},
			"ALERT_ONLINE" : {"conn" : False, "target" : None, "end" : False, "sendMsg" : False, "alert" : True, "friends_list": False, "data" : None}
			"FRIENDS_LIST" : {"conn" : False, "target" : None, "end" : False, "sendMsg" : False, "alert" : False, "friends_list": True, "data" : None}  }

