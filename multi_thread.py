#!/usr/bin/python
# -*- coding: utf_8 -*-

from ressources.controller import Controller
from ressources.parser import get_parameter
from multi_thread.plane_collector import PlaneCollector
from multi_thread.plane_tracker import PlaneTracker
from multi_thread.plane import Plane
from threading import Lock
import socket

rasp_ip = get_parameter('ip')
msg_port = int(get_parameter('msg_port'))

# Motor 1 pins
m1_in1 = int(get_parameter('m1_in1'))  # IN1
m1_in2 = int(get_parameter('m1_in2'))  # IN2
m1_in3 = int(get_parameter('m1_in3'))  # IN3
m1_in4 = int(get_parameter('m1_in4'))  # IN4
motor1_pins = [m1_in1, m1_in2, m1_in3, m1_in4]
controller1 = Controller(motor1_pins, rasp_ip)

# Motor 2 pins
m2_in1 = int(get_parameter('m2_in1'))  # IN1
m2_in2 = int(get_parameter('m2_in2'))  # IN2
m2_in3 = int(get_parameter('m2_in3'))  # IN3
m2_in4 = int(get_parameter('m2_in4'))   # IN4
motor2_pins = [m2_in1, m2_in2, m2_in3, m2_in4]
controller2 = Controller(motor2_pins, rasp_ip)

our_position = {
    'Latitude': float(get_parameter('our_lat')),
    'Longitude': float(get_parameter('our_lon')),
    'Altitude': int(get_parameter('our_alt'))}

closest_plane = Plane()
ip = socket.gethostbyname(rasp_ip)
port = int(get_parameter('msg_port'))
threadLock = Lock()

plane_collector = PlaneCollector(closest_plane,
                                 our_position,
                                 rasp_ip,
                                 msg_port,
                                 threadLock)

motor_thread = PlaneTracker(closest_plane,
                            our_position,
                            controller1,
                            controller2,
                            threadLock)

plane_collector.start()
motor_thread.start()

