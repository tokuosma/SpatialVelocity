import numpy as np

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def get_transformation_matrix_3D(ax1:np.ndarray ,ax2:np.ndarray):
    """ Returns the tranformation matrix q between two two sets of three dimensional coordinate systems.

    """
    if not isinstance(ax1, np.ndarray) or not isinstance(ax2, np.ndarray):
        print("Error! Coordinates must be given as a 3x3 numpy.ndarray")
        raise ValueError
    if(ax1.shape != ax2.shape != (3,3)):
        print("Error! Array shape must be 3x3")
        raise ValueError

    matrix = np.zeros((3,3), dtype=float)
    for i in range(3): 
        for j in range(3):
            v1_u = unit_vector(ax1[i])
            v2_u = unit_vector(ax2[j])
            matrix[i][j] = np.dot(v1_u, v2_u)

    return matrix
    

if __name__ == "__main__":
    v1 = np.array([1,0,0])
    v2 = np.array([0,1,0])
    print("Angle between (1,0,0) and (0,1,0): ", angle_between(v1,v2) * (360/(2*np.pi)))
    print()
    v3 = np.array([5,0,0])
    print("Unit vector (5,0,0): ", unit_vector(v3))
    print()

    ax1 = np.array([[1,0,0],[0,1,0],[0,0,1]], dtype=float)
    ax2 = np.array([[-1,0,0],[0,-1,0],[0,0,-1]], dtype=float)
    Q1 = get_transformation_matrix_3D(ax1, ax2) 
    print("Transformation matrix Q1 between [(1,0,0),(0,1,0),(0,0,1)] and [(-1,0,0),(0,-1,0),(0,0,-1)]:\n",Q1)

    v4 = np.array([5,2,3])
    print("Transform (5,2,3) with Q1: ", Q1 @ v4 )

    Q1_T = np.transpose(Q1)
    print("Q1^T:\n", Q1_T )
    print("Transform (5,2,3) with Q1^T: ", Q1_T @ v4  )

    up = np.array([-0.32, -0.08, 0.94])
    forward = np.array([-0.92, -0.21, -0.33])
    right = np.cross(up, forward)

    ax3 = np.array([forward, right, up])

    Q2 = get_transformation_matrix_3D(ax1, ax3)
    print("Transformation matrix Q2: \n", Q2)
    Q2_t = np.transpose(Q2)
    print("Q2^T: \n", Q2_t)
    v_world = np.array([-659.20,-626.93,0.00])

    print("world velocity v_world: ", v_world )
    print("Transform v_world  with Q2: ", Q2 @ v_world)
    print("Transform v_world  with Q2^T: ", Q2_t @ v_world)


