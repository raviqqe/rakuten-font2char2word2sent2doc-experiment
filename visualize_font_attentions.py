#!/usr/bin/env python

import argparse
import json
import os
import os.path

import gargparse
import matplotlib.image as image
import numpy as np


gargparse.add_argument('char_file', type=argparse.FileType())
gargparse.add_argument('font_file', type=argparse.FileType())
gargparse.add_argument('attention_file', type=argparse.FileType())
gargparse.add_argument('dest_dir')


def main():
    os.makedirs(gargparse.ARGS.dest_dir, exist_ok=True)

    fonts = np.array(json.load(gargparse.ARGS.font_file), dtype=np.uint8)
    assert fonts.min() == 0 and fonts.max() == 255

    for char, font, attention in zip(
            [char.strip() for char in gargparse.ARGS.char_file.readlines()],
            np.stack([255 - fonts] * 3, axis=-1),
            np.array(json.load(gargparse.ARGS.attention_file))):
        assert np.isclose(attention.sum(), 1)

        font[:, :, 1] = font[:, :, 2] = np.minimum(
            font[:, :, 0],
            255 - (255 * np.sqrt(attention)).astype(np.uint8))
        image.imsave(os.path.join(gargparse.ARGS.dest_dir,
                                  hex(ord(char)) + '.img'),
                     font)


if __name__ == '__main__':
    main()
