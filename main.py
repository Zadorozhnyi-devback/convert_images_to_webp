#!/usr/local/bin python3


import os
import sys
from typing import List

from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()


__all__ = 'Handler',


class Handler:
    """ Script to convert image or dir images to webp """

    # todo: write tests

    DEFAULT_DIR = '.'
    IMAGE_EXTENSIONS = [
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.heic'
    ]

    def __init__(self):
        args = sys.argv[1:]
        if len(args) > 0:
            self.path = args[0]
            if self.path.endswith('/'):
                self.path = self.path[:-1]
        else:
            self.path = self.DEFAULT_DIR

    def run(self):
        if os.path.isfile(self.path):
            parts = self.path.split('/')
            self.path = '/'.join(parts[:-1])
            file_name = parts[-1]
            images = [file_name]
        else:
            images = self._get_dir_images()

        images_repr = f'\n - {self.path}/' + f'\n - {self.path}/'.join(images)
        answer = input(
            'Are you sure you want to continue?\n'
            'to continue - y\n\n'
            f'Images: {images_repr}\n\n'
            'to cancel - n or leave empty\n\n'
            'Answer: '
        )
        if answer.lower() in ('y', 'yes'):
            self._convert_images(images)

    def _get_dir_images(self) -> List[str]:
        files = sorted(os.listdir(self.path))

        image_files = [
            file for file in files
            if os.path.splitext(file)[1].lower() in self.IMAGE_EXTENSIONS
        ]
        return image_files

    def _convert_images(self, images: List[str]) -> None:
        for image_name in images:
            image = Image.open(f'{self.path}/{image_name}')
            output_name = f"{image_name.rsplit('.')[0]}.webp"
            image.save(f'{self.path}/{output_name}', 'webp', quality=75)
            print(f'{self.path}/{output_name} - DONE')


if __name__ == '__main__':
    handler = Handler()
    handler.run()
