import pyrealsense2 as rs
import numpy as np
import cv2
import open3d
from datetime import datetime
import os
from pytz import timezone
import matplotlib.pyplot as plt

def make_dirs(path):
    if not os.path.isdir(path):
        os.makedirs(path)

config = rs.config()
bag_file = 'data/20230601/bag_data/cooking.bag'

# ↓ ここでファイル名設定
config.enable_device_from_file(bag_file)

# ストリーミング開始
pipeline = rs.pipeline()
profile = pipeline.start(config)

intr = profile.get_stream(rs.stream.color).as_video_stream_profile().get_intrinsics()
pinhole_camera_intrinsic = open3d.camera.PinholeCameraIntrinsic(intr.width, intr.height, intr.fx, intr.fy, intr.ppx, intr.ppy)

align_to = rs.stream.color
align = rs.align(align_to)

try:
    frame = 1
    while True:
        # フレーム待ち(Color & Depth)
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)

        depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        # color_image = cv2.cvtColor(color_image, cv2.COLOR_RGB2BGR)
        color = open3d.geometry.Image(color_image)

        depth_image = np.asanyarray(depth_frame.get_data())
        depth = open3d.geometry.Image(depth_image)

        rgbd = open3d.geometry.RGBDImage.create_from_color_and_depth(color, depth, depth_scale=10000.0, depth_trunc=10000,convert_rgb_to_intensity = False)
        ply =  open3d.geometry.PointCloud.create_from_rgbd_image(rgbd, pinhole_camera_intrinsic)

        # 時刻設定
        utc_now = datetime.now(timezone('UTC'))
        jst_now = utc_now.astimezone(timezone('Asia/Tokyo'))
        ts = jst_now.strftime("%Y%m%d-%H%M%S")
        date = ts[:8]
        
        # ディレクトリが無いときは作成する
        make_dirs("data/"+date+"/origin_ply")

        print(bag_file[:13])
        ply_dir = bag_file[:13]
        
        open3d.io.write_point_cloud(ply_dir+'/origin_ply/'+str(frame)+".ply", ply)
        # if num %15 == 0:
        #     open3d.io.write_point_cloud("data/"+date+"/data"+str(count)+".ply", pcd)
        #     count+=1

        # 確認用
        # Show images
        plt.subplot(221)
        plt.title('rgbd.color image')
        plt.imshow(rgbd.color)
        plt.subplot(222)
        plt.title('rgbd.depth image')
        plt.imshow(rgbd.depth)
        plt.subplot(223)
        plt.title('depth_image')
        plt.imshow(depth)
        plt.subplot(224)
        plt.title('color_image')
        plt.imshow(color_image)
        plt.show()

        if frame == 1:
            break
        
        frame += 1
        

finally:
    # Stop streaming
    pipeline.stop()