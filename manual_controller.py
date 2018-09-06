#!/usr/bin/python
# -*- coding: utf_8 -*-

import sys
from ressources.controller import Controller

rasp_pi_ip = '192.168.55.15'

# Motor 1 Pins
in1 = 12  # IN1
in2 = 16  # IN2
in3 = 20  # IN3
in4 = 21  # IN4
motor1_pins = [in1, in2, in3, in4]
controller1 = Controller(motor1_pins, rasp_pi_ip)

# Test: move motor by 90 degrees
# end_pos = controller1.get_end_pos(90)
# controller1.go_to_goal(end_pos)

# Motor 2 Pins
in2_1 = 18  # IN1
in2_2 = 17  # IN2
in2_3 = 27  # IN3
in2_4 = 22  # IN4
motor2_pins = [in2_1, in2_2, in2_3, in2_4]
controller2 = Controller(motor2_pins, rasp_pi_ip)

# Horizontal
if len(sys.argv) >= 2:
    controller1.go_to_goal(int(sys.argv[1]))

# Vertical
if len(sys.argv) >= 3:
    controller2.go_to_goal(int(sys.argv[2]))

