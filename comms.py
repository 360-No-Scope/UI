import struct

import socketio
import numpy as np
import math
import serial
import gpiozero as gp

# DO NOT TURN TRUE UNLESS THIS IS THE PI
isPi = False

if isPi:
    ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)
    print(ser.name)

    # GPIO Pins
    flipper = gp.LED("BOARD11")
    rise_fall_pin = gp.LED("BOARD13")
    fpga_single = gp.LED("BOARD21")
    test_pin = gp.LED("BOARD22")
    pi_single = gp.LED("BOARD23")

    # Relay GPIOs
    relay1 = gp.LED("BOARD_27")
    relay2 = gp.LED("BOARD_29")
    relay3 = gp.LED("BOARD_31")
    relay4 = gp.LED("BOARD_33")
    relay5 = gp.LED("BOARD_35")
    relay6 = gp.LED("BOARD_37")
    relay_gpios = [relay1, relay2, relay3, relay4, relay5, relay6]

else:
    print("Not running on a rpi...")

if isPi:
    # do all the weird startup stuff
    # run startup code
    test_stuff = 1  # PLACEHOLDER

# Instantiate socketIO
sio = socketio.Client()

# I have offsets on the connect, this works so removing
@sio.event(namespace='/test')
def connect():
    print('connection established to papa 2')


# So future me doesn't forget this, this is the main data driver of your comms.py file
# It reads the 512 bytes from serial, processes the bytes, and then moves on
@sio.on('big_woad', namespace='/test')
def print_data69(data):
    print("Weady for your woad chaddy daddy o3o")
    if isPi:
        # GPIO FLip
        flipper.on()
        print("Flipper")
        # Serial Read 1024KB
        try:
            data = ser.read(512)
        except:
            print("punish me daddy~ nyea~")
        # print("kisses you and lickies your necky")
        # Format Data to be 0-255 ints not bytes types
        uint8_list = data  # Placeholder TODO: Find out the datatype of data and convert!
        # Send Data
        sio.emit('big_woad2', {'data': uint8_list}, namespace='/test')
        flipper.off()
    else:
        # Fake data, heavily important if we need to fake our project
        fake_data = gen_false_data()
        # print(fake_data)
        sio.emit('big_woad2', {'data': fake_data}, namespace='/test')


def gen_false_data():
    freq = 10  # Hz
    omega2 = 2 * np.pi * freq
    sine_wave = 255*(np.sin(omega2 * np.linspace(-1, 1, 512)))
    zero_to_ff_wave = (sine_wave[sine_wave >= 0]).round()
    fake_array = []
    for item in zero_to_ff_wave.tolist():
        fake_array.append(item)
        fake_array.append(item)
    rounded_array = [int(round(n, 0)) for n in fake_array]
    return rounded_array


def start_360noscope():
    placeholder = "placeholder"
    # configure gpios for relays and whatnot
    # return true if successful, else boot up warning


@sio.on('divisor', namespace='/test')
def print_data2(data):
    print("uwu dat was dewicious")
    divisor = int(data['divisor'])
    # Extract bytes from divisor
    int_to_four_bytes = struct.Struct('<I').pack
    y1, y2, y3, y4 = int_to_four_bytes(divisor & 0xFFFFFFFF)
    bytes_list = [y4, y3, y2, y1]
    if isPi:
        ser.write(0x69)
        for byte in bytes_list:
            ser.write(byte)
    else:
        print("Divisor: " + str(divisor))
        print("Divisor Bytes: ")
        for byte in bytes_list:
            print(hex(byte) + " ")


@sio.on('trigga', namespace='/test')
def print_data3(data):
    print("I need to be punished runs paws down your chest and bites lip")
    trigga = data['data']
    if trigga > 255:
        trigga = 255
    elif trigga < 1:
        trigga = 1

    if isPi:
        ser.write(0x66)
        ser.write(trigga)
    else:
        print("Serial Not Sent (Pi: Disabled): " + '[0x66, ' + hex(trigga) + "]")
    # TODO: Scale trigga do that on the other side?


@sio.on('relays', namespace='/test')
def change_relays(data):
    # Constant Table that my sweet matt will provide
    relays = [(0x1, 25), (0x2, 50), (0x3, 69), (0x4, 69), (0x5, 69), (0x6, 69)]  #TODO: Fill with hex_val divisor pairs
    scalar = data['scalar']
    # Match scalar to relay value
    # Turn on/off appropriate GPIOs
    for relay_pair in relays:
        if scalar == relay_pair[2]:
            if isPi:
                toggle_relay_pins(relay_pair[1])
            else:
                print("Relay Data" + str(relay_pair))
            break


def toggle_relay_pins(relay_bits):
    if isPi:
        for value in range(0, 5, 1):
            if relay_bits & (value + 1) != 0:
                relay_gpios[value].on()
            else:
                relay_gpios[value].off()


@sio.event
def disconnect():
    print('disconnected from server')


sio.connect('http://localhost:5000', namespaces=['/test'])
sio.wait()
