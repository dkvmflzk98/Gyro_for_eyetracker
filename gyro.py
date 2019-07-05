import serial.tools.list_ports
from serial import Serial
import datetime
import time
from scipy.spatial.transform import Rotation as R
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


millis = lambda: int(round(time.time() * 1000))


if __name__ == '__main__':
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if p.serial_number == '55632313838351214152':
            try:
                gyro_sensor = Serial(p.device, 115200, timeout=0.1)
                gyro_sensor.write('r\r\n'.encode('ascii', 'replace'))
                filename = datetime.datetime.now().strftime("./gyro_record_%Y%m%d-%H%M%S.csv")

                with open(filename, 'w') as f:
                    # f.write('time, roll, pitch\n')
                    interval = millis()
                    pos = np.array([0, 10, 0])

                    plt.ion()
                    fig = plt.figure()
                    ax = Axes3D(fig)
                    ax.autoscale(enable=True, axis='both', tight=True)

                    ax.set_xlim3d([-15, 15])
                    ax.set_ylim3d([-15, 15])
                    ax.set_zlim3d([-15, 15])

                    dat_X, dat_Y, dat_Z = [], [], []
                    line1, = ax.plot3D(dat_X, dat_Y, dat_Z)

                    f.write('time,quat w,quat x,quat y,quat z,acc x,acc y,acc z\n')

                    while True:
                        if millis() - interval > 1000:
                            gyro_sensor.write('r\r\n'.encode('ascii', 'replace'))
                            interval = millis()
                        while gyro_sensor.in_waiting:
                            packet = gyro_sensor.readline().decode('ascii', 'replace').split()
                            gyro_sensor.flushInput()
                            if len(packet) == 8:
                                try:
                                    f.write(datetime.datetime.now().__str__())
                                    for value in packet[1:]:
                                        f.write(',' + value)
                                    f.write('\n')

                                    r = R.from_quat(packet[1:5])

                                    rot = r.as_dcm().dot(pos)
                                    dat_X.append(rot[0])
                                    dat_Y.append(rot[1])
                                    dat_Z.append(rot[2])
                                    print(r.as_dcm().dot(pos))

                                    line1.set_xdata(dat_X)
                                    line1.set_ydata(dat_Y)
                                    line1.set_3d_properties(dat_Z)

                                    plt.draw()
                                    plt.show(block=False)
                                    plt.pause(0.0001)
                                except Exception as e:
                                    print(e)

            except Exception as e:
                print(e)
