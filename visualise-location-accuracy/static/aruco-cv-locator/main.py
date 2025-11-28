from pyscript.web import page, when
from pyodide.http import open_url
from pyscript import display, fetch
from js import console

import numpy as np
from datetime import datetime
import json
import zoneinfo
from aruco_markers_cv_localisation_arnard76.aruco_markers_computer_vision.utils import ARUCO_DICT
from aruco_markers_cv_localisation_arnard76.calculating_location.pose_estimation import find_marker_locations_from_video
from aruco_markers_cv_localisation_arnard76.camera_calibration.camera import Camera
from aruco_markers_cv_localisation_arnard76.camera_calibration import load_calibration_details_for_camera_name, default_calibration_folder, default_intrinsic_matrix_filename, default_distortion_coeffecients_filename
from aruco_markers_cv_localisation_arnard76.mega.mega import Mega

def log(message):
    # log to pandas dev console
    print(message)
    # log to JS console
    console.log(message)

class InputsForArucoCVLocations:
    megaLink: str
    videoStartDateTime: str  # is this available from mega?
    camera: dict  # contains rotation, location, name (for calibration details)

    def __init__(self):
        pass

    def already_processed(self):
        file_path = self.store_video_location()
        return os.path.exists(file_path)  

    @property
    def locations_data(self):
        with open(self.store_video_location(), "r") as file:
            return json.load(file)      
    
    def store_video_location(self):
        return f'./calculating_location/output/locations-{self.megaLink.replace("."," ")}{str(self.videoStartDateTime).replace(":", "-")}.json'
        # return "./calculating_location/output/locations-"


@when("click", "button")
async def loadFromURL(event):
    print("loading...")
    inputs = InputsForArucoCVLocations()
    # inputs.megaLink = "https://mega.nz/file/XF0gQL4b#GJs9D9s4iC4ECfs-g9cTA4Mdry8fKshty6oMoJj0O_8"
    inputs.megaLink = page["input#mega-video-link"][0].value
    locations = await calculate_locations(inputs)
    print("locations", locations)
    # page["div#pandas-output"][0].style["display"] = "block"
    # page["div#pandas-dev-console"][0].style["display"] = "block"

    # display(locations, target="pandas-output-inner", append="False")

async def calculate_locations(inputs):
    print(inputs)
    # SCIENCE CENTRE 3-DEMO CAMERA SETUP
    # camera_translation = [73.89, 0, 136.71]   # in metres from origin
    # camera_rotation = [0, 102.6-180, 0]
    camera_translation = [5.32, 0, 10.49]  # in metres from origin
    camera_rotation = [0, 180, 180]
    camera_name="Arnav phone"
    # calibration_details = 
    # Dynamically fetch the file from the server
    # The URL assumes the file is in the same directory as the HTML file
    # distortion_coefficients = await (await fetch("/camera_calibration/previously_calibrated_cameras/Arnav phone/distortion_coefficients.npy")).json()
    # intrinsic_matrix = await (await fetch("/camera_calibration/previously_calibrated_cameras/Arnav phone/intrinsic_matrix.npy")).json()
    # camera_calibration_details = await (await fetch("./camera_calibration/previously_calibrated_cameras/Arnav phone/Arnav phone.txt")).json()
    camera = Camera(
        {"intrinsic_matrix": np.load(default_calibration_folder(camera_name) + "/" + default_intrinsic_matrix_filename),
            "distortion_coefficients": np.load(default_calibration_folder(camera_name) + "/" + default_distortion_coeffecients_filename)},
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
    output_filepath = inputs.store_video_location()
    with open(output_filepath, "w") as output_file:
        json.dump(locations, output_file)
    return locations


