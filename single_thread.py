#!/usr/bin/python
# -*- coding: utf_8 -*-


from ressources.parser import get_parameter
from ressources.controller import Controller
import ressources.calc as calc
import socket
import time

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


def collect_msgs():
    print("\nstarted collecting messages")
    start = time.time()
    planes = {}

    while time.time() - start < 30:
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

            print("found plane with hex: " + plane_hex)
            inner_dic = {'Altitude': plane_alt,
                         'Latitude': plane_lat,
                         'Longitude': plane_lon}
            planes[plane_hex] = inner_dic

    print('\n' + str(planes))
    return planes


while True:
    planes = collect_msgs()

    closest_plane_hex = None
    closest_plane_lat = -1
    closest_plane_lon = -1
    closest_plane_alt = -1
    closest_plane_dis = -1

    for plane_key in planes.keys():
        plane = planes.get(plane_key)
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
