"""
This is the full example to measure locations of an aruco marker given a calibrated camera

CALIBRATE NEW CAMERAS BEFORE MEASURING LOCATION
use `calibrate_camera.py`
"""

import os
from fastapi import FastAPI, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import json
import zoneinfo
from aruco_markers_computer_vision.utils import ARUCO_DICT
from calculating_location.pose_estimation import find_marker_locations_from_video
from camera_calibration.camera import Camera
from camera_calibration import load_calibration_details_for_camera_name
from mega.mega import Mega
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

origins = [
    "https://indoor-localisation-accuracy-testin.vercel.app",
    "https://wifinder-accuracy-testing-tool.vercel.app",
    "http://localhost:5173",
    "https://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/aruco-cv-videos",
    StaticFiles(directory="calculating_location/input_videos"),
    name="static",
)

class InputsForArucoCVLocations(BaseModel):
    megaLink: str
    videoStartDateTime: str  # is this available from mega?
    camera: dict  # contains rotation, location, name (for calibration details)

    # def __init__(self, megaLink:str, videoStartDateTime:str, camera: str):
    #     self.megaLink = megaLink
    #     self.videoStartDateTime = videoStartDateTime
    #     self.camera = camera

    def already_processed(self):
        file_path = self.store_aruco_locations()
        return os.path.exists(file_path)  

    @property
    def locations_data(self):
        with open(self.store_aruco_locations(), "r") as file:
            return json.load(file)      
    
    def store_aruco_locations(self):
        return f'./calculating_location/output/locations-{self.megaLink.replace("https://mega.nz/file/","")}{str(self.videoStartDateTime).replace(":", "-")}.json'
        # return "./calculating_location/output/locations-"


@app.post("/")
async def start_localising_video(inputs: InputsForArucoCVLocations, background_tasks: BackgroundTasks):
    if inputs.already_processed():
        return {"status": "finished", "locations":inputs.locations_data}

    # validate inputs:
    #   check mega video exists
    #   check camera calibration details exist on server
    #   data format for camera rotation and translation
    # check that video timestamp is in the past :)
    # create link using the camera and timestamp
    background_tasks.add_task(calculate_locations, inputs)
    return {"status": "started processing...", "locations": None}

def calculate_locations(inputs:InputsForArucoCVLocations):
    print(inputs)
    # SCIENCE CENTRE 3-DEMO CAMERA SETUP
    # camera_translation = [73.89, 0, 136.71]   # in metres from origin
    # camera_rotation = [0, 102.6-180, 0]
    camera_translation = [5.32, 0, 10.49]  # in metres from origin
    camera_rotation = [0, 180, 180]
    camera = Camera(
        load_calibration_details_for_camera_name(inputs.camera["name"]),
        camera_translation,
        camera_rotation,
    )

    # Find locations
    aruco_dict_type = "DICT_5X5_100"
    aruco_marker_length = 15.9
    current_timezone = zoneinfo.ZoneInfo("Pacific/Auckland")
    video_start_time = datetime(2025, 9, 21, 14, 57, 50, tzinfo=current_timezone)
    mega = Mega()
    m = mega.login()
    video_folder_path = "./calculating_location/input_videos/"
    video_file_url = inputs.megaLink
    # video_file_url = (
    #     "https://mega.nz/file/XF0gQL4b#GJs9D9s4iC4ECfs-g9cTA4Mdry8fKshty6oMoJj0O_8"
    # )
    video_file_path = m.download_url(video_file_url, video_folder_path)

    locations = find_marker_locations_from_video(
        str(video_file_path),
        video_start_time,
        ARUCO_DICT[aruco_dict_type],
        aruco_marker_length,
        camera,
        visualise=True,
    )

    print(locations)
    output_filepath = inputs.store_aruco_locations()
    with open(output_filepath, "w") as output_file:
        json.dump(locations, output_file)
    return locations


