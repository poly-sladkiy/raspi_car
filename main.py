from Class_motors import *
from time import sleep

car = PiCar()

car.forward()
car.drive()
sleep(3)

car.stop()

car.reverse()
car.drive()
sleep(3)

car.clear_all()
