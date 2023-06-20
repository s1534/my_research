import json
import open3d as o3d
import keyboard
import os
import datetime
from concurrent.futures import ProcessPoolExecutor

def make_dirs(path):
    if not os.path.isdir(path):
        os.makedirs(path)
        os.makedirs(os.path.join(path,'bag_data'))
        os.makedirs(os.path.join(path,'origin_ply'))

def capture_bag(num,saving_dir):
    if num == 1:
        config_filename = 'src/config1.json'
    if num == 2:
        config_filename = 'src/config2.json'

    with open(config_filename) as cf:
        rs_cfg = o3d.t.io.RealSenseSensorConfig(json.load(cf))


    time = str(datetime.datetime.now().time())[:8]

    bagfile = 'bag_data/cooking' + str(num) + '-' + time + '.bag'
    print('start capturing camera{}'.format(num))

    bag_dir = os.path.join(saving_dir,bagfile)


    rs = o3d.t.io.RealSenseSensor()
    rs.init_sensor(rs_cfg, 0, bag_dir)
    rs.start_capture(True)  # true: start recording with capture

    while True:
        im_rgbd = rs.capture_frame(True, True)  # wait for frames and align them
        # process im_rgbd.depth and im_rgbd.color
        # if keyboard.read_key() == "q":
            # break

if __name__ == "__main__":
    print('----------------------------------')
    # make folder
    today = datetime.date.today()
    today_ymd = today.strftime('%Y%m%d')
    saving_dir = os.path.join('data',today_ymd)
    make_dirs(saving_dir)

    with ProcessPoolExecutor() as executor:
        executor.submit(capture_bag,1,saving_dir)
        executor.submit(capture_bag,2,saving_dir)
    print('終了')


