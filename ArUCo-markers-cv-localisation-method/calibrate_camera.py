# TODO: turn into an API endpoint because a simple HTTP request is more convenient than a full development setup + understanding code + running it with correct inputs


from image_video_conversion import video_to_frames
from camera_calibration import calibrate, save_calibration_details


# Input: Calibration Video
# Turn Calibration Video for Camera Into Frames
calibration_video_input_folder = "./camera_calibration/previously_calibrated_cameras/"
camera_filename = "Arnav laptop.mp4"
camera_filename_without_file_type = camera_filename.split(".")[0]
frames_folder = camera_filename_without_file_type + "/frames"
video_to_frames(calibration_video_input_folder + camera_filename,
                calibration_video_input_folder + frames_folder)

# Find Calibration Matrices
chessboard_size = 19  # width & height of chessboard (cm)
NUM_SQUARES_IN_CHESSBOARD = 8
NUM_INNER_VERTICES = NUM_SQUARES_IN_CHESSBOARD - 1
calibration_details = calibrate(
    calibration_video_input_folder + frames_folder, chessboard_size, width=NUM_INNER_VERTICES, height=NUM_INNER_VERTICES)
print(calibration_details)
save_calibration_details(
    calibration_details, camera_filename_without_file_type)
