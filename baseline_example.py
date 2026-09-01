from sbot import Robot
robot = Robot()

LeftMotor = robot.motor_board.motors[0]
RightMotor = robot.motor_board.motors[1]

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

lookfor = 1
while True:
    set_motors(0, 0) 
    robot.sleep(0.2) #Time for robot to actually stop
    markers = robot.camera.see()
    target_marker = find_marker(markers, lookfor)
    print("looking for marker " +str(lookfor))
    if target_marker != None:
        angle_to_marker = target_marker.position.horizontal_angle
        distance = target_marker.position.distance
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
            robot.sleep(target_marker.position.distance/2600)
            if target_marker.position.distance/2 < 1000:
                lookfor += 2
                if lookfor > 7:
                    lookfor = 1
        

        elif target_marker.position.distance <= 1000:
            lookfor += 2
            if lookfor > 7:
                lookfor = 1
            
            if lookfor == 1 or lookfor == 7 or lookfor == 3:
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
