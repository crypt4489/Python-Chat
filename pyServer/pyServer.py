import SocketServer
import threading
import pickle
import sys
from pyChatMessageClass import dMessage

class myTCPHandler(SocketServer.BaseRequestHandler):

	def handle(self):
			message = dMessage.makeMessage(self.request.recv(4096))
			sock = self.request
			addr = self.client_address
			server_manager = ServerManager()
			server_manager.process_init(sock, addr, message)


class ServerManager:

	active_users = {}
	known_ips = {"UBUNTU!": "192.168.1.3"}
	known_conns = {}
	message_map = {}

	def __init__(self):
		self.message_map = {
		'end' : self.handle_end,
		'chat' : self.send_data,
		}
		return

	def process_init(self, sock, addr, message):
		if (message.header["conn"] == 1):
			
			usr_Name = str(message.data).split(" ")[0]
			self.known_conns[usr_Name] = sock
			self.known_ips[usr_Name] = addr[0]
			self.active_users[addr[0]] = True
			if (usr_Name != "SERVER"):
				print("Client")
				self.manageClient(addr, sock)
			else:
				self.manageClient(addr, sock)


	def handleServ(self, addr, sock):

		while True:
			data = sock.recv(4096)
			if not data:
				break
			for i, v in self.known_ips.iteritems():
				if (v != addr[0]):
					self.known_conns[i].send(dMessage(False, False, data).makePickle())
				else:
					self.known_conns[i].sendall(str(data))


	def manageClient(self, addr, sock):

			try:
				while self.active_users[addr[0]] == True:
					data = sock.recv(4096)
					if not data:
						break
					message = dMessage.makeMessage(data)
					print(message.data)
					print(message)
					for i, v in message.header.iteritems():
						if i == "chat":
							self.message_map[i](message, addr)
			except:
				print("Error:", sys.exc_info()[0], sys.exc_info()[1])
				print("Lost Connection w/ {}".format(addr[0]))
				del self.active_users[addr[0]]
			finally:
				print("Error:", sys.exc_info()[0], sys.exc_info()[1])
				print("End Connection w/ {}".format(addr[0]))
				if addr[0] in self.active_users:
					del self.active_users[addr[0]]
				return


	def send_data(self, message, addr):
		self.known_conns[message.target].sendall(message.makePickle())


	def handle_end(self, message, addr):
		self.active_users[addr[0]] = False
		print "{}".format(active_users)

class Server(SocketServer.ThreadingMixIn, SocketServer.TCPServer):

	Host, Port = "192.168.1.2", 9000
	def __init__(self):
		print "Server has started on {}".format((self.Host, self.Port))
		server = SocketServer.TCPServer.__init__(self, (self.Host, self.Port), myTCPHandler)
		return

	def get_request(self):
		return SocketServer.TCPServer.get_request(self)


	def server_bind(self):
		return SocketServer.TCPServer.server_bind(self)

	def server_activate(self):
		return SocketServer.TCPServer.server_activate(self)


if __name__ == "__main__":
	server = Server()
	print(server.server_address)
	s_thread = threading.Thread(target=server.serve_forever)
	s_thread.setDaemon(True)
	s_thread.start()
	while True:
		pass


