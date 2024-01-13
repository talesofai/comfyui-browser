import hashlib
import requests
import os
from PIL import Image, ImageSequence, ImageOps
import numpy as np
import torch


import folder_paths

class LoadImageByUrl:
    CATEGORY = "Browser"

    RETURN_TYPES = ("IMAGE", )
    RETURN_NAMES = ("IMAGE", )

    FUNCTION = "run"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "url": ["STRING", {}],
            },
        }


    def __init__(self):
        self.url = ""

    def filename(self):
        return hashlib.md5(self.url.encode()).hexdigest()[:24] + '.jpg'

    def download_by_url(self):
        input_dir = folder_paths.get_input_directory()
        res = requests.get(self.url)
        if res.status_code == 200:
            download_path = os.path.join(input_dir, self.filename())
            with open(download_path, 'wb') as file:
                file.write(res.content)
        else:
            raise ValueError(f"Failed to load image from {self.url}: {res.status_code}")

    def run(self, url):
        self.url = url
        input_dir = folder_paths.get_input_directory()
        image_path = os.path.join(input_dir, self.filename())
        if not os.path.isfile(image_path):
            self.download_by_url()

        img = Image.open(image_path)
        output_images = []
        for i in ImageSequence.Iterator(img):
            i = ImageOps.exif_transpose(i)
            image = i.convert("RGB")
            image = np.array(image).astype(np.float32) / 255.0
            image = torch.from_numpy(image)[None,]
            output_images.append(image)

        if len(output_images) > 1:
            output_image = torch.cat(output_images, dim=0)
        else:
            output_image = output_images[0]

        return (output_image, )
