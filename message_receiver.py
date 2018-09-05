#!/usr/bin/python
# -*- coding: utf_8 -*-

import socket
import time
import ressources.calc as calc
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

# Set our position Here
# 49°29'11.8"N 6°02'04.8"E
our_lat = 49.486617
our_lon = 6.034665
our_alt = 0

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = socket.gethostbyname(rasp_pi_ip)
port = 1337
address = (ip, port)
client.connect(address)


def collect_msgs():
    print("started collecting messages")
    start = time.time()
    planes_pos = {}
    while time.time() - start < 30:
        msg_data = client.recv(1024)
        msg = msg_data.decode('utf-8')
        split_msg = msg.split(',')
        if len(split_msg) > 15 and split_msg[11] != '' and split_msg[14] != '' and split_msg[15] != '' and len(
            split_msg) < 23:
            plane_hex = split_msg[4]
            plane_alt = int(split_msg[11])
            plane_lat = float(split_msg[14])
            plane_lon = float(split_msg[15])
            print("found plane with hex: " + plane_hex)
            inner_dic = {'Altitude': plane_alt, 'Latitude': plane_lat, 'Longitude': plane_lon}
            planes_pos[plane_hex] = inner_dic
    print('\n' + str(planes_pos) + '\n')
    return planes_pos


while True:
    planes_pos = collect_msgs()

    closest_plane_hex = None
    closest_plane_lat = -1
    closest_plane_lon = -1
    closest_plane_alt = -1
    closest_plane_dis = -1

    for plane_key in planes_pos.keys():
        plane = planes_pos.get(plane_key)
        plane_hex = plane_key
        plane_alt = plane['Altitude']
        plane_lat = plane['Latitude']
        plane_lon = plane['Longitude']
        plane_dis = calc.calc_distance(our_lat, our_lon, plane_lat, plane_lon)

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

    if not closest_plane_dis == -1:
        print('\nclosest plane: ' + closest_plane_hex)

        # Set horizontal position
        print('\nsetting horizontal angle:')
        # TODO why do we need to subtract form 360

        hor_angle = 360 - calc.calc_angle(
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


# # 49°29'11.8"N 6°02'04.8"E
# our_lat = 49.486617
# our_lon = 6.034665
#
# # 49°28'59.0"N 6°05'22.0"E
# # 49.483049, 6.089437
# plane_lat = 49.483049
# plane_lon = 6.089437
#
# # 46°11'46.7"N 6°07'21.1"E
# plane_lat = 46.196295
# plane_lon = 6.122516
#
# print(str(ressources.calc.calc_angle(our_lat, our_lon, plane_lat, plane_lon)))
# print(str(ressources.calc.calc_angle(plane_lat, plane_lon, our_lat, our_lon)))



