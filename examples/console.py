import argparse
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

parser = argparse.ArgumentParser(description="Simple console for PELCO")

parser.add_argument('-p', '--port',
                    dest='port',
                    help='Port CH341a',
                    default='/dev/ttyUSB1',
                    type=str)

parser.add_argument('-b', '--baud',
                    dest='baud',
                    help='baud rate camera',
                    default=2400,
                    type=int)

parser.add_argument('-a', '--address',
                    dest='address',
                    help='address camera',
                    default='01',
                    type=str)

parser.add_argument('-pr', '--protocol',
                    dest='protocol',
                    help='protocol camera',
                    default="p",
                    type=str)

parser.add_argument('-c', '--command',
                    dest='command',
                    help='command camera',
                    default='stop',
                    type=str) 
 
parser.add_argument('-do', '--delay_optics',
                    dest='delay_optics',
                    help='delay commands optics',
                    default=0.05,
                    type=float) 

parser.add_argument('-dr', '--delay_runs',
                    dest='delay_runs',
                    help='delay commands tilt and pan',
                    default=0.37,
                    type=float) 

parser.add_argument('-ts', '--dr',
                    dest='til_speed',
                    help='tilt speed set 0-64',
                    default='32',
                    type=str) 

parser.add_argument('-ps', '--pan_speed',
                    dest='pan_speed',
                    help='pan_speed set 0-64',
                    default='32',
                    type=str) 

args = parser.parse_args()
command = args.command
port = args.port
baud = args.baud
address = args.address
protocol = args.protocol
delay_optics = args.delay_optics
delay_runs = args.delay_runs
til_speed = args.til_speed
pan_speed = args.pan_speed

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



