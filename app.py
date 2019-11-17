
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
global trigga
pls_run = False
voffset = 0
hoffset = 0
x1_cursor = 0
y1_cursor = 0
x2_cursor = 0
y2_cursor = 0
trigga = 0
global delayy
delayy = 1

class RandomThread(Thread):
    def __init__(self):
        global delayy
        self.delay = delayy
        #TODO: Make sure this actually works
        super(RandomThread, self).__init__()

    def random_number_generator(self):

        global hscale
        global vscale
        global voffset
        global hoffset
        global trigga
        global delayy
        self.delay = delayy
        """
        Generate a random number every 1 second and emit to a socketio instance (broadcast)
        Ideally to be run in a separate thread?
        """
        # infinite loop of magical random numbers
        print("Making random numbers")
        i = 1
        freq = 1 / 10  # Hz
        omega = 2 * np.pi * freq
        vscale = .2  # V/div
        hscale = 2.5  # ms/div

        while not thread_stop_event.isSet():
            global pls_run
            if pls_run:
                socketio.emit('big_woad', {'data':'o3o wuts this daddy'}, namespace='/test')

            sleep(self.delay)

    def run(self):
        self.random_number_generator()



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
def print_stuff2(data):
    print('Do I need to spell it out for you?')
    print(data)
    print(data['data'][0] + " is having pre-marital sex. Not wavy...")
    if data['data'][0] == 'vertical':
        global voffset
        voffset = float(data['data'][1])
    else:
        global hoffset
        hoffset = float(data['data'][1])


@socketio.on('cursors', namespace='/test')
def print_stuff4(data):
    print('Do I need to spell it out for you?')
    print(data)
    print("cursors " + " is having pre-marital sex. Not wavy...")
    global x1_cursor
    global x2_cursor
    global y1_cursor
    global y2_cursor
    global trigga
    x1_cursor = float(data['data'][0])
    x2_cursor = float(data['data'][1])
    y1_cursor = float(data['data'][2])
    y2_cursor = float(data['data'][3])
    trigger = float(data['data'][4])
    if abs(trigga-trigger) > abs(trigga/1000):
        socketio.emit('trigga', {'data': trigga}, namespace='/test')
        trigga = trigger
    else:
        trigga = trigger


@socketio.on('scales', namespace='/test')
def print_stuff3(data):
    print('Uh oh, stinky')
    print(data)
    print(data['data'][0] + " H E A D")
    if data['data'][0] == 'hageman':
        global hscale
        hscale = float(data['data'][1])
        global delayy
        if hscale > 1:
            delayy = hscale
        else:
            delayy = 1
        div_data = calculate_divisor(hscale)
        divisor = div_data['divisor']
        socketio.emit('divisor', {'divisor': divisor}, namespace='/test')
        if abs(hscale - div_data['window'] >= hscale/1000):
            hscale = div_data['window']

    else:
        global vscale
        vscale = float(data['data'][1])


@socketio.on('big_woad2', namespace='/test')
def format_n_send(data):
    sine_wave_raw = data['data']
    sine_wave = np.array(sine_wave_raw)
    # TODO: Scale data according to vscale stuff
    sample_offset = calculate_samples(hscale, hoffset)
    if 767-sample_offset > 1023:
        sample_offset = -255
    elif 255-sample_offset < 0:
        sample_offset = 255
    print("Sample Offset: " + str(sample_offset))
    sine_wave = sine_wave[255-sample_offset:767-sample_offset]
    time_vals = np.linspace(-abs(hscale/2.0), abs(hscale/2.0), 512)
    sine_wave = sine_wave + voffset
    #time_vals = time_vals + hoffset
    cursors = {'x1': x1_cursor, 'x2': x2_cursor, 'y1': y1_cursor, 'y2': y2_cursor}
    measurements = get_measurements(cursors, sine_wave.tolist(), time_vals.tolist(), trigga)
    print(measurements)

    frequency = measurements['frequency']
    pkpk = measurements['pkpkvolt']
    period = measurements['period']
    if period == math.inf:
        period = 69420
    if frequency == math.inf:
        frequency = 69420
    delta_time = measurements['dt']
    delta_volt = measurements['dv']
    duty = measurements['duty']
    neg_duty = measurements['neg_duty']
    rising_cnt = measurements['rise_count']
    falling_cnt = measurements['fall_count']

    socketio.emit('waveform', {'ch1': {'hscale': hscale, 'vscale': vscale, 'ch1_points': sine_wave.tolist(),
                                       'time': time_vals.tolist(), 'meas': [frequency, pkpk, period,
                                                                            delta_time, delta_volt, duty, neg_duty,
                                                                            rising_cnt, falling_cnt]}
                               }, namespace='/test')


