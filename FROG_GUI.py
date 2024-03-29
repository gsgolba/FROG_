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
import spectrometer
#import ThorLabsMotor
import timeit
from PIL import ImageTk, Image
import time
#from threading import Thread


SPEED_OF_LIGHT = 3e8
FEMTO_TO_SEC = 1e-15
METERS_TO_MILLI = 1e3
FEMTO_TO_MILLI = SPEED_OF_LIGHT * FEMTO_TO_SEC * METERS_TO_MILLI / 2  

#class Controller_Connect()
class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FROG")
        self.geometry('1600x850')
        #self.rowconfigure(6)
        #self.columnconfigure(6)

        #Automatic Connections
        self.spec = spectrometer.Virtual_Spectrometer() #change whether real or virtual
        #self.motor = ThorLabsMotor.Controller('26001568', 'ZST225')
        #self.motor.connect()

        self.spectral_cancel_id = None
        self.motor_cancel_id = None

        self.serial_var = tk.StringVar()
        self.motor_var = tk.StringVar()

        self.jog_size_var = tk.StringVar()
        self.jog_size_var.set('50')

        self.motor_position_entry_var = tk.StringVar()

        self.threshold_data_var = tk.StringVar()

        self.integration_var = tk.StringVar()
        self.integration_var.set('5')

        self.min_wave_var = tk.StringVar()
        self.max_wave_var = tk.StringVar()
        self.max_intens_var = tk.StringVar()
        self.min_intens_var = tk.StringVar()

        self.step_size_var = tk.StringVar()
        self.step_size_var.set('50')
        self.step_size_in_space = 0

        self.scan_width_var = tk.StringVar()
        self.scan_width_var.set('500')
        self.scan_width_in_space = 0

        self.wavelength, self.intensity = self.spec.get_both()
        self.counter = 0

        self.motor_position_label_var = tk.StringVar()
        self.motor_position_label_var.set('Position')

        self.saved_motor_position_label_var = tk.StringVar()
        self.saved_motor_position_label_var.set(self.motor.get_saved_position())

        self.has_background_subtraction = False #will be true when we run a background
        self.has_a_frog_measurement = False #same as above
        
        self.delay = 1 #in ms
        
        self.widget_creation()
        #self.spectral_reading()

        

    def widget_creation(self):
        padding = {'padx': 4, 'pady': 4}
        hw = {'height': 3, 'width': 6}

        self.control_frame = tk.Frame(self, relief='groove', **padding)
        self.control_frame.grid(column=0, row=0)
        self.spec_label = tk.Label(self.control_frame, text='FROG controls')
        self.spec_label.grid(column=0,row=0)

        #Spectrometer
  
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

        self.min_intens_entry = tk.Entry(self.control_frame, textvariable=self.min_intens_var)
        self.min_intens_entry.bind('<Return>', self.set_min_intens)
        self.min_intens_entry.grid(column=1,row=3)
        self.min_intens_label = tk.Label(self.control_frame, text='Intensity min (a.u.)')
        self.min_intens_label.grid(column=0,row=3)
    
        self.max_intens_entry = tk.Entry(self.control_frame, textvariable=self.max_intens_var)
        self.max_intens_entry.bind('<Return>', self.set_max_intens)
        self.max_intens_entry.grid(column=1,row=4)
        self.max_intens_label = tk.Label(self.control_frame, text='Intensity max (a.u.)')
        self.max_intens_label.grid(column=0,row=4)

        self.integration_entry = tk.Entry(self.control_frame, textvariable=self.integration_var)
        self.integration_entry.bind('<Return>', self.set_integration_length)
        self.integration_entry.grid(column=1,row=5)
        self.integration_label = tk.Label(self.control_frame, text='Integration time (ms)')
        self.integration_label.grid(column=0,row=5)

        self.spec_run_button = tk.Button(self.control_frame, text='Run Spec', command=self.spectral_reading)
        self.spec_run_button.grid(column=0,row=6)
        self.spec_stop_run_button = tk.Button(self.control_frame, text='Stop Run', command=self.stop_spectral_reading)
        self.spec_stop_run_button.grid(column=1,row=6)



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

        self.delay_toolbar = NavigationToolbar2Tk(self.delay_canvas, self.delay_frame)
        self.delay_toolbar.update()

        self.delay_button_frame = tk.Frame(self.delay_frame)
        self.delay_button_frame.pack(side = 'bottom', fill='x')

        self.dark_frame_adjust_button = tk.Button(self.delay_button_frame, text='Adjust for Background', command=self.adjust_with_dark_frame)
        self.dark_frame_adjust_button.pack(side='left')

        self.save_data_button = tk.Button(self.delay_button_frame, text='Save FROG Data', command=self.save_FROG_data)
        self.save_data_button.pack(side='left')


        #ThorLabs Stepper Motor
        self.motor_frame = tk.Frame(self, **padding)
        self.motor_frame.grid(column=0, row=1)

        self.step_entry = tk.Entry(self.motor_frame,textvariable=self.step_size_var)
        self.step_entry.grid(column=1, row=0)
        self.step_label = tk.Label(self.motor_frame, text='Step size (fs)')
        self.step_label.grid(column=0, row=0)

        self.scan_width_entry = tk.Entry(self.motor_frame, textvariable=self.scan_width_var)
        self.scan_width_entry.grid(column=1, row=1)
        self.scan_width_label = tk.Label(self.motor_frame, text='Delay scan width (fs)')
        self.scan_width_label.grid(column=0, row=1)

        self.jog_label = tk.Label(self.motor_frame, text='Jog size (fs)')
        self.jog_label.grid(column=0, row=2)
        self.jog_entry = tk.Entry(self.motor_frame, textvariable=self.jog_size_var)
        self.jog_entry.bind('<Return>',self.set_jog )
        self.jog_entry.grid(column=1, row=2)

        self.thershold_data_label = tk.Label(self.motor_frame, text='Threshold data (%)')
        self.thershold_data_label.grid(column=0, row=3)
        self.thershold_data_entry=tk.Entry(self.motor_frame, textvariable=self.threshold_data_var)
        self.thershold_data_entry.grid(column=1, row=3)

        self.motor_position_label = tk.Label(self.motor_frame, bg='gray', textvariable=self.motor_position_label_var)
        self.motor_position_label.grid(column=1, row=4)
        self.get_position_button = tk.Button(self.motor_frame, text='Display Position (mm)', command=self.get_motor_position)
        self.get_position_button.grid(column=0, row=4)
        
        self.motor_homing_button = tk.Button(self.motor_frame, text='Home', command=self.home)
        self.motor_homing_button.grid(column=2, row=4)

        self.motor_jogforward_button = tk.Button(self.motor_frame, text='Jog Forward', command=self.jog_forward)
        self.motor_jogforward_button.grid(column=0,row=5)

        self.motor_jogbackward_button = tk.Button(self.motor_frame, text='Jog Backward', command=self.jog_backward)
        self.motor_jogbackward_button.grid(column=1,row=5)

        self.motor_position_entry_label = tk.Label(self.motor_frame, text='Move to Position (fs)')
        self.motor_position_entry_label.grid(column=0, row=6)
        self.motor_position_entry = tk.Entry(self.motor_frame, textvariable=self.motor_position_entry_var)
        self.motor_position_entry.bind('<Return>', self.move_motor_position)
        self.motor_position_entry.grid(column=1, row=6)

        self.save_motor_position_button = tk.Button(self.motor_frame, text='Save Motor Position', command=self.save_motor_position)
        self.save_motor_position_button.grid(column=0,row=7)
        self.move_to_save_position_button = tk.Button(self.motor_frame, text='Move to Saved Position', command=self.move_to_save_position)
        self.move_to_save_position_button.grid(column=1,row=7)
        self.current_saved_position_label = tk.Label(self.motor_frame, bg ='gray', textvariable=self.saved_motor_position_label_var)
        self.current_saved_position_label.grid(column=2, row=7)
        
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
    def move_motor_position(self,event):
        try:
            converted_position = int(self.motor_position_entry_var.get()) * FEMTO_TO_MILLI
            self.motor.move_absolute(converted_position)
        except:
            print('movement did not work')
    def set_jog(self,event):
        try:
            #convert fs to mm
            converted_step = int(self.jog_size_var.get()) * FEMTO_TO_MILLI
            print(converted_step)
            self.motor.set_jog_step_size(converted_step)
        except:
            print('could not change jog size')
    def home(self):
        try: 
            self.motor.home()
        except:
            print("could not home")
    def jog_forward(self):
        try:
            self.motor.jog_forward()
            #if self.motor.is_controller_busy():
            #    self.motor.wait()
            #self.get_motor_position()
        except:
            print("could not jog forward")
    def jog_backward(self):
        try:
            self.motor.jog_backward()
            #if self.motor.is_controller_busy():
            #    self.motor.wait()
            #self.get_motor_position()
        except:
            print("could not jog backward")
    def wait_for_motor(self):
        if self.motor.is_controller_busy():
            print('wait for motor')
            time.sleep(0.5)
            self.wait_for_motor()
        print('done wait')
        return
    def save_motor_position(self):
        self.motor.save_this_motor_position()
        self.saved_motor_position_label_var.set(self.motor.get_position())

    def move_to_save_position(self):
        self.motor.move_to_saved_motor_position()
        self.wait_for_motor()


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
            down, up = self.I_vs_wavelength.get_ylim()

            if self.min_wave_var.get() != '':
                left = int(self.min_wave_var.get())
                self.I_vs_wavelength.set_xlim([left, right])
            if self.max_wave_var.get() != '':
                self.I_vs_wavelength.set_xlim([left,int(self.max_wave_var.get())])
            if self.min_intens_var.get() != '':
                down = int(self.min_intens_var.get())
                self.I_vs_wavelength.set_ylim([down, up])
            if self.max_intens_var.get() != '':
                self.I_vs_wavelength.set_ylim([down, int(self.max_intens_var.get())])        
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
    def set_max_intens(self,event):
        down,up = self.I_vs_wavelength.get_ylim()
        self.I_vs_wavelength.set_ylim([down,int(self.max_intens_var.get())])
    def set_min_intens(self,event):
        down,up = self.I_vs_wavelength.get_ylim()
        self.I_vs_wavelength.set_ylim([int(self.min_intens_var.get()), up])
    def set_integration_length(self, event):
        if self.spec != None:
            time=self.integration_entry.get()
            self.spec.change_integration_time(time)
            print('time is changed to ' + time)
            #also try to get a dark frame
            self.background_subtraction()
        else:
            msgbox.showerror('Uh Oh', 'No spectrometer connected to change integration length')
    def spectral_reading(self):
        if self.spec == None:
            self.connect_spec()
        self.graph_spectrum()
        self.spectral_cancel_id=self.after(self.delay, self.spectral_reading)
    def stop_spectral_reading(self):
        if self.spectral_cancel_id != None:
            self.after_cancel(self.spectral_cancel_id)
            self.spectral_cancel_id = None
    def background_subtraction(self):
        try:
            answer = msgbox.askyesno(title = 'Warning', message='Will measure a dark frame to account for background, is the beam blocked?')
            if answer:
                print('made new dark frame')
                self.has_background_subtraction = True
                self.dark_frame = np.array(self.spec.get_intensities())
            else:
                msgbox.showinfo(message='smh, try again')
        except:
            print('Some error in doing dark frame function')

    def delay_reading(self): #may have to delete canvas to make it go faster, possible memory leak
        if self.step_size_var.get() == '' or self.scan_width_var.get() =='' or self.jog_size_var.get() == '':
            msgbox.showerror('Uh Oh', 'Need to input step size and scan width')
        else:
            if self.counter == 0: #initialize the number of steps we need to do. And create matrix
                self.step_size_in_space = float(self.step_size_var.get()) * FEMTO_TO_MILLI
                self.scan_width_in_space = float(self.scan_width_var.get()) * FEMTO_TO_MILLI
                self.number_of_steps = int(self.scan_width_in_space / self.step_size_in_space)
                self.delay_matrix = np.zeros((len(self.spec.get_wavelengths()), 2 * self.number_of_steps + 1))
                ### at this point we should move the motor to its desired position
                self.move_to_save_position()
                self.wait_for_motor()
                # then we would start the scan on one side of the scan width. 
                # IE move motor to furthest back position
                self.motor.move_relative(-self.scan_width_in_space)
                self.wait_for_motor()


            while self.counter < 2 * self.number_of_steps + 1: 
                self.wait_for_motor()
                self.wavelength_v_delay.clear() #clear previous imshow from memory
                #print(self.counter)
                #self.wavelength = self.spec.get_wavelengths()
                self.delay_matrix[:, self.counter] = self.spec.get_intensities() #is this grabbing data at the right time?
                self.motor.move_relative(self.step_size_in_space)

                #imshow set data hasn't been working for me so I just imshow again
                self.im = self.wavelength_v_delay.imshow(self.delay_matrix, aspect ='auto', extent=[-int(self.scan_width_var.get()), int(self.scan_width_var.get()), self.wavelength[-1], self.wavelength[0]])
                self.delay_canvas.draw()
                self.update()

                self.counter += 1

            else:
                self.wait_for_motor()
                self.counter = 0
                self.motor.move_relative(-self.step_size_in_space) #go back one step because we move one extra time after measuring the last spot
                self.wavelength_v_delay.set_ylabel('Wavelength (nm)')
                self.wavelength_v_delay.set_xlabel('Delay (fs)')
                #self.wavelength_v_delay.grid(True)
                self.delay_canvas.draw()
                self.has_a_frog_measurement = True
                print('FROG done')
    def adjust_with_dark_frame(self):
        if not self.has_a_frog_measurement or not self.has_background_subtraction:
            msgbox.showerror(message='cannot adjust as either there is no FROG data or no dark frame')
        else:
            print(self.delay_matrix)
            transposed_dark_frame = self.dark_frame[:, np.newaxis]
            #print(transposed_dark_frame)
            self.delay_matrix = self.delay_matrix - transposed_dark_frame
            #print(self.delay_matrix)
            self.delay_matrix = np.where(self.delay_matrix < 0, 0, self.delay_matrix)
            print(self.delay_matrix)
            self.wavelength_v_delay.imshow(self.delay_matrix, aspect ='auto', extent=[-int(self.scan_width_var.get()), int(self.scan_width_var.get()), self.wavelength[-1], self.wavelength[0]])
            self.wavelength_v_delay.set_ylabel('Wavelength (nm)')
            self.wavelength_v_delay.set_xlabel('Delay (fs)')
            self.delay_canvas.draw()
    def adjust_with_threshold_data(self):
        #make sure to save a new matrix, in case want to threshold the old matrix again

        print('nice')
    def save_FROG_data(self):
        if not self.has_a_frog_measurement:
            msgbox.showerror(message='No FROG data to store')
        else:
            f = open('FROG_Data.txt', 'w')
            #Number of delay points
            delay_points = str(self.number_of_steps * 2 + 1)  
            f.write(delay_points + '\n')
            #Number of wavelength points
            f.write(str(len(self.wavelength)) + '\n')
            #Delay Step Size
            f.write(self.step_size_var.get() + '\n')
            #Wavelength step size
            wave_range = self.wavelength[-1] - self.wavelength[0]
            wave_step = wave_range / len(self.wavelength)
            f.write(str(wave_step) + '\n')
            #wavelength center pixel
            center_wave = self.wavelength[int(len(self.wavelength) / 2)]
            f.write(str(center_wave) + '\n')
            f.write(str(self.delay_matrix.T))
            f.close()
            #FROG data

    def kill_it(self):
        self.destroy()
        #self.disconnect_spec()
        self.disconnect_motor()
        plt.close('all')
if __name__ == "__main__":
    window = Window()
    window.protocol('WM_DELETE_WINDOW', window.kill_it)
    window.mainloop()

        