import argparse
import os
from pathlib import Path
from typing import Tuple
from PIL import Image
from tqdm import tqdm


def resize(path: str, resized_shape: Tuple[int], check_raw_shape: Tuple[int] = None) -> None:
    # Load
    img = Image.open(path)

    # Check
    if check_raw_shape:
        if img.size != check_raw_shape:
            print('Skipped. shape = {}, path = {}'.format(img.size, path))  # TODO: make it logger
            return

    # Resize
    img_resize = img.resize(resized_shape)
    # print('{} -> {}'.format(img.size, img_resize.size))

    # Save
    img_resize.save(path)


def main(image_dir_path: str) -> None:
    check_raw_shape = (1920, 1080)  # TODO: 必要になったら汎用化する
    resized_rate = 1/10  # TODO: 必要になったら汎用化する
    target_suffix_list = ['.png', '.jpg']

    # 全てのファイルを巡回する
    path_list = []
    if not Path(image_dir_path).exists:
        raise ValueError('指定されたパスのディレクトリは存在しません')

    for root, dirs, files in os.walk(image_dir_path):
        # TODO: 大文字・小文字の区別
        path = [Path(root) / x for x in files if Path(x).suffix in target_suffix_list]
        path_list.extend(path)

    print('{} Files.'.format(len(path_list)))  # TODO: make it logger

    resized_shape = (check_raw_shape[0] * resized_rate, check_raw_shape[1] * resized_rate)
    resized_shape = (int(resized_shape[0]), int(resized_shape[1]))

    for path in tqdm(path_list):
        resize(path, resized_shape, check_raw_shape)


if __name__ == '__main__':
    # image_dir_path = '../data/work/messy_5'

    parser = argparse.ArgumentParser(description='resize images')
    parser.add_argument('-p', '--image_dir_path')

    args = parser.parse_args()
    main(args.image_dir_path)
    print('Completed.')  # TODO: make it logger
