#!/usr/bin/env python3

import os
import random
import argparse
from collections import defaultdict, OrderedDict
import shutil

from lib.io import list_images, store_json


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('inputs', nargs='+')
    parser.add_argument('-ref', '--reference_dir', required=True)
    parser.add_argument('--count', type=int, default=100)
    parser.add_argument('-m', '--mode', choices=['rate', 'comp'], required=True)
    parser.add_argument('-o', '--out_dir')
    return parser.parse_args()


def main(args):
    print('Preparing experiment: {} images'.format(args.count))
    assert len(args.inputs) % 2 == 0
    inputs = OrderedDict([(args.inputs[2 * i], args.inputs[2 * i + 1])
                          for i in range(len(args.inputs) // 2)])

    print('Treatments:')
    for k, v in inputs.items():
        print('  {} : {}'.format(k, v))

    img_dict = defaultdict(list)
    for input_alias, input_dir in inputs.items():
        for img in list_images(input_dir):
            img_dict[img].append(input_alias)

    imgs = []
    for img, input_aliases in img_dict.items():
        if len(input_aliases) != len(inputs):
            print('Missing some images:', img, input_aliases)
            continue
        imgs.append(img)
    print('Num missing:', len(img_dict) - len(imgs))

    if len(imgs) > args.count:
        random.shuffle(imgs)
        imgs = imgs[:args.count]
    elif len(imgs) < args.count:
        print('Warning: # images, {}, is less than experiment size {}'.format(
            len(imgs), args.count))
    imgs.sort()

    config = {'mode': args.mode,
              'imgs': imgs,
              'names': list(inputs.keys()),
              'input_dirs': list(inputs.values()),
              'reference_dir': args.reference_dir,
              'cmd': ' '.join(os.sys.argv)}

    if args.out_dir is not None:
        os.makedirs(args.out_dir)
        store_json(os.path.join(args.out_dir, 'config.json'), config)
        os.makedirs(os.path.join(args.out_dir, 'reference'))
        for input_alias in inputs.keys():
            os.makedirs(os.path.join(args.out_dir, input_alias))
    else:
        print(config)

    for img in imgs:
        for input_alias, input_dir in inputs.items():
            src_img = os.path.join(input_dir, img)
            assert os.path.exists(src_img)
            if args.out_dir is not None:
                shutil.copyfile(src_img,
                                os.path.join(args.out_dir, input_alias, img),
                                follow_symlinks=True)
        if args.out_dir is not None:
            src_img = os.path.join(args.reference_dir, img)
            assert os.path.exists(src_img)
            shutil.copyfile(src_img,
                            os.path.join(args.out_dir, 'reference', img),
                            follow_symlinks=True)
    print('Done!')


if __name__ == '__main__':
    main(get_args())