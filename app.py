
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

error_plagueis = [105, 100, 32, 121, 111, 117, 32, 101, 118, 101, 114, 32, 104, 101, 97, 114, 32, 116, 104, 101, 32,
                  116, 114, 97, 103, 101, 100, 121, 32, 111, 102, 32, 68, 97, 114, 116, 104, 32, 80, 108, 97, 103,
                  117, 101, 105, 115, 32, 84, 104, 101, 32, 87, 105, 115, 101, 63, 32, 73, 32, 116, 104, 111, 117,
                  103, 104, 116, 32, 110, 111, 116, 46, 32, 73, 116, 39, 115, 32, 110, 111, 116, 32, 97, 32, 115,
                  116, 111, 114, 121, 32, 116, 104, 101, 32, 74, 101, 100, 105, 32, 119, 111, 117, 108, 100, 32,
                  116, 101, 108, 108, 32, 121, 111, 117, 46, 32, 73, 116, 115, 32, 97, 32, 83, 105, 116, 104, 32,
                  108, 101, 103, 101, 110, 100, 46, 32, 68, 97, 114, 116, 104, 32, 80, 108, 97, 103, 117, 101, 105,
                  115, 32, 119, 97, 115, 32, 97, 32, 68, 97, 114, 107, 32, 76, 111, 114, 100, 32, 111, 102, 32, 116,
                  104, 101, 32, 83, 105, 116, 104, 44, 32, 115, 111, 32, 112, 111, 119, 101, 114, 102, 117, 108, 32,
                  97, 110, 100, 32, 115, 111, 32, 119, 105, 115, 101, 32, 104, 101, 32, 99, 111, 117, 108, 100, 32,
                  117, 115, 101, 32, 116, 104, 101, 32, 70, 111, 114, 99, 101, 32, 116, 111, 32, 105, 110, 102, 108,
                  117, 101, 110, 99, 101, 32, 116, 104, 101, 32, 109, 105, 100, 105, 99, 104, 108, 111, 114, 105, 97,
                  110, 115, 32, 116, 111, 32, 99, 114, 101, 97, 116, 101, 32, 108, 105, 102, 101, 46, 32, 72, 101, 32,
                  104, 97, 100, 32, 115, 117, 99, 104, 32, 97, 32, 107, 110, 111, 119, 108, 101, 100, 103, 101, 32, 111,
                  102, 32, 116, 104, 101, 32, 100, 97, 114, 107, 32, 115, 105, 100, 101, 32, 116, 104, 97, 116, 32, 104,
                  101, 32, 99, 111, 117, 108, 100, 32, 101, 118, 101, 110, 32, 107, 101, 101, 112, 32, 116, 104, 101,
                  32, 111, 110, 101, 115, 32, 104, 101, 32, 99, 97, 114, 101, 100, 32, 97, 98, 111, 117, 116, 32, 102,
                  114, 111, 109, 32, 100, 121, 105, 110, 103, 46, 32, 84, 104, 101, 32, 100, 97, 114, 107, 32, 115, 105,
                  100, 101, 32, 111, 102, 32, 116, 104, 101, 32, 70, 111, 114, 99, 101, 32, 105, 115, 32, 97, 32, 112,
                  97, 116, 104, 119, 97, 121, 32, 116, 111, 32, 109, 97, 110, 121, 32, 97, 98, 105, 108, 105, 116, 105,
                  101, 115, 32, 115, 111, 109, 101, 32, 99, 111, 110, 115, 105, 100, 101, 114, 32, 116, 111, 32, 98,
                  101, 32, 117, 110, 110, 97, 116, 117, 114, 97, 108, 46, 32, 72, 101, 32, 98, 101, 99, 97, 109,
                  101, 32, 115, 111, 32, 112, 111, 119, 101, 114, 102, 117, 108, 32, 116, 104, 101, 32, 111, 110, 108,
                  121, 32, 116, 104, 105, 110, 103, 32, 104, 101, 32, 119, 97, 115, 32, 97, 102, 114, 97, 105, 100, 46]

# turn the flask app into a socketio app
socketio = SocketIO(app)

# random number Generator Thread
thread = Thread()
thread_stop_event = Event()
# Global Variable Declaration
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
global delayy
global data_scalar
# Initialize important global variables
# Don't expect these to change
pls_run = False  # Don't collect data off the bat
voffset = 0  # No offset for vertical or horizontal
hoffset = 0
x1_cursor = 0  # Cursors and trigger start at zero
y1_cursor = 0
x2_cursor = 0
y2_cursor = 0
trigga = 0
delayy = 1
data_scalar = 0.010045  # 2V initial vscale


