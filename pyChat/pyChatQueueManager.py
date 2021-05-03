from multiprocessing.managers import BaseManager
from pyChatMessageClass import dMessage, gMessage, messageFormat
import threading, sys
class pyChatManager(BaseManager, object):


	def __init__(self, client, queue1, queue2):
		Process.__init__(self)
		self.client = client
		self.messQueue = queue1
		self.GUIdataqueue = queue2
		self.manage = True
		manThread = threading.Thread(target=self.manager)
		manThread.daemon = True
		manThread.start()
		self.client.start()


	def manager(self):
		while self.manage:
			while(self.messQueue.empty()):
				pass
			dataM = self.messQueue.get()
			if (dataM.messageType == "gui_msg"):
				if (dataM.dataMsg == True):
					args = messageFormat.quickMess["DATA_MSG"]
					args["data"] = dataM.data["data"]
					args["target"] = dataM.data["target"]
					self.client.sendMsg(dMessage(**args).makePickle())
				elif (dataM.quit == True):
					args = messageFormat.quickMess["END_CONN"]
					self.client.sendMsg(dMessage(**args).makePickle())
					self.client.endConnection()
					self.manage = False
				elif (dataM.telnet == True):
					self.client.tellie(dataM.data)
				elif (dataM.cmd == True):
					self.client.cmd_tel(dataM.data)
			else:
				self.GUIdataqueue.put(dataM)


