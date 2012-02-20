#this will change ALOT as i learn about peer to peer networking

import socket, time, string, sys, urlparse
from threading import *
		
class Peer:
	def __init__(self):
		self.ip='localhost'
		self.cport=9091
		self.mport=9090

class DgfNetwork(Thread):
	def __init__(self):
		Thread.__init__(self)
		p=Peer()
		self.peers=[p] #just myself for now
		
	def run(self):
		self.process()

	def bindmsock(self):
		self.msock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.msock.bind(('', 9090))
		self.msock.listen(1)
		print '[Media] Listening on port 9090'

	def acceptmsock(self):
		self.mconn, self.maddr = self.msock.accept()
		print '[Media] Got connection from', self.maddr

	def bindcsock(self):
		self.csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.csock.bind(('', 9091))
		self.csock.listen(1)
		print '[Control] Listening on port 9091'

	def acceptcsock(self):
		self.cconn, self.maddr = self.csock.accept()
		print '[Control] Got connection from', self.maddr

		while 1:
			data = self.cconn.recv(1024)
			if not data: break
			if data[0:4] == "SEND": self.filename="new_dgf.sqlite"#self.filename = data[5:] #todo - fix this in filename
			print '[Control] Getting ready to receive "%s"' % self.filename
			break

	def transfer(self):
		print '[Media] Starting media transfer for "%s"' % self.filename

		f = open(self.filename,"wb")
		while 1:
			data = self.mconn.recv(1024)
			if not data: break
			f.write(data)
		f.close()

		print '[Media] Got "%s"' % self.filename
		print '[Media] Closing media transfer for "%s"' % self.filename

	def close(self):
		self.cconn.close()
		self.csock.close()
		self.mconn.close()
		self.msock.close()

	def process(self):
		while 1:
			self.bindcsock()
			self.acceptcsock()
			self.bindmsock()
			self.acceptmsock()
			self.transfer()
			self.close()

	
	def shareChanges(self):  #todo - this should be threaded so it doesn't lockup the gui?
		FILE='dgf.sqlite'
		f = open(FILE, "rb")
		data = f.read()
		f.close()
		
		for p in self.peers:	

			HOST = p.ip
			CPORT = p.cport
			MPORT = p.mport
			
			cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			cs.connect((HOST, CPORT))
			#todo - really need to be sending a checksum here
			cs.send("SEND " + FILE)
			cs.close()
			
			time.sleep(0.5) #was going too fast. probably a sign of a fundamental problem with the 2 port strategy
			
			ms = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			ms.connect((HOST, MPORT))
		
			ms.send(data)
			ms.close()