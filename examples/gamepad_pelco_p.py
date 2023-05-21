import hid
import time

from commands_pelco_p import pelco_p_stop, pelco_p_tilt_up
from commands_pelco_p import pelco_p_tilt_down, pelco_p_pan_left
from commands_pelco_p import pelco_p_pan_right, pelco_p_zoom_in
from commands_pelco_p import pelco_p_zoom_out, pelco_p_focus_far 
from commands_pelco_p import pelco_p_focus_near
from pelco_transport import write_com_action, write_com_command

port = "/dev/ttyUSB0"
baud = "2400"
address = "01"
protocol = "p"
delay_runs = 1
til_speed = "32"
pan_speed = "32"

#0x0079:0x0011
for device in hid.enumerate():
    print(f"0x{device['vendor_id']:04x}:0x{device['product_id']:04x} {device['product_string']}")

gamepad = hid.device()
gamepad.open(0x0079, 0x0011)
gamepad.set_nonblocking(True)
while True:
    report = gamepad.read(16)
    if report:
        #print(report)
        if report[3] == 0:
            print("left")
            stop = pelco_p_stop(address)
            data = pelco_p_pan_left(address, pan_speed)
            write_com_command(port, baud, data, stop, delay_runs)
        elif report[3] == 255:
            print("right")
            stop = pelco_p_stop(address)
            data = pelco_p_pan_right(address, pan_speed)
            write_com_command(port, baud, data, stop, delay_runs)
        elif report[4] == 0:
            print("up")
            stop = pelco_p_stop(address)
            data = pelco_p_tilt_up(address, til_speed)
            write_com_command(port, baud, data, stop, delay_runs)
        elif report[4] == 255:
            print("down")
            stop = pelco_p_stop(address)
            data = pelco_p_tilt_down(address, til_speed)
            write_com_command(port, baud, data, stop, delay_runs)
        else:
            pass