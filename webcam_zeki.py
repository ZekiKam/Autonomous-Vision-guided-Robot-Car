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

def stayonline(angle_to_marker):
    if angle_to_marker > 10: #REPLACE X WITH SUITABLE VALUE
        print("FAR RIGHT")
        set_motors(0.05,-0.05)
        robot.sleep(0.25)
        set_motors(0,0)

    #ADD CODE HERE TO TURN TOWARD MARKER
    elif angle_to_marker < -10: #REPLACE X WITH SUITABLE VALUE
        print("FAR LEFT")
        set_motors(-0.05,0.05)
        robot.sleep(0.25)
        set_motors(0,0)
        
    else: #on track
        set_motors(0.2,0.2)
        robot.sleep(0.5)
        set_motors(0,0)
    
def stayonline67(angle_to_marker):
    if angle_to_marker > 55:
        print("FAR RIGHT")
        set_motors(0.05,-0.05)
        robot.sleep(0.25)
        set_motors(0,0)
        
    elif angle_to_marker > 35:
        print("FAR LEFT")
        set_motors(-0.05,0.05)
        robot.sleep(0.25)
        set_motors(0,0)
    
    else: #on track
        set_motors(0.2,0.2)
        robot.sleep(0.5)
        set_motors(0,0)
        
        
      
exit = False
for target_id in [1,3,5,7]:
    while True:
        set_motors(0.05, 0.05) #Stop the robot before taking a photo, avoids motion blur
        robot.sleep(0.2) #Time for robot to actually stop
        markers = robot.camera.see()
        target_marker = find_marker(markers, target_id)
        if target_marker != None:
            angle_to_marker = math.degrees(target_marker.position.horizontal_angle)

            if target_id ==1:
                if target_marker.position.distance > 750: #REPLACE Y WITH SUITABLE DISTANCE
                    print("far away1")
                    stayonline(angle_to_marker)
                elif target_marker.position.distance < 750: #REPLACE Y WITH SUITABLE DISTANCE
                    print("close")
                    set_motors(-0.15,0.15)
                    robot.sleep(0.5)
                    set_motors(0,0)
                    break
                
            elif target_id == 3:
                if target_marker.position.distance > 1000: #REPLACE Y WITH SUITABLE DISTANCE
                    print("far away")   
                    stayonline(angle_to_marker)
                elif target_marker.position.distance < 1000: #REPLACE Y WITH SUITABLE DISTANCE
                    set_motors(0.1,-0.1)
                    robot.sleep(0.5)
                    set_motors(0,0)
                    break
                
            elif target_id == 5:
                if target_marker.position.distance > 1000: #REPLACE Y WITH SUITABLE DISTANCE
                    stayonline(angle_to_marker)
                elif target_marker.position.distance < 1000: #REPLACE Y WITH SUITABLE DISTANCE
                    set_motors(-0.1,0.1)
                    robot.sleep(0.8)
                    set_motors(0,0)
                    exit = True
                    break
            
            elif target_id == 7:
                if target_marker.position.distance > 1000: #REPLACE Y WITH SUITABLE DISTANCE
                    stayonline67(angle_to_marker)
                elif target_marker.position.distance < 1000: #REPLACE Y WITH SUITABLE DISTANCE
                    set_motors(-0.1,0.1)
                    robot.sleep(0.8)
                    set_motors(0,0)
                    exit = True
                    break
                
    if exit:
        break

print("Loop finished")
 
#45 degree turn handled as 90
set_motors(-0.4,0.4)
robot.sleep(1)         
ultra_distance = robot.arduino.ultrasound_measure(2,3)
while ultra_distance > 500:
    ultra_distance = robot.arduino.ultrasound_measure(2,3)
    print("Ultrasound:",ultra_distance)
    set_motors(0.4,0.4)
    robot.sleep(0.5)
    set_motors(0,0)
    
set_motors(0,0)
