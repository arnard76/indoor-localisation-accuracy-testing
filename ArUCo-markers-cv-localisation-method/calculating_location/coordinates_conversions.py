import numpy as np
from scipy.spatial.transform import Rotation as R


def transform_camera_to_world_coordinates(coordinates_in_camera_axes, camera_translation, camera_rotation):
    """
    inputs:
    camera_coordinates = [x, y, z] in metres
    camera_translation = [x,y,z] from world origin
    camera_rotation = [angle_x, angle_y, angle_z] in degrees from world rotation

    returns:
    world_coordinates = [x, y, z] in metres
    """

    camera_rotation_radians = np.radians(camera_rotation)

    theta_x = camera_rotation_radians[0]
    R_x = np.array([
        [1, 0, 0],
        [0, np.cos(theta_x), -np.sin(theta_x)],
        [0, np.sin(theta_x), np.cos(theta_x)]
    ])

    theta_y = camera_rotation_radians[1]
    R_y = np.array([
        [np.cos(theta_y), 0, np.sin(theta_y)],
        [0, 1, 0],
        [-np.sin(theta_y), 0, np.cos(theta_y)]
    ])

    theta_z = camera_rotation_radians[2]
    R_z = np.array([
        [np.cos(theta_z), -np.sin(theta_z), 0],
        [np.sin(theta_z), np.cos(theta_z), 0],
        [0, 0, 1]
    ])

    R = R_z @ R_y @ R_x
    rotated_points_3d = np.array(coordinates_in_camera_axes) @ R
    world_coordinates = rotated_points_3d + camera_translation
    return world_coordinates


def transform_orientation_in_euler_to_quarternion(orientation):
    # Define your angles in degrees (e.g., Yaw=90, Pitch=45, Roll=0)
    # 'zyx' specifies the sequence of axes rotated
    r = R.from_euler('yzx', orientation, degrees=True)

    #   xzy
    #     xyz
    # zyx
    # yxz

    # yzx - maybe
    # zxy

    # Get the quaternion [x, y, z, w]
    # Note: SciPy outputs [x, y, z, w] format, while some math texts use [w, x, y, z]
    quaternion = r.as_quat() 
    formatted=  {'x': quaternion[0], 'y': quaternion[1], 'z': quaternion[2], 'w': quaternion[3]}
    return formatted