"""!
@file motor_driver.py
This file contains code which when run through Nucleo L476RG board will initialize
and run a connected motor at a desired duty cycle

@author mecha02
@date   05-Feb-2024
"""

class MotorDriver:
    """! 
    This class implements a motor driver for an ME405 kit. 
    """

    def __init__ (self, en_pin, a_pin, another_pin, timer, ch1, ch2):
        """! 
        Creates a motor driver by initializing GPIO
        pins and turning off the motor for safety. 
        @param en_pin Enable L6206 Pin
        @param a_pin L6206 Pin IN1A
        @param another_pin L6206 Pin IN2A
        @param timer Timer associated with IN1A and IN2A
        @param ch1 Timer Channel associated with IN1A
        @param ch2 Timer Channel associated with IN2A
        """
        self.en_pin = en_pin
        self.in1pin = a_pin
        self.in2pin = another_pin
        self.timer = timer
        self.ch1 = ch1
        self.ch2 = ch2

    def set_duty_cycle (self, level):
        """!
        This method sets the duty cycle to be sent
        to the motor to the given level. Positive values
        cause torque in one direction, negative values
        in the opposite direction. This is accomplished via
        an if statement that checks the sign of the level
        parameter and passes its absolute value through
        one channel and setting the other channel to 0.
        @param level A signed integer holding the duty
               cycle of the voltage sent to the motor 
        """
        # creating a variable to run a while loop to run the motor
        try:
            # check if level is negative and greater than -100
            # this is to check the sign of level, but also that
            # the duty cycle does not exceed its bounds
            if level < 0 :
                self.ch1.pulse_width_percent(0)
                # bias signal channel 2
                self.ch2.pulse_width_percent(abs(level))
            # otherwise if positive, check if level exceeds 100  
            elif level >= 0 :
                self.ch1.pulse_width_percent(abs(level))
                self.ch2.pulse_width_percent(0)
                
        # When ctrl+c/ program stops, keyboard interrupt handling
        except KeyboardInterrupt:
            self.ch1.pulse_width_percent(0)
            self.ch2.pulse_width_percent(0)
        # When non-numeral is entered error handling
        except TypeError:
            print('Set level to signed int')
            
## The following code, if not commented out and all run in a main file, would define the parameters
## passed into the motor driver class method. This code would need to be used in a separate main file
## to properly define the parameters outside of this file that is loaded into the microcontroller.

# if __name__ == "__main__":
#     en_pin = pyb.Pin(pyb.Pin.board.PA10, mode = pyb.Pin.OPEN_DRAIN, pull = pyb.Pin.PULL_UP, value = 1)
#     a_pin = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
#     another_pin = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
#     a_timer = pyb.Timer(3, freq=5000)
#     ch1 = a_timer.channel(1, pyb.Timer.PWM, pin=a_pin)
#     ch2 = a_timer.channel(2, pyb.Timer.PWM, pin=another_pin)
#     moe = MotorDriver(en_pin,a_pin,another_pin,a_timer,ch1,ch2)
#     moe.set_duty_cycle(50)