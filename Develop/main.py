from Class_motors import *
from ball_following_yellow import *
from time import sleep


car = PiCar()
while True:
    way = LocationOfObject()
    print(way)

    if way == "forward":
        car.forward()
        car.drive()

    elif way == "left":
        car.right()
        car.drive()

    elif way == "right":
        car.left()
        car.drive()

    else:
        car.stop()

