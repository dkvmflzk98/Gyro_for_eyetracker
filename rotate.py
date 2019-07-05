from scipy.spatial.transform import Rotation as R
import numpy as np

if __name__=='__main__':
    with open('./gyro_record_20190704-205009.csv') as f:
        lines = f.readlines()
        pos = np.arange(3)
        print(pos)
        for line in lines[2:10]:
            r = R.from_quat(line.split(',')[1:5])
            print(r.as_dcm())

            print(r.as_dcm().dot(pos))
