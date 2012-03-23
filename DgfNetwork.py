#this will change ALOT as i learn about peer to peer networking

import socket, time, string, sys, urlparse
import os
import gnupg
from threading import *
#sqlite stuff
from data_model import *
# metadata.bind = "sqlite:///dgf.sqlite"
# metadata.bind.echo = True
#end sqlite stuff
		
class Peer:
	def __init__(self):
		self.ip='localhost'
		self.cport=0#9091
		self.mport=0#9090

class DgfNetwork(Thread):
	def __init__(self,gpg,my_gpg_stuff,my_ports_ip,peers):
		self.log=open("network_debugging_log"+str(my_ports_ip.cport),"w")
		self.me=my_ports_ip
		self.log.write(str(self.me.cport))
		self.log.write(str(self.me.mport))
		self.peers=peers
		self.peers=filter(lambda p: p.cport != self.me.cport,self.peers)
		self.gpg=gpg
		Thread.__init__(self)
		#this bit is just hardcoded to get started. will be a dynamic list of peers later
		# print blah
		# exit()

				
				
		# Peer()
		# self.me.cport=9091
		# self.me.mport=9090
		# p=Peer()
		# p.cport=9081
		# p.mport=9080
		# self.peers=[p] #just one test client @localhost for now
		###self.gpg=gpg
		# self.gpg = gnupg.GPG(gnupghome='/Users/neilhudson/.gnupg') #todo - this is really bad.
		
	def run(self):
		# self.me=self.my_ports_ip
		# print self.me.ip
		# exit()
		# self.peers=peers
		# self.gpg=gpg
		self.process()

	def bindmsock(self):
		self.msock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.msock.bind(('', self.me.mport))
		self.msock.listen(1)
		print '[Media] Listening on port '+str(self.me.mport)

	def acceptmsock(self):
		self.mconn, self.maddr = self.msock.accept()
		print '[Media] Got connection from', self.maddr

	def bindcsock(self):
		self.csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.csock.bind(('', self.me.cport))
		self.csock.listen(1)
		print '[Control] Listening on port '+str(self.me.cport)

	def acceptcsock(self):
		self.cconn, self.maddr = self.csock.accept()
		print '[Control] Got connection from', self.maddr

		while 1:
			data = self.cconn.recv(1024)
			if not data: break
			if data[0:4] == "SEND": self.filename = data[5:] #todo - fix this in filename
			print '[Control] Getting ready to receive "%s"' % self.filename
			break

	def transfer(self):
		# print '[Media] Starting media transfer for "%s"' % self.filename

		# f = open(self.filename,"wb") #todo - this is not legitimately used. just writes out to a file for debugging
		all_data=""
		while 1:
			data = self.mconn.recv(1024)
			if not data: break
			all_data+=data
			# f.write(data)
		# f.close()
		messages=all_data.split("\n#*#")#todo - this is a horrible delimiter
		all_votes=Vote.query.all()#todo - optimize the following code
		all_citizens=Citizen.query.all()
		all_laws=Law.query.all()
		header="-----BEGIN PGP SIGNED MESSAGE-----\nHash: SHA1\n\n"
		#text here
		footer1="\n-----BEGIN PGP SIGNATURE-----\nVersion: GnuPG v1.4.9 (Darwin)\nComment: GPGTools - http://gpgtools.org\n\n"
		#sig here
		footer2="\n-----END PGP SIGNATURE-----\n\n\n"
		
		for m in messages:
			print m
			if len(m)>0:
				(msg_received,original_sign)=m.split(";")
				sign=header+msg_received+footer1+original_sign+footer2
				if not(self.gpg.verify(sign).valid):#todo - recover gracefully from this
					print "got an invalid signature!"
					exit()
				(citizen_fingerprint,law_name,yes_no)=m.split(";")[0].split(",")
				previous_votes=filter(lambda x: x.citizen.fingerprint==citizen_fingerprint and x.law.name==law_name,all_votes)
				v=""
				if len(previous_votes)>0:
					v=previous_votes[0]
				else:
					v=Vote()
					#todo - the following assumes we already have all laws and citizens. obviously this needs to be fixed
					# but for now just messing around. also assumes we have the public key needed to verify
					v.citizen=filter(lambda x: x.fingerprint==citizen_fingerprint,all_citizens)[0]
					v.law=filter(lambda x: x.name==law_name,all_laws)[0]

				v.yes_no=True if yes_no=="1" else False
				v.sign=original_sign
				session.commit()
		#todo - update the gui here?
				
			

		print '[Media] Got "%s"' % self.filename
		print '[Media] Closing media transfer for "%s"' % self.filename
		print all_data

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
		# FILE='dgf.sqlite'
		# f = open(FILE, "rb")
		# data = f.read()
		# f.close()
		FILE="votes_sent" #todo - not really used
		data=""
		new_votes=Vote.query.all() #should be restricted to a time range but isn't for now
		for v in new_votes:
			e='1' if v.yes_no else '0'
			data+=v.citizen.fingerprint+","+v.law.name+","+e+";"+v.sign+"\n#*#"#what a fucking delimiter...
			

		# print self.peers
		# for p in self.peers:
		# 	print p.ip
		# 	print p.cport
		# 	print p.mport
			
		for p in self.peers:
			
			print self.me.ip
			print self.me.cport
			print self.me.mport
			print p.ip
			print p.cport
			print p.mport
			

			cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			cs.connect((p.ip, p.cport))
			cs.send("SEND " + FILE)
			cs.close()

			time.sleep(2) #todo - was going too fast. probably a sign of a fundamental problem

			ms = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			ms.connect((p.ip, p.mport))

			ms.send(data)
			ms.close()	
	# def shareChangesOld(self):  #todo - this should be threaded so it doesn't lockup the gui?
	# 	FILE='dgf.sqlite'
	# 	f = open(FILE, "rb")
	# 	data = f.read()
	# 	f.close()
	# 	
	# 	for p in self.peers:	
	# 
	# 		HOST = p.ip
	# 		CPORT = p.cport
	# 		MPORT = p.mport
	# 		
	# 		cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# 		cs.connect((HOST, CPORT))
	# 		#todo - really need to be sending a checksum here
	# 		cs.send("SEND " + FILE)
	# 		cs.close()
	# 		
	# 		time.sleep(0.5) #was going too fast. probably a sign of a fundamental problem with the 2 port strategy
	# 		
	# 		ms = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# 		ms.connect((HOST, MPORT))
	# 	
	# 		ms.send(data)
	# 		ms.close()