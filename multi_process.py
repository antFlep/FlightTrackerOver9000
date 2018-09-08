#!/usr/bin/python
# -*- coding: utf_8 -*-
from multiprocessing.managers import BaseManager

from multi_process.plane_collector import PlaneCollector
from multi_process.motor_manager import MotorManager
from multi_process.plane import Plane

from ressources.controller import Controller


class PlaneManager(BaseManager):
    pass


if __name__ == '__main__':

    rasp_ip = '192.168.55.20'

    our_position = {
        'Latitude': 49.486617,
        'Longitude': 6.034665,
        'Altitude': 0}

    # Motor 1 pins
    in1 = 12  # IN1
    in2 = 16  # IN2
    in3 = 20  # IN3
    in4 = 21  # IN4
    motor1_pins = [in1, in2, in3, in4]
    controller1 = Controller(motor1_pins, rasp_ip)

    # Motor 2 pins
    in2_1 = 18  # IN1
    in2_2 = 17  # IN2
    in2_3 = 27  # IN3
    in2_4 = 22  # IN4
    motor2_pins = [in2_1, in2_2, in2_3, in2_4]
    controller2 = Controller(motor2_pins, rasp_ip)

    PlaneManager.register('Plane', Plane)

    plane_manager = PlaneManager()
    plane_manager.start()

    # freeze_support()
    closest_plane = plane_manager.Plane()

    # plane_collector = PlaneCollector(closest_plane, rasp_ip, our_position)
    motor_manager = MotorManager(closest_plane, our_position, controller1, controller2)

    # plane_collector.start()
    motor_manager.start()

    # If this thread ends our PlaneManager will be lost, the use of join prevents this
    # plane_collector.join()
    motor_manager.join()

