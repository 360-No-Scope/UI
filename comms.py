import socketio
import numpy as np
import math
import serial
import gpiozero as gp

isPi = False

if isPi:
    ser = serial.Serial('dev/ttyAMA0', 115200, timeout=1)
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
# do all the weird startup stuff

# Instantiate socketIO
sio = socketio.Client()






@sio.event(namespace='/test')
def connect():
    print('connection established to papa 2')
    try:
        sio.emit('offset', {'data': ['0', '0']}, namespace='/test')
        print("sent my load uwu")
    except:
        print("we're sorry")


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
        print("kisses you and lickies your necky")
        # Format Data to be 0-255 ints not bytes types
        uint8_list = data  # Placeholder
        # Send Data
        sio.emit('big_woad2', {'data': uint8_list}, namespace='/test')
        # Faking the data
        flipper.off()
    else:
        fake_data = gen_false_data()
        sio.emit('big_woad2', {'data': fake_data}, namespace='/test')


def gen_false_data():
    freq = 1 / 10  # Hz
    omega2 = 2 * np.pi * freq
    sine_wave = np.sin(omega2 * np.linspace(-10, 10, 512))
    return sine_wave.tolist()

def start_360noscope():
    # configure gpios for relays and whatnot
    # return true if successful, else boot up warning




@sio.on('divisor', namespace='/test')
def print_data2(data):
    print("uwu dat was dewicious")
    if isPi:
        divisor = float(data['divisor'])

        ser.write()
    # TODO: Send this over serial on the rpi


@sio.on('trigga', namespace='/test')
def print_data3(data):
    print("I need to be punished runs paws down your chest and bites lip")
    # TODO: Scale trigga
    # TODO: Send this over serial on the rpi


@sio.on('relays', namespace='/test')
def change_relays(data):

    relays = [(0x1, 25), (0x2, 50), (0x3, 69), (0x4, 69), (0x5, 69), (0x6,69)]
    scalar = data['scalar']
    # Match scalar to relay value
    # Turn on/off appropriate GPIOs
    for relay_pair in relays:
        if scalar == relay_pair[2]:
            toggle_relay_pins(relay_pair[1])


def toggle_relay_pins(relay_bits):
    for value in range(0,5,1):
        if relay_bits & (value + 1) != 0:
            relay_gpios[value].on()
        else:
            relay_gpios[value].off()





@sio.event
def disconnect():
    print('disconnected from server')


sio.connect('http://localhost:5000', namespaces=['/test'])
sio.wait()
