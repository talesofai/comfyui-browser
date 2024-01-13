import requests
import json
from PIL import Image
import numpy as np
import os
import copy
import pandas as pd

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
        # "x_index": 0,
        # "y_index": 0,
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

    @staticmethod
    def get_filename(ix, iy, i):
        return f"x{ix}_y{iy}_{i}.jpeg"

    @staticmethod
    def get_preview_url(folder_name, filename):
        return f"{SERVER_BASE_URL}/browser/files/view?folder_type=outputs&filename={filename}&folder_path={folder_name}"

    def save_images(self, images):
        if not os.path.exists(self.output_folder_name):
            os.mkdir(self.output_folder_name)

        for index, image in enumerate(images):
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            img = img.convert('RGB')
            filename = self.get_filename(self.x_index, self.y_index, index)
            target_path = os.path.join(self.output_folder_name, filename)
            img.save(target_path, 'JPEG', quality=90)

    def run(self, images, input_x, input_y, value_x, value_y, output_folder_name, prompt, unique_id):
        self.output_folder_name = os.path.join(folder_paths.get_output_directory(), output_folder_name)
        if 'xyz_data' in prompt[unique_id]['inputs']:
            self.x_index = prompt[unique_id]['inputs']['xyz_data']['x_index']
            self.y_index = prompt[unique_id]['inputs']['xyz_data']['y_index']
            self.save_images(images)
            return ()

        batch_size = len(images)
        values_x = value_x.split(";")
        values_y = value_y.split(";")
        new_prompt =  copy.deepcopy(prompt)
        ret = {}
        for ix, vx in enumerate(values_x):
            row = {}
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

                row[vy] = ""
                for i in range(batch_size):
                    filename = self.get_filename(ix, iy, i)
                    preview_url = self.get_preview_url(output_folder_name, filename)
                    row[vy] += f'<img src="{preview_url}" width="100">'

            ret[vx] = row

        # To generate grid HTML
        def gird_title(input):
            return f"#{input['node_id']} {input['node_type']} - {input['widget_name']}"

        df = pd.DataFrame(ret)
        html = df.to_html(escape=False)
        html = f"<h4>X: {gird_title(input_x)}</h4><h4>Y: {gird_title(input_y)}</h4>" + html
        target_path = f"{self.output_folder_name}/result.html"
        with open(target_path, 'w') as f:
            f.write(html)

        return ()