def get_measurements(cursors, waveform, time_values, trigger):

    x2 = cursors['x2']
    x1 = cursors['x1']
    y1 = cursors['y1']
    y2 = cursors['y2']
    if x2 == x1 and y1 == y2:
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
                        'dt': delta_time, 'dv': delta_volt, 'duty': duty, 'neg_duty': neg_duty,
                        'rise_count': rising_cnt, 'fall_count': falling_cnt}
        return measurements

    if y2 == y1:
        delta_volt = 0
    else:
        print("Daddy Hageman pls senpai notice me owo")
        if y2 >= max(waveform):
            y2_val = max(waveform)
        elif y2 <= min(waveform):
            y2_val = min(waveform)
        else:
            y2_val = min(waveform, key=lambda x: abs(x - y2))

        if y1 >= max(waveform):
            y1_val = max(waveform)
        elif y1 <= min(waveform):
            y1_val = min(waveform)
        else:
            y1_val = min(waveform, key=lambda x: abs(x - y1))

        delta_volt = abs(y2_val - y1_val)

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
        print("Daddy Hageman pls senpai notice me owo")
        x2_val = min(time_values, key=lambda x: abs(x - x2))
        x1_val = min(time_values, key=lambda x: abs(x - x1))
        x2_idx = time_values.index(x2_val)
        x1_idx = time_values.index(x1_val)
        if x1_idx == x2_idx:
            if x2_idx + 1 < time_values.__len__()-1:
                x2_idx = x2_idx + 1
            else:
                x1_idx = x1_idx - 1

        if x1_idx < x2_idx:
            trim_waveform = waveform[x1_idx:x2_idx]
            delta_time = abs(time_values[x2_idx] - time_values[x1_idx])
        else:
            trim_waveform = waveform[x2_idx:x1_idx]
            delta_time = abs(time_values[x1_idx] - time_values[x2_idx])
        pkpk = abs(max(trim_waveform) - min(trim_waveform))
        rising_cnt = 0
        falling_cnt = 0
        for idx,point in enumerate(trim_waveform):
            if idx > 0:
                prev_point = trim_waveform[idx-1]
            else:
                prev_point = point
            if prev_point < trigger:
                if point >= trigger:
                    rising_cnt = rising_cnt + 1
            elif prev_point >= trigger:
                if point < trigger:
                    falling_cnt = falling_cnt + 1
        if rising_cnt == 0:
            period = 0
            frequency = math.inf
        else:
            period = delta_time/((rising_cnt+falling_cnt)/2)
            frequency = 1/period
        trim_np = np.array(trim_waveform)
        duty = (trim_np >= trigger).sum().astype(np.int)/len(trim_waveform)
        neg_duty = 1-duty

    measurements = {'frequency': frequency, 'pkpkvolt': pkpk, 'period': period,
                    'dt': delta_time, 'dv': delta_volt, 'duty': duty, 'neg_duty': neg_duty,
                    'rise_count': rising_cnt, 'fall_count': falling_cnt}
    return measurements


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


def calculate_divisor(window_length):
    divisor = round(25e6 / (512 / window_length))
    print(divisor)
    new_window_length = 1.0/(25e6/divisor/512)
    div_dict = {'divisor': divisor, 'window': new_window_length}
    return div_dict


def calculate_samples(window_length, h_offset):
    samples_per_sec = 512.0/window_length
    sample_offset = round(h_offset*samples_per_sec)
    return sample_offset


if __name__ == '__main__':
    socketio.run(app)
