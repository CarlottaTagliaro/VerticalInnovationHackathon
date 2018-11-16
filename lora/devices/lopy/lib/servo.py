# coding=utf-8
from machine import Pin, Timer

VALID_GP_PINS = [9, 10, 11, 24]

PIN_PWM_TIMER = {
    9: 2,
    10: 3,
    11: 3,
    24: 0,
}

PIN_PWM_CHANNEL = {
    9: Timer.B,
    10: Timer.A,
    11: Timer.B,
    24: Timer.A,
}

PIN_PWM_ALT = {
    9: 3,
    10: 3,
    11: 3,
    24: 5,
}

PERC_100 = 10000  # in 100% * 100


class Servo:
    """
    WiPy servo object
    Sets up Timer and Channel and performs calculation so servo angle is automatically converted to duty cycle.
    """

    def __init__(self, gp_pin, frequency, full_range100, pulse_min, pulse_max):
        """
        :param gp_pin: GPIO pin
        :param frequency: in Hz
        :param full_range100: in deg * 100
        :param pulse_min: in µs
        :param pulse_max: in µs
        :return:
        """
        if not gp_pin in VALID_GP_PINS:
            print('invalid GP pin:', gp_pin)

        # Get WiPy PWM configuration constants
        pin_alt = PIN_PWM_ALT[gp_pin]
        timer_nr = PIN_PWM_TIMER[gp_pin]
        timer_channel = PIN_PWM_CHANNEL[gp_pin]

        # Configure PWM timer to pin flow
        Pin('GP' + str(gp_pin), mode=Pin.ALT, alt=pin_alt)
        timer = Timer(timer_nr, mode=Timer.PWM)
        self.channel = timer.channel(timer_channel, freq=frequency)

        # Store object properties
        self.PWM_frame = 1000000 // frequency  # in µs
        self.full_range100 = full_range100
        self.pulse_min = pulse_min
        self.pulse_diff = pulse_max - pulse_min

    def angle(self, angle100):
        """
        Set timer duty cycle to specified angle
        :param angle100: angle in deg * 100
        :return:
        """
        angle_fraction = PERC_100 * angle100 // self.full_range100  # in 100% * 100 format
        pulse_width = self.pulse_min + angle_fraction * self.pulse_diff // PERC_100  # in µs
        duty_cycle = PERC_100 * pulse_width // self.PWM_frame  # in 100% * 100 format
        self.channel.duty_cycle(duty_cycle)
