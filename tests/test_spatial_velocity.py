import unittest
import numpy as np
import sys 
import SpatialVelocity

from SpatialVelocity.spatial_velocity import calculate_row_rms

class TestSpatialVelocity(unittest.TestCase):
    def test_calculate_row_rms(self):
        mat1 = np.array([[1,2,-5],[-1,-3,-5],[-1,-4,-5]])
        print (mat1)
        rms = calculate_row_rms(mat1)
        print (rms)
