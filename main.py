import numpy as np
import datetime
import cv2
import csv
import sys
from pathlib import Path
from typing import Dict, List

from SpatialVelocity import SpatialVelocityDataRow
from SpatialVelocity.spatial_velocity import get_pc_velocities
from SpatialVelocity.spatial_velocity import calculate_row_rms
from SpatialVelocity.spatial_velocity import get_rotation_speeds

option_handle_list = ['--csv', '--v', '--o', '--step', '--lstart' ]
options = {}

#:str: Path to the video file
VIDEO_PATH = ""
#:int: How many log file rows are handled before capturing a screenshot from the video
STEP_SIZE = 2
#:str: Determines where the output will be saved 
OUTPUT_PATH = "./Output"
#:int: Logging start time in the video file [ms]
LOG_START_TIME = 0

def make_dir(path):
    new_path = Path(path)
    if(new_path.exists()):
        return path
    else:
        new_path.mkdir(parents=True)
    # elif(new_path.parent.is_dir()):
    #     new_path.mkdir()
    # else:
    #     make_dir(new_path.parent)
    #     new_path.mkdir()
    



if __name__ == "__main__":

    for option_handle in option_handle_list:
        options[option_handle[2:]] = sys.argv[sys.argv.index(option_handle) + 1] if option_handle in sys.argv else None

    if options['csv'] ==  None:
        print("No csv path given")
        exit(1)

    if options['v'] ==  None:
        print("No video path given")
        exit(1)
    else:
        VIDEO_PATH = options['v'] 

    if options['o'] != None:
        try:
            OUTPUT_PATH = options['o']
            make_dir(OUTPUT_PATH)
        except:
            print("Invalid output directory given.")
            exit(1)

    if options['lstart'] != None:
        try:
            LOG_START_TIME = int(options['lstart'])
            if LOG_START_TIME < 0:
                raise ValueError
        except ValueError:
            print('Invalid log start time given. Give value in milliseconds.')
            exit(1)

    if options['step'] != None :
        try:
            STEP_SIZE = int(options['step'])
            if STEP_SIZE < 2:
                raise ValueError
        except ValueError:
            print("Invalid step size given. Step size must be an integer >= 2")
            exit(1)
    
    # Read data from csv
    data_rows = []
    with open(options['csv']) as csvfile:
        try:
            dialect = csv.Sniffer().sniff(csvfile.read(5000))
            csvfile.seek(0)
            reader = csv.DictReader(csvfile,dialect=dialect)
            for row in reader:
                data_row = SpatialVelocityDataRow(
                row['x'], row['y'], row['z'],
                row['r'], row['p'], row['yw'],
                row['u_x'], row['u_y'], row['u_z'],
                row['f_x'], row['f_y'], row['f_z'],
                row['FPS'],  row['TIMESTAMP']
                )
                data_rows.append(data_row)
        except Exception as e:
            print(".csv file could not be read: %s" % str(e))
            print("Exiting...")
            exit(1)


    # open video file
    cap = cv2.VideoCapture(VIDEO_PATH)

    ax1 = np.array([[1,0,0],[0,1,0],[0,0,1]])
    # First timestamp 
    start_timestamp = data_rows[0].timestamp 
    # Handle steps
    for i in range(0,len(data_rows), STEP_SIZE):
        data_set = data_rows[i:i+ STEP_SIZE]

        # Calculate step rms velocities and rotations
        pc_velocities = get_pc_velocities(data_set)
        rms_pc_velocities = calculate_row_rms(pc_velocities)
        rotations = get_rotation_speeds(data_set)
        rms_rotations = calculate_row_rms(rotations)

        video_time = LOG_START_TIME + 1000 * (data_set[-1].timestamp - start_timestamp).total_seconds()
        cap.set(cv2.CAP_PROP_POS_MSEC, video_time)
        ret, frame = cap.read()
        print( OUTPUT_PATH +'frame%d.png' % i)
        cv2.imwrite( OUTPUT_PATH  + 'frame%d.png' % i, frame)
    
    cap.release()
    cv2.destroyAllWindows()

