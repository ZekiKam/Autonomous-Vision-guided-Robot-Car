from sbot import Robot, AnalogPins, GPIOPinMode
import time

robot = Robot()
LeftMotor = robot.motor_board.motors[0]
RightMotor = robot.motor_board.motors[1]

robot.arduino.pins[AnalogPins.A0].mode = GPIOPinMode.INPUT
left_IR = robot.arduino.pins[AnalogPins.A0]
robot.arduino.pins[AnalogPins.A2].mode = GPIOPinMode.INPUT
right_IR = robot.arduino.pins[AnalogPins.A2]

# PID constants
Kp = 0.01
Ki = 0.01
Kd = 0.01

integral = 0
previous_error = 0
previous_time = time.time()
pos_power_threshold = 0.6
neg_power_threshold = -0.6
left_power = 0.02 
right_power = 0.02 




def set_motors(left, right):
    LeftMotor.power = left
    RightMotor.power = right


def calculate_error(left, right): #Black low intensity, white high intensity
    if left > right:
        error = 1  #slightly left
    elif right > left:
        error = -1  #slightly right
    else:
        error = 0  #centered
    return error


def measure_values():
    left = left_IR.analog_value
    right = right_IR.analog_value
    return left, right





# Main loop for following the line using PID control
while True:
    current_time = time.time()
    time_change = current_time - previous_time
    
    left_value, right_value = measure_values()
    error = calculate_error(left_value, right_value)
    

    proportional = Kp * error
    if time_change > 0:
        integral += error * time_change
        derivative = (error - previous_error) / time_change
    else:
        integral = 0
        derivative = 0


    pid = proportional + (Ki * integral) + (Kd * derivative)
    left_power = 0.02 + pid
    right_power = 0.02 - pid


    if left_power > pos_power_threshold: 
        left_power = pos_power_threshold
    elif left_power < neg_power_threshold:
        left_power = neg_power_threshold

    if right_power > pos_power_threshold: 
        right_power = pos_power_threshold
    elif right_power < neg_power_threshold:
        right_power = neg_power_threshold
    

    print(left_power, right_power)
    set_motors(left_power, right_power)

    previous_error = error
    previous_time = current_time
