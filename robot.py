from sbot import Robot, AnalogPins, GPIOPinMode
import time

#Notes
#Voltage varies between 0-5V
#Adjust Kp value to reduce wobble
#Run test_purple_IR.py to test threshold

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

def calculate_error(left, right): # Black low intensity, white high intensity
    if left > right:
        error = 1  # slightly left
    elif right > left:
        error = -1  # slightly right
    else:
        error = 0  # centered
    return error

def measure_values():
    left = left_IR.analog_value
    right = right_IR.analog_value
    return left, right

def return_track():
    while True:
        left_value, right_value = measure_values()
        if left_value < left_threshold or right_value < right_threshold:  #Adjust threshold
            break
        if left_value > left_threshold and right_value > right_threshold:
            set_motors(0.02, -0.02)  #Spin right if both
        elif left_value > left_threshold:
            set_motors(0.02, -0.02)  
        elif right_value > right_threshold:
            set_motors(-0.02, 0.02)  
            
        time.sleep(0.1) #Adjust
    set_motors(0, 0)  




# Main loop for following the line using PID control
while True:
    current_time = time.time()
    time_change = current_time - previous_time
    
    left_value, right_value = measure_values()

    if left_value > left_threshold and right_value > right_threshold:  # Adjust threshold
        set_motors(0, 0)
        return_track()
        continue
    
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

    set_motors(left_power, right_power)

    previous_error = error
    previous_time = current_time
