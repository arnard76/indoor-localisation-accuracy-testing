import sys
from aruco_markers_computer_vision.utils import ARUCO_DICT
import argparse
from datetime import datetime
from calculating_location.pose_estimation import find_marker_locations_from_video
from camera_calibration import load_calibration_details_from_file
from camera_calibration.camera import Camera

distance_metres = 16
same_distance_pixels = 106
pixels_to_metres_scale = distance_metres / same_distance_pixels
camera_translation = [726 * pixels_to_metres_scale,
                      0, 1154 * pixels_to_metres_scale]   # in metres
# matches the predication translation so pitch, roll, yaw (not roll,pitch, yaw)
camera_rotation = [0, 130, 0]


if __name__ == '__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video_source", required=True,
                    help="Path to the video file to analyse OR a camera index for live video")
    ap.add_argument("-k", "--K_Matrix",
                    help="Path to calibration matrix (numpy file)", default="./camera_calibration/output/calibration_matrix.npy")
    ap.add_argument("-d", "--D_Coeff",
                    help="Path to distortion coefficients (numpy file)", default="./camera_calibration/output/distortion_coefficients.npy")
    ap.add_argument("-t", "--type", type=str,
                    default="DICT_ARUCO_ORIGINAL", help="Type of ArUCo tag to detect")
    args = vars(ap.parse_args())

    if ARUCO_DICT.get(args["type"], None) is None:
        print(f"ArUCo tag type '{args['type']}' is not supported")
        sys.exit(0)

    video_source = args['video_source']
    aruco_dict_type = ARUCO_DICT[args["type"]]
    aruco_marker_length = 15.9
    start_time = datetime(2025, 9, 13, 17, 59, 5)

    camera = Camera(load_calibration_details_from_file(
        args["K_Matrix"], args["D_Coeff"]), camera_translation, camera_rotation)

    find_marker_locations_from_video(
        video_source, start_time, aruco_dict_type, aruco_marker_length, camera)
