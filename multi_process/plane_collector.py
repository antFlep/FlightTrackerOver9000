import socket
import time

from multiprocessing import Process
from ressources import calc


class PlaneCollector(Process):

    def __init__(self, closest_plane, ip, current_position):
        Process.__init__(self)

        self.ip = ip

        self.closest_plane = closest_plane
        self.planes = {}

        # Our current position
        self.our_lat = current_position['Latitude']
        self.our_lon = current_position['Longitude']
        self.our_alt = current_position['Altitude']

        # Network connection
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = socket.gethostbyname(ip)
        self.port = 1337
        self.address = (self.ip, self.port)
        self.client.connect(self.address)

    def run(self):
        while True:
            # Distance of the currently tracked plane
            closest_plane = self.closest_plane.plane_info()
            print(closest_plane)
            closest_plane_distance = closest_plane['Distance']
            closest_plane_time = closest_plane['Time']

            msg_data = self.client.recv(1024)
            msg = msg_data.decode('utf-8')
            split_msg = msg.split(',')

            # Only accept messages that have all information we need
            # TODO: change so that we do not need all information
            if len(split_msg) > 15 and \
                    split_msg[11] != '' and \
                    split_msg[14] != '' and \
                    split_msg[15] != '' and \
                    len(split_msg) < 23:

                plane_hex = split_msg[4]
                plane_alt = int(split_msg[11])
                plane_lat = float(split_msg[14])
                plane_lon = float(split_msg[15])
                plane_tim = time.time()

                plane_dis = calc.calc_distance(
                    self.our_lat,
                    self.our_lon,
                    plane_lat,
                    plane_lon)

                print("found plane with hex: " + plane_hex)
                plane_info = {'Hex':        plane_hex,
                              'Altitude':   plane_alt,
                              'Latitude':   plane_lat,
                              'Longitude':  plane_lon,
                              'Time':       plane_tim,
                              'Distance':   plane_dis}

                self.planes[plane_hex] = plane_info

                # If the current plane is closer than the one we are tracking,
                # switch to the current one and wait for the next message
                if plane_dis < closest_plane_distance or closest_plane_distance == 0:
                    self.closest_plane.plane_info(plane_info)
                    continue

                # If the last message we got from the currently tracked plane is to old,
                # switch to the next closest one in the list
                if time.time() - closest_plane_time > 10:
                    self.select_and_clean()

    def select_and_clean(self):
        closest_plane_hex = None
        closest_plane_lat = -1
        closest_plane_lon = -1
        closest_plane_alt = -1
        closest_plane_dis = -1
        closest_plane_tim = -1

        to_delete = []
        for plane_hex in self.planes.keys():
            plane = self.planes.get(plane_hex)

            plane_tim = plane['Time']

            # If the last message we got from the plane is to old,
            # put the hex in a list, so that we can delete the entry afterwards
            if plane_tim - self.closest_plane.plane_info()['Time'] > 10:
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
            closest_plane_info = {'Hex':        closest_plane_hex,
                                  'Altitude':   closest_plane_alt,
                                  'Latitude':   closest_plane_lat,
                                  'Longitude':  closest_plane_lon,
                                  'Time':       closest_plane_tim,
                                  'Distance':   closest_plane_dis}
            self.closest_plane.plane_info(closest_plane_info)

        # Remove old entries
        for hex in to_delete:
            del self.planes[hex]
