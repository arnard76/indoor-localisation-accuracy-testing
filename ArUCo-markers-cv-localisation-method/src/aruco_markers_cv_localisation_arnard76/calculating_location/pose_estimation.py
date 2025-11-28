'''
Sample Usage:-
python pose_estimation.py --K_Matrix calibration_matrix.npy --D_Coeff distortion_coefficients.npy --type DICT_5X5_100
'''


from datetime import datetime, timedelta
import os
import sys
import time
import numpy as np
import cv2
from aruco_markers_cv_localisation_arnard76.calculating_location.coordinates_conversions import transform_camera_to_world_coordinates
from aruco_markers_cv_localisation_arnard76.aruco_markers_computer_vision.utils import draw_aruco_marker_squares
from aruco_markers_cv_localisation_arnard76.camera_calibration.camera import Camera


def estimate_marker_pose(frame, aruco_dict_type, aruco_marker_length, camera: Camera, resize=1.0):
    '''
    inputs:
        frame - opencv frame from video or image
        aruco_dict_type - what is the format of the aruco marker e.g. 5 by 5 squares (5X5)
        aruco_marker_length - how wide (in cm) the marker is in the real world


    returns the first marker found (if any):
        frame with marker highlighted
        translation of marker from camera
        rotation of the marker from camera
    '''

    def resize_graphic_position(og_position):
        return og_position / resize

    def resize_graphic_positions(og_positions: tuple | list):
        return [round(resize_graphic_position(og_pos)) for og_pos in og_positions]

    aruco_dict = cv2.aruco.getPredefinedDictionary(aruco_dict_type)
    arucoParams = cv2.aruco.DetectorParameters()
    arucoDetector = cv2.aruco.ArucoDetector(aruco_dict, arucoParams)
    corners, ids, rejected = arucoDetector.detectMarkers(frame)
    augmented_frame = draw_aruco_marker_squares(corners, ids, rejected, frame)

    half_len = aruco_marker_length / 2.0
    objpts = np.array([
        [-half_len,  half_len, 0],  # top-left
        [half_len,  half_len, 0],  # top-right
        [half_len, -half_len, 0],  # bottom-right
        [-half_len, -half_len, 0]   # bottom-left
    ], dtype=np.float32)

    # If markers are detected
    if len(corners) > 0:
        for _ in range(0, len(ids)):
            imgpts = corners[0].reshape(-1, 2)  # (4,2)

            retval, marker_rotation_vector, marker_translation_vector = cv2.solvePnP(
                objpts, imgpts, camera.intrinsic_matrix, camera.distortion_coefficients
            )

            if (not retval):
                continue

            # Display Marker Position
            marker_rotation_degrees = np.degrees(marker_rotation_vector)
            marker_translation_metres = marker_translation_vector / 100
            font_size = resize_graphic_position(0.5)
            marker_translation_metres = [float(marker_translation_metres[0][0]),
                                         float(marker_translation_metres[1][0]), float(marker_translation_metres[2][0])]
            augmented_frame = cv2.putText(augmented_frame, f"x: {round(marker_translation_metres[0], 3)}", resize_graphic_positions((30,  30)), cv2.FONT_HERSHEY_SIMPLEX,
                                          font_size, (0, 238, 45), 2)
            augmented_frame = cv2.putText(augmented_frame, f"y (ignore): {round(marker_translation_metres[1], 3)}", resize_graphic_positions((30,  60)), cv2.FONT_HERSHEY_SIMPLEX,
                                          font_size, (0, 238, 45), 2)
            augmented_frame = cv2.putText(augmented_frame, f"z: {round(marker_translation_metres[2], 3)}", resize_graphic_positions((30,  90)), cv2.FONT_HERSHEY_SIMPLEX,
                                          font_size, (0, 238, 45), 2)

            # Display Marker Rotation (not needed)
            # augmented_frame = cv2.putText(augmented_frame, f"pitch: {round(marker_rotation_degrees[0][0])}", (30,  150), cv2.FONT_HERSHEY_SIMPLEX,
            #                               0.5, (255, 0, 0), 2)
            # augmented_frame = cv2.putText(augmented_frame, f"roll: {round(marker_rotation_degrees[1][0])}", (30,  180), cv2.FONT_HERSHEY_SIMPLEX,
            #                               0.5, (255, 0, 0), 2)
            # augmented_frame = cv2.putText(augmented_frame, f"yaw: {round(marker_rotation_degrees[2][0])}", (30,  210), cv2.FONT_HERSHEY_SIMPLEX,
            #                               0.5, (255, 0, 0), 2)

            # Display the marker axes (marker rotation wrt to camera)
            axis_length = aruco_marker_length * 0.5  # pick how long you want them
            axis_3d = np.array([
                [axis_length, 0, 0],   # X axis endpoint
                [0, axis_length, 0],   # Y axis endpoint
                # Z axis endpoint (negative because OpenCV uses camera coords)
                [0, 0, -axis_length]
            ], dtype=np.float32)

            imgpts, _ = cv2.projectPoints(
                axis_3d, marker_rotation_vector, marker_translation_vector, camera.intrinsic_matrix, camera.distortion_coefficients)
            imgpts = imgpts.reshape(-1, 2).astype(int)
            origin = tuple(
                np.mean(corners[0].reshape(-1, 2), axis=0).astype(int))

            try:
                augmented_frame = cv2.line(augmented_frame, origin, tuple(
                    imgpts[0]), (0, 0, 255), 3)   # X axis in red
                augmented_frame = cv2.line(augmented_frame, origin, tuple(
                    imgpts[1]), (0, 255, 0), 3)   # Y axis in green
                augmented_frame = cv2.line(augmented_frame, origin, tuple(
                    imgpts[2]), (255, 0, 0), 3)   # Z axis in blue
            except Exception as e:
                print(e)

            if camera.camera_rotation and camera.camera_translation:
                marker_translation_in_world = transform_camera_to_world_coordinates(
                    marker_translation_metres, camera.camera_translation, camera.camera_rotation).tolist()
                marker_translation_in_world = [round(marker_translation_in_world[0], 3),
                                               round(
                    marker_translation_in_world[1], 3),
                    round(marker_translation_in_world[2], 3)]
                return {"augmented_frame": augmented_frame, "location_in_world": {"translation": marker_translation_in_world}, "location_from_camera": {"rotation": marker_rotation_degrees, "translation": marker_translation_metres}}

            return {"augmented_frame": augmented_frame,  "location_from_camera": {"rotation": marker_rotation_degrees, "translation": marker_translation_metres}}


