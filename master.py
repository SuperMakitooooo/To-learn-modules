import tkinter as tk
from functools import partial 
import datetime
import time

#
month = str(int(datetime.datetime.now().isoformat()[5:7]))
day_list = [29,31,29,31,30,31,30,31,31,30,31,30,31]
week = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]


sub_window = []
main_window = dict()
others = dict()

class button(tk.Button):
	def __init__(self,label_text,run_command):
		super().__init__(self,hedder,label_text,relief=tk.RAISED, width="5", height="1", command=run_command)
		


class carender():
	def __init__(self,master=None):
		main_window["root"] = tk.Tk()
		labels = dict()
		others["hedder"] = tk.Label(main_window["root"],text="",relief=tk.RAISED,pady =0)
		others["hedder_week"] = tk.Label(main_window["root"], text="",padx=0)
	
		
		for k,i in enumerate(week,0):
			others["label_week"]=tk.Label(hedder_week,text=i,width="10",height="1")
			others["label_week"].grid(row=0,column=k)

		main_window["body"] = tk.Label(main_window["root"],text="123")
		main_window["label_month"]=tk.Label(others["hedder"],text=month + "月",width="5",height="1")
		
		others["button_before"] = button(others["hedder"],text="before", partial(self.change,"before"))
		others["button_after"] = button(others["hedder"],text="after", partial(self.change,"after"))
		others["button_quit"] = button(others["hedder"],text="quit",None)
		
		main_window["body"].grid(row=0)
		others["hedder_week"].grid(row=1)
		
		main_window["body"].grid(row=2)
		main_window["label_month"].grid(row=0,column=1)
		
		others["button_before"].grid(row=0,column=0)
		others["button_after"].grid(row=0,column=2)
		others["button_quit"].grid(row=0,column=4)
		self.buttons(int(month),31,0)

	


	def buttons(self,start,dayss,or_destroy):
		if or_destroy:
			try:
				for i in self.button:
					i.destroy()
			except Exception as e:
				#print(e)
				pass	
			
		month_num = int(self.label_month["text"][:-1])
		days = day_list[month_num]
		

		main_window["Buttons"] = []
		for i in range(1,days+1):
			print(i)
			main_window["Buttons"].append(tk.Button(main_window["body"], text = str(i), relief = tk.RAISED,width=10,height=6,bg = "white" ))
		
	
		for i in range(0,len(main_window["Buttons"])):
			first_day = datetime.date(2022,int(self.label_month["text"][:-1]),1).weekday()
			d =  1 + i
			main_window["Buttons"][i].bind("<Enter>", partial(self.subwindows, d, "show", 0))
			main_window["Buttons"][i].bind("<Leave>", partial(self.subwindows, d, "show", 1))
			main_window["Buttons"][i].bind("<ButtonPress>", partial(self.subwindows, d, "write", 0))	
			position = first_day + i
			main_window["Buttons"][i].grid(column=position%7,row=1+int(position//7))
	
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
				self.sub_show.title(self.label_month["text"]+str(day)+"日")

				path = "schedule\\2022\\" + self.label_month["text"][:-1] + "_" + str(day) + ".txt"
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
			path = "schedule\\2022\\" + self.label_month["text"][:-1] + "_" + str(day) + ".txt"
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
			save_button = tk.Button(button_frame_editor, text="Save as", command=save)
			text_editor.bind("<KeyPress>", save_key)
	
			button_frame_editor.grid(row=0,column=0,sticky="ns")
			text_editor.grid(row=0,column=1,sticky="nsew")
			save_button.grid()
			self.editor.mainloop()
					
	def change(self,mode):
		before = self.label_month["text"]
		if mode == "before":
			after = int(before[:-1])  - (1 if before[:-1] != "1" else -11)
			self.label_month.config(text=str(after) + "月")		
		if mode == "after":
			after = int(before[:-1])  + (1 if before[:-1] != "12" else -11)
			self.label_month.config(text=str(after) + "月")	
		self.buttons(2,31,1)


	def button_funcs(self):
		pass


	def test_method(self):
		print(12)

	def mainloops(self,tk_object):
		tk_object.mainloop()



widgets = carender()
widgets.mainloops(widgets.roo

