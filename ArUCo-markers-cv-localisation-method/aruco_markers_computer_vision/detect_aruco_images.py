'''
Sample Command:-
python detect_aruco_images.py --image Images/test_image_1.png --type DICT_5X5_100
'''
import numpy as np
from aruco_markers_computer_vision.utils import ARUCO_DICT, draw_aruco_marker_squares
import argparse
import cv2
import sys


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to input image containing ArUCo tag")
ap.add_argument("-t", "--type", type=str,
                default="DICT_ARUCO_ORIGINAL", help="type of ArUCo tag to detect")
ap.add_argument("-s", "--save_output", action="store_false")
args = vars(ap.parse_args())


print("Loading image...")
image = cv2.imread(args["image"])
h, w, _ = image.shape
width = 600
height = int(width*(h/w))
image = cv2.resize(image, (width, height), interpolation=cv2.INTER_CUBIC)


# verify that the supplied ArUCo tag exists and is supported by OpenCV
if ARUCO_DICT.get(args["type"], None) is None:
    print(f"ArUCo tag type '{args['type']}' is not supported")
    sys.exit(0)

# load the ArUCo dictionary, grab the ArUCo parameters, and detect
# the markers
print("Detecting '{}' tags....".format(args["type"]))
arucoDict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT[args["type"]])
arucoParams = cv2.aruco.DetectorParameters()
arucoDetector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)
corners, ids, rejected = arucoDetector.detectMarkers(image)

detected_markers = draw_aruco_marker_squares(corners, ids, rejected, image)
cv2.imshow("Image", detected_markers)

if args["save_output"]:
    cv2.imwrite("output_sample.png", detected_markers)

cv2.waitKey(0)
