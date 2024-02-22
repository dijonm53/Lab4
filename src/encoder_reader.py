"""!
@file encoder_reader.py
This file contains code that records and prints the total position rotated by the encoder,
even in cases of over- and underflow.

@author mecha02
@date   12-Feb-2024
"""

import time						# Needed to run a delay after each print statement
import motor_driver as moe		# Needed to run the motor at a set duty cycle

class encoder:
    """! 
    This class implements the necessary code to implement a motor encoder
    for an ME405 kit. 
    """
    
    def __init__(self, timer, ch1, ch2):
        """! 
        Initializes the motor encoder by initializing GPIO
        pins and setting values for variables used for tracking the
        total positiion traveled by the motor. 
        @param timer Timer associated with the chosen pins (8)
        @param ch1 Timer Channel associated with the chosen pin1 (C6)
        @param ch2 Timer Channel associated with the chosen pin2 (C7)
        """ 
        self.timer = timer
        self.ch1 = ch1
        self.ch2 = ch2
        
        # Used for tracking the total positiion traveled by the motor
        self.last_count = 0 
        self.current_count = 0
        self.change =  0
        
    def read(self):
        """!
        This method records the total position moved by the motor
        by recording the difference between the current encoder value
        and the previous value, and adding it to the total position moved.
        In cases of overflow or underflow, the total position will be added
        or subtracted by the period, respectively.
        
        @returns the current position read by the encoder to be used
        for a control loop
        """
        # Position moved between intervals
        self.change = self.timer.counter() - self.last_count
        
        # Total position moved
        self.current_count = (self.change) + self.current_count
        # Sets the previous value as the current value, for the next iteration
        self.last_count = self.timer.counter()
        
        # Checks is the position moved between intervals is high, meaning either
        # overflow or underflow
        if abs(self.change) >= 32768:
            # For overflow
            if self.change < 0:
                self.current_count += 65535 
            # For underflow    
            elif self.change >= 0:
                self.current_count -= 65535
                
        # To make sure the same encoder value does not print multiple times
        return self.current_count

           
            
    def zero(self):
        """!
        This method sets the total encoder posotion moved to zero, to
        reset the position. 
        """
        self.current_count = 0
       
# if __name__ == "__main__":
#     # Code needed to initalize motor
#     en_pin = pyb.Pin(pyb.Pin.board.PA10, mode = pyb.Pin.OPEN_DRAIN, pull = pyb.Pin.PULL_UP, value = 1)
#     a_pin = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
#     another_pin = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
#     a_timer = pyb.Timer(3, freq=5000)
#     chm1 = a_timer.channel(1, pyb.Timer.PWM, pin=a_pin)
#     chm2 = a_timer.channel(2, pyb.Timer.PWM, pin=another_pin)
    
#     # Motor Initialization done through imported MotorDriver class
#     nice = moe.MotorDriver(en_pin,a_pin,another_pin,a_timer,chm1,chm2)
    
#     # Code needed to initialize encoder. Set 'tim' to the correct timer
#     # for the pins being used.
#     tim = 8
#     timer = pyb.Timer(tim, prescaler = 0, period = 65535)
    
#     # Depending on the timer used, the code will autometically
#     # initalize the correct channel and pins. For example, if the timer
#     # used is '4', then the B6/B7 pins will be initialized. In this test code,
#     # C6/C7 is used.
#     if tim == 4:
#         ch1 = timer.channel(1,pyb.Timer.ENC_A,pin = pyb.Pin.board.PB6)
#         ch2 = timer.channel(2, pyb.Timer.ENC_B,pin = pyb.Pin.board.PB7)
    
#     elif tim == 8:
#         ch1 = timer.channel(1,pyb.Timer.ENC_A,pin = pyb.Pin.board.PC6)
#         ch2 = timer.channel(2, pyb.Timer.ENC_B,pin = pyb.Pin.board.PC7)
#     else:
#         print("invalid timer")
    
#     # Initializes Encoder
#     some = encoder(timer,ch1,ch2)
    
#     # Number of iterations used for the while loop
#     iteration = 0
    
#     # Runs the motor and reads/prints the total postition moved by the encoder.
#     # After 1000 iterations, the total position moved will be reset.
#     while True:
#         # The duty cycle set should be between 0 and 100. Positive number for
#         # clockwise rotation, and negative number for counterclockwise rotation.
#         nice.set_duty_cycle(-50)
#         some.read()
#         time.sleep(0.05)
        
#         iteration += 1
        
#         if iteration == 1000:
#             some.zero()
#             iteration = 0