def find_marker_locations_from_video(video_source, video_start_time: datetime, aruco_dict_type,  aruco_marker_length, camera: Camera, visualise=True):
    """
    video_source = video file path or camera index (for live video)
    """

    try:
        video_source = int(video_source)
    except ValueError as value_error:
        if (not os.path.isfile(video_source)):
            print(
                f"No valid video source provided. Camera Index is not an integer and Video file path doesn't exist: {video_source}. ")
            sys.exit(0)

    video = cv2.VideoCapture(video_source)
    time.sleep(2.0)
    resize = 0.25

    # For slowing down the video
    # original_fps = video.get(cv2.CAP_PROP_FPS)
    # speed_reduction_factor = 1
    # delay_ms = int(1000 / (original_fps / speed_reduction_factor))

    locations_and_timestamps = []

    while True:
        frame_exists, frame = video.read()

        if not frame_exists:
            break

        pose = estimate_marker_pose(
            frame, aruco_dict_type, aruco_marker_length, camera, resize)
        if pose:
            location = pose['location_in_world']['translation']

            video_timestamp = round(video.get(cv2.CAP_PROP_POS_MSEC))
            timestamp = video_start_time + \
                timedelta(milliseconds=video_timestamp)
            locations_and_timestamps.append(
                {"location": location, "timestamp": str(timestamp)})

            output_frame = pose["augmented_frame"]

        else:
            output_frame = frame

        if visualise:
            output_frame = cv2.resize(
                output_frame, None, fx=resize, fy=resize)
            cv2.imshow('ArUco Marker Pose', output_frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        # cv2.waitKey(delay_ms)

    video.release()
    cv2.destroyAllWindows()

    return locations_and_timestamps


# TODO: create output video with marker highlighted in frames where it was detected
# Great for debugging and demo purposes
