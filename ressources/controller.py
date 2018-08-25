from ressources.stepper import StepperMotor
from pigpio import pi


class Controller:

    def __init__(self, pins):
        rasp_pi_ip = '192.168.50.60'
        rasp_pi = pi(rasp_pi_ip)

        self.motor = StepperMotor(rasp_pi, *pins)
        self.full_circle = 4096  # 8 half-steps times 512
        self.current_pos = 0

    def get_end_pos(self, angle):
        return int((self.full_circle/360) * angle)

    def go_to_goal(self, end_pos):
        if end_pos == self.current_pos:
            return
        if end_pos < self.current_pos:
            diff = self.current_pos - end_pos
            self.motor.do_rotate_counterclockwise(diff)
            self.current_pos -= diff
            print('running counterclockwise')
        else:
            diff = end_pos - self.current_pos
            self.motor.do_rotate_clockwise(diff)
            self.current_pos += diff
            print('running clockwise')
        print('Current Position: ' + str(self.current_pos) + '; End Position: ' + str(end_pos))
        assert end_pos == self.current_pos
