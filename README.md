# Tin-Car-Rally-Robot

An autonomous robot built on the [Student Robotics](https://studentrobotics.org/) `sbot` API. The robot uses its onboard webcam to detect numbered ArUco fiducial markers placed around a course, then navigates checkpoint-to-checkpoint by steering toward each marker in sequence based on its detected angle and distance.

## How it works

1. The robot's camera (`robot.camera.see()`) scans for visible ArUco markers and returns each one's ID, distance, and horizontal angle relative to the robot.
2. The robot searches for a target marker ID (or pair of IDs), rotating in place if it isn't currently visible.
3. Once a marker is found, the robot steers toward it — either using fixed-threshold turning or a PID control loop — using the marker's angle as the error signal.
4. When the robot gets close enough to the marker, it executes a turn (left or right, depending on which marker/gate it just passed) and advances to the next marker in the sequence.
5. This repeats until the course is complete.

## Hardware / framework requirements

- A Student Robotics competition robot kit (motor board, Arduino board, webcam)
- [`sbot`](https://studentrobotics.org/) — the Student Robotics Python API
- Printed ArUco fiducial markers positioned around the physical course

## Files

| File | Description |
|---|---|
| `webcam_PID_final_used.py` | **Main navigation script.** Detects markers via webcam and steers using independent PID control loops on each motor, with the marker's angle as the error signal. |
| `webcam_no_PID.py` | Earlier version using fixed-angle thresholds instead of PID, with per-marker distance tuning and a motor power offset to compensate for physical motor imbalance. |
| `baseline_example.py` | Minimal baseline example demonstrating marker detection and basic threshold-based steering, without PID. |
| `test_IR_method.py` | Standalone calibration utility — averages 100 IR sensor readings on a purple track surface to determine a detection threshold. Not currently wired into the navigation scripts. |
