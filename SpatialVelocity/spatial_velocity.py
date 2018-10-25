import numpy as np
import datetime
import cv2
import sys

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

    data = []
    import csv
    with open(options['csv']) as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(5000))
        csvfile.seek(0)
        reader = csv.DictReader(csvfile,dialect=dialect)
        for row in reader:
            data.append(row)

    for row in data:
        timestamp = datetime.datetime.strptime(row["TIMESTAMP"], "%Y-%m-%dT%H:%M:%S.%fZ")
        print ("pos: %.2f,%.2f,%.2f" % (float(row['x']),float(row['y']),float(row['z'])))
        print (str(timestamp),row["TIMESTAMP"] )

    cap = cv2.VideoCapture(options['v'])
    cap.set(cv2.CAP_PROP_POS_MSEC, 500000)
    ret, frame = cap.read()
    cv2.imwrite('frame.png', frame)
    cap.release()
    cv2.destroyAllWindows()


