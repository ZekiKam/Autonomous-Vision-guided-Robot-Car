'''
PID + webcam vision
Replaces fixed-threshold turning with independent PID loops for each motor, using the marker's angle as the error signal.
'''

from sbot import Robot
import time
import math
robot = Robot()

LeftMotor = robot.motor_board.motors[0]
RightMotor = robot.motor_board.motors[1]

#PID constants (adjustable)
Kp = 0.1  # Proportional
Ki = 0.01  # Integral
Kd = 0.001  # Derivative 

#Just more PID variables
error_left = 0
error_right = 0
integral_left = 0
integral_right = 0
derivative_left = 0
derivative_right = 0
previous_error_left = 0
previous_error_right = 0
previous_time = time.time()

#Motor variables
left_forward_power = 0.651
right_forward_power = 0.65
left_turning_power = 0.2
right_turning_power = 0.2



def set_motors(left, right):
    LeftMotor.power = left
    RightMotor.power = right

# This function checks visible maker list for a specific target
def find_marker(markers, id_number):
    for marker in markers:
        if marker.id == id_number:
            return marker
    return None



#Main loop
current_marker = 1
while True:
    set_motors(0,0) 
    robot.sleep(0.2) #Time for robot to actually stop
    markers = robot.camera.see()
    target_marker = find_marker(markers, current_marker)
    print(f"Searching for marker {current_marker}")
    if target_marker != None:
        current_time = time.time()
        dt = current_time - previous_time
        angle_to_marker = math.degrees(target_marker.position.horizontal_angle)
        distance = target_marker.position.distance
    
        #PID --- Marker's horizontal angle = error for the motors
        error_left = angle_to_marker 
        error_right = -angle_to_marker  #Motor turns opposite direction if the error is to the left, vice versa
        integral_left += error_left * dt
        integral_right += error_right * dt
        derivative_left = (error_left - previous_error_left) / dt
        derivative_right = (error_right - previous_error_right) / dt
        
        # Calculate PID output for left and right motors
        pid_output_left = Kp * error_left + Ki * integral_left + Kd * derivative_left
        pid_output_right = Kp * error_right + Ki * integral_right + Kd * derivative_right

        #Update previous error and time
        previous_error_left = error_left
        previous_error_right = error_right
        previous_time = current_time    
        
        #Adjust motor speeds using PID output
        left_speed = left_forward_power + pid_output_left
        right_speed = right_forward_power + pid_output_right
        
        
        if angle_to_marker > 10:
            print("Marker on the right")
            set_motors(left_turning_power, -right_turning_power)
            robot.sleep(0.1)
            print("A")
           
        elif angle_to_marker < -10:
            print("Marker on the left")
            set_motors(-left_turning_power, right_turning_power)
            robot.sleep(0.1)
            print("B")
            
        elif target_marker.position.distance > 1000:
            print("Marker forward")
            set_motors(left_forward_power, right_forward_power)
            robot.sleep(target_marker.position.distance/3000) # 3000 speed t=d/v (test experiment to find speed)
            print(f"Distance from wall:{target_marker.position.distance}")
        
            if (target_marker.position.distance/2) <= 1000:
                current_marker += 2
                if current_marker > 7:
                    current_marker = 1
                
                if current_marker == 1 or current_marker == 3 or current_marker == 7:
                    set_motors(-left_turning_power, right_turning_power)
                    robot.sleep(0.4)
                    print("Wall detected, turn left")
                else:             
                    set_motors(left_turning_power, -right_turning_power)
                    robot.sleep(0.4)
                    print("Wall detected, turn right")
    
            
    #can't find marker, so rotate
    else:   
        if current_marker == 1 or current_marker == 3 or current_marker == 7:
            print(f"Can't find marker {current_marker}")
            set_motors(-left_turning_power, right_turning_power)
            robot.sleep(0.4)
            set_motors(left_forward_power, right_forward_power)
            robot.sleep(0.2)
        else:
            print(f"Can't find marker {current_marker}")
            set_motors(left_turning_power, -right_turning_power)
            robot.sleep(0.4)
            set_motors(left_forward_power, right_forward_power)
            robot.sleep(0.2)

            
