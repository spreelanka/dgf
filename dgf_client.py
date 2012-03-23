#!/usr/bin/python


import Tkinter
import tkMessageBox
#sqlite stuff
from data_model import *


import os
import gnupg
import re
import time
import DgfNetwork
import sys
import getopt


class simpleapp_tk(Tkinter.Frame):#Tkinter.Tk):
	def __init__(self,parent,my_ip_info):
		# Tkinter.Tk.__init__(self,parent)
		Tkinter.Frame.__init__(self,parent)
		self.parent = parent
		
		#####menus and stuff
		self.parent.title("DGF")
		self.configure(height=600,width=200)
		
		#Create the Menu base
		self.menu = Tkinter.Menu(self)
		self.parent.config(menu=self.menu)
		
		self.config_menu = Tkinter.Menu(self.menu)
		self.menu.add_cascade(label="configure", menu=self.config_menu)
		self.config_menu.add_command(label="set gpg keystore path", command=self.set_gpg_keystore_path_clicked)
		# self.tkMenu.add_separator()
		
		self.initialize()

	def set_gpg_keystore_path_clicked(self):
		self.gpg_keystore_window=Tkinter.Toplevel()
		self.gpg_keystore_window.title('configuration')
		self.gpg_keystore_window.geometry("400x100+100+130")
		self.gpg_keystore_window.lift(aboveThis=self)
		
		Tkinter.Label(self.gpg_keystore_window,text="gpg keystore path",anchor="w").pack()
		self.gpg_keystore_path_entry_variable=Tkinter.StringVar()
		gpg_keystore_entry=Tkinter.Entry(self.gpg_keystore_window,textvariable=self.gpg_keystore_path_entry_variable)
		
		gpg_keystore_entry.bind("<Return>",self.on_gpg_keystore_press_enter) #this may be a really bad strategy
		gpg_keystore_entry.pack()

	def on_gpg_keystore_press_enter(self,event):		
		c=Configuration.query.filter_by(variable='gpg_keystore_path').all()
		if len(c)==0:
			c[0]=Configuration()
			c[0].variable='gpg_keystore_path'

		c[0].value=self.gpg_keystore_path_entry_variable.get()
		session.commit()
		self.gpg=gnupg.GPG(gnupghome=c[0].value)
		self.gpg_keystore_window.destroy()

	def initialize(self):
		
		#pgp stuff
		#todo - move this somewhere else/set up better
		gnupghome=Configuration.query.filter_by(variable='gpg_keystore_path').all()
		if len(gnupghome)==0:
			gnupghome[0]=Configuration()
			gnupghome[0].variable='gpg_keystore_path'
			#????what do we even do here without a gpg keystore path
			
		self.gpg = gnupg.GPG(gnupghome=gnupghome[0].value)

		# input_data = self.gpg.gen_key_input(
		#     name_email='john_doe@example.com',
		#     passphrase='pass')
		# key = self.gpg.gen_key(input_data)
		# print key.fingerprint
		# c=Citizen()
		# c.name='john doe'
		# c.fingerprint=key.fingerprint
		# c.public_key=self.gpg.export_keys(key.fingerprint)
		# session.commit()
		# exit()
		
		self.my_gpg_stuff={'keyid':'blah','passphrase':'nothing'} #just a placeholder for the structure

		private_key_list=self.gpg.list_keys(True) #private keys only
 		# if len(private_key_list)==0:
 		# 			tkMessageBox.showinfo("info","you must provide a valid gnupg keystore path!")
 		# 			self.set_gpg_keystore_path_clicked()
 		# 			private_key_list=self.gpg.list_keys(True) #private keys only

		#this probably shouldn't be here
		
		#ask the user to give their private key passcode
		self.login_window=Tkinter.Toplevel()
		self.login_window.title('who are you?')
		self.login_window.geometry("500x100+100+130")
		self.login_window.lift(aboveThis=self)
		
		
		private_key_names=map(lambda x: x['uids'][0] ,private_key_list)

		self.private_key_names_variable = Tkinter.StringVar()
		#does a default user already exist? if so, auto select this user
		default_users=Configuration.query.filter_by(variable='default_user').all()
		if len(default_users)>0:
			print "we have a default user!"
			self.private_key_names_variable.set(default_users[0].value) # known last user, let's start with him
		else:
			self.private_key_names_variable.set(private_key_names[0]) # unknown, just use the first
			
		arglist=[self.login_window, self.private_key_names_variable]+private_key_names
		w = Tkinter.OptionMenu(*arglist)
		w.pack()

		Tkinter.Label(self.login_window,text="passcode",anchor="w").pack()
		self.passcode_entry_variable=Tkinter.StringVar()
		passcode_entry=Tkinter.Entry(self.login_window,textvariable=self.passcode_entry_variable,show="*")
		# self.login_window=login_window
		# passcode_entry.bind("<Return>",lambda x:login_window.destroy()) #this may be a really bad strategy
		passcode_entry.bind("<Return>",self.OnPasscodePressEnter) #this may be a really bad strategy
		passcode_entry.pack()
		# 		self.my_gpg_stuff={'keyid':self.gpg.list_keys()[2]['fingerprint'],'passphrase':'oreo'}
		# # l=filter(lambda x: x['uids'][0]=="john doe <test_case@example.com>",gpg.list_keys(True))
		# # print l[0]['fingerprint']

		
		# self.who_am_i=Citizen.query.first()

		peers=[DgfNetwork.Peer(),DgfNetwork.Peer()] #todo - legitimately populate this
		peers[0].cport=9081
		peers[0].mport=9080
		peers[0].ip='localhost'
		peers[1].cport=9091
		peers[1].mport=9090
		peers[1].ip='localhost'
		
		self.dnetwork=DgfNetwork.DgfNetwork(self.gpg,self.my_gpg_stuff,my_ip_info,peers) #my_ip_info is passed in as argument
		self.dnetwork.start()
		

		
		#gui stuff start
		self.grid()

		self.citizenNameVariable = Tkinter.StringVar()
		self.entry = Tkinter.Label(self,textvariable=self.citizenNameVariable)
		
		self.entry.grid(column=1,row=0,sticky='EW')
		# self.entry.bind("<Return>", self.OnPressEnter)
		self.citizenNameVariable.set("noone")#self.who_am_i.name+"yes it's working")
		
		self.labelVariable = Tkinter.StringVar()
		label = Tkinter.Label(self,textvariable=self.labelVariable,anchor="w",fg="white",bg="blue")
		label.grid(column=0,row=0,columnspan=1,sticky='EW')
		self.labelVariable.set(u"citizen id")
		
		self.legislatureHashVariable = Tkinter.StringVar()
		self.legislatureHash = Tkinter.Entry(self,textvariable=self.legislatureHashVariable)
		
		self.legislatureHash.grid(column=1,row=1,sticky='EW')
		# self.legislatureHash.bind("<Return>", self.OnPressEnter)
		self.legislatureHashVariable.set(u"afafaf777ffee")
		
		self.legHashLabelVariable = Tkinter.StringVar()
		legHashLabel = Tkinter.Label(self,textvariable=self.legHashLabelVariable,anchor="w",fg="white",bg="blue")
		legHashLabel.grid(column=0,row=1,columnspan=1,sticky='EW')
		self.legHashLabelVariable.set(u"group hash")
		
		# 		
		# 		button = Tkinter.Button(self,text=u"Click me !",command=self.OnButtonClick)
		# 		button.grid(column=1,row=0)
		# 		
		# 		self.labelVariable = Tkinter.StringVar()
		# 		label = Tkinter.Label(self,textvariable=self.labelVariable,anchor="w",fg="white",bg="blue")
		# 		label.grid(column=0,row=1,columnspan=2,sticky='EW')
		# 		
		# 		self.labelVariable.set(u"Hello !")

		r_c=self.updateLawDisplay()
		
		self.newLawLabelVariable = Tkinter.StringVar()
		self.new_law_label = Tkinter.Label(self,textvariable=self.newLawLabelVariable,anchor="w",fg="white",bg="blue")
		self.new_law_label.grid(column=0,row=r_c,columnspan=1,sticky='EW')
		self.newLawLabelVariable.set(u"new law section")
		r_c+=1
		
		self.newLawNameLabelVariable = Tkinter.StringVar()
		self.new_law_name_label = Tkinter.Label(self,textvariable=self.newLawNameLabelVariable,anchor="w",fg="white",bg="blue")
		self.new_law_name_label.grid(column=0,row=r_c,columnspan=1,sticky='EW')
		self.newLawNameLabelVariable.set(u"name")
		
		self.newLawNameVariable = Tkinter.StringVar()
		self.new_law_name = Tkinter.Entry(self,textvariable=self.newLawNameVariable)
		
		self.new_law_name.grid(column=1,row=r_c,sticky='EW')
		# self.entry.bind("<Return>", self.OnPressEnter)
		# self.newLawNameVariable.set(self.who_am_i.name)
		r_c+=1
		
		self.newLawDescLabelVariable = Tkinter.StringVar()
		self.new_law_desc_label = Tkinter.Label(self,textvariable=self.newLawDescLabelVariable,anchor="w",fg="white",bg="blue")
		self.new_law_desc_label.grid(column=0,row=r_c,columnspan=1,sticky='EW')
		self.newLawDescLabelVariable.set(u"description")
		
		self.newLawDescVariable = Tkinter.StringVar()
		self.new_law_desc = Tkinter.Entry(self,textvariable=self.newLawDescVariable)
		self.new_law_desc.grid(column=1,row=r_c,sticky='EW')
		r_c+=1

		self.create_law_button=Tkinter.Button(self,text=u"create new law",command=lambda rr=r_c:self.CreateLawButtonClick(rr))
		self.create_law_button.grid(column=0,row=r_c)
		r_c+=1
		
		self.share_changes_button=Tkinter.Button(self,text=u"submit changes",command=self.shareChangesClick)
		self.share_changes_button.grid(column=0,row=r_c)
		

		


		self.grid_columnconfigure(0,weight=1)
		# self.resizable(True,False)
		# self.update()
		# self.geometry(self.geometry())	   
		# self.entry.focus_set()
		# self.entry.selection_range(0, Tkinter.END)
	def updateLawDisplay(self):
		c_c=0
		r_c=2
		laws=Law.query.all()
		for l in laws:
			name_txt = Tkinter.StringVar()
			print name_txt
			name = Tkinter.Label(self,textvariable=name_txt,
								  anchor="w",fg="white",bg="blue")
			name.grid(column=0,row=r_c,sticky='EW')
			name_txt.set(l.name)
		
			desc_txt = Tkinter.StringVar()
			desc = Tkinter.Label(self,textvariable=desc_txt,
								  anchor="w",fg="white",bg="blue")
			desc.grid(column=1,row=r_c,sticky='EW')
			desc_txt.set(l.description)
			

			
			v_count_txt = Tkinter.StringVar()
			v_count = Tkinter.Label(self,textvariable=v_count_txt,
								  anchor="w",fg="white",bg="blue")
			v_count.grid(column=2,row=r_c,sticky='EW')
			v_count_txt.set(len(filter(lambda x:x.yes_no,l.votes)))
			
			v_count_txt = Tkinter.StringVar()
			v_count = Tkinter.Label(self,textvariable=v_count_txt,
								  anchor="w",fg="white",bg="blue")
			v_count.grid(column=3,row=r_c,sticky='EW')
			v_count_txt.set(len(l.votes))
			
			#this lambda stuff was a pain to get right but i like it.
			Tkinter.Button(self,text=u"yes",command=lambda n=l: self.YesButton(n)).grid(column=4,row=r_c)
			Tkinter.Button(self,text=u"no",command=lambda n=l: self.NoButton(n)).grid(column=5,row=r_c)
			
			
			# print len(l.votes)
			r_c+=1

			
		
		return r_c

	def updateCreateLawButtons(self,r_c):
		self.new_law_label.grid(column=0,row=r_c,columnspan=1,sticky='EW')
		r_c+=1
		self.new_law_name_label.grid(column=0,row=r_c,columnspan=1,sticky='EW')
		self.new_law_name.grid(column=1,row=r_c,sticky='EW')
		r_c+=1
		self.new_law_desc_label.grid(column=0,row=r_c,columnspan=1,sticky='EW')
		self.new_law_desc.grid(column=1,row=r_c,sticky='EW')
		r_c+=1
		self.create_law_button.grid(column=0,row=r_c)
		r_c+=1
		self.share_changes_button.grid(column=0,row=r_c)
		r_c+=1
		return r_c
		
	def YesNoButtonHelper(self,l,election):
		# self.labelVariable.set(l.name)
		
		previous_votes=filter(lambda x:x.law==l,self.who_am_i.votes)
		v=""
		if(len(previous_votes)>0):
			v=previous_votes[0]
			v.yes_no=election
		else:
			v=Vote()
			v.citizen=self.who_am_i
			v.fingerprint=v.citizen.fingerprint #i don't really like this
			v.law=l
			v.yes_no=election
		
		#todo- add nonce/timestamp to this. also, use hashes/fingerprints vs text names
		e='1' if v.yes_no else '0'
		text=v.citizen.fingerprint+","+v.law.name+","+e

		sign=self.gpg.sign(text,**self.my_gpg_stuff)
		raw_data=sign.data

		p=re.compile(".*-----BEGIN PGP SIGNED MESSAGE-----.*",re.M|re.S)
		reduced_sign=''
		if p.match(raw_data):				
			#todo - clean up the following. it's pretty messy
			p=re.compile('.*BEGIN PGP SIGNATURE-*\n([^\n]*\n){1,2}\n\n*(.*)\n-----END PGP SIGNATURE-----.*',re.M|re.S)

			print raw_data
			m=p.match(raw_data)
			# print m.group(1)
			# print m.group(2)
			# exit()
			reduced_sign=m.group(2)
			p=re.compile('\n',re.M|re.S)
			reduced_sign=p.sub('',reduced_sign)
		else:
			reduced_sign=raw_data
		v.sign=reduced_sign
		v.verified=True
		
		session.commit()
		self.updateLawDisplay()
		
	def YesButton(self,l):
		self.YesNoButtonHelper(l,True)

	def NoButton(self,l):
		self.YesNoButtonHelper(l,False)
			
	def CreateLawButtonClick(self,r_c):
		l=Law()
		l.name=self.newLawNameVariable.get()
		l.description=self.newLawDescVariable.get()
		session.commit()
		self.newLawDescVariable.set("")
		self.newLawNameVariable.set("")
		self.updateLawDisplay()
		self.updateCreateLawButtons(r_c)
		
	def shareChangesClick(self):
		session.flush()
		self.dnetwork.shareChanges()		
		
	def OnButtonClick(self):
		self.labelVariable.set( self.citizenNameVariable.get()+" (You clicked the button)" )
		self.entry.focus_set()
		self.entry.selection_range(0, Tkinter.END)

	def OnPasscodePressEnter(self,event):
		k=self.private_key_names_variable.get()
		p=self.passcode_entry_variable.get()

		fp=filter(lambda x: x['uids'][0]==k,self.gpg.list_keys(True))[0]['fingerprint']
		self.my_gpg_stuff={'keyid':fp,'passphrase':p}
		self.dnetwork.my_gpg_stuff={'keyid':fp,'passphrase':p}
		sign_verify=self.gpg.sign("random text(timestamp maybe)",**self.my_gpg_stuff) #static text works fine here.
															#any actual votes cast get a nonce so this is really
															#just a convenience for the user
		if not(self.gpg.verify(sign_verify.data).valid):
			tkMessageBox.showinfo("info","passcode incorrect")
		else:
			tkMessageBox.showinfo("info","passcode correct! welcome!")
			#remember this user and show it automatically next time the program starts
			default_user_variables=Configuration.query.filter_by(variable='default_user').all()
			if len(default_user_variables)==0:
				default_user_variables=[Configuration()]
				default_user_variables[0].variable='default_user'
			default_user_variables[0].value=k
			session.commit()
			
			#find what citizen we are in the db(by matching pubkey), and save needed gpg data for use
			temp_pub_key=self.gpg.export_keys(self.my_gpg_stuff['keyid'])
			matching_citizens=Citizen.query.filter_by(public_key=temp_pub_key).all()
			if len(matching_citizens)>0:
				self.who_am_i=matching_citizens[0]
			else: #how do we even verify that the keypair is a valid voter? besides that we find them in our db?
				tkMessageBox.showinfo("info","however...citizen not found in the db")
				exit()
						
			self.citizenNameVariable.set(self.who_am_i.name)
			self.login_window.destroy()
			
			
	def OnPressEnter(self,event):
		self.labelVariable.set( self.citizenNameVariable.get()+" (You pressed ENTER)" )
		self.entry.focus_set()
		self.entry.selection_range(0, Tkinter.END)

