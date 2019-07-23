from scipy.spatial.transform import Rotation
import numpy as np
import pandas as pd
from visualize import sphere_heatmap


def as_spherical(cartesian):
    x, y, z = cartesian[0], cartesian[1], cartesian[2]
    r = np.sqrt(x**2 + y**2 + z**2)
    theta = np.arccos(z/r) * 180 / np.pi
    phi = np.arctan2(y, x) * 180 / np.pi
    return [r, theta, phi]


if __name__ == '__main__':
    write_file = False
    visualize = True
    filename = './gyro_record_20190704-205009.csv'

    with open(filename) as f:
        lines = f.readlines()
        pos = np.array([1, 0, 0])

        if write_file:
            with open('./gyro_spherical_record' + filename.split('_')[2], 'w') as rf:
                # theta: 0~180, phi: -180~180
                rf.write('n,r,theta,phi\n')
                for n, line in enumerate(lines[1:]):
                    out = str(n)
                    rot_info = Rotation.from_quat(line.split(',')[1:5])
                    result_vector = rot_info.as_dcm().dot(pos)

                    for value in as_spherical(result_vector):
                        out += ',' + str(value)
                    rf.write(out + '\n')

        if visualize:
            df = pd.read_csv(filename, sep=',', header=0)
            rot_data = Rotation.from_quat(df.values[:, 1:5])
            gaze_vec = np.array([[1, 0, 0] for _ in range(df.shape[0])])
            rot_gaze = np.array([as_spherical(rot_info.as_dcm().dot(gaze)) for rot_info, gaze in zip(rot_data, gaze_vec)])
            rot_gaze_norm = np.array(rot_gaze)

            theta, phi = np.linspace(0, 180, 74, endpoint=True), np.linspace(-180, 180, 145, endpoint=False)
            gaze_map, _, _ = np.histogram2d(rot_gaze[:, 1], rot_gaze[:, 2], [theta, phi])

            sphere_heatmap(np.linspace(-180, 180, 144, endpoint=False), np.linspace(-90, 90, 73, endpoint=True), gaze_map)
