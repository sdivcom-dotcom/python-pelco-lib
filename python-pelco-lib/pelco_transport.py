import logging
import time

import serial
#import paramiko

def write_com_command(port, baud, data, data_stop, delay):
    ser = serial.Serial(port=port, baudrate=baud)
    data_hex = bytes.fromhex(data)
    data_stop_hex = bytes.fromhex(data_stop)
    ser.write(data_hex)
    time.sleep(delay)
    ser.write(data_stop_hex)
    ser.close()


def write_com_action(port, baud, data):
    ser = serial.Serial(port=port, baudrate=baud)
    data_hex = bytes.fromhex(data)
    ser.write(data_hex)
    ser.close()
