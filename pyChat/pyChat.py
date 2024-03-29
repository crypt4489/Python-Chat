from multiprocessing import Process, JoinableQueue
from pyChatGTK import chatGUI
from pyChatClient import Client
from pyChatQueueManager import pyChatManager
from pyChatSettings import setup_environment
import sys



if __name__ == '__main__':
	setup_environment()
	chatq1 = JoinableQueue()
	chatq2 = JoinableQueue()
	clienth = Client(sys.argv[1], sys.argv[2], chatq1)
	manager = pyChatManager(clienth, chatq1, chatq2)
	guih = chatGUI(chatq1, chatq2)
	manager.start()
	guih.start()

