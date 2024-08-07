from sbot import Robot, AnalogPins
import time
robot = Robot()

LeftMotor = robot.motor_board.motors[0]
RightMotor = robot.motor_board.motors[1]

left_IR = robot.arduino.pins[AnalogPins.A1]
right_IR = robot.arduino.pins[AnalogPins.A2]

# PID constants
Kp = 0.0  
Ki = 0.0 
Kd = 0.0 

integral = 0
previous_error = 0
previous_time = time.time()





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
     
    left_power = 0.2 + pid
    right_power = 0.2 - pid
    
    set_motors(left_power, right_power)

    previous_error = error
    previous_time = current_time
