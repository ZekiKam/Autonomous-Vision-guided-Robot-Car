#Place robot one purple area -> get IR values -> take average

from sbot import Robot, AnalogPins, GPIOPinMode
import time

robot = Robot()
robot.arduino.pins[AnalogPins.A0].mode = GPIOPinMode.INPUT
left_IR = robot.arduino.pins[AnalogPins.A0]
robot.arduino.pins[AnalogPins.A2].mode = GPIOPinMode.INPUT
right_IR = robot.arduino.pins[AnalogPins.A2]

def purple_threshold():
    left_list = []
    right_list = []
    for x in range(100):  
        left_value = left_IR.analog_value
        right_value = right_IR.analog_value
        left_list.append(left_value)
        right_list.append(right_value)
        time.sleep(0.1)  

    left = sum(left_list) / len(left_list)
    right = sum(right_list) / len(right_list)
    return left, right

left, right = purple_threshold()
print(f"Left: {left}")
print(f"Right: {right}")
