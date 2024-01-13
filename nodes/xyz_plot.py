import requests
import json
from PIL import Image
import numpy as np
import os
import copy

import folder_paths

from ..utils import SERVER_BASE_URL

class XyzPlot:
    CATEGORY = "Browser"

    RETURN_TYPES = ()
    RETURN_NAMES = ()

    FUNCTION = "run"

    OUTPUT_NODE = True

    # xyz_data = {
        # "source_unique_id": "",
        # "output_folder_name": "",
        # "filename": "",
    # }
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ["IMAGE", {}],
                "input_x": ["INPUT", {}],
                "input_y": ["INPUT", {}],
                "value_x": ["STRING", {"multiline": True, "placeholder": 'X values split by semicolon such as "1girl; 1boy"'}],
                "value_y": ["STRING", {"multiline": True, "placeholder": 'Y values split by semicolon such as "1girl; 1boy"'}],
                "output_folder_name": ["STRING", {"default": "xyz_plot"}],
            },
            "hidden": {
                "prompt": "PROMPT",
                "unique_id": "UNIQUE_ID",
                # "xyz_data": "XYZ",
            },
        }

    @classmethod
    def IS_CHANGED(s, *args):
        return True

    def __init__(self) -> None:
        self.output_folder_name = os.path.join(folder_paths.get_output_directory(), "xyz_plot")
        self.x_index = 0
        self.y_index = 0

    def save_images(self, images):
        if not os.path.exists(self.output_folder_name):
            os.mkdir(self.output_folder_name)

        for index, image in enumerate(images):
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            img = img.convert('RGB')
            filename = f"x_{self.x_index}_y_{self.y_index}_{index}.jpeg"
            target_path = os.path.join(self.output_folder_name, filename)
            img.save(target_path, 'JPEG', quality=90)

    def run(self, images, input_x, input_y, value_x, value_y, output_folder_name, prompt, unique_id):
        self.output_folder_name = os.path.join(folder_paths.get_output_directory(), output_folder_name)
        print(prompt[unique_id]['inputs'])
        if 'xyz_data' in prompt[unique_id]['inputs']:
            self.x_index = prompt[unique_id]['inputs']['xyz_data']['x_index']
            self.y_index = prompt[unique_id]['inputs']['xyz_data']['y_index']
            self.save_images(images)
            return ()

        values_x = value_x.split(";")
        values_y = value_y.split(";")
        new_prompt =  copy.deepcopy(prompt)
        for ix, vx in enumerate(values_x):
            for iy, vy in enumerate(values_y):
                new_prompt[input_x["node_id"]]["inputs"][input_x["widget_name"]] = vx
                new_prompt[input_y["node_id"]]["inputs"][input_y["widget_name"]] = vy
                new_prompt[unique_id]['inputs']['xyz_data'] = {
                    "source_unique_id": unique_id,
                    "output_folder_name": output_folder_name,
                    "x_index": ix,
                    "y_index": iy,
                }
                data = json.dumps({
                    'prompt': new_prompt
                }).encode('utf-8')
                requests.post(SERVER_BASE_URL + '/prompt', data=data)

        return ()
