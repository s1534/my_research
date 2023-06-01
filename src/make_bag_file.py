import json
import open3d as o3d
import keyboard

config_filename = 'src/config.json'

with open(config_filename) as cf:
    rs_cfg = o3d.t.io.RealSenseSensorConfig(json.load(cf))

saving_dir = 'data/0601/bag_data/cooking.bag'

rs = o3d.t.io.RealSenseSensor()
rs.init_sensor(rs_cfg, 0, saving_dir)
rs.start_capture(True)  # true: start recording with capture

while True:
    im_rgbd = rs.capture_frame(True, True)  # wait for frames and align them
    # process im_rgbd.depth and im_rgbd.color
    if keyboard.read_key() == "q":
        break

rs.stop_capture()