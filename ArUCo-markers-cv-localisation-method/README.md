# ArUCo markers and Computer Vision for Localisation
This module was modified from [ArUCo-Markers-Pose-Estimation-Generation-Python](https://github.com/GSNCodes/ArUCo-Markers-Pose-Estimation-Generation-Python). The original license still applies to this code regardless of these modifications.

## Purpose

The purpose of this module is to convert a video into an array of locations & timestamps like this:
```
[{"location": [108.404, -0.314, 172.88], "timestamp": "2025-09-13 17:59:31.348000"}, 
{"location": [108.378, -0.304, 172.877], "timestamp": "2025-09-13 17:59:31.414000"}, 
...
{"location": [109.216, -0.114, 173.852], "timestamp": "2025-09-13 18:00:02.558000"}]
```

## Equipment Required
* a camera 
    high-quality camera = more precision further away from camera
* a printed ArUCo tag
* a chessboard for calibration 
    printed on paper or a real game board

## Setup Repository

Create a virtual environment
Windows: `python -m venv venv`
Activate virtual environment
Windows: `venv/Scripts/activate`
Install dependencies
`pip install -r requirements.txt`
Setup Done, start localising below 🙃


## Localisation Method

### Step 0: Calibrate camera
This means to find out your current camera calibration including distortion (skew, round distortion) and intrinsic camera properties (focal length, principal point). The calibration output is two matrices which are saved as `intrinsic_matrix.npy` and `distortion_coefficients.npy`.

To calibrate your camera, do:
a. take a video of a chessboard
b. save the video under `previously_calibrated_cameras`
c. open `calibrate_camera.py`
d. adjust `camera_filename, chessboard_size` to match
e. run `python calibrate_camera.py`

### Step 1: Place your camera

During localisation the camera needs to be fixed in the same place. It is ok if the target is moving. Notice where you place your camera i.e. what is the translation and rotation relative to a origin (e.g. corner of building). Adjust these variables in the `measure_locations.py` file:

```
camera_translation = [103.849, 0, 183.396]   # in metres from origin
camera_rotation = [0, 90, 0]
camera = Camera(load_calibration_details_for_camera_name("My Smartphone Camera"),
                camera_translation, camera_rotation)
```

### Step 2: State your ArUCo tag

State how which type of ArUCo tag you printed out and how big it is in cm:

```py
aruco_dict_type = "DICT_5X5_100"
aruco_marker_length = 15.9
```

If you don't have a ArUCo tag, use the following command to generate one and then print it out after:

```
python ./aruco_markers_computer_vision/generate_aruco_tags.py --id 24 --type DICT_5X5_100 --output tags/
```

### Step 3: Record localisation video

Placing your calibrated camera in its correct spot, record a video and specify its location and when you started recording:

```py
video_start_time = datetime(2025, 9, 18, 14, 55, 28)
video_file_path = f"./calculating_location/original_source_videos/{video_name}"
```

### Step 4: Run `python measure_locations.py`

By default, the locations are output to `calculating_location/output` folder.

### <ins>Notes</ins>


If you found this repository useful, take a look at and star ⭐️ the [original repository](https://github.com/GSNCodes/ArUCo-Markers-Pose-Estimation-Generation-Python). 

Feel free to reach out to me or the original author:

Me - arnard76@gmail.com or ashe292@aucklanduni.ac.nz

Original Author - [github.com/GSNCodes](https://github.com/GSNCodes)

Happy Learning! Keep chasing your dreams!

## References
1. https://docs.opencv.org/4.x/d9/d6d/tutorial_table_of_content_aruco.html
2. https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html
