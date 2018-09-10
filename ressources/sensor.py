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

        rasp_pi.set_mode(self.ECHO, OUTPUT)
        rasp_pi.set_mode(self.TRIG, OUTPUT)


