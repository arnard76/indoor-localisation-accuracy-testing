"""
This is the full example to measure the current locations of an aruco marker given a calibrated camera

CALIBRATE NEW CAMERAS BEFORE MEASURING LOCATION
use `calibrate_camera.py`
"""

from datetime import datetime
import json
import zoneinfo
from aruco_markers_computer_vision.utils import ARUCO_DICT
from calculating_location.pose_estimation import locate_marker_from_live_video
from camera_calibration.camera import Camera
from camera_calibration import load_calibration_details_for_camera_name
from mega.mega import Mega
import os

from datetime import datetime
start_time = datetime.now()

# Camera setup
camera_translation = [0, 0, 0]  # in metres from origin
camera_rotation = [0, 0, 0]
camera = Camera(
    load_calibration_details_for_camera_name("Arnav laptop"),
    camera_translation,
    camera_rotation,
)

# Marker Config
aruco_dict_type = "DICT_5X5_100"
aruco_marker_length = 19.0

# Video details
current_timezone = zoneinfo.ZoneInfo("Pacific/Auckland")
# video_url = "https://mega.nz/file/cZ1VXCBJ#R1X3ZRAynZ3gXpSc8n2D0CikCog88LwBjpNgU1l9tC8"
# mega = Mega()
# m = mega.login()
# video_folder_path = "./calculating_location/input_videos/"
# video_file_name="real-world-test-mohammed-phone-16-04-2026-9-33-49.MOV"
# video_file_name = f"Tracking Robot {str(video_start_time).replace(':', '-')}.mp4"
# m.download_url(video_url, video_folder_path, video_file_name)
video_source = 0

# Result
locations = locate_marker_from_live_video(
    video_source,
    ARUCO_DICT[aruco_dict_type],
    aruco_marker_length,
    camera,
    True
)

print(locations)
output_folder = "./calculating_location/output/"
output_filepath = f'{output_folder}/locations-video{video_source}-{str(start_time).replace(":", "-")}.json'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

with open(output_filepath, "w") as output_file:
    json.dump(locations, output_file)

print("Time taken: "+ str(datetime.now() - start_time))