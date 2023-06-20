import json
import open3d as o3d
import keyboard
import os
import datetime

today = datetime.date.today()
today_ymd = today.strftime('%Y%m%d')
time = str(datetime.datetime.now().time())[:8]

config_filename = 'src/config.json'

def make_dirs(path):
    if not os.path.isdir(path):
        os.makedirs(path)
        os.makedirs(os.path.join(path,'bag_data'))
        os.makedirs(os.path.join(path,'origin_ply'))

with open(config_filename) as cf:
    rs_cfg = o3d.t.io.RealSenseSensorConfig(json.load(cf))

saving_dir = os.path.join('data',today_ymd)

make_dirs(saving_dir)
bagfile = 'bag_data/cooking-'+time+'.bag'
bag_dir = os.path.join(saving_dir,bagfile)

rs = o3d.t.io.RealSenseSensor()
rs.init_sensor(rs_cfg, 0, bag_dir)
rs.start_capture(True)  # true: start recording with capture

while True:
    im_rgbd = rs.capture_frame(True, True)  # wait for frames and align them
    # process im_rgbd.depth and im_rgbd.color
    # if keyboard.read_key() == "q":
        # break

rs.stop_capture()