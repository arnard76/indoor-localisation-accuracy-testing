class Camera:
    """
     matrix_coefficients - Intrinsic matrix of the calibrated camera
        distortion_coefficients - Distortion coefficients associated with your camera

    optional inputs:
        include both these inputs 👇 to calculate a world "pose" of the marker
        camera_translation: in metres from origin
        camera_rotation: matches the prediction translation so pitch, roll, yaw (not roll,pitch, yaw)
    """

    def __init__(self, calibration_details, camera_translation=None, camera_rotation=None) -> None:
        self.intrinsic_matrix = calibration_details['intrinsic_matrix']
        self.distortion_coefficients = calibration_details['distortion_coefficients']
        self.camera_translation = camera_translation
        self.camera_rotation = camera_rotation
