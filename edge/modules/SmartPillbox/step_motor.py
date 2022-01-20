import RPi.GPIO as GPIO
import asyncio
import time


class StepMotor():
    # careful lowering this, at some point you run into the mechanical limitation of how quick your motor can move
    step_sleep = 0.001

    step_count_360 = 4096  # 5.625*(1/64) per step, 4096 steps is 360°

    # defining stepper motor sequence (found in documentation http://www.4tronix.co.uk/arduino/Stepper-Motors.php)
    step_sequence = [[1, 0, 0, 1],
                     [1, 0, 0, 0],
                     [1, 1, 0, 0],
                     [0, 1, 0, 0],
                     [0, 1, 1, 0],
                     [0, 0, 1, 0],
                     [0, 0, 1, 1],
                     [0, 0, 0, 1]]

    def __init__(self, pins):
        self.pins = pins

    def cleanup(self):
        for pin in self.pins:
            GPIO.output(pin, GPIO.LOW)
        GPIO.cleanup()

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)

        for pin in self.pins:
            GPIO.output(pin, GPIO.LOW)

    def rotate(self, rounds, clock_wise=True):
        async def async_rotate():
            self.setup()
            step_count = int(StepMotor.step_count_360 * rounds)
            motor_step_counter = 0

            for _ in range(step_count):
                for i, pin in enumerate(self.pins):
                    GPIO.output(pin,
                                StepMotor.step_sequence[motor_step_counter][i])

                if clock_wise:
                    motor_step_counter += 1
                else:
                    motor_step_counter -= 1

                motor_step_counter %= len(StepMotor.step_sequence)

                # time.sleep(StepMotor.step_sleep)
                await asyncio.sleep(StepMotor.step_sleep)

            self.cleanup()

        asyncio.run(async_rotate())


step_motor_a = StepMotor([17, 18, 27, 22])
step_motor_b = StepMotor([23, 24, 10, 25])
