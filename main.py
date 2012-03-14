#!/usr/bin/python


import Tkinter
import tkMessageBox
#sqlite stuff
from data_model import *
from mock_data import *

metadata.bind = "sqlite:///dgf.sqlite"
metadata.bind.echo = True	
setup_all()
#end sqlite stuff

import os
import gnupg
import re
import time
from DgfNetwork import *


class simpleapp_tk(Tkinter.Tk):
	def __init__(self,parent):
		Tkinter.Tk.__init__(self,parent)
		self.parent = parent
		self.initialize()

	def initialize(self):
		#pgp stuff
		#todo - move this somewhere else/set up better
		self.gpg = gnupg.GPG(gnupghome='/Users/neilhudson/.gnupg') #todo - this is really bad.
		# self.my_gpg_stuff={'keyid':self.gpg.list_keys()[2]['fingerprint'],'passphrase':'oreo'}
		self.my_gpg_stuff={'keyid':'blah','passphrase':'nothing'}

		private_key_list=self.gpg.list_keys(True) #private keys only

		#this probably shouldn't be here
		
		#ask the user to give their private key passcode
		self.login_window=Tkinter.Toplevel()
		self.login_window.title('who are you?')
		self.login_window.geometry("500x100+100+130")
		self.login_window.lift(aboveThis=self)
		
		
		private_key_names=map(lambda x: x['uids'][0] ,private_key_list)

		self.private_key_names_variable = Tkinter.StringVar()
		self.private_key_names_variable.set(private_key_names[0]) # default value
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
		self.dnetwork=DgfNetwork()
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
		self.resizable(True,False)
		self.update()
		self.geometry(self.geometry())	   
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
			v.law=l
			v.yes_no=election
		
		#todo- add nonce/timestamp to this. also, use hashes/fingerprints vs text names
		e='1' if v.yes_no else '0'
		text=v.citizen.name+","+v.law.name+","+e
		
		sign=self.gpg.sign(text,**self.my_gpg_stuff)
		raw_data=sign.data
		p=re.compile(".*-----BEGIN PGP SIGNED MESSAGE-----.*",re.M|re.S)
		reduced_sign=''
		if p.match(raw_data):				
			#todo - clean up the following. it's pretty messy
			p=re.compile('.*Comment: GPGTools - http://gpgtools.org\n\n?(.*)\n-----END PGP SIGNATURE-----.*',re.M|re.S)

			m=p.match(raw_data)
			reduced_sign=m.group(1)
			p=re.compile('\n',re.M|re.S)
			reduced_sign=p.sub('',reduced_sign)
		else:
			reduced_sign=raw_data
		v.sign=reduced_sign
		
		print self.private_key_names_variable.get()
		print self.passcode_entry_variable.get()
		exit()
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
		sign_verify=self.gpg.sign("random text(timestamp maybe)",**self.my_gpg_stuff) #static text works fine here.
															#any actual votes cast get a nonce so this is really
															#just a convenience for the user
		if not(self.gpg.verify(sign_verify.data).valid):
			tkMessageBox.showinfo("info","passcode incorrect")
		else:
			tkMessageBox.showinfo("info","passcode correct! welcome!")
			temp_pub_key=self.gpg.export_keys(self.my_gpg_stuff['keyid'])
			self.who_am_i=filter(lambda x: x.public_key==temp_pub_key, Citizen.query.all())[0]
			#todo - maybe we should make sure we had some success here? what if it filters to null set?
			#on that note, how do we even verify that the keypair is a valid voter?
			self.citizenNameVariable.set(self.who_am_i.name)
			self.login_window.destroy()
			
			
	def OnPressEnter(self,event):
		self.labelVariable.set( self.citizenNameVariable.get()+" (You pressed ENTER)" )
		self.entry.focus_set()
		self.entry.selection_range(0, Tkinter.END)

if __name__ == "__main__":
	
	app = simpleapp_tk(None)
	app.title('dgf')

	app.mainloop()
	session.flush()#not sure if needed but just in case
	exit() #really maybe we should call app.dnetwork.close() but this seems to cover all threads