from gpiozero import AngularServo


servo1 = AngularServo(18, min_pulse_width=0.0005, max_pulse_width=0.0023)


def unlock():
    servo1.angle = 0


def lock():
    servo1.angle = 90
