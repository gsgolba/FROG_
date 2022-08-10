import tkinter as tk
import tkinter.messagebox as msgbox
from matplotlib import image
import numpy as np
import matplotlib
from pyparsing import col
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
#import stepperMotor
import spectrometer
import ThorLabsMotor
import timeit
from PIL import ImageTk, Image


SPEED_OF_LIGHT = 3e8
FEMTO_TO_SEC = 1e-15
METERS_TO_MILLI = 1e-3

#class Controller_Connect()
class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FROG")
        self.geometry('1400x800')
        #self.rowconfigure(6)
        #self.columnconfigure(6)

        #Automatic Connections
        self.spec = spectrometer.Virtual_Spectrometer() #change whether real or virtual
        self.motor = ThorLabsMotor.Controller('26001568', 'ZST225')
        self.motor.connect()

        self.cancel_id = None
        self.serial_var = tk.StringVar()
        self.motor_var = tk.StringVar()

        self.jog_size_var = tk.StringVar()
        self.jog_size_var.set('5')
        self.jog_size_in_space = 0
        self.threshold_data_var = tk.StringVar()

        self.integration_var = tk.StringVar()
        self.integration_var.set('5')

        self.min_wave_var = tk.StringVar()
        self.max_wave_var = tk.StringVar()

        self.step_size_var = tk.StringVar()
        self.step_size_var.set('5')
        self.step_size_in_space = 0

        self.scan_width_var = tk.StringVar()
        self.scan_width_var.set('50')
        self.scan_width_in_space = 0

        self.wavelength, self.intensity = self.spec.get_both()
        self.counter = 0

        self.motor_position_label_var = tk.StringVar()
        self.motor_position_label_var.set('Position')

        
        self.delay = 1 #in ms
        
        self.widget_creation()
        #self.spectral_reading()

        

    def widget_creation(self):
        #for serial number and device name
        padding = {'padx': 4, 'pady': 4}
        hw = {'height': 3, 'width': 6}

        self.control_frame = tk.Frame(self, relief='groove', **padding)
        self.control_frame.grid(column=0, row=0)
        self.spec_label = tk.Label(self.control_frame, text='FROG controls')
        self.spec_label.grid(column=0,row=0)

        #Spectrometer
        #img = ImageTk.PhotoImage(Image.open('Frog.jpeg'))
        #self.frog_image= tk.Label(self.control_frame, image=img)
        #self.frog_image.grid(column=1, row=0)
        '''
        self.spec_connect_button = tk.Button(self.control_frame, text='Connect Spectrometer', command=self.connect_spec)
        self.spec_connect_button.pack(side = 'left', fill='both')
        self.spec_disconnect_button = tk.Button(self.control_frame, text='Disconnect Spectrometer', command=self.disconnect_spec)
        self.spec_disconnect_button.pack(side='left',fill='both')
        
        ## Creating plot from spectrometer spectrum measurement
        self.graph_button = tk.Button(self.control_frame, text='Spectrum', command=self.graph_spectrum, **hw)
        self.graph_button.pack(side='left',fill='both')
        '''
        self.spectral_frame = tk.Frame(self, **padding)
        self.spectral_frame.grid(column=2, columnspan=1, row=0, rowspan=1)
        self.spectral_figure = plt.figure(figsize=(5,5))

        self.I_vs_wavelength = self.spectral_figure.add_subplot()
        self.I_vs_wavelength.set_xlabel('Wavelength (nm)')
        self.I_vs_wavelength.set_ylabel('Intensity (a.u.)')
        self.I_vs_wavelength.grid(True)

        self.spectral_canvas = FigureCanvasTkAgg(self.spectral_figure, self.spectral_frame)
        self.spectral_canvas.draw()
        self.spectral_canvas.get_tk_widget().pack(expand=True)

        self.spectral_toolbar = NavigationToolbar2Tk(self.spectral_canvas, self.spectral_frame)
        self.spectral_toolbar.update()

        ### Ability to change the wavelength range
        
        self.min_wave_entry = tk.Entry(self.control_frame, textvariable=self.min_wave_var)
        self.min_wave_entry.bind('<Return>', self.set_min_wave)
        self.min_wave_entry.grid(column=1,row=1)
        self.min_wave_label = tk.Label(self.control_frame, text='Wavelength min (nm)')
        self.min_wave_label.grid(column=0,row=1)

        self.max_wave_entry = tk.Entry(self.control_frame, textvariable=self.max_wave_var)
        self.max_wave_entry.bind('<Return>', self.set_max_wave)
        self.max_wave_entry.grid(column=1,row=2)
        self.max_wave_label = tk.Label(self.control_frame, text='Wavelength max (nm)')
        self.max_wave_label.grid(column=0,row=2)

        self.integration_entry = tk.Entry(self.control_frame, textvariable=self.integration_var)
        self.integration_entry.bind('<Return>', self.set_integration_length)
        self.integration_entry.grid(column=1,row=3)
        self.integration_label = tk.Label(self.control_frame, text='Integration time (ms)')
        self.integration_label.grid(column=0,row=3)

        self.spec_run_button = tk.Button(self.control_frame, text='Run Spec', command=self.spectral_reading)
        self.spec_run_button.grid(column=0,row=4)
        self.spec_stop_run_button = tk.Button(self.control_frame, text='Stop Run', command=self.stop_spectral_reading)
        self.spec_stop_run_button.grid(column=1,row=4)

        #Graphing the delay
        self.delay_frame = tk.Frame(self, **padding)
        self.delay_frame.grid(column=3, columnspan=1, row=0, rowspan=1)
        self.delay_figure = plt.figure(figsize=(5,5))

        self.wavelength_v_delay = self.delay_figure.add_subplot()
        self.wavelength_v_delay.set_ylabel('Wavelength (nm)')
        self.wavelength_v_delay.set_xlabel('Delay (fs)')
        self.wavelength_v_delay.grid(True)

        self.delay_canvas = FigureCanvasTkAgg(self.delay_figure, self.delay_frame)
        self.delay_canvas.draw()
        self.delay_canvas.get_tk_widget().pack(expand=True)

        self.step_entry = tk.Entry(self.control_frame,textvariable=self.step_size_var)
        self.step_entry.grid(column=1, row=5)
        self.step_label = tk.Label(self.control_frame, text='Step size (fs)')
        self.step_label.grid(column=0, row=5)

        self.scan_width_entry = tk.Entry(self.control_frame, textvariable=self.scan_width_var)
        self.scan_width_entry.grid(column=1, row=6)
        self.scan_width_label = tk.Label(self.control_frame, text='Delay scan width (fs)')
        self.scan_width_label.grid(column=0, row=6)

        self.delay_toolbar = NavigationToolbar2Tk(self.delay_canvas, self.delay_frame)
        self.delay_toolbar.update()

        #ThorLabs Stepper Motor
        self.motor_frame = tk.Frame(self, **padding)
        self.motor_frame.grid(column=0, row=1)

        self.jog_label = tk.Label(self.motor_frame, text='Jog size (fs)')
        self.jog_label.grid(column=0, row=0)
        self.jog_entry =tk.Entry(self.motor_frame, textvariable=self.jog_size_var)
        self.jog_entry.grid(column=1, row=0)

        self.thershold_data_label = tk.Label(self.motor_frame, text='Threshold data (%)')
        self.thershold_data_label.grid(column=0, row=1)
        self.thershold_data_entry=tk.Entry(self.motor_frame, textvariable=self.threshold_data_var)
        self.thershold_data_entry.grid(column=1, row=1)

        self.motor_button = tk.Button(self.motor_frame, text='Connect Motor')#, command=self.connect_motor)
        self.motor_button.grid(column=0, row=2)

        self.motor_position_label = tk.Label(self.motor_frame, bg='gray', textvariable=self.motor_position_label_var)
        self.motor_position_label.grid(column=0, row=3)
        
        self.motor_homing_button = tk.Button(self.motor_frame, text='Home', command=self.home())
        self.motor_homing_button.grid(column=0, row=4)

        self.motor_position_button = tk.Button(self.motor_frame, text='Position', command=self.get_motor_position())
        self.motor_position_button.grid(column=0, row=5)
        
        #Program close
        self.delay_scan_button = tk.Button(self, text='FROG', command=self.delay_reading)
        self.delay_scan_button.grid(column=0,row=5)

        kill_button = tk.Button(self, text='Kill program', command=self.kill_it)
        kill_button.grid(column=0, row=6, **padding)


    #Motor Functions
    def connect_motor(self):
        try:
            msgbox.showinfo('umm', 'normally I would connect to the motor here')
        except:
            msgbox.showerror('uh oh', 'Could not connect to motor')
    def disconnect_motor(self):
        try:
            self.motor.disconnect()
        except:
            print('no motor to disconnect')
    def get_motor_position(self):
        try:
            self.motor_position_label_var.set(self.motor.get_position())
        except:
            print('position bad')
    def home(self):
        try: 
            self.motor.home()
        except:
            print("could not home")


    #Spectrometer Functions
    def connect_spec(self):
        try:
            #WARNING: change to real after done testing
            self.spec = spectrometer.Spectrometer()
            #self.spec = spectrometer.Virtual_Spectrometer()
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
            self.I_vs_wavelength.clear() #not sure what axes function wouldn't get rid of the axes labels
            #so I just write in the labels and grid lines each time we graph (definitely not optimal)
            self.wavelength, self.intensities = self.spec.get_both()
            self.I_vs_wavelength.plot(self.wavelength, self.intensities)
            self.I_vs_wavelength.set_xlabel('Wavelength (nm)')
            self.I_vs_wavelength.set_ylabel('Intensity (a.u.)')
            self.I_vs_wavelength.grid(True)

            #if we had bounds, enforce them again
            left,right = self.I_vs_wavelength.get_xlim()
            left = int(left)
            right = int(right)
            if self.min_wave_var.get() != '':
                left = int(self.min_wave_var.get())
                self.I_vs_wavelength.set_xlim([left, right])
            if self.max_wave_var.get() != '':
                self.I_vs_wavelength.set_xlim([left,int(self.max_wave_var.get())])        
            self.spectral_canvas.draw()
        else:
            msgbox.showerror('Uh Oh', 'No spectrometer connected')
    def set_min_wave(self,event): #find old bounds, and update them accordingly
        left, right = self.I_vs_wavelength.get_xlim()
        min_ = int(self.min_wave_var.get())
        self.I_vs_wavelength.set_xlim([min_,right])
        self.spectral_canvas.draw()
    def set_max_wave(self,event):
        left, right = self.I_vs_wavelength.get_xlim()
        max_ = int(self.max_wave_var.get())
        self.I_vs_wavelength.set_xlim([left,max_])
        self.spectral_canvas.draw()
    def set_integration_length(self, event):
        if self.spec != None:
            time=self.integration_entry.get()
            self.spec.change_integration_time(time)
            print('time is changed to ' + time)
        else:
            msgbox.showerror('Uh Oh', 'No spectrometer connected to change integration length')
    def spectral_reading(self):
        if self.spec == None:
            self.connect_spec()
        self.graph_spectrum()
        self.cancel_id=self.after(self.delay, self.spectral_reading)
    def stop_spectral_reading(self):
        if self.cancel_id != None:
            self.after_cancel(self.cancel_id)
            self.cancel_id = None

    def delay_reading(self): #may have to delete canvas to make it go faster, possible memory leak
        if self.step_size_var.get() == '' or self.scan_width_var.get() =='' or self.jog_size_var.get() == '':
            msgbox.showerror('Uh Oh', 'Need to input step size and scan width')
        else:
            if self.counter == 0: #initialize the number of steps we need to do. And create matrix
                self.step_size_in_space = float(self.step_size_var.get()) * SPEED_OF_LIGHT * FEMTO_TO_SEC
                self.scan_width_in_space = float(self.scan_width_var.get()) * SPEED_OF_LIGHT * FEMTO_TO_SEC
                #self.motor.set_jog_step_size(self.jog_size_in_space)
                self.number_of_steps = int(self.scan_width_in_space / self.step_size_in_space)
                self.delay_matrix = np.zeros((len(self.spec.get_wavelengths()), 2 * self.number_of_steps - 1))
                self.im = self.wavelength_v_delay.imshow(self.delay_matrix, aspect ='auto', extent=[-int(self.scan_width_var.get()), int(self.scan_width_var.get()), self.wavelength[-1], self.wavelength[0]])

            if self.counter < 2 * self.number_of_steps - 1: 
                #for item in self.delay_canvas.get_tk_widget().find_all():
                #    self.delay_canvas.get_tk_widget().delete(item)
                self.wavelength_v_delay.clear() #clear previous imshow from memory
                print(self.counter)
                self.wavelength = self.spec.get_wavelengths()
                self.delay_matrix[:, self.counter] = self.spec.get_intensities()
                #imshow set data hasn't been working for my so I just imshow again
                self.im = self.wavelength_v_delay.imshow(self.delay_matrix, aspect ='auto', extent=[-int(self.scan_width_var.get()), int(self.scan_width_var.get()), self.wavelength[-1], self.wavelength[0]])
                self.delay_canvas.draw()


                self.counter += 1
                self.after(self.delay, self.delay_reading)

            else:
                self.counter = 0
                self.wavelength_v_delay.set_ylabel('Wavelength (nm)')
                self.wavelength_v_delay.set_xlabel('Delay (fs)')
                self.wavelength_v_delay.grid(True)
                self.delay_canvas.draw()
                print('FROG done')

    def kill_it(self):
        self.destroy()
        #self.disconnect_spec()
        self.disconnect_motor()
        plt.close('all')
if __name__ == "__main__":
    window = Window()
    window.protocol('WM_DELETE_WINDOW', window.kill_it)
    window.mainloop()

        