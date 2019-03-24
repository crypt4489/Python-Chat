from multiprocessing.managers import BaseManager
from pyChatMessageClass import dMessage, gMessage, messageFormat
import threading
class pyChatManager(BaseManager, object):


	def __init__(self, client, queue1, queue2):
		self.client = client
		self.messQueue = queue1
		self.GUIdataqueue = queue2
		manThread = threading.Thread(target=self.manager)
		manThread.daemon = True
		manThread.start()


	def manager(self):
		while True:
			while(self.messQueue.empty()):
				pass
			dataM = self.messQueue.get()
			if (type(dataM) == str):
				self.GUIdataqueue.put(dataM)
				pass
			if (dataM.messageType == "gui_msg"):
				if (dataM.dataMsg == True):
					args = messageFormat.quickMess["DATA_MSG"]
					args["data"] = dataM.data
					args["target"] = "UBUNTU!"
					self.client.sendMsg(dMessage(**args).makePickle())
				elif (dataM.quit == True):
					args = messageFormat.quickMess["END_CONN"]
					self.client.sendMsg(dMessage(**args).makePickle())
					self.client.end_tellie()
				elif (dataM.telnet == True):
					self.client.tellie(dataM.data)
				elif (dataM.cmd == True):
					self.client.cmd_tel(dataM.data)
			else:
				self.GUIdataqueue.put(dataM.data)


