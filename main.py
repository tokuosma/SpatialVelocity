import numpy as np
import matplotlib.pyplot as plt
import datetime
import cv2
import csv
import sys

from pathlib import Path
from typing import Dict, List
from SpatialVelocity import SpatialVelocityDataRow
from SpatialVelocity.spatial_velocity import get_pc_velocities
from SpatialVelocity.spatial_velocity import calculate_col_rms
from SpatialVelocity.spatial_velocity import get_rotation_speeds
from SpatialVelocity.spatial_velocity import get_avg_row_SF

option_handle_list = ['--csv', '--v', '--o', '--step', '--lstart', '--show', '--saveimg' ]
options = {}

#:str: Path to the video file
VIDEO_PATH = ""
#:int: How many log file rows are averaged per each screenshot captured from the video
STEP_SIZE = 2
#:str: Determines where the output will be saved 
OUTPUT_PATH = "./Output"
#:int: Logging start time in the video file [ms]
LOG_START_TIME = 0
#:float: Aspect ratio (width/height) for scene camera
ASPECT_RATIO = 1.777
#:bool: If set to true, displays each screenshot during processing
SHOW_IMAGES = False
#:bool: If set to true, each image processed is saved to output folder
SAVE_IMAGES = False

def make_dir(path):
    new_path = Path(path)
    if(new_path.exists()):
        return path
    else:
        new_path.mkdir(parents=True)

if __name__ == "__main__":
    """ Calculates spatial velocities.

        For details, see: 
            So, R. H., Ho, A., & Lo, W. T. (2001).
            A metric to quantify virtual scene movement for the study of cybersickness: Definition, implementation, and verification. 
            Presence: Teleoperators & Virtual Environments, 10(2), 193-215.

    """

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
    
    if options['show'] != None:
        SHOW_IMAGES = True

    if options['saveimg'] != None:
        SAVE_IMAGES = True
    
    # Read data from log file
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
    # First timestamp 
    START_TIMESTAMP = data_rows[0].timestamp 
    
    # Handle steps:
    # Calculate average scene velocities
    # Calculate average spatial frequencies  
    # Calculate spatial velocities
    spatial_velocities = []
    for i in range(0,len(data_rows), STEP_SIZE):
        print("Processing row %d of %d " %(i, len(data_rows)))
        data_set = data_rows[i:i+ STEP_SIZE]
        # Calculate step rms velocities and rotations
        pc_velocities = get_pc_velocities(data_set)
        rms_pc_velocities = calculate_col_rms(pc_velocities)
        rotations = get_rotation_speeds(data_set)
        rms_rotations = calculate_col_rms(rotations)

        # All velocities
        V = np.array([rms_pc_velocities, rms_rotations]).transpose()

        # Move video to the current timestamp
        video_time = LOG_START_TIME + 1000 * (data_set[-1].timestamp - START_TIMESTAMP).total_seconds()
        cap.set(cv2.CAP_PROP_POS_MSEC, video_time)
        
        # Read frame
        ret, frame = cap.read()

        if(np.shape(frame) == ()):
            # Stop run if no frame could be read
            print("Video end.")
            break

        # Convert to grayscale
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 

        if(SHOW_IMAGES):
            cv2.imshow('frame', image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        if(SAVE_IMAGES):
            path = Path(OUTPUT_PATH).joinpath('frame_%d.png' % i)
            print(str(path))
            cv2.imwrite(str(path) , image)

        #Calculate row SF
        # https://stackoverflow.com/a/33976969
        avg_row_sf = get_avg_row_SF(image) 
        
        #Calculate column SF        
        image_t = image.transpose()
        avg_col_sf = get_avg_row_SF(image_t)

        #Calculate radial SF
        avg_rad_sf = np.sqrt(avg_col_sf ** 2 + avg_row_sf ** 2)

        # Calculate spatial velocities:
        
        sv_x = avg_rad_sf * V[0][0] 
        sv_roll = avg_rad_sf * V[0][1]
        sv_y = avg_row_sf * V[1][0] 
        sv_pitch = avg_col_sf * V[1][1] # SF_col * V_pitch
        sv_z = avg_col_sf * V[2][0]
        sv_yaw = avg_row_sf * V[2][1] # SF_row * V_yaw
        SV = np.array([[sv_x, sv_roll], [sv_y, sv_pitch], [sv_z, sv_yaw]])
        SV_dict =  {
            'Timestamp': data_set[-1].timestamp.isoformat(),
            'TimeDelta': video_time,
            'scene_velocity_x': V[0][0],
            'scene_velocity_y': V[1][0],
            'scene_velocity_z': V[2][0],
            'scene_velocity_roll': V[0][1],
            'scene_velocity_pitch': V[1][1],
            'scene_velocity_yaw': V[2][1],
            'row_avg_SF': avg_row_sf,
            'col_avg_SF': avg_col_sf,
            'rad_avg_SF': avg_rad_sf,
            'SV_X': sv_x,
            'SV_Y': sv_y,
            'SV_Z': sv_z,
            'SV_roll': sv_roll,
            'SV_pitch': sv_pitch,
            'SV_yaw': sv_yaw
        }
        spatial_velocities.append(SV_dict)

    # Write results 
    with open( Path(OUTPUT_PATH).joinpath('results.csv'), 'w',  newline='') as csvfile:
        fieldnames = ['Timestamp','TimeDelta',
        'scene_velocity_x','scene_velocity_y','scene_velocity_z',
        'scene_velocity_roll', 'scene_velocity_pitch', 'scene_velocity_yaw',
        'row_avg_SF','col_avg_SF','rad_avg_SF',
        'SV_X', 'SV_Y', 'SV_Z',
        'SV_roll', 'SV_pitch', 'SV_yaw']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in spatial_velocities:
            writer.writerow(row)

    cap.release()
    cv2.destroyAllWindows()

