import numpy as np
import datetime
import cv2
import sys
from sv_data_row import SpatialVelocityDataRow

option_handle_list = ['--csv', '--v', '--o']
options = {}

if __name__ == "__main__":


    for option_handle in option_handle_list:
        options[option_handle[2:]] = sys.argv[sys.argv.index(option_handle) + 1] if option_handle in sys.argv else None

    if options['csv'] ==  None:
        print("No csv path given")
        exit(1)

    if options['v'] ==  None:
        print("No video path given")
        exit(1)

    if options['o'] == None:
        print("No output path given")

    raw_data = []
    import csv
    with open(options['csv']) as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(5000))
        csvfile.seek(0)
        reader = csv.DictReader(csvfile,dialect=dialect)
        for row in reader:
            raw_data.append(row)

    data_rows = []
    for row in raw_data:
        data_row = SpatialVelocityDataRow(
            row['x'], row['y'], row['z'],
            row['r'], row['p'], row['yw'],
            row['u_x'], row['u_y'], row['u_z'],
            row['f_x'], row['f_y'], row['f_z'],
            row['FPS'],  row['TIMESTAMP']
        )
        print(data_row.timestamp)
        data_rows.append([data_row])
        
        # timestamp = datetime.datetime.strptime(row["TIMESTAMP"], "%Y-%m-%dT%H:%M:%S.%fZ")
        # print(row)
        # print ("pos: %.2f,%.2f,%.2f" % (float(row['x']),float(row['y']),float(row['z'])))
        # print (str(timestamp),row["TIMESTAMP"] )

    cap = cv2.VideoCapture(options['v'])
    cap.set(cv2.CAP_PROP_POS_MSEC, 1000)
    ret, frame = cap.read()
    cv2.imwrite('frame.png', frame)
    cap.release()
    cv2.destroyAllWindows()