def usage():
	print "Syntax: dgf_client [options] \n\
	\n\
	Commands:\n\
	\n\
	     --cport=                   specify cport\n\
	     --mport=                   specify mport\n\
	     --ip=                      specify ip\n\
	     --db=                      specify db file\n\
	 -h, --help                     show this guide\n\
	"
if __name__ == "__main__":
	
	try:
		opts, args = getopt.getopt(sys.argv[1:], "h:v", ["help","cport=","mport=","ip=","db="])
	except getopt.GetoptError, err:
		# print help information and exit:
		print str(err) # will print something like "option -a not recognized"
		usage()
		sys.exit(2)
	# verbose = False
	ip='localhost'
	cport=9091
	mport=9090
	db='dgf'
	for o, a in opts:
		if o == "-v":
			verbose = True
		elif o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o =="--mport":
			mport=a
		elif o == "--cport":
			cport = a
		elif o == "--ip":
			ip = a
		elif o == "--db":
			db = a
		else:
			assert False, "unhandled option"

	my_ip_info=DgfNetwork.Peer()
	my_ip_info.ip=ip
	my_ip_info.cport=int(cport)
	my_ip_info.mport=int(mport)

	metadata.bind = "sqlite:///"+db+".sqlite"
	# metadata.bind.echo = True	#??
	# from mock_data import * #don't always need this
	setup_all()
	
	# app = simpleapp_tk(None)
	root=Tkinter.Tk()
	app = simpleapp_tk(root,my_ip_info)

	app.mainloop()
	session.flush()#not sure if needed but just in case
	exit() #really maybe we should call app.dnetwork.close() but this seems to cover all threads