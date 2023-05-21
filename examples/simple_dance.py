#LEFT-RIGHT-UP-DOWN-ZOOM PLUS-MINUS
from commands_pelco_d import pelco_d_stop, pelco_d_tilt_up
from commands_pelco_d import pelco_d_tilt_down, pelco_d_pan_left
from commands_pelco_d import pelco_d_pan_right, pelco_d_zoom_in
from commands_pelco_d import pelco_d_zoom_out, pelco_d_focus_far 
from commands_pelco_d import pelco_d_focus_near
from commands_pelco_p import pelco_p_stop, pelco_p_tilt_up
from commands_pelco_p import pelco_p_tilt_down, pelco_p_pan_left
from commands_pelco_p import pelco_p_pan_right, pelco_p_zoom_in
from commands_pelco_p import pelco_p_zoom_out, pelco_p_focus_far 
from commands_pelco_p import pelco_p_focus_near
from pelco_transport import write_com_action, write_com_command

print("Enter the command:")
command = input()
port = "/dev/ttyUSB1"
baud = "2400"
address = "01"
protocol = "p"
delay_optics = 0.05
delay_runs = 1
til_speed = "32"
pan_speed = "32"


if command == "up":
    if protocol == "d":
        stop = pelco_d_stop(address)
        data = pelco_d_tilt_up(address, til_speed)
        write_com_command(port, baud, data, stop, delay_runs)
    elif protocol == "p":
        stop = pelco_p_stop(address)
        data = pelco_p_tilt_up(address, til_speed)
        write_com_command(port, baud, data, stop, delay_runs)
    else:
        pass


elif command == "down":
    if protocol == "d":
        stop = pelco_d_stop(address)
        data = pelco_d_tilt_down(address, til_speed)
        write_com_command(port, baud, data, stop, delay_runs)
    elif protocol == "p":
        stop = pelco_p_stop(address)
        data = pelco_p_tilt_down(address, til_speed)
        write_com_command(port, baud, data, stop, delay_runs)
    else:
        pass

elif command == "right":
    if protocol == "d":
        stop = pelco_d_stop(address)
        data = pelco_d_pan_right(address, pan_speed)
        write_com_command(port, baud, data, stop, delay_runs)
    elif protocol == "p":
        stop = pelco_p_stop(address)
        data = pelco_p_pan_right(address, pan_speed)
        write_com_command(port, baud, data, stop, delay_runs)
    else:
        pass

elif command == "left":
    if protocol == "d":
        stop = pelco_d_stop(address)
        data = pelco_d_pan_left(address, pan_speed)
        write_com_command(port, baud, data, stop, delay_runs)
    elif protocol == "p":
        stop = pelco_p_stop(address)
        data = pelco_p_pan_left(address, pan_speed)
        write_com_command(port, baud, data, stop, delay_runs)
    else:
        pass

elif command == "zoom_plus":
    if protocol == "d":
        stop = pelco_d_stop(address)
        data = pelco_d_zoom_in(address)
        write_com_command(port, baud, data, stop, delay_optics)
    elif protocol == "p":
        stop = pelco_p_stop(address)
        data = pelco_p_zoom_in(address)
        write_com_command(port, baud, data, stop, delay_optics)
    else:
        pass


elif command == "zoom_minus":
    if protocol == "d":
        stop = pelco_d_stop(address)
        data = pelco_d_zoom_out(address)
        write_com_command(port, baud, data, stop, delay_optics)
    elif protocol == "p":
        stop = pelco_p_stop(address)
        data = pelco_p_zoom_out(address)
        write_com_command(port, baud, data, stop, delay_optics)
    else:
        pass


elif command == "focus_plus":
    if protocol == "d":
        stop = pelco_d_stop(address)
        data = pelco_d_focus_far(address)
        write_com_command(port, baud, data, stop, delay_optics)
    elif protocol == "p":
        stop = pelco_p_stop(address)
        data = pelco_p_focus_far(address)
        write_com_command(port, baud, data, stop, delay_optics)
    else:
        pass


elif command == "focus_minus":
    if protocol == "d":
        stop = pelco_d_stop(address)
        data = pelco_d_focus_near(address)
        write_com_command(port, baud, data, stop, delay_optics)
    elif protocol == "p":
        stop = pelco_p_stop(address)
        data = pelco_p_focus_near(address)
        write_com_command(port, baud, data, stop, delay_optics)
    else:
        pass

elif command == "stop":
    if protocol == "d":
        stop = pelco_d_stop(address)
        write_com_action(port, baud, stop)
    elif protocol == "p":
        stop = pelco_p_stop(address)
        write_com_action(port, baud, stop)
    else:
        pass

else:
    print("Not command")
