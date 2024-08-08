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
while True:
    set_motors(0, 0) #Stop the robot before taking a photo, avoids motion blur
    robot.sleep(0.2) #Time for robot to actually stop
    markers = robot.camera.see()
    target_marker = find_marker(markers, 1)
    if target_marker != None:
        angle_to_marker = math.degrees(target_marker.position.horizontal_angle)
    if angle_to_marker > 5: #REPLACE X WITH SUITABLE VALUE
        set_motors(-0.2,0.2)
        robot.sleep(0.5)
        set_motors(0,0)
    #ADD CODE HERE TO TURN TOWARD MARKER
    elif angle_to_marker < -5: #REPLACE X WITH SUITABLE VALUE
        set_motors(0.2,-0.2)
        robot.sleep(0.5)
        set_motors(0,0)
    #ADD CODE HERE TO TURN TOWARD MARKER
    elif target_marker.position.distance > 500: #REPLACE Y WITH SUITABLE DISTANCE
        print("close")
#ADD CODE HERE TO GO FORWARD
#ADD CODE HERE TO FIND NEXT MARKER AND COMPLETE HALF A LAP
