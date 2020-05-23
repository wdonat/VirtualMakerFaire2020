import sysparam
import serial
import os
import time

ser = serial.Serial(port=sysparam.port, baudrate=sysparam.baud, timeout=0)
ser.reset_input_buffer()

curr_variable_one = 0
curr_variable_two = 0
curr_variable_three = 0

last_variable_one = 0
last_variable_two = 0
last_variable_three = 0


def readValuesFromArduino():
    # Values I read from the Arduino
    # variable_one
    # variable_two
    # variable_three
    global curr_variable_one
    global curr_variable_two
    global curr_variable_three
    global last_variable_one
    global last_variable_two
    global last_variable_three
    global ser

    s = str(ser.readline())
    values = s.split(',')
    if len(values) == 3:
        curr_variable_one = values[0]
        curr_variable_two = values[1]
        curr_variable_three = values[2][:-2]
        last_variable_one = curr_variable_one
        last_variable_two = curr_variable_two
        last_variable_three = curr_variable_three

    else:
        curr_variable_one = last_variable_one
        curr_variable_two = last_variable_two
        curr_variable_three = last_variable_three

    return [curr_variable_one, curr_variable_two, curr_variable_three]


while 1:
    x = readValuesFromArduino()
    os.system('clear')
    print 'Var One:   ', x[0]
    print 'Var Two:   ', x[1]
    print 'Var Three: ', x[2]
    time.sleep(0.5)

