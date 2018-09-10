# -*- coding: utf_8 -*-

from ressources.stepper import StepperMotor


class Controller(object):

    def __init__(self, pins, rasp_pi_ip):
        self.motor = StepperMotor(rasp_pi_ip, *pins)
        self.full_circle = 4096  # 8 half-steps times 512
        self.current_pos = 0

    def get_end_pos(self, angle):
        return int((self.full_circle/360) * angle)

    def go_to_goal(self, end_pos):
        print('current position: ' + str(self.current_pos))

        if end_pos == self.current_pos:
            return

        if end_pos < self.current_pos:
            print('running counterclockwise')
            diff = self.current_pos - end_pos
            self.motor.do_rotate_counterclockwise(diff)
            self.current_pos -= diff
            
        else:
            print('running clockwise')
            diff = end_pos - self.current_pos
            self.motor.do_rotate_clockwise(diff)
            self.current_pos += diff

        print('current position: ' + str(self.current_pos) + '; end position: ' + str(end_pos))
        assert end_pos == self.current_pos
