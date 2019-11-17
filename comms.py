import socketio

sio = socketio.Client()


@sio.event(namespace='/test')
def connect():
    print('connection established to papa 2')
    try:
        sio.emit('offset', {'data': ['0', '0']}, namespace='/test')
        print("sent my load uwu")
    except:
        print("we're sorry")


@sio.on('waveform', namespace='/test')
def print_data(data):
    print("Did we beat em cap?")
    print("data")


@sio.on('scale2', namespace='/test')
def print_data2(data):
    print("uwu dat was dewicious")


@sio.event
def disconnect():
    print('disconnected from server')


sio.connect('http://localhost:5000', namespaces=['/test'])
sio.wait()
