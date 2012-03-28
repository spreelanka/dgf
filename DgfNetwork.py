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
	def __init__(self,raw_peer=""):
		if len(raw_peer)>0:
			if raw_peer[0:5]=='FROM ':
				raw_peer=raw_peer[5:]				
			self.ip,self.cport,self.mport=raw_peer.split(',')
			self.cport=int(self.cport)
			self.mport=int(self.mport)
		else:
			self.ip='localhost'
			self.cport=0#9091
			self.mport=0#9090

class DgfNetwork(Thread):
	def __init__(self,gpg,my_gpg_stuff,my_ports_ip,peers):
		self.mconn=None
		self.msock=None
		self.cconn=None
		self.csock=None
		
		self.me=my_ports_ip
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
			raw_peer,msg=data.split(";")
			peer=Peer(raw_peer)
			print msg
			if msg[0:10] == "SEND_VOTES":
				print '[Control] Getting ready to receive votes'
				self.bindmsock()
				self.acceptmsock()
				self.transfer(peer)
				break
			elif msg[0:16]=="REQUEST_CITIZEN ":
				requested_citizen_fingerprint=msg[16:]
				print '[Control] sending citizen '+requested_citizen_fingerprint
				self.sendCitizen(peer,requested_citizen_fingerprint)
				break
			elif msg[0:12]=="REQUEST_LAW ":
				requested_law_uuid=msg[12:]
				print '[Control] sending law '+requested_law_uuid
				self.sendLaw(peer,requested_law_uuid)
				break
			elif msg[0:12]=="SEND_CITIZEN":
				print '[Control] getting ready to receive requested citizen'
				self.bindmsock()
				self.acceptmsock()
				self.receiveCitizen()
				break
			elif msg[0:9]=="SEND_LAW ":
				print '[Control] getting ready to receive requested law'
				self.bindmsock()
				self.acceptmsock()
				self.receiveLaw()
				break
			else:
				print '[Control] got some other weird message...wtf is this? '+msg
				
	def sendCitizen(self,peer,fingerprint):  
		# print " send citizen"
		data=""
		p=peer

		citizens=Citizen.query.filter_by(fingerprint=fingerprint).all()
		if len(citizens)==0:
			print "puke! we don't have the citizen that's been requested!"
			exit()
		cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		cs.connect((p.ip, p.cport))
		cs.send("FROM "+str(self.me.ip)+","+str(self.me.cport)+","+str(self.me.mport)+";"+"SEND_CITIZEN ")
		cs.close()

		time.sleep(2) #todo - was going too fast. probably a sign of a fundamental problem

		ms = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ms.connect((p.ip, p.mport))

		ms.send(fingerprint+","+citizens[0].name+","+citizens[0].public_key)
		# self.gpg.export_keys(fingerprint)))
		ms.close()
	def sendLaw(self,peer,uuid):  
		data=""
		p=peer

		laws=Law.query.filter_by(uuid=uuid).all()
		if len(laws)==0:
			print "puke! we don't have the law that's been requested!"
			exit()
		time.sleep(2)
		cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		cs.connect((p.ip, p.cport))
		cs.send("FROM "+str(self.me.ip)+","+str(self.me.cport)+","+str(self.me.mport)+";"+"SEND_LAW ")
		cs.close()

		time.sleep(1) #todo - was going too fast. probably a sign of a fundamental problem

		ms = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ms.connect((p.ip, p.mport))
				#todo - really need to handle this better instead of making up bullshit delimiters
		ms.send(uuid+"<<>>"+laws[0].name+"<<>>"+laws[0].description) 
		ms.close()
				
	#todo - Q: shouldn't these receiveXXX functions make sure we aren't adding duplicates? A: yes.		
	def receiveCitizen(self):
		all_data=""
		print "[Media] receive citizen"
		while 1:
			data = self.mconn.recv(1024)
			if not data: break
			all_data+=data
		c=Citizen()
		c.fingerprint,c.name,c.public_key=all_data.split(",")
		session.commit()
		import_result=self.gpg.import_keys(c.public_key) #imports into gpg directory
		print "successfully imported " +str(import_result.count)+ " citizens"
		
		self.verifyVotes()
		
	def receiveLaw(self): #todo - so verify votes but not law text? seems pretty exploitable
		all_data=""
		print "[Media] receive law "
		while 1:
			data = self.mconn.recv(1024)
			if not data: break
			all_data+=data
		l=Law()
		l.uuid,l.name,l.description=all_data.split("<<>>")
		session.commit()
		
		#make sure all these votes know their owner
		unlawed_votes=Vote.query.filter_by(law_uuid=l.uuid).all()
		for v in unlawed_votes:
			v.law=l
		session.commit()
	
	
	def verifyVotes(self):
		unverified_votes=Vote.query.filter_by(verified=False).all()
		for v in unverified_votes:
			e='1' if v.yes_no else '0'
			reconstructed_msg=v.fingerprint+','+v.law.uuid+','+e
			original_sign=self.addHeadersToSign(reconstructed_msg,v.sign)
			if self.gpg.verify(original_sign).valid:#todo - recover gracefully from this
				v.verified=True
				#this is not technically vote verifying but we're doing it here anyway! rawr!
				matching_citizens = Citizen.query.filter_by(fingerprint=v.fingerprint).all()
				if len(matching_citizens)>0:
					v.citizen=matching_citizens[0]
				else:
					print "this should not happen"
					exit()
				session.commit()
				
			else:
				print "this vote could not be verified"
				

	def addHeadersToSign(self,msg_received,original_sign): #i really don't like this part
		header="-----BEGIN PGP SIGNED MESSAGE-----\nHash: SHA1\n\n"
		#text here
		footer1="\n-----BEGIN PGP SIGNATURE-----\nVersion: GnuPG v1.4.9 (Darwin)\nComment: GPGTools - http://gpgtools.org\n\n"
		#sig here
		footer2="\n-----END PGP SIGNATURE-----\n\n\n"
		sign=header+msg_received+footer1+original_sign+footer2
		return sign
		
	def transfer(self,peer):
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
		
		for m in messages:
			print m
			if len(m)>0:
				(msg_received,original_sign)=m.split(";")
				(citizen_fingerprint,law_uuid,yes_no)=m.split(";")[0].split(",")
				
				sign=self.addHeadersToSign(msg_received,original_sign)
				was_vote_verified=False
				if not(self.gpg.verify(sign).valid):#todo - recover gracefully from this
					

					fingerprint_search_results=filter(lambda k: k['fingerprint']==citizen_fingerprint,self.gpg.list_keys())
					if len(fingerprint_search_results)>0:
						print "invalid signature for a known citizen! or fingerprint collision? or bad message?"
						print sign
						exit()
					else:
						print "got an invalid signature! requesting citizen data pubkey"
						self.requestCitizenPubkey(peer,citizen_fingerprint)
						was_vote_verified=False #for clarity only. a bit redundant
				
					# print msg_received
					# return()
				else:
					was_vote_verified=True
				
				previous_votes=filter(lambda x: x.fingerprint==citizen_fingerprint and x.law_uuid==law_uuid,all_votes)
				v=""
				if len(previous_votes)>0:
					v=previous_votes[0]
				else:
					v=Vote()
					#todo - the following assumes we already have all laws and citizens. obviously this needs to be fixed
					# but for now just messing around. also assumes we have the public key needed to verify
					citizen_objects=filter(lambda x: x.fingerprint==citizen_fingerprint,all_citizens)
					if len(citizen_objects)==1:
						v.citizen=citizen_objects[0]
					elif len(citizen_objects)>1:
						print "fingerprint collision or duplicate citizens. this should never happen."
						exit()
					matching_laws=Law.query.filter_by(uuid=law_uuid).all()
					if len(matching_laws)>1:
						print "law uuid collision?! this should never happen"
						exit()
					elif len(matching_laws)==1: #found one law matching the vote, record it as such
						v.law=matching_laws[0]
					else:
						self.requestLaw(peer,law_uuid)
						#no law found, request it
						

				v.yes_no=True if yes_no=="1" else False
				v.sign=original_sign
				v.fingerprint=citizen_fingerprint
				v.verified=was_vote_verified
				session.commit()
		#todo - update the gui here?
				
			

		print '[Media] Got all votes'
		print '[Media] Closing media transfer'
		# print all_data

	def close(self):
		self.cconn.close()
		self.csock.close()
		try:
			self.mconn
			self.msock
		except NameError:
			self.mconn=None
			self.msock=None
		if not( self.mconn is None):
			self.mconn.close()
		if not( self.msock is None):
			self.msock.close()

	def process(self):
		while 1:
			self.bindcsock()
			self.acceptcsock()
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
			data+=v.fingerprint+","+v.law_uuid+","+e+";"+v.sign+"\n#*#"#what a fucking delimiter...
			

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
			cs.send("FROM "+str(self.me.ip)+","+str(self.me.cport)+","+str(self.me.mport)+";"+"SEND_VOTES")
			cs.close()

			time.sleep(2) #todo - was going too fast. probably a sign of a fundamental problem

			ms = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			ms.connect((p.ip, p.mport))

			ms.send(data)
			ms.close()	

	def requestCitizenPubkey(self,peer,fingerprint):
		print 'requesting pubkey from '+peer.ip+':'+str(peer.cport)
		cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		cs.connect((peer.ip, peer.cport))
		cs.send("FROM "+str(self.me.ip)+","+str(self.me.cport)+","+str(self.me.mport)+";"+"REQUEST_CITIZEN " + fingerprint)
		cs.close()
		
	def requestLaw(self,peer,uuid):
		time.sleep(2) #oh god, it hurts
		print 'requesting law uuid from '+peer.ip+':'+str(peer.cport)
		cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		cs.connect((peer.ip, peer.cport))
		cs.send("FROM "+str(self.me.ip)+","+str(self.me.cport)+","+str(self.me.mport)+";"+"REQUEST_LAW " + uuid)
		cs.close()
