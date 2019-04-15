


import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf
from multiprocessing import Process, JoinableQueue
from pyChatMessageClass import gMessage
import threading, sys


class chatGUI(Gtk.Window, Process, object):




	def update_friends_list(self):
		green_image = GdkPixbuf.Pixbuf.new_from_file_at_size(self.active_user["link"], self.active_user["width"], self.active_user["height"])
		red_image = GdkPixbuf.Pixbuf.new_from_file_at_size(self.inactive_user["link"], self.inactive_user["width"], self.inactive_user["height"])
		self.friends_list.clear()
		self.friends_list.append(list(("Drew", green_image)))
		self.friends_list.append(list(("Name1", red_image)))
		
		self.treeview.set_model(self.friends_list)


	def sendMsg(self, widget):
		try:
			first_in = self.input_buf.get_start_iter()
			last_in = self.input_buf.get_end_iter()
			first_chat = self.chat_buf.get_end_iter()
			data = str(self.input_buf.get_text(first_in, last_in, False).split("\n")[0])
			if not data:
				return
			self.queue1.put(gMessage(False, True, False, False, data))
			self.chat_buf.insert(first_chat, "You: " +data+"\n", length=-1)
			self.input_buf.delete(first_in, last_in)
			self.input_buf.place_cursor(first_in)
			return 'break'
		except:
			print("ERROR: sendMsg from GUI")


	def recvMsg(self):
		while True:
			try:
				while(self.queue2.empty()):
					pass
				if (self.notebook.get_current_page() == 0):
					res = self.queue2.get()
					if (res.header["alert"] == True):
						self.update_friends_list()
					else:
						first_chat = self.chat_buf.get_end_iter()
						self.chat_buf.insert(first_chat, "Server: " + res.data + "\n")
				else:
					oneEnd = self.interact_buf.get_end_iter()
					data = self.queue2.get().data
					self.interact_buf.insert(oneEnd, data)
					
				self.queue2.task_done()
				
			except:
				print("ERROR: something went wrong with gui.recv" + str(sys.exc_info()[0]) + str(sys.exc_info()[1]) )

	
	def setup_tel(self, widget):
		data = (self.ip_buf.get_text(), self.usr_buf.get_text(), self.pwd_buf.get_text())
		self.pwd_buf.delete_text(0, -1)
		self.queue1.put(gMessage(False, False, True, False, data))

	def send_cmd(self, widget):
		
		first_in_iter = self.interact_buf.get_start_iter()
		last_in = self.interact_buf.get_end_iter()
		data = str(self.interact_buf.get_text(first_in_iter, last_in, False).split("\n")[0])
	
		self.queue1.put(gMessage(False, False, False, True, data))


	def quit(self, widget):
		self.queue1.put(gMessage(True, False, False, False, ""))
		self.destroy()
		Gtk.main_quit()

	def clear(self, widget):
		first_in = self.interact_buf.get_start_iter()
		last_in = self.interact_buf.get_end_iter()
		self.interact_buf.delete(first_in, last_in)
		self.interact_buf.place_cursor(first_in)		


	def setup_chat_page(self):
		self.main_chat = Gtk.Grid(column_homogeneous = True, column_spacing = 5, 						row_spacing = 5)
		self.set_border_width(10)

		#create chat buffer/frame
		self.chat_text = Gtk.TextView()
		self.chat_text.set_editable(False)
		self.chat_text.set_cursor_visible(False)
		self.chat_buf = self.chat_text.get_buffer()
		#create input buffer/frame
		self.input_text = Gtk.TextView()
		self.input_buf = self.input_text.get_buffer()

		#make chat a scrolled window
		scrolledwindow = Gtk.ScrolledWindow()
		scrolledwindow.set_hexpand(True)
		scrolledwindow.set_vexpand(True)
		scrolledwindow.add(self.chat_text)



		self.main_chat.attach(scrolledwindow, 0, 1, 3, 1)

		#make input a scrolled window
		scrolledwindow = Gtk.ScrolledWindow()
		scrolledwindow.set_hexpand(True)
		scrolledwindow.set_vexpand(True)
		scrolledwindow.add(self.input_text)

		
		self.main_chat.attach(scrolledwindow, 0, 2, 2, 1)

		#create send button
		self.button = Gtk.Button(label="Send Message")
		self.button.connect("clicked", self.sendMsg)
		self.main_chat.attach(self.button, 2, 2, 2, 2)
			
		#create friends list listview
		self.image = GdkPixbuf.Pixbuf.new_from_file_at_size(self.inactive_user["link"], self.inactive_user["width"], self.inactive_user["height"])
		self.friends_list = Gtk.ListStore(str, GdkPixbuf.Pixbuf)
		self.friends_list.append(list(("Drew", self.image)))
		self.friends_list.append(list(("Sean", self.image)))
		self.language_filter = self.friends_list.filter_new()
		self.treeview = Gtk.TreeView.new_with_model(self.language_filter)
		
		#create column headings/types
		renderer = Gtk.CellRendererText()
		column = Gtk.TreeViewColumn("Contact", renderer, text=0)
		column.set_expand(True)
		self.treeview.append_column(column)
		renderer_pix = Gtk.CellRendererPixbuf()
		column = Gtk.TreeViewColumn("Status", renderer_pix, pixbuf=1)
		column.set_expand(True)
		self.treeview.append_column(column)

		#make the friends list scrollable
		scrolledwindow = Gtk.ScrolledWindow()
		scrolledwindow.set_hexpand(True)
		scrolledwindow.set_vexpand(True)
		scrolledwindow.add(self.treeview)
		self.main_chat.attach(scrolledwindow, 3, 1, 1, 1)

	def setup_telnet_page(self):
		self.page2 = Gtk.Grid(column_homogeneous = True, column_spacing = 5, 						row_spacing = 5)
		self.page2.attach(Gtk.Label("IP Address"), 0, 0, 1, 1)
		self.page2.attach(Gtk.Label("Username"), 0, 1, 1, 1)
		self.page2.attach(Gtk.Label("Password"), 0, 2, 1, 1)
		self.ip_addr = Gtk.Entry()
		self.ip_buf = self.ip_addr.get_buffer()
		self.page2.attach(self.ip_addr, 1, 0, 1, 1)
		self.usr = Gtk.Entry()
		self.usr_buf = self.usr.get_buffer()
		self.page2.attach(self.usr, 1, 1, 1, 1)
		self.pwd = Gtk.Entry()
		self.pwd.set_visibility(False)
		self.pwd_buf = self.pwd.get_buffer()
		self.page2.attach(self.pwd, 1, 2, 1, 1)
		self.tel_button = Gtk.Button(label="Connect")
		self.tel_button.connect("clicked", self.setup_tel)
		self.page2.attach(self.tel_button, 1, 3, 1, 1)
		self.interact_view = Gtk.TextView()
		self.interact_buf = self.interact_view.get_buffer()
		scrolledwindow = Gtk.ScrolledWindow()
		scrolledwindow.set_hexpand(True)
		scrolledwindow.set_vexpand(True)
		scrolledwindow.add(self.interact_view)
		self.page2.attach(scrolledwindow, 0, 4, 4, 1)
		self.tel_button2 = Gtk.Button(label="Send Command")
		self.tel_button2.connect("clicked", self.send_cmd) 
		self.tel_button3 = Gtk.Button(label="Clear")
		self.tel_button3.connect("clicked", self.clear) 
		self.page2.attach(self.tel_button2, 4, 3, 1, 1)
		self.page2.attach(self.tel_button3, 4, 4, 1, 1)
		



	def __init__ (self, queue1, queue2):
		Process.__init__(self)
		self.queue1 = queue1
		self.queue2 = queue2
		self.active_user = {"link": "/home/crypt4489/Documents/pyChatFiles/icons/Green.ico", "width": 16, "height": 16}


		self.inactive_user = {"link": "/home/crypt4489/Documents/pyChatFiles/icons/red-dot.ico", "width": 24, "height": 24}
		Gtk.Window.__init__(self, title="Drew Chat")
		self.set_size_request(800, 600)
		self.timeout_id = None
		self.set_border_width(10)
		self.notebook = Gtk.Notebook()
		self.add(self.notebook)
		self.setup_chat_page()
		self.setup_telnet_page()
		self.notebook.append_page(self.main_chat, Gtk.Label("Chat"))
		
		self.notebook.append_page(self.page2, Gtk.Label("Telnet"))

		
		self.show_all()
		self.connect("destroy", self.quit)
		rThread = threading.Thread(target=self.recvMsg)
		rThread.daemon = True
		rThread.start()
		Gtk.main()


if __name__ == '__main__':
	chatGUI()

