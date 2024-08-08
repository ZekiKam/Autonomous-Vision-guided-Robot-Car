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


marker_ids = [1, 3, 5]
target_distances = [750, 1000, 1200]  


# Main loop function
def loop(target_id, target_distance):
    while True:
        set_motors(0, 0)  
        robot.sleep(0.2)  
        markers = robot.camera.see()
        target_marker = find_marker(markers, target_id)

        if target_marker != None:
            angle_to_marker = math.degrees(target_marker.position.horizontal_angle)
            if angle_to_marker > 10:  
                set_motors(0.05, -0.05)  # Turn right
                robot.sleep(0.25)
                set_motors(0, 0)
            elif angle_to_marker < -10:  
                set_motors(-0.05, 0.05)  # Turn left
                robot.sleep(0.25)
                set_motors(0, 0)
            elif target_marker.position.distance > target_distance + 100:  
                set_motors(0.2, 0.2)
                robot.sleep(0.5)
                set_motors(0, 0)
            elif target_marker.position.distance < target_distance - 100:  
                set_motors(-0.15, -0.15)
                robot.sleep(0.5)
                set_motors(0, 0)
            else:
                break  

for i in range(len(marker_ids)):
    loop(marker_ids[i], target_distances[i])
