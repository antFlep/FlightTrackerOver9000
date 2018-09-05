#!/usr/bin/python
# -*- coding: utf_8 -*-

import math


def calc_angle(our_lat, our_lon, plane_lat, plane_lon):

    our_lat = math.radians(our_lat)
    our_lon = math.radians(our_lon)
    plane_lat = math.radians(plane_lat)
    plane_lon = math.radians(plane_lon)

    d_lon = (plane_lon - our_lon)

    y = math.sin(d_lon) * math.cos(plane_lat)
    x = math.cos(our_lat) * math.sin(plane_lat) - math.sin(our_lat) \
        * math.cos(plane_lat) * math.cos(d_lon)

    angle = math.atan2(y, x)
    angle = math.degrees(angle)
    angle = (angle + 360) % 360

    return angle


def calc_vertical_angle(our_lat, our_lon, our_alt, plane_lat, plane_lon, plane_alt):
    diff_alt = plane_alt - our_alt
    distance = calc_distance(our_lat, our_lon, plane_lat, plane_lon)
    return math.degrees(math.atan(diff_alt/distance))


def calc_distance(our_lat, our_lon, plane_lat, plane_lon):
    earth_radius = 6378.137  # Radius of earth in KM
    d_lat = plane_lat * math.pi / 180 - our_lat * math.pi / 180
    d_lon = plane_lon * math.pi / 180 - our_lon * math.pi / 180
    a = math.sin(d_lat / 2) * math.sin(d_lat / 2) + math.cos(our_lat * math.pi / 180) * \
        math.cos(plane_lat * math.pi / 180) * math.sin(d_lon / 2) * math.sin(d_lon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = earth_radius * c
    return d * 1000  # meters


def feet_to_meter(x):
    return x * 0.3048


if __name__ == '__main__':

    our_lat = 49.486617
    our_lon = 6.034665

    plane_lat = 46.196295
    plane_lon = 6.122516
    distance = calc_distance(our_lat, our_lon, plane_lat, plane_lon)
    print(str(distance))
    print(str(360 - calc_angle(our_lat, our_lon, plane_lat, plane_lon)))


