import glob
import csv
import sys
import os
import errno

import numpy as np

option_handle_list = ['--o', '--s' ]
options = {}

OUTPUT_PATH = './SUMMARY.CSV'
SOURCE_PATH = './'


def main():

    for option_handle in option_handle_list:
        options[option_handle[2:]] = sys.argv[sys.argv.index(option_handle) + 1] if option_handle in sys.argv else None

    

    if options['o'] != None:
        try:
            if not os.path.exists(os.path.dirname(options['o'])):
                try:
                    os.makedirs(os.path.dirname(options['o']))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            
            OUTPUT_PATH = options['o']
        except:
            print("Invalid output directory given.")
            exit(1)

    if options['s'] != None:
        SOURCE_PATH = options['s']

    fnames = glob.glob(SOURCE_PATH + '/*.csv')
    
    summary_rows = []
    for i in range(len(fnames)):
        summary_dict = {}
        warnings = []
        result_rows = []

        ID, ORDER, CONDITION = os.path.basename(fnames[i]).split('_')
        CONDITION = CONDITION.split('.')[0]
        summary_dict['ID'] = ID
        summary_dict['ORDER'] = ORDER
        summary_dict['CONDITION'] = CONDITION

        with open(fnames[i]) as csvfile:
            try:
                dialect = csv.Sniffer().sniff(csvfile.read(5000))
                csvfile.seek(0)
                reader = csv.reader(csvfile,dialect=dialect)
                for row in reader:
                    if(row[2] != 'scene_velocity_x' and float(row[2]) == 0):
                        # Stop when movement stops
                        break
                    result_rows.append(row)                
                    
                    
            except Exception as e:
                print(".csv file could not be read: %s" % str(e))
                print("Exiting...")
                exit(1)

        summary_dict['COUNT'] = len(result_rows)
        if(len(result_rows) > 1950  or len(result_rows) < 1910):
            warnings.append('Unusual log length')            

        headers = result_rows[0][2:15]
        columns = {}
        for header in headers:
            idx = headers.index(header)
            col = np.array([row[idx + 2] for row in result_rows[1:]], dtype=float)
            columns[header] = col
        
        for header in columns: 
            # summary_dict[header + '_SUM'] = np.sum(columns[header])
            summary_dict[header + '_AVG'] = np.average(columns[header])
            # summary_dict[header + '_MIN'] = np.min(columns[header])
            # summary_dict[header + '_MAX'] = np.max(columns[header])
            summary_dict[header + '_STD'] = np.std(columns[header])
        
        # RECALCULATE SPATIAL VELOCITY PITCH AND YAW VALUES

        sv_pitch = columns['col_avg_SF'] * columns['scene_velocity_pitch']
        # summary_dict['SV_pitch' + '_SUM'] = np.sum(sv_pitch)
        summary_dict['SV_pitch' + '_AVG'] = np.average(sv_pitch)
        # summary_dict['SV_pitch' + '_MIN'] = np.min(sv_pitch)
        # summary_dict['SV_pitch' + '_MAX'] = np.max(sv_pitch)
        summary_dict['SV_pitch' + 'STD'] = np.std(sv_pitch)

        sv_yaw = columns['row_avg_SF'] * columns['scene_velocity_yaw']
        # summary_dict['SV_yaw' + '_SUM'] = np.sum(sv_yaw)
        summary_dict['SV_yaw' + '_AVG'] = np.average(sv_yaw)
        # summary_dict['SV_yaw' + '_MIN'] = np.min(sv_yaw)
        # summary_dict['SV_yaw' + '_MAX'] = np.max(sv_yaw)
        summary_dict['SV_yaw' + '_STD'] = np.std(sv_yaw)

        summary_dict['WARNINGS'] = ','.join(warnings)
        summary_rows.append(summary_dict)

    with open( OUTPUT_PATH, 'w',  newline='') as csvfile:
        fieldnames = summary_rows[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in summary_rows:
            writer.writerow(row)

if __name__ == "__main__":
    main()
