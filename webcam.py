from sbot import Robot
import math
robot = Robot()
offset = 1.05
# Name the motors to make it easier
LeftMotor = robot.motor_board.motors[0]
RightMotor = robot.motor_board.motors[1]
# Helper function to set motor speeds
def set_motors(left, right):
    LeftMotor.power = left * offset
    RightMotor.power = right
# This function checks visible maker list for a specific target
def find_marker(markers, id_number):
    for marker in markers:
        if marker.id == id_number:
            return marker
    return None
def stayonline():
    if angle_to_marker > 10: #REPLACE X WITH SUITABLE VALUE
        print("far right")
        set_motors(0.05,-0.05)
        robot.sleep(0.25)
        set_motors(0,0)

    #ADD CODE HERE TO TURN TOWARD MARKER
    elif angle_to_marker < -10: #REPLACE X WITH SUITABLE VALUE
        print("FAR LEFT")
        set_motors(-0.05,0.05)
        robot.sleep(0.25)
        set_motors(0,0)

distance = [1000,1200]
for target_id in [1,3,5,6]:
    while True:
        set_motors(0, 0) #Stop the robot before taking a photo, avoids motion blur
        robot.sleep(0.2) #Time for robot to actually stop
        markers = robot.camera.see()
        target_marker = find_marker(markers, target_id)
        if target_marker != None:
            angle_to_marker = math.degrees(target_marker.position.horizontal_angle)
            stayonline()

            if target_id ==1:
            #ADD CODE HERE TO TURN TOWARD MARKER
                if target_marker.position.distance > 750: #REPLACE Y WITH SUITABLE DISTANCE
                    print("far away")
                    set_motors(0.2,0.2)
                    robot.sleep(0.5)
                    set_motors(0,0)
                elif target_marker.position.distance < 750: #REPLACE Y WITH SUITABLE DISTANCE
                    print("close")
                    set_motors(-0.15,0.15)
                    robot.sleep(0.5)
                    set_motors(0,0)
                    break
                
            elif target_id == 3:
                if target_marker.position.distance > 1000: #REPLACE Y WITH SUITABLE DISTANCE
                    set_motors(0.2,0.2)
                    robot.sleep(0.5)
                    set_motors(0,0)
                elif target_marker.position.distance < 1000: #REPLACE Y WITH SUITABLE DISTANCE
                    set_motors(0.1,-0.1)
                    robot.sleep(0.5)
                    set_motors(0,0)
                    break
                
            elif target_id == 5:
                if target_marker.position.distance > 1000: #REPLACE Y WITH SUITABLE DISTANCE
                    set_motors(0.2,0.2)
                    robot.sleep(0.75)
                    set_motors(0,0)
                elif target_marker.position.distance < 1000: #REPLACE Y WITH SUITABLE DISTANCE
                    set_motors(-0.4,0.4)
                    robot.sleep(0.8)
                    set_motors(0,0)
                    break
            
            elif target_id == 6:
                if target_marker.position.distance > 800: #REPLACE Y WITH SUITABLE DISTANCE
                    set_motors(0.2,0.2)
                    robot.sleep(0.5)
                    set_motors(0,0)
                elif target_marker.position.distance < 800: #REPLACE Y WITH SUITABLE DISTANCE
                    set_motors(-0.15,0.15)
                    robot.sleep(0.5)
                    set_motors(0,0)
                    break
                
                
