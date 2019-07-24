import pandas as pd
import os


class GazeData:
    def __init__(self, filename):
        self.path = os.path.join('./', filename)
        self.gaze_data = pd.read_csv(filename, sep=',', header=0)
        self.gaze_data['time'] = pd.to_datetime(self.gaze_data['time'], format="%Y-%m-%d %H:%M:%S.%f")

    def data_time_extract(self, start_time, end_time):
        return self.gaze_data.loc[(lambda x: (start_time <= x) & (x <= end_time))(self.gaze_data['time'])]


if __name__ == '__main__':
    file = './gaze_spherical_record_20190704-205009.csv'

    test_data = GazeData(file)
    st_time = pd.to_datetime('2019-07-04 20:50:13.5', format="%Y-%m-%d %H:%M:%S.%f")
    ed_time = pd.to_datetime('2019-07-04 20:50:14.0', format="%Y-%m-%d %H:%M:%S.%f")
    print(test_data.data_time_extract(st_time, ed_time))
