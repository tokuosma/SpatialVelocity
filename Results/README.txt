12.2.2019

These files contain the results calculated from the log files. Results were calculated only for 
test subjects who completed both test runs. 

The results were calculated using a step size of 2 (~ 2.5 Hz video sample rate). 

FILE NAMES:
Test subject id, test order number and test condition are encoded in the filenames:
XX_YY_ZZ.csv

XX = Test subject id
YY = Test order number (1 or 2)
ZZ = Test condition (High detail or low detail)

SUMMARY.csv contains a summary of all the individual test runs.

INDIVIUDAL RESULT VARIABLES:

Timestamp: IS0-8601 timestamp
TimeDelta: Video time (ms)
Scene velocities (x,y,z): Average velocities within step
	scene_velocity_x
	scene_velocity_y
	scene_velocity_z
Angular velocities (roll,pitch,yaw): Average angular velocities within step
	scene_velocity_roll
	scene_velocity_pitch
	scene_velocity_yaw
Spatial frequencies:
	row_avg_SF: Average dominant SF calculated from image rows
	col_avg_SF: Average dominant SF calculated from image columns
	rad_avg_SF: Radial SF, calcluated as SQRT(row_avg_SF ** 2 + col_avg_SF ** 2)
Spatial velocities:
	SV_X
	SV_Y 
	SV_Z
	SV_roll
	SV_pitch
	SV_yaw


SUMMARY VARIABLES:
ID: Test subject id
ORDER: Test order number
CONDITION: Test condition

The summary also contains all the velocities, spatial frequencies and spatial velocities, 
with following statistical quantities extracted from each individual test run result:
SUM: sum of all run values
AVG: Average of run values
MIN: Minimum run value
MAX: Maximum run value:
VAR: Variance


Refs:
SO, Richard HY; HO, Andy; LO, W. T. 
A metric to quantify virtual scene movement for the study of cybersickness: Definition, implementation, and verification. 
Presence: Teleoperators & Virtual Environments, 2001, 10.2: 193-215.