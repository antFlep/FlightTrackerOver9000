# -*- coding: utf_8 -*-

from multiprocessing import Process
from ressources import calc
import time


class MotorManager(Process):

    def __init__(self, closest_plane, current_position, motor1, motor2):
        Process.__init__(self)

        self.closest_plane = closest_plane

        self.our_lat = current_position['Latitude']
        self.our_lon = current_position['Longitude']
        self.our_alt = current_position['Altitude']

        self.controller1 = motor1
        self.controller2 = motor2

    def run(self):
        while True:
            closest_plane = self.closest_plane.plane_info()
            if closest_plane['Hex'] == '':
                continue

            closest_plane_hex = closest_plane['Hex']
            closest_plane_alt = closest_plane['Altitude']
            closest_plane_lat = closest_plane['Latitude']
            closest_plane_lon = closest_plane['Longitude']

            print('\nclosest plane: ' + closest_plane_hex)

            # Set horizontal position
            print('\nsetting horizontal angle:')

            hor_angle = calc.calc_horizontal_angle(
                self.our_lat,
                self.our_lon,
                closest_plane_lat,
                closest_plane_lon)

            end_pos = self.controller1.get_end_pos(hor_angle)
            self.controller1.go_to_goal(end_pos)

            # Set vertical position
            print('\nsetting vertical angle:')
            closest_plane_alt = calc.feet_to_meter(closest_plane_alt)

            # TODO explain formulas
            ver_angle = calc.calc_vertical_angle(
                self.our_lat,
                self.our_lon,
                self.our_alt,
                closest_plane_lat,
                closest_plane_lon,
                closest_plane_alt)

            print('altitude: ' + str(closest_plane_alt) + '; angle: ' + str(ver_angle))
            end_pos = self.controller2.get_end_pos(ver_angle)
            self.controller2.go_to_goal(end_pos)
            time.sleep(0.1)
