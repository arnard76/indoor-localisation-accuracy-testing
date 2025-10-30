'''
Sample Usage:-
python calibration.py --dir calibration_checkerboard/ --square_size 0.024
'''

import datetime
from random import shuffle
import numpy as np
import cv2
import os
import argparse


def default_calibration_folder(camera_name: str) -> str:
    return f"./camera_calibration/previously_calibrated_cameras/{camera_name}"


default_calibration_folder_unnamed = "./camera_calibration/output"
default_distortion_coeffecients_filename = "distortion_coefficients.npy"
default_intrinsic_matrix_filename = "intrinsic_matrix.npy"


def calibrate(dirpath, square_size, width, height, visualize=False):
    """ Apply camera calibration operation for images in the given directory path. """

    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(8,6,0)
    objp = np.zeros((height*width, 3), np.float32)
    objp[:, :2] = np.mgrid[0:width, 0:height].T.reshape(-1, 2)

    objp = objp * square_size

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.

    images = os.listdir(dirpath)
    print(f'finding chessboard in {len(images)} images...')
    show_progress = len(images) > 100
    shuffle(images)
    flags = cv2.CALIB_CB_ADAPTIVE_THRESH | cv2.CALIB_CB_NORMALIZE_IMAGE | cv2.CALIB_CB_FAST_CHECK
    for index, fname in enumerate(images):
        img = cv2.imread(os.path.join(dirpath, fname))

        if img is None:
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(
            gray, (width, height), flags=flags)
        # If found, add object points, image points (after refining them)
        if ret:
            objpoints.append(objp)

            corners2 = cv2.cornerSubPix(
                gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)

            # Draw and display the corners
            img = cv2.drawChessboardCorners(
                img, (width, height), corners2, ret)

        if show_progress and index % 10 == 0:
            print(
                f"analysed {index} images (found {len(imgpoints)} chessboards so far)...")

        if visualize:
            small = cv2.resize(img, None, fx=0.5, fy=0.5)
            cv2.imshow('img', small)
            cv2.waitKey(0)

    max_images_used = 30
    print(f"found chessboard in {len(imgpoints)} images")
    if (len(imgpoints) == 0):
        raise Exception(
            "Couldn't find a chessboard in any of the images. Try placing a even white border around it and using a flat, undamaged, smooth chessboard.")

    print(
        f'calibrating camera using {max_images_used if len(imgpoints) > max_images_used else len(imgpoints)} images with chessboard...')
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
        objpoints[:max_images_used], imgpoints[:max_images_used], gray.shape[::-1], None, None)  # type: ignore

    if not ret:
        raise Exception("could not calibrate")

    return {"intrinsic_matrix": mtx, "distortion_coefficients": dist, "rotation_vectors": rvecs, "translation_vectors": tvecs}


def load_calibration_details_for_camera_name(camera_name: str):
    return {"intrinsic_matrix": np.load(default_calibration_folder(camera_name) + "/" + default_intrinsic_matrix_filename),
            "distortion_coefficients": np.load(default_calibration_folder(camera_name) + "/" + default_distortion_coeffecients_filename)}


def load_calibration_details_from_file(distortion_coeffecients_filepath=None, intrinsic_matrix_filepath=None):
    distortion_coeffecients_filepath = distortion_coeffecients_filepath or f"{default_calibration_folder_unnamed}/{default_distortion_coeffecients_filename}"
    intrinsic_matrix_filepath = intrinsic_matrix_filepath or f"{default_calibration_folder_unnamed}/{default_intrinsic_matrix_filename}"
    return {"intrinsic_matrix": np.load(intrinsic_matrix_filepath), "distortion_coefficients": np.load(distortion_coeffecients_filepath)}


def save_calibration_details(calibration_details, calibration_name=None):
    """
    calibration_details is the direct output of the calibrate function
    """
    calibration_name = calibration_name or str(
        datetime.datetime.now()).replace(':', '-')
    output_folder = default_calibration_folder(calibration_name)

    with open(f"{output_folder}/{calibration_name}.txt", 'w') as calibration_summary_file:
        calibration_summary_file.write(repr(calibration_details))

    with open(f'{output_folder}/{default_intrinsic_matrix_filename}', 'wb') as intrinsic_matrix_file:
        np.save(intrinsic_matrix_file, calibration_details["intrinsic_matrix"])
    with open(f'{output_folder}/{default_distortion_coeffecients_filename}', 'wb') as distortion_coefficients_file:
        np.save(distortion_coefficients_file,
                calibration_details["distortion_coefficients"])


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dir", required=True,
                    help="Path to folder containing checkerboard images for calibration")
    ap.add_argument("-w", "--width", type=int,
                    help="Width of checkerboard (default=9)",  default=6)
    ap.add_argument("-t", "--height", type=int,
                    help="Height of checkerboard (default=9)", default=6)
    ap.add_argument("-s", "--square_size", type=float,
                    default=1, help="Length of one edge (in metres)")
    ap.add_argument("-v", "--visualize", type=str, default="False",
                    help="To visualize each checkerboard image")
    args = vars(ap.parse_args())

    dirpath = args['dir']
    # square_size in cm
    square_size = args['square_size']

    width = args['width']
    height = args['height']

    if args["visualize"].lower() == "true":
        visualize = True
    else:
        visualize = False

    ret, mtx, dist, rvecs, tvecs = calibrate(
        dirpath, square_size, visualize=visualize, width=width, height=height)

    print(mtx)
    print(dist)

    np.save("calibration_matrix", mtx)
    np.save("distortion_coefficients", dist)
