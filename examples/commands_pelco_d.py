def _checksum(command):
    checksum = 0
    for i in range(0, len(command), 2):
        byte = command[i:i+2]
        checksum += int(byte, 16)
    checksum &= 0xFF
    checksum_value = hex(checksum)[2:].upper().zfill(2)
    return checksum_value


def _set_pan_speed(param_pan_speed):
    param_pan_speed = int(param_pan_speed)
    if param_pan_speed < 0:
        param_pan_speed = 0
    elif param_pan_speed > 63:
        param_pan_speed = 63
    speed_value = hex(param_pan_speed)[2:].upper().zfill(2)
    speed_len = len(speed_value)
    if speed_len == 1:
        speed_value = speed_value + "0"
    return speed_value


def _til_speed(param_til_speed):
    param_til_speed = int(param_til_speed)
    if param_til_speed < 0:
        param_til_speed = 0
    elif param_til_speed > 63:
        param_til_speed = 63
    speed_value = hex(param_til_speed)[2:].upper().zfill(2)
    speed_len = len(speed_value)
    if speed_len == 1:
        speed_value = speed_value + "0"
    return speed_value


def _collect_message(address, data_1_2, pan_speed, til_speed):
    start_byte = "FF"
    address = str(address)
    data_1_2 = str(data_1_2)
    pan_speed = str(pan_speed)
    til_speed = str(til_speed)
    if not address:
        print("The variable 'address' blank")
    if not data_1_2:
        print("The variable 'data_1' blank")
    if not pan_speed:
        print("The variable 'pan_speed' blank")
    if not til_speed:
        print("The variable 'til_speed' blank")
    message_without_checksum = address + data_1_2 + pan_speed + til_speed
    check = _checksum(message_without_checksum)
    message = start_byte + message_without_checksum + check
    return message


def _two_zeros():
    zeros = "00"
    return zeros


def pelco_d_stop(address):
    pan_speed_value = _two_zeros()
    til_speed_value = _two_zeros()
    data_1_2_hex = "0000"
    message_action = _collect_message(address, data_1_2_hex,
                                      pan_speed_value, til_speed_value)
    return message_action


def pelco_d_tilt_up(address, til_speed):
    data_1_2_hex = "0008"
    pan_speed = _two_zeros()
    til_speed = _til_speed(til_speed)
    message_action = _collect_message(address, data_1_2_hex,
                                      pan_speed, til_speed)
    return message_action

def pelco_d_tilt_down(address, til_speed):
    data_1_2_hex = "0010"
    pan_speed = _two_zeros()
    til_speed = _til_speed(til_speed)
    message_action = _collect_message(address, data_1_2_hex,
                                      pan_speed, til_speed)
    return message_action


def pelco_d_tilt(address, up, down, til_speed):
    pan_speed = _two_zeros()
    til_speed = _til_speed(til_speed)
    if up == 1:
        message_action = pelco_d_tilt_up(address, pan_speed, til_speed)
    elif down == 1:
        message_action = pelco_d_tilt_down(address, pan_speed, til_speed)
    elif up == 0:
        message_action = pelco_d_stop(address)
    elif down == 0:
        message_action = pelco_d_stop(address)
    else:
        message_action = pelco_d_stop(address)
    return message_action


def pelco_d_pan_left(address, pan_speed):
    data_1_2_hex = "0004"
    pan_speed = _set_pan_speed(pan_speed)
    til_speed = _two_zeros()
    message_action = _collect_message(address, data_1_2_hex,
                                      pan_speed, til_speed)
    return message_action


def pelco_d_pan_right(address, pan_speed):
    data_1_2_hex = "0002"
    pan_speed = _set_pan_speed(pan_speed)
    til_speed = _two_zeros()
    message_action = _collect_message(address, data_1_2_hex,
                                      pan_speed, til_speed)
    return message_action


def pelco_d_pan(address, right, left, pan_speed):
    pan_speed = _set_pan_speed(pan_speed)
    til_speed = _two_zeros()
    if right == 1:
        message_action = pelco_d_pan_right(address, pan_speed, til_speed)
    elif left == 1:
        message_action = pelco_d_pan_left(address, pan_speed, til_speed)
    elif right == 0:
        message_action = pelco_d_stop(address)
    elif left == 0:
        message_action = pelco_d_stop(address)
    else:
        message_action = pelco_d_stop(address)
    return message_action


def pelco_d_upleft(address, pan_speed, til_speed):
    data_1_2_hex = "000C"
    pan_speed = _set_pan_speed(pan_speed)
    til_speed = _til_speed(til_speed)
    message_action = _collect_message(address, data_1_2_hex,
                                      pan_speed, til_speed)
    return message_action


def pelco_d_upright(address, pan_speed, til_speed):
    data_1_2_hex = "000A"
    pan_speed = _set_pan_speed(pan_speed)
    til_speed = _til_speed(til_speed)
    message_action = _collect_message(address, data_1_2_hex,
                                      pan_speed, til_speed)
    return message_action


def pelco_d_down_left(address, pan_speed, til_speed):
    data_1_2_hex = "0014"
    pan_speed = _set_pan_speed(pan_speed)
    til_speed = _til_speed(til_speed)
    message_action = _collect_message(address, data_1_2_hex,
                                      pan_speed, til_speed)
    return message_action


def pelco_d_down_right(address, pan_speed, til_speed):
    data_1_2_hex = "0012"
    pan_speed = _set_pan_speed(pan_speed)
    til_speed = _til_speed(til_speed)
    message_action = _collect_message(address, data_1_2_hex,
                                      pan_speed, til_speed)
    return message_action


def pelco_d_zoom_in(address):
    data_1_2_hex = "0020"
    pan_speed = _two_zeros()
    til_speed = _two_zeros()
    message_action = _collect_message(address, data_1_2_hex,
                                      pan_speed, til_speed)
    return message_action


def pelco_d_zoom_out(address):
    data_1_2_hex = "0040"
    pan_speed = _two_zeros()
    til_speed = _two_zeros()
    message_action = _collect_message(address, data_1_2_hex,
                                      pan_speed, til_speed)
    return message_action


def pelco_d_focus_far(address):
    data_1_2_hex = "0080"
    pan_speed = _two_zeros()
    til_speed = _two_zeros()
    message_action = _collect_message(address, data_1_2_hex,
                                      pan_speed, til_speed)
    return message_action


def pelco_d_focus_near(address):
    data_1_2_hex = "0100"
    pan_speed = _two_zeros()
    til_speed = _two_zeros()
    message_action = _collect_message(address, data_1_2_hex,
                                      pan_speed, til_speed)
    return message_action

if __name__ == '__main__':
    pass
