#!/usr/bin/env python3

import os
import random
import argparse
from flask import Flask, render_template, send_file, request

from lib.io import load_json

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('exp_dir')
    parser.add_argument('-p', '--port', type=int, default=10000)
    return parser.parse_args()


def shuffle_list(l):
    l = list(l)
    random.shuffle(l)
    return l


def build_flask_app(exp_dir):
    config = load_json(os.path.join(exp_dir, 'config.json'))
    print('Config:', config)

    mode = config['mode']
    images = config['imgs']
    names = config['names']

    app = Flask(__name__, template_folder='templates', static_folder='static')

    app.jinja_env.filters['shuffle'] = shuffle_list

    @app.route('/')
    def root():
        blind = request.args.get('blind', 1, type=int) != 0
        if mode == 'comp':
            return render_template(
                'comp.html', images=images, names=names, blind=blind,
                num_imgs=len(images),
                has_reference=config['reference_dir'] is not None)
        elif mode == 'rate':
            images_copy = []
            for n in names:
                images_copy.extend((img, n) for img in images)
            random.shuffle(images_copy)

            return render_template(
                'rate.html', images=images_copy, names=names, blind=blind,
                num_imgs=len(images_copy),
                has_reference=config['reference_dir'] is not None)
        else:
            raise NotImplementedError(mode)

    @app.route('/image/<name>/<img_name>')
    def get_image(name, img_name):
        return send_file(os.path.join(exp_dir, name, img_name))

    return app


def main(args):
    app = build_flask_app(args.exp_dir)

    # Serve updated templates if they are edited when the server is running
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    # debug=true means the server will restart when the code is edited
    app.run(debug=True, port=args.port, host='0.0.0.0')


if __name__ == '__main__':
    main(get_args())