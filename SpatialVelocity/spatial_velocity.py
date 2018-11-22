import numpy as np
import datetime
import cv2
import csv
import sys
from typing import Dict, List
from .sv_data_row import SpatialVelocityDataRow
from .vector_util import get_transformation_matrix_3D
from scipy.signal import welch


# Standard world coordinate axises
STD_AXIS = np.array([[1,0,0],[0,1,0],[0,0,1]])

def get_pc_velocities(sv_data_rows:List[SpatialVelocityDataRow]):
    """ Returns a np array of velocities in the player centered coordinate system from list of data rows.
        Each velocity is calculated from two successive entries in the sv_data_rows and transformed to 
        the player centered coordinate system.  

        Args:
            sv_data_rows (:obj:'list' of :obj:'SpatialVelocityDataRow'): List of spatial velocity data rows

        Returns:
            np.ndarray: Array of the player centered velocities
    """
    pc_velocities = []
    for i in range(1, len(sv_data_rows)):
        d_pos = sv_data_rows[i].wpos -  sv_data_rows[i - 1].wpos # calculate wpos displacement
        d_time = (sv_data_rows[i].timestamp -  sv_data_rows[i - 1].timestamp) # calculate time difference
        w_velocity = d_pos/(d_time.total_seconds()) # calculate average velocity

        # Calculate the transformation matrix for transforming the velocity to player centered coordinates
        Q = get_transformation_matrix_3D(
            STD_AXIS,
            np.array([sv_data_rows[i].forward, sv_data_rows[i].right, sv_data_rows[i].up]) 
        )

        pc_velocity = Q @ w_velocity
        pc_velocities.append(pc_velocity)
    return np.array(pc_velocities)

def get_rotation_speeds(sv_data_rows:List[SpatialVelocityDataRow]):
    """ Returns a np array of average rotation speed from list of data rows.
        Each rotation speed is calculated from two successive entries in the sv_data_rows.

        Args:
            sv_data_rows (:obj:'list' of :obj:'SpatialVelocityDataRow'): List of spatial velocity data rows

        Returns:
            np.ndarray: Array of the player centered velocities
    """
    rot_velocities = []
    for i in range(1, len(sv_data_rows)):
        d_rot = sv_data_rows[i].rot -  sv_data_rows[i - 1].rot
        d_time = (sv_data_rows[i].timestamp -  sv_data_rows[i - 1].timestamp)
        rot_velocities.append(d_rot/(d_time.total_seconds()))
        # print (rot_velocities)
    return np.array(rot_velocities)

def get_avg_row_SF(image, window = 'hanning', nfft = 256):
    """ Calculates the SF for each row in image and returns the average spatial frequency

        Args:
            image : Source image (grayscale)
            window (str,optional): Desired window to use
            nfft (int,optional): Fourier transform size

        Returns:
            float: Average row SF value for image   
    """
    row_frqs = []
    for i in range(image.shape[0]):
        # Calculate row power spectral density using Welch's method
        f, psd = welch( image[i],
            window=window,
            nperseg=nfft,
            nfft=nfft
        )
        if psd.all() == 0:
            # Skip rows with no intensity variation
            row_frqs.append(0) 
            continue

        # Calculate the spatial frequency according to power spectral density distribution
        mean_f = np.average(f, weights=psd)
        row_frqs.append(mean_f)
        
    avg_row_sf = np.average(np.array(row_frqs)) 
    return avg_row_sf

def calculate_row_rms(array:np.ndarray):
    return np.sqrt(np.mean(np.square(array), axis=0))
