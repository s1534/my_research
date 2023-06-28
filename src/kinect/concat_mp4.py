import cv2
import glob
import os
from tqdm import tqdm
import collections
import re


def concat_mp4(output_path, txt_path):
    os.system(
        'ffmpeg -f concat -safe 0 -i {} -c copy {}'.format(txt_path, output_path))
    print(output_path, txt_path)


def make_txt(file_paths, txt_path):
    print(file_paths)
    f = open(txt_path, 'w')
    for file in file_paths:
        f.write('file ')
        f.write(file + "\n")
    f.close()


def make_dir(output_dir):
    if not os.path.exists(output_dir):
        os.system('mkdir -p {}'.format(output_dir))


if __name__ == '__main__':
    folder = 'NICT/mp4'
    # ディレクトリ内の動画をリストで取り出す
    files = glob.glob(os.path.join(folder, '*.mp4'))

    movie_dict = collections.defaultdict(list)
    temp_dict = collections.defaultdict(list)

    print('create folder')
    for file in tqdm(files):
        mp4_file = file.split('/')[2]
        date = mp4_file.split('_')[0][4:]
        time = mp4_file.split('_')[1]
        pov_idx = mp4_file.split('_')[2]

        # dirなかったら作成する
        mp4_dir = '/'.join([folder, date, time, pov_idx])
        make_dir(mp4_dir)

        # 辞書型でmp4をまとめる,
        # key：取得日時＿視点idx, value:mp4のパス
        key = date+'_'+pov_idx
        key = '_'.join([date, time, pov_idx])
        movie_dict[key].append(file)

        # ここから追加分
        mp4_file_noextention = os.path.splitext(mp4_file)[0]
        frame = mp4_file_noextention.split('_')[3]
        temp_dict[key].append(mp4_file)

    for key in tqdm(movie_dict):
        mp4_dir = key.replace('_', '/')
        mp4_dir = os.path.join(folder, mp4_dir)
        output_path = os.path.join(mp4_dir, 'output.mp4')

        txt_path = os.path.join(folder, 'concat.txt')
        mp4_file_list = sorted(temp_dict[key], key=lambda s: int(
            re.findall(r'\d+', s)[3]))
        # concat.txt作成
        make_txt(mp4_file_list, txt_path)
        # concat　mp4
        concat_mp4(output_path, txt_path)

    # print(temp_dict)
