# -*- coding: utf-8 -*-
"""
Created on Mon May 24 17:26:55 2021

@author: sheet
"""

from tkinter import *

win = Tk() 
w, h = win.winfo_screenwidth(), win.winfo_screenheight()
win.geometry("%dx%d+0+0" % (w, h))

w = Label(win, text ='StudyTonight', font = "200",fg="Navyblue") 
w.pack() 
	
msg = Message(win,font = "150", text = " Data URLs are composed of four parts: a prefix (data:), a MIME type indicating the type of data, an optional base64 token if non-textual, and the data itself . If the data is textual, you can embed the text (using the appropriate entities or escapes based on the enclosing document's type). If omitted, defaults to text/plain;charset=US-ASCII . If data contains characters defined in RFC 3986 as reserved characters, or contains space characters, newline characters, those characters must be percent-encoded ") 
	
msg.pack() 

win.mainloop() 