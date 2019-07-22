from scipy.spatial.transform import Rotation
import numpy as np


def as_spherical(cartesian):
    x, y, z = cartesian[0], cartesian[1], cartesian[2]
    r = np.sqrt(x**2 + y**2 + z**2)
    theta = np.arccos(z/r) * 180 / np.pi
    phi = np.arctan2(y, x) * 180 / np.pi
    return [r, theta, phi]


if __name__ == '__main__':
    with open('./gyro_record_20190704-205009.csv') as f:
        lines = f.readlines()
        pos = np.array([1, 0, 0])
        print(pos)
        with open('./gyro_spherical_record_20190704-205009.csv', 'w') as rf:
            # theta: 0~180, phi: -180~180
            rf.write('n,r,theta,phi\n')
            for n, line in enumerate(lines[1:]):
                out = str(n)
                rot_info = Rotation.from_quat(line.split(',')[1:5])
                for value in as_spherical(rot_info.as_dcm().dot(pos)):
                    out += ',' + str(value)
                rf.write(out + '\n')
