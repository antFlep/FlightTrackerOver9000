# -*- coding: utf_8 -*-

from collections import deque
from time import sleep
from pigpio import pi, OUTPUT

fullStepSequence = (
    (1, 0, 0, 0),
    (0, 1, 0, 0),
    (0, 0, 1, 0),
    (0, 0, 0, 1)
)

halfStepSequence = (
    (1, 0, 0, 0),
    (1, 1, 0, 0),
    (0, 1, 0, 0),
    (0, 1, 1, 0),
    (0, 0, 1, 0),
    (0, 0, 1, 1),
    (0, 0, 0, 1),
    (1, 0, 0, 1)
)


class StepperMotor(object):

    def __init__(self, ip, pin1, pin2, pin3, pin4, sequence=halfStepSequence, delay_after_step=0.001):
        """
        Stepper motor

        :param ip: ip of server running pigpiod
        :param pin1: Pin 1 of the motor
        :param pin2: Pin 2 of the motor
        :param pin3: Pin 3 of the motor
        :param pin4: Pin 4 of the motor
        :param sequence: fullStepSequence or halfStepSequence
        :param delay_after_step: time to delay between each step
        """

        rasp_pi = pi(ip)

        if not isinstance(rasp_pi, pi):
            raise TypeError("Is not pigpio.pi instance.")

        rasp_pi.set_mode(pin1, OUTPUT)
        rasp_pi.set_mode(pin2, OUTPUT)
        rasp_pi.set_mode(pin3, OUTPUT)
        rasp_pi.set_mode(pin4, OUTPUT)

        self.pin1 = pin1
        self.pin2 = pin2
        self.pin3 = pin3
        self.pin4 = pin4

        self.pi = rasp_pi
        self.delayAfterStep = delay_after_step
        self.deque = deque(sequence)

    def do_counterclockwise_step(self):
        """
        Do a counterclockwise step
        """

        self.deque.rotate(-1)
        self.do_step_and_delay(self.deque[0])

    def do_clockwise_step(self):
        """
        Do a clockwise step
        """
        self.deque.rotate(1)
        self.do_step_and_delay(self.deque[0])

    def do_step_and_delay(self, step):
        """
        Write step values to gpio pins and wait for a bit
        :param step: Step sequence to write
        """
        self.pi.write(self.pin1, step[0])
        self.pi.write(self.pin2, step[1])
        self.pi.write(self.pin3, step[2])
        self.pi.write(self.pin4, step[3])
        sleep(self.delayAfterStep)

    def do_rotate_clockwise(self, steps):
        """
        Rotate motor clockwise
        :param steps: number of steps to rotate
        """
        for _ in range(steps):
            self.do_clockwise_step()

    def do_rotate_counterclockwise(self, steps):
        """
        Rotate motor counterclockwise
        :param steps: number of steps to rotate
        """
        for _ in range(steps):
            self.do_counterclockwise_step()
