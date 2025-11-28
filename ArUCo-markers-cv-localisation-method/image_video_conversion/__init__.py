import cv2
import os
import shutil
import numpy as np


def video_to_frames(video_file_name: str, output_folder: str):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    video = cv2.VideoCapture(video_file_name)
    # if not video.isOpened():
    # print("Error: Could not open video.")
    # exit()

    frame_count = 0
    while True:
        ret, frame = video.read()

        if not ret:  # Break the loop if no more frames are available
            break

        # Construct the output filename
        frame_filename = os.path.join(
            output_folder, f"frame_{frame_count:04d}.jpg")

        # Save the frame as an image
        cv2.imwrite(frame_filename, frame)

        frame_count += 1
    print(f"Extracted {frame_count} frames to '{output_folder}'")

    video.release()
    cv2.destroyAllWindows()


def delete_frames_after_use(frames_output_folder:str):
    if os.path.exists(frames_output_folder):
        shutil.rmtree(frames_output_folder, ignore_errors=False)