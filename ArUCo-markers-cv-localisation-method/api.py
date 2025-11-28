import os
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import json
import zoneinfo
from aruco_markers_computer_vision.utils import ARUCO_DICT
from calculating_location.pose_estimation import find_marker_locations_from_video
from camera_calibration.camera import Camera
from camera_calibration import calibrate, save_calibration_details, load_calibration_details_for_camera_name
from image_video_conversion import video_to_frames, delete_frames_after_use
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


class InputsForCameraCalibration(BaseModel):
    cameraName: str | None = None
    megaLink: str | None = None

    def is_calibration_completed(self, calibration_output_folder:str):
        if not self.cameraName: 
            return False

        folder = os.path.join(calibration_output_folder, self.cameraName)
        return os.path.exists(os.path.join(folder, "distortion_coefficients.npy")) and os.path.exists(os.path.join(folder, "intrinsic_matrix.npy"))

@app.post("/calibrate")
async def calibrate_camera(camera_calibration_inputs: InputsForCameraCalibration):
    calibration_video_input_folder = "./camera_calibration/previously_calibrated_cameras/"
    
    if camera_calibration_inputs.is_calibration_completed(calibration_video_input_folder):
        return {"status": "finished"}
    
    if not camera_calibration_inputs.megaLink:
        raise HTTPException(status_code=400, detail="Camera with this name hasn't been calibrated yet, and no mega link to the calibration video was provided.")

    mega = Mega()
    m = mega.login()
    video_file_url = camera_calibration_inputs.megaLink
    # video_file_url = (
    #     "https://mega.nz/file/XF0gQL4b#GJs9D9s4iC4ECfs-g9cTA4Mdry8fKshty6oMoJj0O_8"
    # )
    camera_filename = os.path.basename(m.download_url(video_file_url, calibration_video_input_folder, camera_calibration_inputs.cameraName))
    # camera_filename = "Arnav phone.mp4"
    print(camera_filename)
    camera_video_file_path = os.path.join(calibration_video_input_folder, camera_filename)
    camera_filename_without_file_type = camera_filename.split(".")[0]
    frames_folder = camera_filename_without_file_type + "/frames"
    video_to_frames(camera_video_file_path, calibration_video_input_folder + frames_folder)

    # Find Calibration Matrices
    chessboard_size = 30  # the width and height in cm of chessboard
    NUM_SQUARES_IN_CHESSBOARD = 8
    NUM_INNER_VERTICES = NUM_SQUARES_IN_CHESSBOARD - 1
    calibration_details = calibrate(
        calibration_video_input_folder + frames_folder, chessboard_size, width=NUM_INNER_VERTICES, height=NUM_INNER_VERTICES)
    print(calibration_details)
    save_calibration_details(
        calibration_details, camera_filename_without_file_type)
    
    delete_frames_after_use(calibration_video_input_folder + frames_folder)
    if os.path.exists(camera_video_file_path):
        os.remove(camera_video_file_path)
    return {"status": "finished", "cameraName": camera_filename_without_file_type}
