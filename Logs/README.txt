12.2.2019

These log files contain the raw data measured during the test runs. 
The spatial velocity values and other calculated values can be found in the results folder.

The log was updated at a 5 Hz rate. 

FILE NAMES:
Test subject id, test order number and test condition are encoded in the filenames:
XX_YY_ZZ.csv

XX = Test subject id
YY = Test order number (1 or 2)
ZZ = Test condition (High detail or low detail)

LOG VARIABLES:

x,y,z: player character world coordinates
r,p,yw: camera rotation (roll, pitch, yaw)
u_x,u_y,u_z: camera coordinate system up axis direction
f_x,f_y,f_z: camera coordinate system forward axis direction
HMD_aa_x,HMD_aa_y,HMD_aa_z: HMD IMU angular acceleration
HMD_la_x,HMD_la_y,HMD_la_z: HMD IMU linear acceleration
HMD_av_x,HMD_av_y,HMD_av_z: HMD IMU angular velocity
HMD_lv_x,HMD_lv_y,HMD_lv_z: HMD IMU linear velocity
HMD_td: IMU timestamp
FPS: estimated frames per second 
TIMESTAMP: ISO-8601 format timestamp