class RandomThread(Thread):
    def __init__(self):
        global delayy
        self.delay = delayy
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
        print("Asking nicely for some fresh hot data if you hit start")

        vscale = 1.99  # height of window (V)
        hscale = .99  # length of window (S)

        while not thread_stop_event.isSet():
            global pls_run
            if pls_run:
                socketio.emit('big_woad', {'data':'o3o wuts this daddy'}, namespace='/test')
                self.delay = delayy

            sleep(self.delay)

    def run(self):
        self.random_number_generator()


@app.route('/')
def index():
    # only by sending this page first will the client be connected to the socketio instance
    return render_template('charts.html')


# Socket that starts the data collection on the pi's end
# data['data'] == poopy --> Run
# data['data'] == head  --> Stop
@socketio.on('bussy', namespace='/test')
def print_stuff(data):
    print('Do I need to spell it out for you?')
    print(data['data'] + " H E A D")
    global pls_run
    if data['data'] == 'poopy':
        pls_run = True
    else:
        pls_run = False


# Socket that sets the global vertical and horizontal offset values
# Vertical Offset       data = {'data':['vertical',v_offset_value]}
# Horizontal Offset     data = {'data':['horizontal',h_offset_value]}
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


# Cursors Socket - Changes values for cursors and trigger
# data = {'data':[x1, x2, y1, y2, trigger]}
# Trigger only changes value (involves UART comms) if significant change
@socketio.on('cursors', namespace='/test')
def print_stuff4(data):
    print('Its a seven inch itch cursor pls')
    print(data)
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
        scaled_trigger = trigga / data_scalar  # Divide to turn V back into -128-127
        scaled_trigger = round(scaled_trigger + 128)  # Bring it back to 0-255
        socketio.emit('trigga', {'data': scaled_trigger}, namespace='/test')
        trigga = trigger
    else:
        trigga = trigger


# Scales Socket  - Grabs the time_window or voltage_window
# If hscale (h_window (s)) is > 1 s, set the delay longer
# Else keep it 1s
# If vscale, find appropriate relay to change it to and change relays (socket to comms.py)
# Hscale -  data = {'data':['hageman', hscale]}
# Vscale -  data = {'data':['bussy', vscale]}
@socketio.on('scales', namespace='/test')
def print_stuff3(data):
    print('Uh oh, stinky')
    print(data)
    print(data['data'][0] + " H E A D")
    # Horizontal Scale
    if data['data'][0] == 'hageman':
        # Global Variable declaration
        global hscale
        global delayy
        # Window length
        hscale = float(data['data'][1])
        # If window length is longer than sampling time, change sampling time, otherwise change back to 1s
        if hscale > 1:
            delayy = hscale
        else:
            delayy = 1
        print("Hscale: " + str(hscale))
        # Calculate the new divisor and return dict with new window and divisor
        div_data = calculate_divisor(hscale)
        divisor = div_data['divisor']
        new_window = div_data['window']

        # Socket to comms.py with new divisor for sample rate
        socketio.emit('divisor', {'divisor': divisor}, namespace='/test')
        # Check for significant change, if so change the user's window length, else do nothing
        if abs(hscale - new_window >= hscale/1000):
            print("Pretty BIG change owo")
            hscale = new_window
        print("Hscale when Pi is done: " + str(hscale))

    else:
        # Vertical Scale
        global vscale
        global data_scalar
        vscale = float(data['data'][1])
        new_relay = find_relay(vscale)
        data_scalar = get_scalar_from_relay(new_relay)
        # Emit Relay Scalar to comms.py to change relays
        socketio.emit('relays', {'scalar': data_scalar}, namespace='/test')


