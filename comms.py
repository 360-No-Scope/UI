import struct
import time
import socketio
import numpy as np
import math
import serial
import gpiozero as gp

old_data = []

# DO NOT TURN TRUE UNLESS THIS IS THE PI
isPi = True

if isPi:
    ser = serial.Serial('/dev/ttyS0', 115200, timeout=None)
    print(ser.name)

    # GPIO Pins
    flipper = gp.LED("BOARD11")
    rise_fall_pin = gp.LED("BOARD13")
    fpga_single = gp.LED("BOARD21")
    test_pin = gp.LED("BOARD22")
    pi_single = gp.LED("BOARD23")

    # Relay GPIOs
    relay1 = gp.LED("BOARD27")
    relay2 = gp.LED("BOARD29")
    relay3 = gp.LED("BOARD31")
    relay4 = gp.LED("BOARD33")
    relay5 = gp.LED("BOARD35")
    relay6 = gp.LED("BOARD37")
    relay_gpios = [relay1, relay2, relay3, relay4, relay5, relay6]

    # run startup code
    flipper.off()
    test_stuff = 1  # PLACEHOLDER
else:
    print("Not running on a rpi...")

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
    global old_data
    print("Weady for your woad chaddy daddy o3o")
    if isPi:
        # GPIO FLip
        flipper.on()
        print("Flipper")
        uint8_list = []
        # Serial Read 512B
        data = ser.read(512)
        # print("kisses you and lickies your necky")
        # Format Data to be 0-255 ints not bytes types
        for item in data:
            uint8_list.append(int(item))
        mean_list = sum(uint8_list) / len(uint8_list)
        if mean_list <= 26 and old_data != []:
            old_data = uint8_list
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
    sine_wave = 223*(np.sin(omega2 * np.linspace(-1, 1, 512)))
    zero_to_ff_wave = (sine_wave[sine_wave >= 33]).round()
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
        print("Sent trigga Mr. Fuzzy Balls")
    else:
        print("Serial Not Sent (Pi: Disabled): " + '[0x66, ' + hex(trigga) + "]")


@sio.on('relays', namespace='/test')
def change_relays(data):
    # Constant Table that my sweet matt will provide
    relay_hex = [0x12, 0x1A, 0x02, 0x08, 0x10, 0x18, 0x13, 0x1B, 0x0C, 0x14, 0x01, 0x09, 0x11, 0x19,
                 0x05, 0x0D, 0x15, 0x1D, 0x25]
    scalar_list = [0.287, 0.251125, 0.125563, 0.10045, 0.07175, 0.062781, 0.0574, 0.050225, 0.04018, 0.0287, 0.025113,
                   0.02009, 0.01435, 0.012556, 0.010045, 0.008036, 0.00574, 0.005023, 0.002009]
    scalar = data['scalar']
    # Match scalar to relay value
    # Turn on/off appropriate GPIOs
    for scale in scalar_list:
        if scalar == scale:
            relay_b = relay_hex[scalar_list.index(scale)]
            if isPi:
                toggle_relay_pins(relay_b)
            else:
                print("Relay Data: " + str(relay_b))
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
