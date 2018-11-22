import unittest
import numpy as np
import sys 
import cv2

from SpatialVelocity.spatial_velocity import calculate_row_rms
from SpatialVelocity.spatial_velocity import get_avg_row_SF

class TestSpatialVelocity(unittest.TestCase):
    def test_calculate_row_rms(self):
        mat1 = np.array([[1,2,-5],[-1,-3,-5],[-1,-4,-5]])
        rms = calculate_row_rms(mat1)



    def test_avg_row_sf_bars(self):
        """ Calculate average row and column SF's from test image.
            Test image features black and white vertical bars.
            Col SF should be zero
        """
        image_bars = cv2.imread('./tests/bars.png', 0)
        image_bars_t = np.transpose(image_bars)
        # Calculate row SF
        avg_bars= get_avg_row_SF(image_bars)
        # Rotate image 90 degrees and calculate col SF 
        avg_bars_t= get_avg_row_SF(image_bars_t)
        self.assertTrue(avg_bars > 0)
        self.assertTrue(avg_bars > avg_bars_t)
        self.assertEqual(0, avg_bars_t)

    def test_avg_row_sf_grid(self):
        """ Calculate average row and column SF's from test image.
            Test image features an uneven grid with denser horizontal stripes
            Col SF should be greater than row SF 
        """
        image_bars = cv2.imread('./tests/grid.png', 0)
        image_bars_t = np.transpose(image_bars)
        # Calculate row SF
        avg_bars= get_avg_row_SF(image_bars)
        # Rotate image 90 degrees and calculate col SF 
        avg_bars_t= get_avg_row_SF(image_bars_t)
        print(avg_bars, avg_bars_t)
        self.assertTrue(avg_bars < avg_bars_t)