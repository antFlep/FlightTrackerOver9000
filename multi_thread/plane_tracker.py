from threading import Thread
import ressources.calc as calc
import time


class PlaneTracker(Thread):

    def __init__(self, closest_plane, current_position, motor1, motor2, lock):
        Thread.__init__(self)
        self.lock = lock

        self.closest_plane = closest_plane

        self.our_lat = current_position['Latitude']
        self.our_lon = current_position['Longitude']
        self.our_alt = current_position['Altitude']

        self.controller1 = motor1
        self.controller2 = motor2

    def run(self):
        while True:
            if self.closest_plane.hex == '':
                continue

            self.lock.acquire()
            closest_plane_hex = self.closest_plane.hex
            closest_plane_alt = self.closest_plane.alt
            closest_plane_lat = self.closest_plane.lat
            closest_plane_lon = self.closest_plane.lon
            self.lock.release()

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
