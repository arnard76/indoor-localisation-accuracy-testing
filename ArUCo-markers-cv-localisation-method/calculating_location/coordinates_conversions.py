import numpy as np


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
