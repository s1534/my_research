import open3d as o3d
import glob

# データセット読み込み
dataset = sorted(glob.glob('ply_data/0418/*'))

# ウィンドウ初期化
vis = o3d.visualization.Visualizer()
vis.create_window(
    window_name="test",  # ウインドウ名
    width=800,           # 幅
    height=600,          # 高さ
    left=50,             # 表示位置(左)
    top=50               # 表示位置(上)
)

pre_ply = o3d.io.read_point_cloud(dataset[0])

# Geometry追加
vis.add_geometry(pre_ply)

for ply_file in dataset:
    ply = o3d.io.read_point_cloud(ply_file)
    print(ply_file)

    # vis.add_geometry(ply)
  # 更新処理
    vis.update_geometry(ply)
    vis.poll_events()
    vis.update_renderer()
