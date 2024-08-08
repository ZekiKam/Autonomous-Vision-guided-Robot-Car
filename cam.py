from sbot import Robot
import math
robot = Robot()
# Name the motors to make it easier
LeftMotor = robot.motor_board.motors[0]
RightMotor = robot.motor_board.motors[1]
# Helper function to set motor speeds
def set_motors(left, right):
    LeftMotor.power = left
    RightMotor.power = right
# This function checks visible maker list for a specific target
def find_marker(markers, id_number):
    for marker in markers:
        if marker.id == id_number:
            return marker
    return None

set_motors(0.2, 0.2)
robot.sleep(1)
set_motors(0,0)
target_id = 1
distance = [1000,1200]
for target_id in [1,3,5]:
    while True:
        set_motors(0, 0) #Stop the robot before taking a photo, avoids motion blur
        robot.sleep(0.2) #Time for robot to actually stop
        markers = robot.camera.see()
        target_marker = find_marker(markers, target_id)
        if target_marker != None:
            angle_to_marker = math.degrees(target_marker.position.horizontal_angle)
            if angle_to_marker > 10: #REPLACE X WITH SUITABLE VALUE
                set_motors(0.05,-0.05)
                robot.sleep(0.25)
                set_motors(0,0)
            #ADD CODE HERE TO TURN TOWARD MARKER
            elif angle_to_marker < -10: #REPLACE X WITH SUITABLE VALUE
                set_motors(-0.05,0.05)
                robot.sleep(0.25)
                set_motors(0,0)
            #ADD CODE HERE TO TURN TOWARD MARKER
            elif target_marker.position.distance > 750: #REPLACE Y WITH SUITABLE DISTANCE
                set_motors(0.2,0.2)
                robot.sleep(0.5)
                set_motors(0,0)
            elif target_marker.position.distance < 750: #REPLACE Y WITH SUITABLE DISTANCE
                set_motors(-0.15,0.15)
                robot.sleep(0.5)
                set_motors(0,0)
            elif target_marker.position.distance < distance[0]