# Socket to measure and send data to front end
# data = {'data':[512 uint8s]}
@socketio.on('big_woad2', namespace='/test')
def format_n_send(data):
    # Define constants
    samples_per_window = 256

    # Initialize Global Variables
    global data_scalar
    global trigga
    global vscale
    global hscale

    # Read raw data and convert to numpy
    sine_wave_raw = data['data']
    if sine_wave_raw == error_plagueis:
        print("SERIAL ERROR!!!")
    sine_wave_numpy = np.array(sine_wave_raw)

    # Convert horizontal offset to samples
    h_scale_offset = calculate_samples(hscale, hoffset)

    # Limit min/max of offset so that h_scale doesn't overflow
    if h_scale_offset > 127:
        h_scale_offset = 127
    elif h_scale_offset < -127:
        h_scale_offset = -127
    first_quarter = round(2*samples_per_window) * .25 - 1
    third_quarter = round(2*samples_per_window) * .75 - 1
    # Debug for offset
    print("Sample Offset: " + str(h_scale_offset))
    wave_start = int(first_quarter-h_scale_offset)
    wave_stop = int(third_quarter-h_scale_offset)

    # Get real waveform with middle 256 Bytes adjusted for by horizontal offset
    sine_wave_small = sine_wave_numpy[wave_start:wave_stop]

    # Bring down to [-127:128] from [0-255] because it's really centered around 0
    sine_wave_adjusted = sine_wave_small - 127
    # print("Reduced Sine Wave: " + str(sine_wave_adjusted))  # Debug
    # Scale down numbers to real voltage values
    sine_wave_scaled = sine_wave_adjusted * data_scalar
    # Generate time values with "0s" in the center
    # TODO: Talk to matt about this, I don't think this is right, maybe sampling_rate*samples + and -
    time_vals = np.linspace(-abs(hscale/2.0), abs(hscale/2.0), samples_per_window)
    # print(time_vals)
    # Use Vertical Offset (filthily easy software implementation)
    sine_wave_measure = sine_wave_scaled + voffset

    # Grab measurements of fully scaled data
    cursors = {'x1': x1_cursor, 'x2': x2_cursor, 'y1': y1_cursor, 'y2': y2_cursor}
    measurements = get_measurements(cursors, sine_wave_measure.tolist(), time_vals.tolist(), trigga)
    print(measurements)

    # Take measurement vals and send them to front end with 'waveform' socket
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

    socketio.emit('waveform', {'ch1': {'hscale': hscale, 'vscale': vscale, 'ch1_points': sine_wave_measure.tolist(),
                                       'time': time_vals.tolist(), 'meas': [frequency, pkpk, period,
                                                                            delta_time, delta_volt, duty, neg_duty,
                                                                            rising_cnt, falling_cnt]}
                               }, namespace='/test')


# Grabs measurements from the waveform
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
        for idx, point in enumerate(trim_waveform):
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


# The on connect Socket, starts the routine thread requests for juicy data when we want them
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

# The disconnect Socket, just prints when the client disconnected.
@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


# Function to calculate the h_scale divisor to send to the FPGA
def calculate_divisor(window_length):

    # constants
    samples_per_window = 256.0  # unit: samples
    base_sampling_freq = 25e6  # unit: Hz (1/s)
    base_period = 1.0/base_sampling_freq  # unit: s

    # Calculate Divisor
    seconds_per_sample = window_length/samples_per_window  # seconds/sample
    divisor = round(seconds_per_sample/base_period)  # Unit: unit-less, it's a scalar

    # Calculate New Window Length
    base_sampling_freq = 25e6
    base_period = 1.0/base_sampling_freq
    new_period = base_period*divisor
    new_sampling_freq = 1.0/new_period  # units = samples/sec
    # print(new_sampling_freq)
    new_window = 1.0/(new_sampling_freq/samples_per_window)

    # Format and return data
    div_dict = {'divisor': divisor, 'window': new_window}
    return div_dict


# Function to calculate how many samples a horizontal offset in seconds is
# Returns in Samples
def calculate_samples(window_length, h_offset):
    samples_per_window = 256.0  # Unit: Samples
    samples_per_sec = samples_per_window/window_length  # Unit: Samples/Sec
    sample_offset = round(h_offset * samples_per_sec)  # Unit: Samples
    return sample_offset


# Function to find the nearest relay setting

# Doesn't do use until we have the table
def find_relay(v_scale):
    percent_bad = 25
    relay_list = np.array([73.472, 64.288, 32.144, 25.7152, 18.368, 16.072, 14.6944, 12.8576, 10.28608, 7.3472, 6.4288,
                           5.14304, 3.6736, 3.2144, 2.57152, 2.057216, 1.46944, 1.28576, 0.514304])
    # V-Scale and Relay are in pkpk form
    desired_relay = (1+(percent_bad/100))*v_scale
    fitting_relay_list = relay_list[relay_list >= desired_relay]
    if fitting_relay_list.size == 0:
        print("owo it's so big!!! +-35 volts really?")
        set_relay = float(max(relay_list))
    else:
        set_relay = float(fitting_relay_list.min())
        print("Relay found: " + str(set_relay))
    return set_relay


def get_scalar_from_relay(relay):
    scalar_list = [0.287, 0.251125, 0.125563, 0.10045, 0.07175, 0.062781, 0.0574, 0.050225, 0.04018, 0.0287, 0.025113,
                   0.02009, 0.01435, 0.012556, 0.010045, 0.008036, 0.00574, 0.005023, 0.002009]
    relay_list = [73.472, 64.288, 32.144, 25.7152, 18.368, 16.072, 14.6944, 12.8576, 10.28608, 7.3472, 6.4288,
                  5.14304, 3.6736, 3.2144, 2.57152, 2.057216, 1.46944, 1.28576, 0.514304]
    relay_idx = relay_list.index(relay)
    scalar = scalar_list[relay_idx]
    return scalar


if __name__ == '__main__':
    socketio.run(app)
