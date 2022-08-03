import tkinter as tk
import tkinter.messagebox as msgbox
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
#import stepperMotor
import spectrometer



#class Controller_Connect()
class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hello Tkinter")
        self.geometry('1000x700')
        self.spec = None #using to intialize

        self.serial_var = tk.StringVar()
        self.motor_var = tk.StringVar()
        
        self.widget_creation()
        

    def widget_creation(self):
        #for serial number and device name
        padding = {'padx': 5, 'pady': 5}

        #ThorLabs Stepper Motor
        #for now lets just assume we always use the same serial number and motor name
        motor_button = tk.Button(self, text='Connect Motor', command=self.connect_motor)
        motor_button.grid(column=0, row=0, **padding)

        #Spectrometer
        spec_connect_button = tk.Button(self, text='Connect Spectrometer', command=self.connect_spec)
        spec_connect_button.grid(column=1, row=0, **padding)
        spec_disconnect_button = tk.Button(self, text='Disconnect Spectrometer', command=self.disconnect_spec)
        spec_disconnect_button.grid(column=2,row=0, **padding)

        ## Creating plot from spectrometer spectrum measurement
        test_button = tk.Button(self, text='Spectrum', command=self.graph_spectrum)
        test_button.grid(column=3, row=0, **padding)
        self.spectral_frame = tk.Frame(self)
        self.spectral_frame.grid(column=0, columnspan=2, row=1, rowspan=2, **padding)
        self.spectral_figure = plt.figure(figsize=(4,4), dpi=100)
        plt.xlabel('nice')
        self.I_vs_wavelength = self.spectral_figure.add_subplot()
        self.spectral_canvas = FigureCanvasTkAgg(self.spectral_figure, self.spectral_frame)
        self.spectral_canvas.draw()
        self.spectral_canvas.get_tk_widget().pack()
        self.spectral_toolbar = NavigationToolbar2Tk(self.spectral_canvas, self.spectral_frame)
        self.spectral_toolbar.update()
        ### Ability to chance the wavelength range
        '''
        test_frame = tk.Frame(self)
        test_frame.grid(column=2,columnspan=2,row=1,rowspan=2, **padding)
        test_fig = plt.figure(figsize=(4,4))
        plt.xlabel('bruh')
        test_sub = test_fig.add_subplot()
        test_c = FigureCanvasTkAgg(test_fig, test_frame)
        test_c.draw()
        test_c.get_tk_widget().pack()
        '''



        #Program close
        kill_button = tk.Button(self, text='Kill program', command=self.kill_it)
        kill_button.grid(column=4, row=0, **padding)



        #self.canvas.get_tk_widget().grid(column=0,row=1,**padding, )

        #toolbar = NavigationToolbar2Tk(self.canvas, self)
        #toolbar.update()
        #self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    #Motor Functions
    def connect_motor(self):
        try:
            msgbox.showinfo('umm', 'normally I would connect to the motor here')
            #stepperMotor.Controller(self.serial_var.get(), self.motor_var.get())
            #stepperMotor.Controller('26001568', 'KST101')
        except:
            msgbox.showerror('uh oh', 'Could not connect to motor')

    #Spectrometer Functions
    def connect_spec(self):
        try:
            #WARNING: change to real after done testing
            #self.spec = spectrometer.Spectrometer()
            self.spec = spectrometer.Virtual_Spectrometer()
            print(self.spec)
        except:
            msgbox.showerror('Uh Oh', 'Could not connect to spectrometer')
    def disconnect_spec(self):
        try:
            self.spec.destroy()
            self.spec = None
        except:
            msgbox.showerror('Uh Oh', 'No spectrometer to disconnect')
    def graph_spectrum(self):
        if self.spec != None:
            self.I_vs_wavelength.cla()
            wavelength, intensities = self.spec.get_both()
            self.I_vs_wavelength.plot(wavelength, intensities)
            self.spectral_canvas.draw()
        else:
            msgbox.showerror('Uh Oh', 'No spectrometer connected')
    def kill_it(self):
        self.destroy()
        #self.disconnect_spec()
        plt.close('all')

if __name__ == "__main__":
    window = Window()
    window.protocol('WM_DELETE_WINDOW', window.kill_it)
    window.mainloop()
        