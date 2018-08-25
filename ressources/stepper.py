import pigpio
from time import sleep
from collections import deque

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


class StepperMotor:

    def __init__(self, pi, pin1, pin2, pin3, pin4, sequence=halfStepSequence, delay_after_step=0.001):
        if not isinstance(pi, pigpio.pi):
            raise TypeError("Is not pigpio.pi instance.")

        pi.set_mode(pin1, pigpio.OUTPUT)
        pi.set_mode(pin2, pigpio.OUTPUT)
        pi.set_mode(pin3, pigpio.OUTPUT)
        pi.set_mode(pin4, pigpio.OUTPUT)

        self.pin1 = pin1
        self.pin2 = pin2
        self.pin3 = pin3
        self.pin4 = pin4

        self.pi = pi
        self.delayAfterStep = delay_after_step
        self.deque = deque(sequence)

    def do_counterclockwise_step(self):
        self.deque.rotate(-1)
        self.do_step_and_delay(self.deque[0])

    def do_clockwise_step(self):
        self.deque.rotate(1)
        self.do_step_and_delay(self.deque[0])

    def do_step_and_delay(self, step):
        self.pi.write(self.pin1, step[0])
        self.pi.write(self.pin2, step[1])
        self.pi.write(self.pin3, step[2])
        self.pi.write(self.pin4, step[3])
        sleep(self.delayAfterStep)

    def do_rotate_clockwise(self, steps):
        for _ in range(steps):
            self.do_clockwise_step()

    def do_rotate_counterclockwise(self, steps):
        for _ in range(steps):
            self.do_counterclockwise_step()
