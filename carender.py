import tkinter as tk
from functools import partial 
import datetime
import time
import numpy as np
import json
import pprint

date_set = None

def all_grid(positions):
	if type(positions) != type(list()):
		raise  Exception
		print("positons which gived to all_grid() must be list.")
	for obj in positions:
		[obj[0][i].grid(column=x, row=y) for i,(x,y) in enumerate(obj[1],0)]
		
def json_insert(path, add):
	with open(path, "r", encoding="utf-8") as f:
		try:
			text= json.load(f)
		except Exception as e:
			print(e)
			text = {}
	text.update(add)


	with open(path, "w", encoding="utf-8") as f:
		json.dump(text,f,indent=3)	



month_now = str(int(datetime.datetime.now().isoformat()[5:7]))
day_list = [29,31,29,31,30,31,30,31,31,30,31,30,31]
week = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]


class carender(tk.Frame):


	def __init__(self,master):
		super().__init__(master)
		self.date_set = None
		self.grid()		
		self.month = int(month_now) 
		self.make()
		self.many_bind()
		self.many_grid()
		#Placing and binding objects on crender app


	def make(self):
		#Making objects to put on carender app; hedder, button that show date, label that show weekdays, etc

		
		self.hedders = [
			hedder := tk.Label(
					self,text="",
					relief=tk.RAISED,
					pady =0
					),
			hedder_week := tk.Label(
						self, 
						text="",
						padx=0
						)
			]

		self.control_buttons = [
			button_before := tk.Button(
						hedder, 
						text="before", 
						relief=tk.RAISED,
						width = "5", height = "1",
						command=partial(self.change,"before")
						),
			button_after := tk.Button(
						hedder,
						text="after",
						relief=tk.RAISED,
						width = "5",height = "1",
						command=partial(self.change,"after")
						),
			button_quit := tk.Button(
						hedder,
						text="quit"
						)
			]


		self.control_buttons = [	button_before := tk.Button(	hedder, 
								text="before", 
								relief=tk.RAISED,
								width = "5", height = "1",
								command=partial(self.change,"before")	),
					
					button_after := tk.Button(	hedder,
								text="after",
								relief=tk.RAISED,
								width = "5",height = "1",
								command=partial(self.change,"after")	),

					button_quit := tk.Button(	hedder,
								text="quit"			)	]


		
		self.labels = [
			label_weeks := tk.Label(
						hedder_week, 
						text=i, 
						width="10", height="1") 
						for i in week
			] + [
			label_month := tk.Label(
						hedder,
						text=str(self.month) + "月",
						width="5",height="1"
						),
			body := tk.Label(
						self,
						text="123"
						)
			]

		days = day_list[self.month]		
		self.day_buttons = [
				tk.Button(
						body, 
						text=str(i), 
						relief=tk.RAISED, 
						width=10, height=6, 
						bg="white", 
						command=partial(self.set,i,self.month)
					)
				 for i in range(1,days+1)]
	



	def many_grid(self):
		#Placing objects which made by make() in Master Label object(a "self" object that below careder()).

		first_day = datetime.date(2022,self.month,1).weekday()

			
		grid_positions = [
				[self.control_buttons,	[(0,0),(2,0),(4,0)]],
				[self.hedders,		[(0,0),(0,1)]],
				[self.labels,		[(k,0) for k in range(7)]+[(1,0),(0,2)]],
				[self.day_buttons,		[(i%7, 1+int(i//7)) for i in range(first_day-1, first_day+day_list[self.month]-1)]]
				]

		all_grid(grid_positions)


	def many_bind(self):
		#Binding objects as many_grid() with set().
		binding_day_buttons =[	[	button.bind(	"<Enter>", 
								partial(self.passed,self.passed)		),
	
						button.bind(	"<Leave>", 
								partial(self.passed,self.passed)		),
	
						button.bind(	"<ButtonPress>",
								self.passed			)]
					for i,button in enumerate(self.day_buttons,0)				]


	def passed(self,a=None,b=None):
		pass
		

	def set(self,day,month):
		# Getting value of a date from the binded objects and the many_bind() function and set global variable "date_set" to the value. 
		self.date_set = [month,day]



	def change(self,mode):
		#Chenging state of date.
		before = self.month
		if mode == "before":
			after = before  - (1 if before != "1" else -11)
			self.month = after		
		if mode == "after":
			after = before  + (1 if before != "12" else -11)
			self.month = after	
		self.make()
		self.grid()
		self.bind()
 
	
	
	"""
	def subwindows(self,day,mode,other,event_variable):
		if mode == "show":
			if other :
				self.stop = True
				try:
					self.sub_show.destroy()
				except  Exception as e:
					print("")
			else:	
					
				self.sub_show = tk.Toplevel(self.root)
				self.sub_show.geometry("+"+(str(  int(self.root.winfo_x() + self.root.winfo_width())  ) )+"+"+str(  int(self.root.winfo_y()  )))
				self.sub_show.title(str(self.month)+str(day)+"日")

				path = "schedule\\2022\\" + str(self.month)[:-1] + "_" + str(day) + ".txt"
				with open(path, "r", encoding="utf-8") as texts:
					self.body_sub_show = tk.Label(self.sub_show, text=texts.read())
				self.body_sub_show.grid(row=0)	
				self.sub_show.mainloop()
			

		if mode == "write":
			try:
				self.editor.destroy()
			except Exception as e:
				print (e)
	
			self.editor = tk.Toplevel(self.root)
			self.editor.geometry("+"+(str(  int(self.root.winfo_x() + self.root.winfo_width())  ) )+"+"+str(  int(self.root.winfo_y()  )))
			text_editor = tk.Text(self.editor)
			path = "schedule\\2022\\" + str(self.month)[:-1] + "_" + str(day) + ".txt"
			print(path)
			with open(path,"r",encoding="utf-8") as texts:
				text_editor.insert(tk.END,texts.read())
			print(self.root.winfo_x)

			def save():
				with open(path,"w",encoding="utf-8") as save_file:
					save_file.write(text_editor.get("1.0",tk.END))


			def save_key(e):
				print(e.keysym)
				if e.keysym == "F5":
					save()

			button_frame_editor = tk.Frame(self.editor)

			save_button = tk.Button(
						button_frame_editor, 
						text="Save as", 
						command=save
						)
			text_editor.bind("<KeyPress>", save_key)
	
			button_frame_editor.grid(
						row=0,
						column=0,
						sticky="ns"
						)
			text_editor.grid(row=0,column=1,sticky="nsew")
			save_button.grid()
			self.editor.mainloop()
					
	"""

	def button_funcs(self):
		pass


	def test_method(self):
		print(12)

	def mainloops(self,tk_object):
		tk_object.mainloop()


class dialy(tk.Text):
	def __init__(self,master):
		super().__init__(master)
		self.text = None
		self.date_set = 1
		self.bind("<KeyPress>", self.save)
		self.grid()		
		self.load(1)


	def load(self,e):
		month, day = date_set if date_set != None else [1,1]
		file_path = "dialy/" + str(month) + "_" + str(day) + ".txt"
		with open(	file_path, 
				"r+", 
				encoding="utf-8"	) as f:
			text= f.read()
		self.insert(tk.END, text)
		


	def save(self,e):
		if self.text != self.get("1.0", tk.END):
			month, day = date_set if date_set != None else [1,1]
			file_path = "dialy/" + str(month) + "_" + str(day) + ".txt"
			with open(	file_path, 
					"w+", 
					encoding="utf-8"		) as f:
				f.write(self.get("1.0",tk.END))


class task_init:
	"""task_scの__init__内です実行する関数をまとめてここで定義する"""
	def Init(self):
		self.load()
		self.grid_buttons()
		self.grid_edits()


	def load(self):
		#起動時の読み込み
		with open(	"tasks/incomplete.json",
				"r+",
				encoding = "utf-8"		) as f:
			try:
				self.task_string = json.load(f)[0]
			except Exception as e:
				print(e, 354)
				self.task_string = dict()


	def grid_buttons(self):

		self.tasks = {	task: {	"deadline": self.task_string[task],
					"var":(var := tk.IntVar(value=0)),
					"button":tk.Checkbutton(self, text=task+":"+str(self.tasks[task]), variable=var),
					"var_name":var	}
				for task in self.task_string 								}


	def grid_edits(self):
		self.edits = [	edit_box 		:= tk.Frame(self),
				task_label 	:= tk.Label(edit_box, text="タスク:",height=1),
				input_task 	:= tk.Text(edit_box,width=10, height=1),
				deadline_label 	:= tk.Label(edit_box, text="締め切り:",height=1),
				input_deadline 	:= tk.Text(edit_box,width=10, height=1)			]

		
		length = len(self.tasks)

		none = [		[	self.tasks[task]["button"].grid(column=0, row=i) 
					for i,task in enumerate(self.tasks, 0)		],
				[	edit_widget.grid(column=i, row=50 if i==0 else 0) 
					for i,edit_widget in enumerate(self.edits, 0)			]		]

		
class task_sc(tk.Frame, task_init):
	"""
	init→
	
	"""	
	def __init__(self, master):
		print("__init__ g")
		super().__init__(master)
		super().Init()
		self.binds()
		self.grid()		
			


	def binds(self):
		binding_buttons = 	[	self.tasks[task]["button"].bind("<ButtonPress>", self.for_binding_button) 
					for task in self.tasks					]
		binding_edits = 	[	self.edits[2].bind("<KeyRelease>", self.for_binding_editor),
					self.edits[4].bind("<KeyRelease>", self.for_binding_editor)	]


	def for_binding_button(self,e):
		self.replace_buttons()
		

	def for_binding_editor(self,e):
		self.edit(e)
		self.replace_buttons()


	def replace_buttons(self):
		placing = [	[self.tasks[task]["button"].grid()]
				for task in self.tasks
				if not self.tasks[task]["var"].get()	]
		self.binds()	
		deleting = [	[self.tasks[task]["button"].destroy()]
				for task in self.tasks
				if self.tasks[task]["var"].get()		]
		self.deleting_data()
				
	def deleting_data(self):
		for task in self.tasks:
			if self.tasks[task]["var"].get():			
				self.tasks.pop(task) 
								

	def edit_files(self):
		inserting = [	 json_insert(	"tasks/complete.json",
					{task: self.tasks[task]["deadline"]}	)
				for task in self.tasks
				if self.tasks[task]["var"]					]
		
		self.replace_buttons()
		
		to_dump = {task: self.tasks[task]["deadline"] for task in self.tasks}
		with open("tasks/incomplete.json", "w", encoding="utf-8") as f:
				json.dump(to_dump, f, indent=3)

	
	def edit(self,a):
		task = 	self.edits[2].get("1.0",tk.END)[:-1]
		dl =	self.edits[4].get("1.0", tk.END)[:-2]
		if  a.keysym == "Return":
			add = {	task: {	"deadline": dl,
					"var":(var := tk.IntVar(value=0)),
					"button":tk.Checkbutton(	self,
								text=task+":"+dl, 
								variable=var	)	}	}
				
			self.tasks.update(add) 
			
			self.edits[2].delete("1.0", tk.END)
			self.edits[4].delete("1.0", tk.END)
			self.edit_files()
			assert task in self.tasks

		




if __name__ == "__main__":
	root = tk.Tk()
	t = task_sc(root)	
	root.mainloop()
	


