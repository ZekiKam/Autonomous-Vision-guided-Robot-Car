from sbot import Robot
import math
import time

robot = Robot()
LeftMotor = robot.motor_board.motors[0]
RightMotor = robot.motor_board.motors[1]

# PID constants
Kp = 0.6
Ki = 0
Kd = 0

integral = 0
previous_error = 0
previous_time = time.time()
pos_power_threshold = 0.6
neg_power_threshold = -0.6

# Helper function to set motor speeds
def set_motors(left, right):
    LeftMotor.power = left
    RightMotor.power = right

# This function checks visible marker list for a specific target
def find_marker(markers, id_pair):
    for marker in markers:
        if marker.id in id_pair:  # Check if marker is in either of the IDs in the pair
            return marker
    return None

# Function to keep adjust robot speed so it will keep aligned with the marker using PID control
def stay_on_track(detected_marker):
    global integral, previous_error, previous_time
    while True:
        # Get the current time and calculate the time difference
        current_time = time.time()
        time_change = current_time - previous_time

        # Calculate the error (angle to the marker)
        angle_to_marker = math.degrees(detected_marker.position.horizontal_angle)
        error = angle_to_marker
        print("Error:",error)

        # PID calculations
        proportional = Kp * error
        if time_change > 0:
            integral += error * time_change
            derivative = (error - previous_error) / time_change
        else:
            integral = 0
            derivative = 0

        pid = proportional + (Ki * integral) + (Kd * derivative)
        print("PID:",pid)

        # Adjust motor speeds based on PID output
        left_power = 0.2 + pid  # Adjust the base speed as needed
        right_power = 0.2 - pid
        
        if left_power > pos_power_threshold: 
            left_power = pos_power_threshold
        elif left_power < neg_power_threshold:
            left_power = neg_power_threshold

        if right_power > pos_power_threshold: 
            right_power = pos_power_threshold
        elif right_power < neg_power_threshold:
            right_power = neg_power_threshold

        # Set the motor speeds
        set_motors(left_power, right_power)

        # Update previous values for next iteration
        previous_error = error
        previous_time = current_time

        # Stop the loop if the robot is close enough to the marker
        distance_to_marker = detected_marker.position.distance
        if distance_to_marker < 800:  # Adjust the stopping distance as needed
            set_motors(0,0)
            print("LOOP FINISHED")
            break
        



# List of marker pairs to detect
id_list = [[0,1],[2,3],[4,5],[6,7]]

# Main loop to iterate through each marker pair
for target_ids in id_list:

    detected_marker = None  # Initialize detected_marker as None

    while True:
        if detected_marker is None:  # If no marker is detected yet
            set_motors(0,0)  # Stop the robot before taking a photo, avoids motion blur
            robot.sleep(0.5)  # Time for robot to actually stop
            markers = robot.camera.see()
            detected_marker = find_marker(markers, target_ids)

            if detected_marker is None:
                print(f"Marker {target_ids} not detected")
                set_motors(-0.2, 0.2)  # Turn slightly to search for markers
                robot.sleep(0.3)
                set_motors(0, 0)
            else:
                print(f"Detected marker {detected_marker.id}")

        # If a marker is detected, move towards it using PID control
        if detected_marker is not None:
            stay_on_track(detected_marker)
            break  # Exit loop and move to next marker pair
