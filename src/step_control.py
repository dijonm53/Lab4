"""!
@file step_control.py
Run step-response output for motor/encoder and plot the results. This program
utilizes a simple GUI with a plot in it. It uses Tkinter to display the GUI. The experiemental results
are taken from the Nucleo, which is received by the serial port. This is run multiple times to compare different gain values
set by the user

This file uses a template for the GUI, given by Dr. John Ridgely

@author mecha02
@date   20-Feb-2024 
"""

## List of imports needed to run the program
import time
import tkinter
import serial
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)


def plot_example(plot_axes, plot_canvas, xlabel, ylabel, ser, x_values, y_values, title):
    """!
    Makes two plots, the experimental and theoretical output
    @param plot_axes The plot axes supplied by Matplotlib
    @param plot_canvas The plot canvas supplied by Matplotlib
    @param xlabel The label for the plot's horizontal axis
    @param ylabel The label for the plot's vertical axis
    @param ser The data read from the serial object
    @param x_values The x-values for the step response output
    @param y_values The y-values for the step response output
    @param title The title for the graph
    """
    
    # Clears lists for data collection after run is pressed
    x_values.clear()
    y_values.clear()
    
    # Clears values grabbed by the serial
    x_value = 0
    y_value = 0
    
    # Takes/sends input from user and sends carriage return for input in main
    while True:
        try:
            inp = float(input("Set ur gain: ")) 
            inp = str(inp) + '\r\n'
            ser.reset_output_buffer()
            ser.write(inp.encode())
            break
        
        # In case the input is invalid
        except ValueError:
            print("Invalid input. Please enter a valid float value.") 

    # Add delay to step response
    time.sleep(2)
    
    while True:
        # Converts the printed statements of the output to float and puts them in lists 
        try:
            response = ser.readline().decode('utf-8').strip()
            
            # Breaks loop if 'end' is printed in main
            if response == 'end':
                break
            
            values = response.split(',')
            
            x_value = int(values[0])
            y_value = float(values[1])
            
            x_values.append(x_value)
            y_values.append(y_value)
            
        except ValueError:
            print('error')
            continue
        
        except IndexError:
            print('index')
            continue

    # Drawing the plot when Run is hit
    
    plot_axes.plot(x_values, y_values, linestyle='dashed')
    plot_axes.set_xlabel(xlabel)
    plot_axes.set_ylabel(ylabel)
    plot_axes.set_title(title)
    plot_axes.grid(True)
    plot_canvas.draw()

def tk_matplot(plot_function, xlabel, ylabel, title):
    """!
    This function receives the output from the serial port using the serial class.
    It then places the output in corresponding lists, used later for plotting. This
    function also makes the GUI window, displays it, and runs the user interface
    until the user closes the window. 
    @param plot_function The function which creates a plot
    @param xlabel The label for the plot's horizontal axis
    @param ylabel The label for the plot's vertical axis
    @param title A title for the plot
    """
    
    # Parameters for serial port
    serial_port = '/dev/tty.usbmodem2070366F394E2'  
    baud_rate = 9600
    
    # Opens serial port
    ser = serial.Serial(serial_port, baud_rate, timeout=0.5)
    
    # Initializes the lists used for plotting
    x_values = []
    y_values = []
    
    
    # Create the main program window and give it a title
    tk_root = tkinter.Tk()
    tk_root.wm_title(title)

    # Create a Matplotlib 
    fig = Figure()
    axes = fig.add_subplot()

    # Create the drawing canvas and a handy plot navigation toolbar
    canvas = FigureCanvasTkAgg(fig, master=tk_root)
    toolbar = NavigationToolbar2Tk(canvas, tk_root, pack_toolbar=False)
    toolbar.update()

    # Create the buttons that run tests, clear the screen, and exit the program
    button_quit = tkinter.Button(master=tk_root,
                                 text="Quit",
                                 command=tk_root.destroy)
    button_clear = tkinter.Button(master=tk_root,
                                  text="Clear",
                                  command=lambda: axes.clear() or canvas.draw())
    button_run = tkinter.Button(master=tk_root,
                                text="Run Test",
                                command=lambda: plot_function(axes, canvas,
                                                              xlabel, ylabel, ser, x_values, y_values, title))

                                

    # Arrange things in a grid because "pack" is weird
    canvas.get_tk_widget().grid(row=0, column=0, columnspan=3)
    toolbar.grid(row=1, column=0, columnspan=3)
    button_run.grid(row=2, column=0)
    button_clear.grid(row=2, column=1)
    button_quit.grid(row=2, column=2)

    # This function runs the program until the user decides to quit
    tkinter.mainloop()


# This main code is run if this file is the main program but won't run if this
# file is imported as a module by some other main program
if __name__ == "__main__":
    
    tk_matplot(plot_example,
               xlabel="Time (ms)",
               ylabel="Position (Encoder Count)",
               title="Step Response of Motor Control")



