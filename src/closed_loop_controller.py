"""!
@file closed_loop_controller.py
This file contains code that will implement the associated motor_driver and encoder_reader .py files
for use with step_control.py to visually plot step responses with proportional gains.

@author mecha02
@date   26-Feb-2024
"""

import encoder_reader as enc
import motor_driver as moe
import utime

class control:
    """! 
    This class implements the necessary code to implement a motor controller
    for an ME405 kit. 
    """
    def __init__(self):
        """! 
        Initializes the the proportional gain and setpoint values.
        """
        self.gain = 0
        self.setpoint = 0
        
        # Used for the step response function:
        self.state = 0
        self.steady_counter = 0
        self.print_counter = 0
        self.init_time = 0
        self.position = []
    
    def set_setpoint(self, user_p):
        """! 
        Setting the setpoint to be a fixed value for repeated testing
        @param user_p gain given by whatever is calling the function
        """
        self.setpoint = user_p
  
    def set_Kp(self, user_p):
        """! 
        Function that will set the gain for the proportional control loop
        @param user_p gain given by the program
        """
        
        # Sets controller gain to user_p
        self.gain = float(user_p)
        
        # The code below was used for the previous iteration of this function, where
        # it asked the user for a gain value
        # while True:
        #     try:
        #         user_gain = input('Set ur gain:  ' )
        #         self.gain = float(user_gain)
        #         break
            
        #     # In case of values other than ints or floats
        #     except ValueError:
        #         print("Invalid input. Please enter a valid float value.")  
                
    def run(self, actual):
        """!
        Function that will be run repeatedly in the main loop to implement
        a control scheme that is a function of the current motor position,
        the desired setpoint, and the user input gain.
        @param actual the current position of the motor read by the encoder
        @returns the duty cycle to be fed into the motor driver
        """
        
        # Equation
        pwm = self.gain*(self.setpoint - actual)
        return pwm
    
    def cl_loop_response(self, motor, encoder, controller, gain):
        """!
        Function that runs the step reponse for the motor. This function
        implements a finite-state-machine and class variables to keep track of 
        what the program needs to do. Near the end of the function, the program
        prints the step response in .CSV-style format to plotting purposes.
        @param motor motor driver object running the motor
        @param encoder encoder object returning the position of the motor
        @param controller controller object responsible for runnning functions within class
        @param gain gain needed for following run
        """
        try:          
            # State 0: Step-response
            if self.state == 0:
                # Continously runs the step response with a delay of 10 ms ...
                actual = encoder.read()
                duty_cycle = controller.run(actual)
                motor.set_duty_cycle(duty_cycle)
                self.position.append(actual)
                # utime.sleep_ms(10)
            
            # ... until the set motor position is reached
                if abs(duty_cycle) <= 10:
                    # Sets next state
                    self.state += 1
                    
            # State 1: Step-Response Redundancy
            # Places the ending value of the step response 10 times
            # For cleaner plots
            elif self.state == 1:
                actual = encoder.read()
                self.position.append(actual)
                # utime.sleep_ms(10)
                
                # Counter for this state
                self.steady_counter += 1
                
                # Sets next state once counter reaches it's limit
                if self.steady_counter == 10:
                    self.state += 1
                    
                    # Grabs initial time
                    self.init_time = utime.ticks_ms()
            
            # State 2: Printing Step Response
            elif self.state == 2:                             
                # Prints time and encoder position in .CSV style format
                print(f"{utime.ticks_ms() - self.init_time},{self.position[self.print_counter]}")
                
                # Counter for this state
                # Exits when printing raises an IndexError
                self.print_counter += 1
                
                # utime.sleep_ms(9)
            
            # State 3:Ending
            elif self.state == 3: 
                # Prints end once the code is done running through 
                # Indicates to GUI when to start plotting
                print('end')
                
                # Clears position list
                self.position.clear()
                
                # Sets Kp value
