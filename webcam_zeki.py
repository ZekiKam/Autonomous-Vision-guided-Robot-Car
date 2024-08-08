from sbot import Robot
import math
import time
robot = Robot()
offset = 1.08

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
    if angle_to_marker > 10: #turn right when the angle is to large
        print("far right")
        set_motors(0.15, -0.15)
        robot.sleep(0.25)
        time.sleep(0.5)
        set_motors(0,0)

    
    elif angle_to_marker < -10: #REPLACE X WITH SUITABLE VALUE
        print("FAR LEFT")
        set_motors(-0.05,0.05)
        robot.sleep(0.25)
        set_motors(0,0)

distance = [1000,1200]
for target_id in [1,3,5,6]:

    while True:
        set_motors(0, 0) #Stop the robot before taking a photo, avoids motion blur
        robot.sleep(0.75) #Time for robot to actually stop
        markers = robot.camera.see()
        target_marker = find_marker(markers, target_id)

        if target_marker == None:
            print("not detected")
            #search for any markers nearby
            set_motors(-0.2, 0.2)
            robot.sleep(0.3)
            set_motors(0,0)
        
        elif target_marker != None:
            print(f"detected {target_id}")
            angle_to_marker = math.degrees(target_marker.position.horizontal_angle)
            stayonline()

            if target_id ==1:

            #ADD CODE HERE TO TURN TOWARD MARKER
                if target_marker.position.distance > 780: #REPLACE Y WITH SUITABLE DISTANCE

                    print("far away")
                    set_motors(0.5,0.5)
                    robot.sleep(0.5)
                    set_motors(0,0)
                    robot.sleep(0.5)
                elif target_marker.position.distance > 750 and target_marker.position.distance< 780:
                    print("slower")
                    set_motors(0.2,0.2)
                    robot.sleep(0.75)
                    set_motors(0,0)
                elif target_marker.position.distance < 750: #REPLACE Y WITH SUITABLE DISTANCE

                    print("close")
                    set_motors(-0.15,0.15)
                    robot.sleep(0.75)
                    set_motors(0,0)
                    break
                
            elif target_id == 3:
                if target_marker.position.distance > 1200: #REPLACE Y WITH SUITABLE DISTANCE

                    set_motors(0.5,0.5)
                    robot.sleep(0.5)
                    set_motors(0,0)
                    robot.sleep(0.5)
                elif target_marker.position.distance > 1000 and target_marker.position.distance< 1200:
                    print("slower")
                    set_motors(0.2,0.2)
                    robot.sleep(0.75)
                    set_motors(0,0)
                elif target_marker.position.distance < 1000: #REPLACE Y WITH SUITABLE DISTANCE

                    set_motors(0.1,-0.1)
                    robot.sleep(0.5)
                    set_motors(0,0)
                    break
                
            elif target_id == 5:
                if target_marker.position.distance > 900: #REPLACE Y WITH SUITABLE DISTANCE, rememeber touse reasonable range!
                    set_motors(0.5,0.5)
                    robot.sleep(0.75)
                    set_motors(0,0)
        
                elif target_marker.position.distance > 770 and target_marker.position.distance< 900:
                    print("slower")
                    set_motors(0.2,0.2)
                    robot.sleep(0.75)
                    set_motors(0,0)
                elif target_marker.position.distance < 770: #REPLACE Y WITH SUITABLE DISTANCE

                    set_motors(-0.4,0.4)
                    robot.sleep(0.8)
                    set_motors(0,0)
                    break
            
            elif target_id == 6:

                if target_marker.position.distance > 800: #REPLACE Y WITH SUITABLE DISTANCE

                    set_motors(0.2,0.2)
                    robot.sleep(0.5)
                    set_motors(0,0)
                elif target_marker.position.distance > 780 and target_marker.position.distance< 800:
                    print("slower")
                    set_motors(0.2,0.2)
                    robot.sleep(0.75)
                    set_motors(0,0)
                elif target_marker.position.distance < 780: #REPLACE Y WITH SUITABLE DISTANCE

                    set_motors(-0.15,0.15)
                    robot.sleep(0.5)
                    set_motors(0,0)
                    break
