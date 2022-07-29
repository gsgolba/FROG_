from ast import Lambda
import tkinter as tk

from setuptools import Command

def test_function(userEntry):
    print('this is %s', userEntry)

#def main():
window = tk.Tk()
frame = tk.Frame(window, bg='blue')
frame.place(relx = 0.1, rely = 0.1, relwidth=0.8, relheight=0.8)

entry = tk.Entry(frame)
entry.place(relx = 0, rely = 0, relwidth=0.3, relheight=0.3)

button = tk.Button(frame)
button.place(relx = 0.35, rely = 0, relwidth=0.3, relheight=0.3)
button.bind('<Button-1>', print('nice'))



window.mainloop()


#if __name__ == "__main__":
#    main()