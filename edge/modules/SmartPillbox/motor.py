import RPi.GPIO as GPIO
import asyncio
import time

IN1 = 17
IN2 = 18
IN3 = 27
IN4 = 22

# careful lowering this, at some point you run into the mechanical limitation of how quick your motor can move
STEP_SLEEP = 0.001

STEP_COUNT_360 = 4096  # 5.625*(1/64) per step, 4096 steps is 360°

CLOCK_WISE = True  # True for clockwise, False for counter-clockwise

# defining stepper motor sequence (found in documentation http://www.4tronix.co.uk/arduino/Stepper-Motors.php)
STEP_SEQUENCE = [[1, 0, 0, 1],
                 [1, 0, 0, 0],
                 [1, 1, 0, 0],
                 [0, 1, 0, 0],
                 [0, 1, 1, 0],
                 [0, 0, 1, 0],
                 [0, 0, 1, 1],
                 [0, 0, 0, 1]]


def cleanup():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    GPIO.cleanup()


def init():
    # setting up
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.setup(IN3, GPIO.OUT)
    GPIO.setup(IN4, GPIO.OUT)

    # initializing
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)


def turn(round, clock_wise=True):
    init()

    motor_pins = [IN1, IN2, IN3, IN4]

    step_count = int(STEP_COUNT_360 * round)
    motor_step_counter = 0

    for _ in range(step_count):
        for pin in range(len(motor_pins)):
            GPIO.output(motor_pins[pin],
                        STEP_SEQUENCE[motor_step_counter][pin])

        if CLOCK_WISE:
            motor_step_counter += 1
        else:
            motor_step_counter -= 1

        motor_step_counter %= len(STEP_SEQUENCE)

        time.sleep(STEP_SLEEP)

    cleanup()
