# -*- coding: utf_8 -*-


class Plane(object):

    def __init__(self):
        self.information = {
            'Hex': '',
            'Altitude': 0,
            'Latitude': 0,
            'Longitude': 0,
            'Time': 0,
            'Distance': 0}

    def plane_info(self, new_info=None):
        if new_info:
            self.information = new_info
        return self.information
