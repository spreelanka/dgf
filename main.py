#!/usr/bin/python


import Tkinter
from data_model import *
# setup_all()

class simpleapp_tk(Tkinter.Tk):
	def __init__(self,parent):
		Tkinter.Tk.__init__(self,parent)
		self.parent = parent
		self.initialize()

	def initialize(self):
		#this probably shouldn't be here
		self.who_am_i=Citizen.query.first()
		
		#gui stuff start
		self.grid()

		self.entryVariable = Tkinter.StringVar()
		self.entry = Tkinter.Entry(self,textvariable=self.entryVariable)
		
		self.entry.grid(column=1,row=0,sticky='EW')
		# self.entry.bind("<Return>", self.OnPressEnter)
		self.entryVariable.set(self.who_am_i.name)
		
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

		


		self.grid_columnconfigure(0,weight=1)
		self.resizable(True,False)
		self.update()
		self.geometry(self.geometry())	   
		self.entry.focus_set()
		self.entry.selection_range(0, Tkinter.END)
	def updateLawDisplay(self):
		c_c=0
		r_c=2
		laws=Law.query.all()
		for l in laws:
			# print "\n\nPAY ATTENTION TO ME\n\n"
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
		return r_c
		
	def YesButton(self,l):
		# self.labelVariable.set(l.name)
		
		previous_votes=filter(lambda x:x.law==l,self.who_am_i.votes)
		if(len(previous_votes)>0):
			previous_votes[0].yes_no=True
		else:
			v=Vote()
			v.citizen=self.who_am_i
			v.law=l
			v.yes_no=True
		
		session.commit()
		self.updateLawDisplay()
		self.entry.focus_set()
		self.entry.selection_range(0, Tkinter.END)

	def NoButton(self,l):
		# self.labelVariable.set(l.name)
		previous_votes=filter(lambda x:x.law==l,self.who_am_i.votes)
		if(len(previous_votes)>0):
			previous_votes[0].yes_no=False
		else:
			v=Vote()
			v.citizen=self.who_am_i
			v.law=l
			v.yes_no=False			

		session.commit()
		self.updateLawDisplay()
		self.entry.focus_set()
		self.entry.selection_range(0, Tkinter.END)
			
	def CreateLawButtonClick(self,r_c):
		# newLawDescVariable
		# newLawNameLabelVariable
		l=Law()
		l.name=self.newLawNameVariable.get()
		l.description=self.newLawDescVariable.get()
		session.commit()
		self.newLawDescVariable.set("")
		self.newLawNameVariable.set("")
		self.updateLawDisplay()
		self.updateCreateLawButtons(r_c)
		# self.labelVariable.set( self.entryVariable.get()+" (You clicked the button)" )
		# self.entry.focus_set()
		# self.entry.selection_range(0, Tkinter.END)		
		
		
	def OnButtonClick(self):
		self.labelVariable.set( self.entryVariable.get()+" (You clicked the button)" )
		self.entry.focus_set()
		self.entry.selection_range(0, Tkinter.END)

	def OnPressEnter(self,event):
		self.labelVariable.set( self.entryVariable.get()+" (You pressed ENTER)" )
		self.entry.focus_set()
		self.entry.selection_range(0, Tkinter.END)

if __name__ == "__main__":
	app = simpleapp_tk(None)
	app.title('my application')
	app.mainloop()