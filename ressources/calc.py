# -*- coding: utf_8 -*-

import math


def calc_horizontal_angle(our_lat, our_lon, plane_lat, plane_lon):
    our_lat = math.radians(our_lat)
    our_lon = math.radians(our_lon)
    plane_lat = math.radians(plane_lat)
    plane_lon = math.radians(plane_lon)

    d_lon = (plane_lon - our_lon)

    y = math.sin(d_lon) * math.cos(plane_lat)
    x = math.cos(our_lat) * math.sin(plane_lat) - \
        math.sin(our_lat) * math.cos(plane_lat) * math.cos(d_lon)

    angle = math.atan2(y, x)
    angle = math.degrees(angle)
    angle = (angle + 360) % 360

    return angle


def calc_vertical_angle(our_lat, our_lon, our_alt, plane_lat, plane_lon, plane_alt):
    d_alt = plane_alt - our_alt
    distance = calc_distance(our_lat, our_lon, plane_lat, plane_lon)
    return math.degrees(math.atan(d_alt/distance))


def calc_distance(our_lat, our_lon, plane_lat, plane_lon):
    earth_radius = 6378137  # Earth radius in m

    our_lat = math.radians(our_lat)
    our_lon = math.radians(our_lon)
    plane_lat = math.radians(plane_lat)
    plane_lon = math.radians(plane_lon)

    d_lat = plane_lat - our_lat
    d_lon = plane_lon - our_lon

    a = math.sin(d_lat / 2) * math.sin(d_lat / 2) +     \
        math.cos(our_lat) * math.cos(plane_lat) *       \
        math.sin(d_lon / 2) * math.sin(d_lon / 2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = earth_radius * c

    return distance


def feet_to_meter(x):
    return x * 0.3048


if __name__ == '__main__':

    our_test_lat = 49.486617
    our_test_lon = 6.034665

    plane_test_lat = 46.196295
    plane_test_lon = 6.122516

    test_distance = calc_distance(our_test_lat,
                                  our_test_lon,
                                  plane_test_lat,
                                  plane_test_lon)

    vertical_angle = calc_vertical_angle(our_test_lat,
                                         our_test_lon,
                                         0,
                                         plane_test_lat,
                                         plane_test_lon,
                                         1000)

    print(test_distance)
    print(vertical_angle)



