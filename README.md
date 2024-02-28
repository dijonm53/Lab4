For this lab, we implemented a scheduler (using costask) in order to run two motors simultaneously. 
Currently, the test program runs the step response once for motor at different setpoints. However, when
running the motors continously, we noticed that motors ran depending on their priority set in the schsduler function. 
The test program ran well, as we saw no noticable hiccups or unexpected delays when running. The motor gain values were 
also set to not overshoot (for the test), and the motors didn't overshoot when run continously

When running one motor (with flywheel) through the scheduler, we toyed around with the period values to find 'best 
possible' value, or the slowest value in which it did not drastically impacted performance. Shown below is the step 
response of the period value that we thought was ideal, with a safety factor of around 10ms. We set the period to 
be 50ms

![gud](https://github.com/dijonm53/Lab4/assets/79309467/c67548a3-943c-43aa-8f59-974acb54d4c7)

When we set the period to a much higher number, the step response introduced overshoot and took longer to reach the desired
position. Shown below is a step response where we ran it at around 100 ms.

![bad](https://github.com/dijonm53/Lab4/assets/79309467/19bfb7a6-d3ae-4363-afa1-bb52761f2f68)

For these tests, we set the

