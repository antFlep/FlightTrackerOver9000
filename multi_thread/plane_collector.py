from threading import Thread
import ressources.calc as calc
import socket
import time


class PlaneCollector(Thread):

    def __init__(self, closest_plane, current_position, ip, port, lock, tracking_time=10):
        Thread.__init__(self)
        self.lock = lock

        self.closest_plane = closest_plane
        self.planes = {}
        self.tracking_time = tracking_time

        # Our current position
        self.our_lat = current_position['Latitude']
        self.our_lon = current_position['Longitude']
        self.our_alt = current_position['Altitude']

        # Network connection
        address = (ip, port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(address)

    def run(self):
        while True:
            msg_data = self.client.recv(1024)
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
                plane_dis = calc.calc_distance(self.our_lat, self.our_lon, plane_lat, plane_lon)
                plane_tim = time.time()

                print("found plane with hex: " + plane_hex)
                inner_dic = {'Altitude': plane_alt,
                             'Latitude': plane_lat,
                             'Longitude': plane_lon,
                             'Time': plane_tim,
                             'Distance': plane_dis}
                self.planes[plane_hex] = inner_dic

                if plane_dis < self.closest_plane.dis or self.closest_plane.dis == 0:
                    self.lock.acquire()
                    self.closest_plane.hex = plane_hex
                    self.closest_plane.alt = plane_alt
                    self.closest_plane.lat = plane_lat
                    self.closest_plane.lon = plane_lon
                    self.closest_plane.dis = plane_dis
                    self.closest_plane.tim = plane_tim
                    self.lock.release()
                    time.sleep(0.1)
                    continue

                if time.time() - self.closest_plane.tim > self.tracking_time:
                    self.select_and_clean()

    def select_and_clean(self):
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
            self.lock.acquire()
            self.closest_plane.hex = closest_plane_hex
            self.closest_plane.alt = closest_plane_alt
            self.closest_plane.lat = closest_plane_lat
            self.closest_plane.lon = closest_plane_lon
            self.closest_plane.dis = closest_plane_dis
            self.closest_plane.tim = closest_plane_tim
            self.lock.release()

        # remove old entries
        for plane in to_delete:
            del self.planes[plane]
