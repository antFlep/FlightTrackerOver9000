#!/usr/bin/python
# -*- coding: utf_8 -*-

import sys
from ressources.controller import Controller
from ressources.parser import get_parameter

rasp_ip = get_parameter('ip')

# Motor 1 pins
m1_in1 = int(get_parameter('m1_in1'))
m1_in2 = int(get_parameter('m1_in2'))
m1_in3 = int(get_parameter('m1_in3'))
m1_in4 = int(get_parameter('m1_in4'))
motor1_pins = [m1_in1, m1_in2, m1_in3, m1_in4]
controller1 = Controller(motor1_pins, rasp_ip)

# Motor 2 pins
m2_in1 = int(get_parameter('m2_in1'))
m2_in2 = int(get_parameter('m2_in2'))
m2_in3 = int(get_parameter('m2_in3'))
m2_in4 = int(get_parameter('m2_in4'))
motor2_pins = [m2_in1, m2_in2, m2_in3, m2_in4]
controller2 = Controller(motor2_pins, rasp_ip)

# Horizontal
if len(sys.argv) >= 2:
    controller1.go_to_goal(int(sys.argv[1]))

# Vertical
if len(sys.argv) >= 3:
    controller2.go_to_goal(int(sys.argv[2]))

