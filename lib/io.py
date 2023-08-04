import os
import json


def load_json(fpath):
    with open(fpath) as fp:
        return json.load(fp)


def store_json(fpath, obj, indent=2):
    kwargs = {}
    if indent is not None:
        kwargs['indent'] = indent
    with open(fpath, 'w') as fp:
        json.dump(obj, fp, **kwargs)


def load_text(fpath):
    with open(fpath, 'r') as fp:
        return fp.read().strip()


def store_text(fpath, s):
    with open(fpath, 'w') as fp:
        fp.write(s)


def list_images(img_dir, exts=('.jpg', '.png')):
    return [x for x in os.listdir(img_dir) if x.endswith(exts)]