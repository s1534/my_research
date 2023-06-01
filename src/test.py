import open3d as o3d
import numpy as np
import glob

if __name__ == "__main__":

    # Loading point cloud
    print("Loading point cloud")
    files = sorted(glob.glob('data/0418/processed_data/*'))

    ply = o3d.io.read_point_cloud(files[170])

    # confirmation
    print(ply)
    print(np.asarray(ply.points))

    # Visualization in window
    o3d.visualization.draw_geometries([ply])
