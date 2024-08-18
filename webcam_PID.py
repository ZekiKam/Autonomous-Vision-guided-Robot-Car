from sbot import Robot
import time
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
left_forward_speed = 0.651
right_forward_speed = 0.65
left_turning_speed = 0.2
right_turning_speed = 0.2




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
lookfor = 1
while True:
    set_motors(0, 0) 
    robot.sleep(0.2) #Time for robot to actually stop
    markers = robot.camera.see()
    target_marker = find_marker(markers, lookfor)
    print("looking for marker " + str(lookfor))
    if target_marker != None:
        current_time = time.time()
        dt = current_time - previous_time
        angle_to_marker = target_marker.position.horizontal_angle
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
        left_speed = left_forward_speed + pid_output_left
        right_speed = right_forward_speed + pid_output_right
        
        
        if angle_to_marker > 0.2:
            print("marker on right")
            set_motors(left_turning_speed, -(right_turning_speed))
            robot.sleep(0.1)
           
        elif angle_to_marker < -0.2:
            print("marker on left")
            set_motors(-(left_turning_speed), right_turning_speed)
            robot.sleep(0.1)
            
        elif target_marker.position.distance > 1000:
            print("marker ahead")
            set_motors(left_forward_speed, right_forward_speed)
            robot.sleep(target_marker.position.distance/2600)  # 2600 speed t=d/v
            if target_marker.position.distance/2 < 1000:
                lookfor += 2 #3 then 5 then 7
                if lookfor > 7:
                    lookfor = 1 #finishes half of the arena, so back to 1 to finish the other half
        

        elif target_marker.position.distance <= 1000:
            lookfor += 2
            if lookfor > 7:
                lookfor = 1
            
            if lookfor == 1 or lookfor == 3 or lookfor == 7:
                set_motors(-0.2, 0.2)
                robot.sleep(0.4)
                print('close enough, turn left')
            else:             
                set_motors(0.2, -0.2)
                robot.sleep(0.4)
                print('close enough, turn right')
            
   
    else:
        if lookfor == 1 or lookfor == 3 or lookfor == 7:
            print("can't find it")
            set_motors(-(left_turning_speed), right_turning_speed)
            robot.sleep(0.4)
            set_motors(0.2,0.2)
            robot.sleep(0.2)
        else:
            print("can't find it")
            set_motors(left_turning_speed, -right_turning_speed)
            robot.sleep(0.4)
            set_motors(0.2, 0.2)
            robot.sleep(0.2)
            
