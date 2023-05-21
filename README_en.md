## python-pelco-lib
# Library for working with devices supporting PELCO-D and PELCO-P. 
Here is my small library for easy work with the PELCO-P and PELCO-D protocol. I will describe its main functions:
Applies to all functions!
For correct working it is required to pass the address of each camera in format "00" where zeros are numbers of camera address on the bus.
til_speed is tilt speed and should be 00 to 63. It is desirable to pass the number as int.
pan_speed is the speed on the left or right rotation axis and it should be from 00 to 63. Preferably pass the number as int.
Below are the functions for the PELCO-P protocol. commands_pelco_p.py file
Below are the functions for the PELCO-D protocol. commands_pelco_d.py file
1. pelco_p_stop(address) - stops camera movement.
2. pelco_p_tilt_up(address, til_speed) - upward camera movement.
3. pelco_p_tilt_down(address, til_speed) - downward camera movement.
4. pelco_p_tilt(address, up, down, til_speed) - camera moves down and up. 
If pass up = 1 then camera will move up. 
If pass down = 1 then camera will move downwards.
5. pelco_p_pan_left(address, pan_speed) - Move the camera to the left.
6. pelco_p_pan_pan_right(address, pan_speed) - Move the camera to the right.
7. pelco_p_pan(address, right, left, pan_speed) - Move the camera left or right. 
If you pass right = 1, the camera will move to the right.
If you pass left = 1, the camera will move to the left.
8. pelco_p_upleft(address, pan_speed, til_speed) - Move camera up and left.
9. pelco_p_upright(address, pan_speed, til_speed) - camera moves up and to the right.
10. pelco_p_down_left(address, pan_speed, til_speed) - camera movement down to the left.
11. pelco_p_down_right(address, pan_speed, til_speed) - Move camera down and to the right.
12. pelco_p_zoom_in(address) - Lens zoom moves forward.
13. pelco_p_zoom_out(address) - Lens zoom moves backwards.
14. pelco_p_focus_far(address) - lens focus moves forward.
15. pelco_p_focus_near(address) - the lens focus moves backwards.
16. pelco_d_stop(address) - stops camera movement.
17. pelco_d_tilt_up(address, til_speed) - camera motion up.
18. pelco_d_tilt_down(address, til_speed) - camera movement down.
19. pelco_d_tilt(address, up, down, til_speed) - camera movement down and up. 
If you pass up = 1 then camera will move up. 
If you pass down = 1, the camera will move down.
20. pelco_d_pan_left(address, pan_speed) - camera movement to the left.
21. pelco_d_pan_right(address, pan_speed) - camera movement to the right.
22. pelco_d_pan(address, right, left, pan_speed) - camera movement to the left or right. 
If you pass right = 1, the camera will move to the right.
If you pass left = 1, the camera will move to the left.
23. pelco_d_upleft(address, pan_speed, til_speed) - camera moves up and left.
24. pelco_d_upright(address, pan_speed, til_speed) - camera moves up and to the right.
25. pelco_d_down_left(address, pan_speed, til_speed) - camera movement down to the left.
26. pelco_d_down_right(address, pan_speed, til_speed) - camera movement down and to the right.
27. pelco_d_zoom_in(address) - Lens zoom moves forward.
28. pelco_d_zoom_out(address) - lens zoom moves backwards.
29. pelco_d_focus_far(address) - lens focus moves forward.
30. pelco_d_focus_near(address) - lens focus moves backwards.
Also we have a transport module with two functions for working with the COM port. To work with it you need to add the library pyserial
For both functions we have parameters.
Port - Here we pass the number of the COM port from the system. This is a virtual com port created in your system when you connect your usb-rs485 adapter.
baud - The baudrate for the protocol is set in the settings of the camera. Usually it is (1200, 1800, 2400, 4800, 9600).
data - command which we want to send.
data_stop is where we send the string that the stop command generated. Here is an example of it (see below).
delay - The delay between the commands in seconds.
31. write_com_command(port, baud, data, data_stop, delay) sends the command and wait for the set time interval and send the stop command. This is useful for small steps in a movement.
32. write_com_action(port, baud, data) simply sends data.
A standard example of working with the library looks like this. 
We add what we need to our program file. 
```
from commands_pelco_d import pelco_d_stop, pelco_d_tilt_up
from pelco_transport import write_com_action, write_com_command
port = "/dev/ttyUSB1"
baud = "2400"
address = "01"
delay = 1
til_speed = "32"
data = pelco_d_tilt_up(address, til_speed)
data_stop = pelco_d_stop(address)
write_com_command(port, baud, data, data_stop, delay)
```
Here we have a code which sends via COM port available at address "/dev/ttyUSB1" with baudrate 2400 a command via PELCO-D protocol to raise the lens up one second and stop the camera at address "01".