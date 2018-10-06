#!/usr/bin/python3
# -*- coding: utf_8 -*-

from multiprocessing.managers import BaseManager
from multi_process.plane_collector import PlaneCollector
from multi_process.plane_tracker import MotorManager
from multi_process.plane import Plane
from ressources.controller import Controller
from ressources.parser import get_parameter


class PlaneManager(BaseManager):
    pass


# This condition is needed (at least on Windows) for multiprocessing
if __name__ == '__main__':

    rasp_ip = get_parameter('ip')
    msg_port = int(get_parameter('msg_port'))

    # Our Position
    our_position = {
        'Latitude': float(get_parameter('our_lat')),
        'Longitude': float(get_parameter('our_lon')),
        'Altitude': int(get_parameter('our_alt'))}

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
    m2_in4 = int(get_parameter('m2_in4'))  # IN4
    motor2_pins = [m2_in1, m2_in2, m2_in3, m2_in4]
    controller2 = Controller(motor2_pins, rasp_ip)

    # Register Plane Class with PlaneManager so that we can create a "shared" plane object
    PlaneManager.register('Plane', Plane)
    plane_manager = PlaneManager()
    plane_manager.start()
    closest_plane = plane_manager.Plane()

    plane_collector = PlaneCollector(closest_plane, our_position, rasp_ip, msg_port)
    motor_manager = MotorManager(closest_plane, our_position, controller1, controller2)

    # Start the two processes
    plane_collector.start()
    motor_manager.start()

    # If this thread ends our PlaneManager will be lost, the use of join prevents this
    plane_collector.join()
    motor_manager.join()

