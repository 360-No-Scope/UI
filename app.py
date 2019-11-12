
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
global hoffset
global voffset
global vscale
global x1_cursor
global y1_cursor
global x2_cursor
global y2_cursor
pls_run = False
voffset = 0
hoffset = 0
x1_cursor = 0
y1_cursor = 0
x2_cursor = 0
y2_cursor = 0

class RandomThread(Thread):
    def __init__(self):
        self.delay = 1
        super(RandomThread, self).__init__()

    def random_number_generator(self):

        global hscale
        global vscale
        global voffset
        global hoffset
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
            sine_wave = sine_wave + voffset
            time_vals = time_vals + hoffset
            cursors = {'x1':x1_cursor,'x2':x2_cursor,'y1':y1_cursor,'y2':y2_cursor}
            measurements = self.get_measurements(cursors, sine_wave, time_vals)
            i += 1
            if i >= 6:
                i = 1
            global pls_run
            if pls_run:
                socketio.emit('waveform', {'ch1': {'hscale': hscale, 'vscale': vscale, 'ch1_points': sine_wave.tolist(),
                                               'time': time_vals.tolist()},
                                           'mezzes':{'frequency':frequency, 'pkpkvolt':pkpk, 'period':period,
                                                     'dt':delta_time,'dv':delta_volt, 'duty':duty,'neg_duty':neg_duty
                                                     'rise_count':rising_cnt,'fall_count':falling_cnt}}, namespace='/test')
            sleep(self.delay)

    def run(self):
        self.random_number_generator()

    def get_measurements(self, cursors, sine_wave, time_vales):
        print("Daddy Hageman pls senpai notice me owo")
        x2 = cursors['x2']
        x1 = cursors['x1']
        y1 = cursors['y1']
        y2 = cursors['y2']
        if x2 ==  x1 and y1 == y2 :
            frequency = 0
            pkpk = 0
            period = math.inf
            delta_time = 0
            duty = 0
            neg_duty = 1
            rising_cnt = 0
            falling_cnt = 0
            delta_volt = 0
            measurements = {'frequency': frequency, 'pkpkvolt': pkpk, 'period': period,
                            'dt': delta_time, 'dv': delta_volt, 'duty': duty, 'neg_duty': neg_duty
                            'rise_count': rising_cnt, 'fall_count': falling_cnt}
            return measurements

        if y2 == y1:
            delta_volt = 0
        else:
            y2_val = min(sine_wave.tolist, key=lambda x: abs(x - y2))
            y1_val = min(sine_wave.tolist, key=lambda x: abs(x - y1))

        if x1 == x2:
            frequency = 0
            pkpk = 0
            period = math.inf
            delta_time = 0
            duty = 0
            neg_duty = 1
            rising_cnt = 0
            falling_cnt = 0
        else:
            # Find all this stuff

        measurements = {'frequency':frequency, 'pkpkvolt':pkpk, 'period':period,
                                                     'dt':delta_time,'dv':delta_volt, 'duty':duty,'neg_duty':neg_duty
                                                     'rise_count':rising_cnt,'fall_count':falling_cnt}
        return

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

@socketio.on('offset', namespace='/test')
def print_stuff(data):
    print('Do I need to spell it out for you?')
    print(data)
    print(data['data'][0] + " is having pre-marital sex. Not wavy...")
    if data['data'][0] == 'vertical':
        global voffset
        voffset = float(data['data'][1])
    else:
        global hoffset
        hoffset = float(data['data'][1])



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
