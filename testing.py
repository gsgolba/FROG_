import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import tkinter as tk
from tkinter import ttk

class My_GUI:

    def __init__(self,master):
        self.master=master
        master.title("Dashboard")
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        a.scatter([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])
        canvas1=FigureCanvasTkAgg(f,master)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side="top",fill='both',expand=True)
        canvas1.pack(side="top",fill='both',expand=True)

root=tk.Tk()
gui=My_GUI(root)
root.mainloop()