from flask import render_template, session, redirect, url_for, current_app, escape, Flask, Response, request, g
from .. import db
from . import api
import json
import logging
import platform
import time
import numpy as np
import os
import random
import sysparam
import serial
import shutil
import termios

logging.basicConfig(filename=sysparam.app_log_loc, format='%(asctime)s %(message)s', level=logging.DEBUG)

random.seed()

# global variables
state = {}
ser = serial.Serial(port=sysparam.port, baudrate=sysparam.baud, timeout=0)
ser.reset_input_buffer()
time.sleep(0.1)
line_counter = 0

sysparam_location = '/home/wolf/PycharmProjects/presentation/sysparam.py'


def createState():
    global state
    state = {}

    # Realtime graphs
    state['variable_one'] = {}
    state['variable_one']['time_period'] = 5
    state['variable_one']['overall_min'] = 0
    state['variable_one']['overall_max'] = 20
    state['variable_one']['data_points'] = []  # List of two-item lists

    state['variable_two'] = {}
    state['variable_two']['time_period'] = 5
    state['variable_two']['overall_min'] = -30
    state['variable_two']['overall_max'] = 30
    state['variable_two']['data_points'] = []

    state['variable_three'] = {}
    state['variable_three']['time_period'] = 5
    state['variable_three']['overall_min'] = -100
    state['variable_three']['overall_max'] = 600
    state['variable_three']['data_points'] = []

    for i in np.arange(0, 5.25, 0.25):
        state['variable_one']['data_points'].append([i, 0.0])
        state['variable_two']['data_points'].append([i, 0.0])
        state['variable_three']['data_points'].append([i, 0.0])

    return


def readValuesFromArduino():
    # Values I read from the Arduino
    # variable_one
    # variable_two
    # variable_three

    global state
    global ser
    s = str(ser.readline())
    values = s.split(',')
    print (values)
    if len(values) == 3:
        curr_variable_one = values[0][3:]
        curr_variable_two = values[1]
        curr_variable_three = values[2][:-5]

        for i in range(20):
            state['variable_one']['data_points'][i][1] = state['variable_one']['data_points'][i + 1][1]
            state['variable_two']['data_points'][i][1] = state['variable_two']['data_points'][i + 1][1]
            state['variable_three']['data_points'][i][1] = state['variable_three']['data_points'][i + 1][1]

        state['variable_one']['data_points'][20][1] = curr_variable_one
        state['variable_two']['data_points'][20][1] = curr_variable_two
        state['variable_three']['data_points'][20][1] = curr_variable_three
    return


def getCurrentReadings():
    global state
    readValuesFromArduino()

    vals = {
            'variable_one': state['variable_one'],
            'variable_two': state['variable_two'],
            'variable_three': state['variable_three'],
        }
    return vals


def readFromArduino():
    global ser
    s = str(ser.readline())
    values = s.split(',')
    print (values[0])
    print (values[1])
    print (values[2][:-2])


#################################################
#              COMMAND HANDLER                  #
#################################################

@api.route('/commandHandler', methods=['POST'])
def commandHandler():
    global state
    y = request.get_json(force=True)

    if y['command'] == 'openMain':
        x = {'responseCode': '1',
             'responseMessage': 'Success'
             }
        return json.dumps(x)

    elif y['command'] == 'openIndex':
        x = {'responseCode': '1',
             'responseMessage': 'Success'
             }
        return json.dumps(x)

    elif y['command'] == 'getCurrentReadings':
        if not state:
            createState()
        readings = getCurrentReadings()
        x = {'responseCode': '1',
             'responseMessage': 'Success',
             'data': readings}
        return json.dumps(x)

    return
