#!/usr/bin/python
# -*- coding: utf_8 -*-

import socket
import time
import ressources.calc as calc
from ressources.controller import Controller
from threading import Lock, Thread
from ressources.parser import get_parameter

rasp_ip = get_parameter('ip')

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

# Set our position Here
# 49°29'11.8"N 6°02'04.8"E
our_lat = float(get_parameter('our_lat'))
our_lon = float(get_parameter('our_lon'))
our_alt = int(get_parameter('our_alt'))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = socket.gethostbyname(rasp_ip)
port = int(get_parameter('msg_port'))
address = (ip, port)
client.connect(address)

threadLock = Lock()


class PlaneCollector(Thread):

    def __init__(self, closest_plane):
        Thread.__init__(self)
        self.closest_plane = closest_plane
        self.planes = {}

    def run(self):
        while True:
            msg_data = client.recv(1024)
            msg = msg_data.decode('utf-8')
            split_msg = msg.split(',')

            if len(split_msg) > 15 and \
                    split_msg[11] != '' and \
                    split_msg[14] != '' and \
                    split_msg[15] != '' and \
                    len(split_msg) < 23:

                plane_hex = split_msg[4]
                plane_alt = int(split_msg[11])
                plane_lat = float(split_msg[14])
                plane_lon = float(split_msg[15])
                plane_dis = calc.calc_distance(our_lat, our_lon, plane_lat, plane_lon)
                plane_tim = time.time()

                print("found plane with hex: " + plane_hex)
                inner_dic = {'Altitude': plane_alt,
                             'Latitude': plane_lat,
                             'Longitude': plane_lon,
                             'Time': plane_tim,
                             'Distance': plane_dis}
                self.planes[plane_hex] = inner_dic

                if plane_dis < self.closest_plane.dis or self.closest_plane.dis == 0:
                    threadLock.acquire()
                    self.closest_plane.hex = plane_hex
                    self.closest_plane.alt = plane_alt
                    self.closest_plane.lat = plane_lat
                    self.closest_plane.lon = plane_lon
                    self.closest_plane.dis = plane_dis
                    self.closest_plane.tim = plane_tim
                    threadLock.release()
                    time.sleep(0.1)
                    continue

                if time.time() - self.closest_plane.tim > 10:
                    closest_plane_hex = None
                    closest_plane_lat = -1
                    closest_plane_lon = -1
                    closest_plane_alt = -1
                    closest_plane_dis = -1
                    closest_plane_tim = -1

                    to_delete = []
                    for plane_key in self.planes.keys():
                        plane_hex = plane_key
                        plane = self.planes.get(plane_key)
                        plane_tim = plane['Time']

                        if plane_tim - self.closest_plane.tim > 10:
                            to_delete.append(plane_hex)
                            continue

                        plane_alt = plane['Altitude']
                        plane_lat = plane['Latitude']
                        plane_lon = plane['Longitude']
                        plane_dis = plane['Distance']

                        print('hex: ' + plane_hex +
                              '; alt: ' + str(plane_alt) +
                              '; lat: ' + str(plane_lat) +
                              '; lon: ' + str(plane_lon) +
                              '; dis: ' + str(plane_dis))

                        if plane_dis < closest_plane_dis or closest_plane_dis < 0:
                            closest_plane_hex = plane_hex
                            closest_plane_alt = plane_alt
                            closest_plane_lat = plane_lat
                            closest_plane_lon = plane_lon
                            closest_plane_dis = plane_dis
                            closest_plane_tim = plane_tim

                    if closest_plane_hex:
                        threadLock.acquire()
                        self.closest_plane.hex = closest_plane_hex
                        self.closest_plane.alt = closest_plane_alt
                        self.closest_plane.lat = closest_plane_lat
                        self.closest_plane.lon = closest_plane_lon
                        self.closest_plane.dis = closest_plane_dis
                        self.closest_plane.tim = closest_plane_tim
                        threadLock.release()

                    # remove old entries
                    for hex in to_delete:
                        del self.planes[hex]


class Plane(object):

    def __init__(self):
        self.hex = ''
        self.alt = 0
        self.lat = 0
        self.lon = 0
        self.dis = 0
        self.tim = 0


class MotorThread(Thread):

    def __init__(self, closest_plane):
        Thread.__init__(self)
        self.closest_plane = closest_plane

    def run(self):
        while True:
            if self.closest_plane.hex == '':
                continue

            threadLock.acquire()
            closest_plane_hex = self.closest_plane.hex
            closest_plane_alt = self.closest_plane.alt
            closest_plane_lat = self.closest_plane.lat
            closest_plane_lon = self.closest_plane.lon
            threadLock.release()

            print('\nclosest plane: ' + closest_plane_hex)

            # Set horizontal position
            print('\nsetting horizontal angle:')

            hor_angle = calc.calc_horizontal_angle(
                our_lat,
                our_lon,
                closest_plane_lat,
                closest_plane_lon)

            end_pos = controller1.get_end_pos(hor_angle)
            controller1.go_to_goal(end_pos)

            # Set vertical position
            print('\nsetting vertical angle:')
            closest_plane_alt = calc.feet_to_meter(closest_plane_alt)

            # TODO explain formulas
            ver_angle = calc.calc_vertical_angle(
                our_lat,
                our_lon,
                our_alt,
                closest_plane_lat,
                closest_plane_lon,
                closest_plane_alt)

            print('altitude: ' + str(closest_plane_alt) + '; angle: ' + str(ver_angle))
            end_pos = controller2.get_end_pos(ver_angle)
            controller2.go_to_goal(end_pos)
            time.sleep(0.1)


closest_plane = Plane()
plane_collector = PlaneCollector(closest_plane)
motor_thread = MotorThread(closest_plane)

plane_collector.start()
motor_thread.start()

