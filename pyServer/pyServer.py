import SocketServer
import threading
import pickle
import sys
from pyChatMessageClass import dMessage, messageFormat
from pyServerSQL import check_if_db_exists, create_user, resolve_name_to_addr, validate_pwd, validate_token, get_all_names


class ServerManager:

	active_users = {}
	known_conns = {}
	message_map = {}

	def __init__(self):
		self.message_map = {
		'end' : self.handle_end,
		'chat' : self.send_data,
		'alert' : self.alert_active_users,
		'names' : self.send_names_list,
		}
		return

	def process_init(self, sock, addr, message):
		try:
			if (message.header["conn"] == 1):	
				usr_Name = str(message.data).split(" ")[0]
				pwd = str(message.data).split(" ")[1]
				token = str(message.data).split(" ")[2]
				valid_token = validate_token(token)
				if (valid_token == False):
					raise Exception("invalid token")
					self.send_end_conn(sock, "invalid token")
					return
				res = create_user(addr[0], usr_Name, pwd)
				if (res == "SQL_UPDATE"):
					res = validate_pwd(usr_name, pwd)
					if (res == False):
						raise Exception("invalid pwd")
						self.send_end_conn(sock, "invalid pwd")
						return
				hash_addr = hash(addr[0])
				self.known_conns[hash_addr] = sock
				self.active_users[hash_addr] = True			
			  	alert_thread=threading.Thread(
					target=self.message_map["alert"], args=
					(usr_Name, addr[0],))
				alert_thread.start()
				names_thread=threading.Thread(
					target=self.message_map["names"], args=
					(sock,))
				names_thread.start()
				self.manageClient(addr, sock)
		except Exception as instance:
			print(instance)

	def alert_active_users(self, usrName, addr):
		args = messageFormat.quickMess["ALERT_ONLINE"]
		args["data"] = usrName
		message = dMessage(**args).makePickle()
		for hash_ip, socket in self.known_conns.iteritems():
			if (hash(addr) != hash_ip):
				self.socket.sendall(message)
	
	def send_end_conn(self, sock, text):
		args = messageFormat.quickMess["END_CONN"]
		args["data"] = text
		message = dMessage(**args).makePickle()
		sock.sendall(message)
		sock.close()

	def send_names_list(self, sock):
		args = messageFormat.quickMess["FRIENDS_LIST"]
		args["data"] = get_all_names()
		message = dMessage(**args).makePickle()
		sock.sendall(message)
		sock.close()

	def manageClient(self, addr, sock):

			try:
				while self.active_users[addr[0]] == True:
					data = sock.recv(4096)
					message = dMessage.makeMessage(data)
					for i, v in message.header.iteritems():
						if i == "chat":
							self.message_map["chat"](message, addr)
			except:
				print("Error:", sys.exc_info()[0], sys.exc_info()[1])
				print("Lost Connection w/ {}".format(addr[0]))
				del self.active_users[addr[0]]
			finally:
				print("End Connection w/ {}".format(addr[0]))
				if hash(addr[0]) in self.active_users.keys():
					self.message_map["end"](addr[0])
				return


	def send_data(self, message, addr):
		addr = resolve_name_to_addr(message.target)
		if (addr == ""):
			return
		self.known_conns[hash(addr)].sendall(message.makePickle())


	def handle_end(self, addr):
		self.active_users.pop(hash(addr[0]))
		print "{}".format(active_users)


class myTCPHandler(SocketServer.BaseRequestHandler):

	def handle(self):
			message = dMessage.makeMessage(self.request.recv(4096))
			sock = self.request
			addr = self.client_address
			self.server_manager = ServerManager()
			self.server_manager.process_init(sock, addr, message)

class Server(SocketServer.ThreadingMixIn, SocketServer.TCPServer):

	Host, Port = "192.168.1.4", 9000
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
	check_if_db_exists()
	s_thread = threading.Thread(target=server.serve_forever)
	s_thread.setDaemon(True)
	s_thread.start()
	while True:
		pass


