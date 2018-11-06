import unittest
import numpy as np
from ..vector_util import get_transformation_matrix_3D
from ..vector_util import angle_between
from ..vector_util import unit_vector


class TestVectorUtility(unittest.TestCase):

    def test_unit_vector(self):
        """ Calculate unit vector
        """
        vec = np.array([5,0,0])
        uvec = unit_vector(vec)
        self.assertTrue(np.equal(np.array([1,0,0]),uvec).all())

    def test_angle_betwee(self):
        vec1 = np.array([1,0,0])
        vec2 = np.array([0,1,0])

        angle = angle_between(vec1, vec2)

        self.assertEqual(np.pi/2, angle)

    def test_transformation_matrix_3D_invalid_args(self):
        """ Try calculating transformation matrix with invalid arg types 
        """
        arr1 = np.zeros((3,3), dtype=float)
        arr2 = np.zeros((3,3), dtype=float)

        with self.assertRaises(ValueError):
            get_transformation_matrix_3D(arr1,2)

        with self.assertRaises(ValueError):
            get_transformation_matrix_3D(1,arr2)
        
        with self.assertRaises(ValueError):
            get_transformation_matrix_3D(1,2)
    
    def test_transformation_matrix_3D_invalid_shape(self):
        """ Try calculating transformation matrix for non 3D coordinate systems         
        """
        arr1 = np.zeros((3,3), dtype=float)
        arr2 = np.zeros((1,3), dtype=float)

        with self.assertRaises(ValueError):
            get_transformation_matrix_3D(arr1, arr2)

        with self.assertRaises(ValueError):
            get_transformation_matrix_3D(arr2, arr1)

        with self.assertRaises(ValueError):
            get_transformation_matrix_3D(arr2, arr2)
            
            
    def test_transformation_matrix_3D_rot_Z_90(self):
        """ Calculate transformation matrix from normal coordinate system to a 
            system that has been rotated 90 degrees along the around the z-axis
        """
        arr1 = np.array([[1,0,0],[0,1,0],[0,0,1]])
        arr2 = np.array([[0,1,0],[-1,0,0],[0,0,1]])
        vec = np.transpose(np.array([1,0,0]))

        Q_90 = get_transformation_matrix_3D(arr1, arr2)
        vec_rot = Q_90 @ vec

        self.assertTrue(np.equal(np.array([0,-1,0]), vec_rot).all())
        
    
