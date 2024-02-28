"""!
@file basic_tasks.py
    This file contains a demonstration program that runs some tasks, an
    inter-task shared variable, and a queue. The tasks don't really @b do
    anything; the example just shows how these elements are created and run.

@author JR Ridgely
@date   2021-Dec-15 JRR Created from the remains of previous example
@copyright (c) 2015-2021 by JR Ridgely and released under the GNU
    Public License, Version 2. 
"""

import gc
import pyb
import cotask
import task_share
import encoder_reader as enc
import motor_driver as moe
import closed_loop_controller as closed

def task1_fun(shares):
    """!
    Task which runs the first motor using a scheduler. This function is run 
    every period interval.
    @param shares A list holding the share and queue used by this task
    """
    # Get references to the share and queue which have been passed to this task
    my_share, my_queue = shares

    # Stuff copied over from last lab below
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
    controller = closed.control()
    
    # Sets gain and setpoint values and resets the encoder before running
    # the step response
    controller.set_setpoint(6900)
    controller.set_Kp(0.1)
    encoder.zero()
    
    # Running step response
    while True:
        controller.cl_loop_response(motor, encoder, controller)
        
        yield 0


def task2_fun(shares):
    """!
    Task which runs the second motor using a scheduler. This function is run 
    every period interval.
    @param shares A tuple of a share and queue from which this task gets data
    """
    # Get references to the share and queue which have been passed to this task
    the_share, the_queue = shares
    
    # Stuff copied over from last lab below
    # Code needed to initalize motor
    en_pin = pyb.Pin(pyb.Pin.board.PC1, mode = pyb.Pin.OPEN_DRAIN, pull = pyb.Pin.PULL_UP, value = 1)
    a_pin = pyb.Pin(pyb.Pin.board.PA0, pyb.Pin.OUT_PP)
    another_pin = pyb.Pin(pyb.Pin.board.PA1, pyb.Pin.OUT_PP)
    m_timer = pyb.Timer(5, freq=5000)
    chm1 = m_timer.channel(1, pyb.Timer.PWM, pin=a_pin)
    chm2 = m_timer.channel(2, pyb.Timer.PWM, pin=another_pin)
    
    # Motor Initialization done through imported MotorDriver class
    motor_2 = moe.MotorDriver(en_pin,a_pin,another_pin,m_timer,chm1,chm2)
    
    # Code needed to initialize encoder. Set 'tim' to the correct timer
    # for the pins being used.
    tim = 4
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
    encoder_2 = enc.encoder(timer,ch1,ch2)          
    
    # Initializes Motor Controller
    controller_2 = closed.control()
    
    # Sets gain and setpoint values and resets the encoder before running
    # the step response
    controller_2.set_setpoint(6900)
    controller_2.set_Kp(0.1)
    encoder_2.zero()
    
    # Running step response
    while True:
        controller_2.cl_loop_response(motor_2, encoder_2, controller_2)
        
        yield 0
    


# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":

    # Create a share and a queue to test function and diagnostic printouts
    share0 = task_share.Share('h', thread_protect=False, name="Share 0")
    q0 = task_share.Queue('L', 16, thread_protect=False, overwrite=False,
                          name="Queue 0")

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    task1 = cotask.Task(task1_fun, name="Task_1", priority=1, period=10,
                        profile=True, trace=False, shares=(share0, q0))
#     task2 = cotask.Task(task2_fun, name="Task_2", priority=2, period=50,
#                          profile=True, trace=False, shares=(share0, q0))
    cotask.task_list.append(task1)
#     cotask.task_list.append(task2)

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect()

    # Run the scheduler with the chosen scheduling algorithm. Quit if ^C pressed
    while True:
        try:
            cotask.task_list.pri_sched()
        except KeyboardInterrupt:
            break

    # Print a table of task data and a table of shared information data
    print('\n' + str (cotask.task_list))
    print(task_share.show_all())
    print(task1.get_trace())
    print('')
