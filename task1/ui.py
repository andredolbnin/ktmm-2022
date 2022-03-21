import json
import os.path
from tkinter import *
from tkinter import ttk
import tkinter.filedialog
from ModelViewer import ModelViewer


filename = ""

def run():
    MV = ModelViewer()
    MV.main_loop()
    
def choose():
    global filename
    file = tkinter.filedialog.askopenfile("r")
    filename = file.name
    print(filename)
    
#def params():
#    if os.path.exists(filename):
#        with open(filename, 'r') as f:
#            data = json.load(f)
#            s = "Параметры:\n"
#            for key in data:
#                s += f'{key}: {data[key]} \n'
#            return s

root = Tk()

root.geometry("500x200")

b1 = Button(text="Модель", width=15, height=3)
b1.config(command=run)
b1.pack(side=TOP)

b2 = Button(text="Выбрать файл", width=15, height=3)
b2.config(command=choose)
b2.pack(side=TOP)

b3 = Button(text="Выйти", width=15, height=3)
b3.config(command=root.destroy)
b3.pack(side=TOP)
root.mainloop()
