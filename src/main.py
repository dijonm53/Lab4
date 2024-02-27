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
import utime



def task1_fun(shares):
    """!
    Task which puts things into a share and a queue.
    @param shares A list holding the share and queue used by this task
    """
    # Get references to the share and queue which have been passed to this task
    my_share, my_queue = shares

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
    
    controller.set_setpoint()
    controller.set_Kp()
    encoder.zero()
    position = []
    
    while True:
        try:
            # Continously runs the step response with a delay of 10 ms ...
            actual = encoder.read()
            duty_cycle = controller.run(actual)
            motor.set_duty_cycle(duty_cycle)
            position.append(actual)
#             utime.sleep_ms(10)
            # ... until the set motor position is reached
            if abs(duty_cycle) <= 10:
                # Appends the current encoder value 100 times for plotting purposes
                for i in range(100):
                    position.append(actual)
#                     utime.sleep_ms(10)
                    
                # Grabs initial time
                init_time = utime.ticks_ms()
                
                # Prints time and encoder position in .CSV style format
                for i in position:
                    print(f"{utime.ticks_ms() - init_time},{i}")
                    utime.sleep_ms(9)
                
                # Prints end once the code is done running through 
                print('end')
                
                # Clears position list
                position.clear()
                utime.sleep_ms(9)
                
                # Asks for another Kp value and zeros encoder
                controller.set_Kp()
                encoder.zero()
        
        # This portion only runs the first time through
        # This makes the motor run initially
        except TypeError:
            duty_cycle = controller.run(0)
            motor.set_duty_cycle(duty_cycle)
            position.append(0)
#             utime.sleep_ms(10)


        yield 0


def task2_fun(shares):
    """!
    Task which takes things out of a queue and share and displays them.
    @param shares A tuple of a share and queue from which this task gets data
    """
    # Get references to the share and queue which have been passed to this task
    the_share, the_queue = shares

    while True:
        # Show everything currently in the queue and the value in the share
        print(f"Share: {the_share.get ()}, Queue: ", end='')
        while q0.any():
            print(f"{the_queue.get ()} ", end='')
        print('')

        yield 0


# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    print("Testing ME405 stuff in cotask.py and task_share.py\r\n"
          "Press Ctrl-C to stop and show diagnostics.")

    # Create a share and a queue to test function and diagnostic printouts
    share0 = task_share.Share('h', thread_protect=False, name="Share 0")
    q0 = task_share.Queue('L', 16, thread_protect=False, overwrite=False,
                          name="Queue 0")

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    task1 = cotask.Task(task1_fun, name="Task_1", priority=1, period=30,
                        profile=True, trace=False, shares=(share0, q0))
#     task2 = cotask.Task(task2_fun, name="Task_2", priority=2, period=5000,
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