#                 controller.set_Kp(gain)
                
                # Zeros outs necessary values and parameters for next run 
                # through
                encoder.zero()
                self.state = 4
                self.print_counter = 0
                self.steady_counter = 0
                
        
        # This portion only runs the first time through
        # This makes the motor run initially
        except TypeError:
            duty_cycle = controller.run(0)
            motor.set_duty_cycle(duty_cycle)
            self.position.append(0)
            # utime.sleep_ms(10)
            
        # Only runs when finished printing the step-response values
        except IndexError:
            self.state += 1
        
        # except ValueError:
        #     self.state += 1
            

if __name__ == "__main__":
    # Code needed to initalize motor
    en_pin = pyb.Pin(pyb.Pin.board.PA10, mode = pyb.Pin.OPEN_DRAIN, pull = pyb.Pin.PULL_UP, value = 1)
    a_pin = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
    another_pin = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
    m_timer = pyb.Timer(3, freq=5000)
    chm1 = m_timer.channel(1, pyb.Timer.PWM, pin=a_pin)
    chm2 = m_timer.channel(2, pyb.Timer.PWM, pin=another_pin)
    
    # Motor Initialization done through imported MotorDriver class
    motor = moe.MotorDriver(en_pin,a_pin,another_pin,m_timer,chm1,chm2)
    
    # Code needed to initialize encoder. Set 'tim' to the correct timer
    # for the pins being used.
    tim = 8
    timer = pyb.Timer(tim, prescaler = 0, period = 65535)
    
    # Depending on the timer used, the code will autometically
    # initalize the correct channel and pins. For example, if the timer
    # used is '4', then the B6/B7 pins will be initialized. In this test code,
    # C6/C7 is used.
    if tim == 4:
        ch1 = timer.channel(1,pyb.Timer.ENC_A,pin = pyb.Pin.board.PB6)
        ch2 = timer.channel(2, pyb.Timer.ENC_B,pin = pyb.Pin.board.PB7)
    
    elif tim == 8:
        ch1 = timer.channel(1,pyb.Timer.ENC_A,pin = pyb.Pin.board.PC6)
        ch2 = timer.channel(2, pyb.Timer.ENC_B,pin = pyb.Pin.board.PC7)
    else:
        print("invalid timer")
    
    # Initializes Encoder
    encoder = enc.encoder(timer,ch1,ch2)          
    
    # Initializes Motor Controller
    controller = control()
       
    controller.set_setpoint(6900)
    controller.set_Kp(0.07)
    position = []
    encoder.zero()
    
    while True:
        controller.cl_loop_response(motor, encoder, controller)
    
    # Prompts user to input a controller gain
    # Initializes variables to be used in the while loop
#     controller.set_setpoint()
#     controller.set_Kp()
#     encoder.zero()
#     position = []
#     
#     while True:
#         try:
#             # Continously runs the step response with a delay of 10 ms ...
#             actual = encoder.read()
#             duty_cycle = controller.run(actual)
#             motor.set_duty_cycle(duty_cycle)
#             position.append(actual)
#             utime.sleep_ms(10)
#             # ... until the set motor position is reached
#             if abs(duty_cycle) <= 10:
#                 # Appends the current encoder value 100 times for plotting purposes
#                 for i in range(100):
#                     position.append(actual)
#                     utime.sleep_ms(10)
#                     
#                 # Grabs initial time
#                 init_time = utime.ticks_ms()
#                 
#                 # Prints time and encoder position in .CSV style format
#                 for i in position:
#                     print(f"{utime.ticks_ms() - init_time},{i}")
#                     utime.sleep_ms(9)
#                 
#                 # Prints end once the code is done running through 
#                 print('end')
#                 
#                 # Clears position list
#                 position.clear()
#                 utime.sleep_ms(9)
#                 
#                 # Asks for another Kp value and zeros encoder
#                 controller.set_Kp()
#                 encoder.zero()
#         
#         # This portion only runs the first time through
#         # This makes the motor run initially
#         except TypeError:
#             duty_cycle = controller.run(0)
#             motor.set_duty_cycle(duty_cycle)
#             position.append(0)
#             utime.sleep_ms(10)
#             continue