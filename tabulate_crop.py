#!/usr/bin/env python3

import argparse
from collections import defaultdict
from tabulate import tabulate

from lib.io import load_json


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('label_file')
    return parser.parse_args()


def get_unique(key, data):
    return sorted(list({x[key] for x in data}))


def main(args):
    labels = load_json(args.label_file)

    treatment = get_unique('name', labels)
    tags = get_unique('tag', labels)

    # Number of images with tags by treatment
    name_tag_to_images = defaultdict(set)
    for label in labels:
        name_tag_to_images[(label['name'], label['tag'])].add(label['img'])
        name_tag_to_images[(label['name'], 'ANY')].add(label['img'])

        for tag in tags:
            if tag != label['tag']:
                name_tag_to_images[
                    (label['name'], 'ANY~{}'.format(tag))
                ].add(label['img'])

    columns = ['ANY'] + tags
    data = []
    for name in treatment:
        data.append([name] + [
            len(name_tag_to_images[(name, c)]) for c in columns])

    print(tabulate(data, headers=['Method'] + columns))
    print()

    columns2 = ['ANY~{}'.format(x) for x in tags]
    data2 = []
    for name in treatment:
        data2.append([name] + [
            len(name_tag_to_images[(name, c)]) for c in columns2])
    print(tabulate(data2, headers=['Method'] + columns2))

    print('Done!')


if __name__ == '__main__':
    main(get_args())
