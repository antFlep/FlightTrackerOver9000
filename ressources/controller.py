# -*- coding: utf_8 -*-

from ressources.stepper import StepperMotor


class Controller(object):

    def __init__(self, pins, rasp_pi_ip):
        """
        Controller used to steer the motors so that it points to a certain angle

        :param pins: motor pins
        :param rasp_pi_ip: ip-address of the raspberry pi running a pigpiod server
        """

        self.motor = StepperMotor(rasp_pi_ip, *pins)
        self.full_circle = 4096  # 8 half-steps times 512
        self.current_pos = 0

    def get_end_pos(self, angle):
        """
        Calculates and returns the position/steps corresponding to provided angle

        :param angle: angel we want our pointer to point to
        :return: position corresponding to the provided angle
        """
        return int((self.full_circle/360) * angle)

    def go_to_goal(self, end_pos):
        """
        Rotates our motor to the  provided position,
        making sure it will never rotate over 360 degrees

        :param end_pos: position to which we turn our motor to
        """

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

        assert end_pos == self.current_pos
