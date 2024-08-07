from sbot import Robot, AnalogPins
import time

# Initialize the robot and sensors
robot = Robot()
LeftMotor = robot.motor_board.motors[0]
RightMotor = robot.motor_board.motors[1]
left_IR = robot.arduino.pins[AnalogPins.A0]
right_IR = robot.arduino.pins[AnalogPins.A2]

# PID constants (tune these through testing)
Kp = 1.0  # Proportional gain
Ki = 0.0  # Integral gain
Kd = 0.0  # Derivative gain

# Initialize PID variables
integral = 0
previous_error = 0
previous_time = time.time()

# Function to convert analog values to error value
def calculate_error(left_value, right_value):
    # Assuming both sensors over white returns 0 error (perfect center)
    if left_value > right_value:
        error = 1  # positive error (veer to the left)
    elif right_value > left_value:
        error = -1  # negative error (veer to the right)
    else:
        error = 0  # no error (centered)
    return error

# Function to measure raw values under both sensors
def measure_values():
    left = left_IR.analog_value
    right = right_IR.analog_value
    return left, right

# Main loop for following the line using PID control
while True:
    current_time = time.time()
    time_delta = current_time - previous_time
    
    # Measure sensor values
    left_value, right_value = measure_values()
    
    # Calculate error
    error = calculate_error(left_value, right_value)
    
    # Calculate PID terms
    proportional = Kp * error
    integral += error * time_delta
    derivative = (error - previous_error) / time_delta if time_delta > 0 else 0

    # PID output
    pid_output = proportional + (Ki * integral) + (Kd * derivative)
    
    # Adjust motor speeds based on PID output
    left_motor_speed = 0.02 + pid_output
    right_motor_speed = 0.02 - pid_output
    
    # Set the motor speeds
    set_motors(left_motor_speed, right_motor_speed)
    
    # Update previous values for next iteration
    previous_error = error
    previous_time = current_time

# Function to set motor speeds
def set_motors(left, right):
    LeftMotor.power = left
    RightMotor.power = right
