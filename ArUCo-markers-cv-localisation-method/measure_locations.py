"""
This is the full example to measure locations of an aruco marker given a calibrated camera

CALIBRATE NEW CAMERAS BEFORE MEASURING LOCATION 
use `calibrate_camera.py`

TODO: turn this file into a jupyter notebook for an easy-to-follow guide
"""

from datetime import datetime
import json
import zoneinfo
from aruco_markers_computer_vision.utils import ARUCO_DICT
from calculating_location.pose_estimation import find_marker_locations_from_video
from camera_calibration.camera import Camera
from camera_calibration import load_calibration_details_for_camera_name

# SCIENCE CENTRE 3-DEMO CAMERA SETUP
# camera_translation = [73.89, 0, 136.71]   # in metres from origin
# camera_rotation = [0, 102.6-180, 0]
camera_translation = [5.32, 0, 10.49]   # in metres from origin
camera_rotation = [0, 180, 180]
camera = Camera(load_calibration_details_for_camera_name("Arnav phone"),
                camera_translation, camera_rotation)


# Find locations
aruco_dict_type = "DICT_5X5_100"
aruco_marker_length = 15.9
current_timezone = zoneinfo.ZoneInfo('Pacific/Auckland')
video_start_time = datetime(2025, 9, 21, 14, 57, 50, tzinfo=current_timezone)
video_file_name = "Arnav home demo.mp4"
video_file_path = "./calculating_location/input_videos/" + video_file_name

locations = find_marker_locations_from_video(
    video_file_path, video_start_time, ARUCO_DICT[aruco_dict_type], aruco_marker_length, camera)

print(locations)
output_filepath = f'./calculating_location/output/locations-{video_file_name.replace("."," ")}{str(video_start_time).replace(":", "-")}.json'
with open(output_filepath, 'w') as output_file:
    json.dump(locations, output_file)
