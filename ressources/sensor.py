# -*- coding: utf_8 -*-

from pigpio import pi, OUTPUT, INPUT
import time


class DistanceSensor(object):

    def __init__(self, ip, echo_pin, trigger_pin):
        rasp_pi = pi(ip)

        if not isinstance(rasp_pi, pi):
            raise TypeError("Is not pigpio.pi instance.")

        self.ECHO = echo_pin
        self.TRIG = trigger_pin

        rasp_pi.set_mode(self.TRIG, OUTPUT)
        rasp_pi.set_mode(self.ECHO, INPUT)

        self.pi = rasp_pi

    def distance(self):
        # set Trigger High
        self.pi.write(self.TRIG, 1)

        # set Trigger after 0.1ms low
        time.sleep(0.00001)
        self.pi.write(self.TRIG, 0)

        start_time = time.time()
        end_time = time.time()

        # store start time
        while self.pi.read(self.ECHO) == 0:
            start_time = time.time()

        # store arrival
        while self.pi.read(self.ECHO) == 1:
            end_time = time.time()

        # elapsed time
        time_elapsed = end_time - start_time
        # multiply with speed of sound (34300 cm/s)
        # and division by two
        distance = (time_elapsed * 34300) / 2

        return distance


