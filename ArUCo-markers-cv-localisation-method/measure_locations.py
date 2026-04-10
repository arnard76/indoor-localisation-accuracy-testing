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
from mega.mega import Mega
import os

# SCIENCE CENTRE 3-DEMO CAMERA SETUP
# camera_translation = [73.89, 0, 136.71]   # in metres from origin
# camera_rotation = [0, 102.6-180, 0]
camera_translation = [ 6.57,0,4.22   ]  # in metres from origin
camera_rotation = [90, 0, 50-90]
camera = Camera(
    load_calibration_details_for_camera_name("Arnav phone"),
    camera_translation,
    camera_rotation,
)


# Find locations
aruco_dict_type = "DICT_5X5_100"
aruco_marker_length = 19.0
current_timezone = zoneinfo.ZoneInfo("Pacific/Auckland")
video_start_time = datetime(2025, 9, 21, 14, 57, 50, tzinfo=current_timezone)

video_url = "https://mega.nz/file/cZ1VXCBJ#R1X3ZRAynZ3gXpSc8n2D0CikCog88LwBjpNgU1l9tC8"
mega = Mega()
m = mega.login()
video_folder_path = "./calculating_location/input_videos/"
video_file_name = f"Tracking Robot {str(video_start_time).replace(':', '-')}.mp4"
m.download_url(video_url, video_folder_path, video_file_name)

locations = find_marker_locations_from_video(
    video_folder_path + video_file_name,
    video_start_time,
    ARUCO_DICT[aruco_dict_type],
    aruco_marker_length,
    camera,
)

print(locations)
output_folder = "./calculating_location/output/"
output_filepath = f'{output_folder}/locations-{video_file_name.replace("."," ")}{str(video_start_time).replace(":", "-")}.json'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

with open(output_filepath, "w") as output_file:
    json.dump(locations, output_file)

