
import os
import open3d as o3d
import numpy as np
import glob
import matplotlib.pyplot as plt

base_dir = 'data/0418/origin_data/'

dataset_dir = sorted(glob.glob('data/0418/origin_data/*'))
save_dir = 'data/0418/processed_data/'

# SAMPLE_DIR = "ply_data/0419"

def display_inlier_outlier(cloud, ind):
    inlier_cloud = cloud.select_by_index(ind)
    outlier_cloud = cloud.select_by_index(ind, invert=True)

    print("Showing outliers (red) and inliers (gray): ")
    outlier_cloud.paint_uniform_color([1, 0, 0])
    inlier_cloud.paint_uniform_color([0.8, 0.8, 0.8])
    o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud],
                                      zoom=0.3412,
                                      front=[0.4257, -0.2125, -0.8795],
                                      lookat=[2.6172, 2.0475, 1.532],
                                      up=[-0.0694, -0.9768, 0.2024])

# 外れ値処理
# Radius outlier removal
def out_removal(pcd):
    print("Statistical oulier removal")
    cl, ind = pcd.remove_radius_outlier(nb_points = 30, radius=0.035)
    # display_inlier_outlier(pcd, ind)
    return cl

# if not os.path.exists(SAMPLE_DIR):
#     # ディレクトリが存在しない場合、ディレクトリを作成する
#     os.makedirs(SAMPLE_DIR)

for pcd_file in dataset_dir:
    print(pcd_file)
    origin_pcd = o3d.io.read_point_cloud(pcd_file)
    processed_pcd = out_removal(origin_pcd)
    # new_color = np.zeros(np.asarray(processed_pcd.points).shape)
    # processed_pcd.colors = o3d.utility.Vector3dVector(new_color)
    # 可視化
    # o3d.visualization.draw_geometries([processed_pcd])
    save_file_name = save_dir + pcd_file[22:]
    o3d.io.write_point_cloud(save_file_name, processed_pcd)
