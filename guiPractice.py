import tkinter as tk
import tkinter.messagebox as msgbox
#import stepperMotor


#class Controller_Connect()
class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hello Tkinter")
        self.geometry('900x600')

        self.serial_var = tk.StringVar()
        self.motor_var = tk.StringVar()
        self.widget_creation()
        '''
        self.name_text = tk.StringVar()

        self.label = tk.Label(self, textvar=self.label_text)
        self.label.pack(fill=tk.BOTH, expand=1, padx=100, pady=10)

        self.name_entry = tk.Entry(self, textvar=self.name_text)
        self.name_entry.pack(fill=tk.BOTH, expand=1, padx=20, pady=20)

        hello_button = tk.Button(self, text="Say Hello", command=self.say_hello)
        hello_button.pack(side=tk.LEFT, padx=(20, 0), pady=(0, 20))

        goodbye_button = tk.Button(self, text="Say Goodbye", command=self.say_goodbye)
        goodbye_button.pack(side=tk.RIGHT, padx=(0, 20), pady=(0, 20))
        '''

        #self.serial_entry = tk.Entry(self, )
    def widget_creation(self):
        #for serial number and device name
        padding = {'padx': 5, 'pady': 5}
        tk.Label(self, text='Motor Serial Number and Name:').grid(column=0, row=0, **padding)
        serial_entry = tk.Entry(self, textvariable=self.serial_var)
        serial_entry.grid(column=1,row=0, **padding)
        motor_name_entry = tk.Entry(self, textvariable=self.motor_var)
        motor_name_entry.grid(column=2, row=0, **padding)
        serial_button = tk.Button(self, text='Try connecting', command=self.connect_motor)
        serial_button.grid(column=3, row=0, **padding)
        kill_button = tk.Button(self, text='Kill program', command=self.kill_it)
        kill_button.grid(column=1, row=1, **padding)

    def connect_motor(self):
        try:
            msgbox.showinfo('umm', 'normally I would connect to the motor here')
            #stepperMotor.Controller(self.serial_var.get(), self.motor_var.get())
            #stepperMotor.Controller('26001568', 'KST101')
        except:
            msgbox.showerror('uh oh', 'Could not connect')
    '''
    def say_hello(self):
        message = "Hello there " + self.name_entry.get()
        msgbox.showinfo("Hello", message)

    def say_goodbye(self):
        if msgbox.askyesno("Close Window?", "Would you like to close this window?"):
            message = "Window will close in 2 seconds - goodybye " + self.name_entry.get()
            self.label_text.set(message)
            self.after(2000, self.destroy)
        else:
            msgbox.showinfo("Not Closing", "Great! This window will stay open.")
    '''
    def kill_it(self):
        self.destroy()

if __name__ == "__main__":
    window = Window()
    window.mainloop()
        