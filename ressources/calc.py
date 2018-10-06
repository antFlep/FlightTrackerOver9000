# -*- coding: utf_8 -*-

import math


def calc_horizontal_angle(our_lat, our_lon, plane_lat, plane_lon):
    """
    Calculates horizontal between 2 positions.
    In our case between our position and that of a plane

    :param our_lat: point1/our latitude in degrees
    :param our_lon: point1/our longitude in degrees
    :param plane_lat: point2/plane latitude in degrees
    :param plane_lon: point2/plane longitude in degrees
    :return: horizontal angle between our position and that of a plane
    """

    # convert deg to rad
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
    """
    Calculates vertical angle between two positions
    using simple trigonometry.
    In our case between our position and that of a plane.

    :param our_lat: point1/our latitude in degrees
    :param our_lon: point1/our longitude in degrees
    :param our_alt: point1/our altitude in meter
    :param plane_lat: point2/plane latitude in degrees
    :param plane_lon: point2/plane longitude in degrees
    :param plane_alt: point2/plane longitude in meter
    :return: vertical angle between our position and that of a plane
    """

    d_alt = plane_alt - our_alt
    distance = calc_distance(our_lat, our_lon, plane_lat, plane_lon)
    return math.degrees(math.atan(d_alt/distance))


def calc_distance(our_lat, our_lon, plane_lat, plane_lon):
    """
    Calculates great circle distance between 2 points on earth

    :param our_lat: point1 latitude
    :param our_lon: point1 longitude
    :param plane_lat: point2 latitude
    :param plane_lon: point2 longitude
    :return: great circle distance between point1 and 2
    """

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
    """
    Converts feet to meters

    :param x: value in feet
    :return: value in meter
    """

    return x * 0.3048



