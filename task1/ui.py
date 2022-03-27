import config
import numpy as np
from tkinter import *
from tkinter import ttk
import tkinter.filedialog
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from numpy import genfromtxt

from ModelViewer import ModelViewer
from EquationSolver import EquationSolver


def resolve():
    global data, mn, mx
    ES = EquationSolver(coef_file, sol_file)
    t = sv.get()
    try:
        ES.solve(int(t))
        
    except:
        ES.solve()
        
    with open(sol_file, 'r') as f:
        data = np.loadtxt(f)
        
    mn = np.amin(data[:, 1:6])
    mx = np.amax(data[:, 1:6])
    
    T.delete(1.0, END)
    T.insert(END, "Файл с параметрами: " + coef_file + 
             "\nФайл для записи результатов: " + sol_file)
    
    plot()
    plot_colorbar()
    
    
def choose():
    global coef_file
    file = tkinter.filedialog.askopenfile('r')
    try:
        coef_file = file.name
        resolve()
        
    except Exception as e:
        print(f"Error in `choose`: {e}")
    
    
def choose2():
    global sol_file
    file = tkinter.filedialog.askopenfile('r')
    try:
        sol_file = file.name
        resolve()

    except Exception as e:
        print(f"Error in `choose2`: {e}")
    
    
def run():
    MV = ModelViewer(data)
    MV.main_loop()


def plot():
    global canvas
    matplotlib.use("Agg")
    fig = plt.figure(figsize=(4, 4), dpi=100)
    
    try:
        for i in range(5):
            plt.plot(data[:, 0], data[:, i + 1], label=f"T{i + 1}")
            
            plt.grid()  
            plt.xlabel('t')  
            plt.legend(loc="best")
            plt.title("Температуры")
            
            canvas = FigureCanvasTkAgg(fig, master=root)
            canvas.draw()
            canvas.get_tk_widget().place(x=60, y=200)
            
    except:
        pass
    
    return fig


def plot_colorbar():
    global canvas2
    matplotlib.use("Agg")
    fig = plt.figure(figsize=(1, 4), dpi=100)
    
    try:
        ax = fig.add_axes([0.05, 0.05, 0.3, 0.9])
        cb = matplotlib.colorbar.ColorbarBase(ax, orientation='vertical', cmap=cm,
            norm=matplotlib.colors.Normalize(vmin=mn, vmax=mx))
        canvas2 = FigureCanvasTkAgg(fig, master=root)
        canvas2.draw()
        canvas2.get_tk_widget().place(x=520, y=200)
        
    except:
        pass
    
    return fig
    

def handler(event):
    resolve()
    
    
coef_file = config.coef_file
sol_file = config.sol_file
data = None
mn, mx = None, None
  
root = Tk()

root.geometry("650x650+10+10") #200
#root.attributes("-fullscreen", True)
root.title(" ")

b1 = Button(root, text="Выбор параметров", width=17, height=3)
b2 = Button(root, text="Выбор записи", width=15, height=3)
#b3 = Button(root, text="График", width=15, height=3)
b4 = Button(root, text="Модель", width=15, height=3)
b5 = Button(root, text="Выйти", width=15, height=3)
#b6 = Button(root, text="Пересчитать", width = 10, heigh=2)

b1.config(command=choose)
b2.config(command=choose2)
#b3.config(command=plot)
b4.config(command=run)
b5.config(command=root.destroy)
#b6.config(command=resolve)

b1.place(x=0, y=0)
b2.place(x=130, y=0)
#b3.place(x=245, y=0)
b4.place(x=245, y=0)
b5.pack(side=TOP, anchor=E)
#b6.place(x=540, y=125)

l = Label(root, text="Введите время:")
l.place(x=370, y=5)

sv = StringVar()
Time = Entry(root, width=13, textvariable=sv)
Time.bind('<Return>', handler)
Time.place(x=375, y=30)

T = Text(root, height=5, width=60)
T.place(x=20, y=80)
T.insert(END, "Файл с параметрами: " + coef_file + 
         "\nФайл для записи результатов: " + sol_file)

canvas = FigureCanvasTkAgg(plot(), master=root)
canvas.draw()
canvas.get_tk_widget().place(x=60, y=200)

cm = matplotlib.colors.LinearSegmentedColormap.from_list("", 
    [[0.0, 0.0, 1.0],
     [0.0, 0.2, 1.0],
     [0.0, 0.4, 1.0],
     [0.0, 0.6, 0.9],
     [0.9, 0.9, 0.0],
     [1.0, 0.8, 0.0],
     [1.0, 0.6, 0.0],
     [1.0, 0.4, 0.0],
     [1.0, 0.2, 0.0],
     [1.0, 0.0, 0.0]])

canvas2 = FigureCanvasTkAgg(plot_colorbar(), master=root)
canvas2.draw()
canvas2.get_tk_widget().place(x=520, y=200)

resolve()

root.mainloop()
