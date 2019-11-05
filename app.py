
# Start with a basic flask app webpage.
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from random import random
from time import sleep
from threading import Thread, Event
import math
import numpy as np

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

# turn the flask app into a socketio app
socketio = SocketIO(app)

# random number Generator Thread
thread = Thread()
thread_stop_event = Event()
global pls_run
global hscale
global vscale
pls_run = False


class RandomThread(Thread):
    def __init__(self):
        self.delay = 1
        super(RandomThread, self).__init__()

    def random_number_generator(self):

        global hscale
        global vscale
        """
        Generate a random number every 1 second and emit to a socketio instance (broadcast)
        Ideally to be run in a separate thread?
        """
        # infinite loop of magical random numbers
        print("Making random numbers")
        i = 1
        data_vals = []
        time_vals = []
        sampling_period = 1 / 5  # 4Khz
        start_time = -10
        curr_time = start_time
        freq = 1 / 10  # Hz
        omega = 2 * np.pi * freq
        vscale = .2  # V/div
        hscale = 2.5  # ms/div

        while not thread_stop_event.isSet():
            sine_wave = np.sin(i * omega * np.linspace(-10, 10, 400))
            sine_wave2 = 2 * sine_wave
            time_vals = np.linspace(-10, 10, 400)
            i += 1
            if i >= 6:
                i = 1
            global pls_run
            if pls_run:
                socketio.emit('waveform', {'ch1': {'hscale': hscale, 'vscale': vscale, 'ch1_points': sine_wave.tolist(),
                                               'time': time_vals.tolist()},
                                       'ch2': {'hscale': hscale, 'vscale': vscale, 'ch2_points': sine_wave2.tolist(),
                                               'time': time_vals.tolist()}}, namespace='/test')
            sleep(self.delay)

    def run(self):
        self.random_number_generator()

    def old_sine(self):
        print("Daddy Hageman")
        # amplitude = [1, 2, 3, 4, 5]
        # data_vals = []
        # time_vals = []
        # sampling_period = 1 / 5  # 4Khz
        # start_time = -10
        # curr_time = start_time
        # freq = 1/10  # Hz
        # omega = 2 * math.pi * freq
        # sin_arg = round(omega * curr_time, 2)
        # data_val = math.sin(sin_arg)
        # data_val = data_val * amplitude[i]
        # data_vals.append(data_val)
        # time_vals.append(curr_time)
        # curr_time += sampling_period
        # if curr_time > 10:
        #     curr_time = -10


@app.route('/')
def index():
    # only by sending this page first will the client be connected to the socketio instance
    return render_template('charts.html')


@socketio.on('bussy', namespace='/test')
def print_stuff(data):
    print('Do I need to spell it out for you?')
    print(data['data'] + " H E A D")
    global pls_run
    if data['data'] == 'poopy':
        pls_run = True
    else:
        pls_run = False


@socketio.on('scales', namespace='/test')
def print_stuff(data):
    print('Uh oh, stinky')
    print(data)
    print(data['data'][0] + " H E A D")
    if data['data'][0] == 'hageman':
        global hscale
        hscale = float(data['data'][1])
    else:
        global vscale
        vscale = float(data['data'][1])


@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    # Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = RandomThread()
        thread.start()


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)
