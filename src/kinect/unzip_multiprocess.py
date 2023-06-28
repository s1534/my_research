# multiprocessing使ったらもっと早くなるかも
import glob
import shutil
from tqdm import tqdm
import os
import time
import multiprocessing

def process_one_file(folder, filename):
    try:
        shutil.unpack_archive(filename, os.path.join(folder, 'mkv'))
    except:
        print('can not unpiz {}'.format(filename))


if __name__ == '__main__':
    num_cpu = 8
    folder = 'NICT_0625'
    files = glob.glob(os.path.join(folder, 'zip/*'))
    pool = multiprocessing.Pool(num_cpu)

    for input_file in tqdm(files):
        print(input_file)
        pool.apply_async(process_one_file, folder, input_file)
    
