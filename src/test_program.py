"""!
@file test_program.py
Test code for running motors with the scheduler.

@author mecha02
@date   26-Feb-2024 
"""

import gc
import cotask
import main as test

# This code creates two tasks, then starts the tasks. The
# tasks run until somebody presses Ctrl+C
if __name__ == "__main__":

    # Create the task objects
    t1 = test.task1_fun
    t2 = test.task2_fun
    
    # Create the tasks for the scheduler
    task1 = cotask.Task(t1, name="Task_1", priority=2, period=100,
                        profile=True, trace=False)
    task2 = cotask.Task(t2, name="Task_2", priority=1, period=50,
                         profile=True, trace=False)
    cotask.task_list.append(task1)
    cotask.task_list.append(task2)

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