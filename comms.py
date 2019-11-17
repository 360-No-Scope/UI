import socketio
import numpy as np
import math



sio = socketio.Client()


@sio.event(namespace='/test')
def connect():
    print('connection established to papa 2')
    try:
        sio.emit('offset', {'data': ['0', '0']}, namespace='/test')
        print("sent my load uwu")
    except:
        print("we're sorry")


@sio.on('big_woad',namespace='/test')
def print_data69(data):
    print("Weady for your woad chaddy daddy o3o")
    # GPIO FLip
    print("Flipper")
    # Serial Read 1024KB
    print("kisses you and lickies your necky")
    # Send Data
    # sio.emit('big_woad2', {'data':big_list}, namespace='/test')
    # Faking the data
    fake_data = genFalseData()
    sio.emit('big_woad2', {'data': fake_data}, namespace='/test')

def genFalseData():
    freq = 1 / 10  # Hz
    omega2 = 2 * np.pi * freq
    sine_wave = np.sin(omega2 * np.linspace(-10, 10, 1024))
    return sine_wave.tolist()


@sio.on('divisor', namespace='/test')
def print_data2(data):
    print("uwu dat was dewicious")
    # TODO: Send this over serial on the rpi

@sio.on('trigga', namespace='/test')
def print_data3(data):
    print("I need to be punished runs paws down your chest and bites lip")
    # TODO: Scale trigga
    # TODO: Send this over serial on the rpi

@sio.event
def disconnect():
    print('disconnected from server')


sio.connect('http://localhost:5000', namespaces=['/test'])
sio.wait()
