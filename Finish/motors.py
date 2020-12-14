import RPi.GPIO as gpio


class PiCar:

    def __init__(self, duty_cycle=100, hz=100):
        gpio.setmode(gpio.BCM)

        gpio.setup(17, gpio.OUT)  # ENA
        gpio.setup(27, gpio.OUT)  # IN 1
        gpio.setup(22, gpio.OUT)  # IN 2

        gpio.setup(21, gpio.OUT)  # ENB
        gpio.setup(16, gpio.OUT)  # IN 3
        gpio.setup(20, gpio.OUT)  # IN 4

        self.duty_cycle = duty_cycle
        self.hz = hz

        self.pwm_a = gpio.PWM(17, self.hz)
        self.pwm_b = gpio.PWM(21, self.hz)

    @staticmethod
    def forward() -> None:
        gpio.output(27, 1)  # IN 1
        gpio.output(22, 0)  # IN 2

        gpio.output(16, 0)  # IN 3
        gpio.output(20, 1)  # IN 4

    @staticmethod
    def reverse() -> None:
        gpio.output(27, 0)  # IN 1
        gpio.output(22, 1)  # IN 2

        gpio.output(16, 1)  # IN 3
        gpio.output(20, 0)  # IN 4

    @staticmethod
    def right() -> None:
        gpio.output(27, 0)  # IN 1
        gpio.output(22, 1)  # IN 2

        gpio.output(16, 0)  # IN 3
        gpio.output(20, 1)  # IN 4

    @staticmethod
    def left() -> None:
        gpio.output(27, 1)  # IN 1
        gpio.output(22, 0)  # IN 2

        gpio.output(16, 1)  # IN 3
        gpio.output(20, 0)  # IN 4

    def drive(self) -> None:
        self.pwm_a.start(self.duty_cycle)
        self.pwm_b.start(self.duty_cycle)

    def stop(self):
        self.pwm_a.stop()
        self.pwm_b.stop()

    def clear_all(self):
        self.pwm_a.stop()
        self.pwm_b.stop()
        gpio.cleanup()
