import numpy as np
import datetime

class SpatialVelocityDataRow:
    def __init__(self, x,y,z, roll,pitch,yaw, u_x,u_y,u_z, f_x,f_y,f_z, fps, timestamp):
        self.wpos:np.ndarray = np.array([float(x), float(y), float(z)])
        self.rot:np.ndarray = np.array([float(roll), float(pitch), float(z)])
        self.forward:np.ndarray = np.array([float(f_x), float(f_y), float(f_z)])
        self.up:np.ndarray = np.array([float(u_x), float(u_y), float(u_z)])
        self.right:np.ndarray = np.cross(self.forward, self.up)
        self.fps:float = float(fps)
        self.timestamp:datetime.datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")

    def __str__(self):
        return '<SpatialVelocityDataRow:'  +str(self.timestamp.isoformat()) + '>'


