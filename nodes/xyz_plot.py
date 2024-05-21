import shutil
import time
import json
from PIL import Image
import numpy as np
import os
import copy

import folder_paths

from ..utils import SERVER_BASE_URL, http_client

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
                "value_z": ["STRING", {"multiline": True, "placeholder": 'Z values split by semicolon such as "1girl; 1boy"'}],
                "output_folder_name": ["STRING", {"default": "xyz_plot"}],
            },
            "optional": {
                "input_z": ["INPUT", {}],
            },
            "hidden": {
                "prompt": "PROMPT",
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
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
    def get_filename(ix, iy, iz, i):
        if (iz >= 0):
            return f"x{ix}_y{iy}_z{iz}_{i}.jpeg"
        else:
            return f"x{ix}_y{iy}_{i}.jpeg"

    @staticmethod
    def get_preview_url(folder_name, filename):
        return f"/browser/files/view?folder_type=outputs&filename={filename}&folder_path={folder_name}"

    def save_images(self, images):
        os.makedirs(self.output_folder_name, exist_ok=True)

        for index, image in enumerate(images):
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            img = img.convert('RGB')
            filename = self.get_filename(self.x_index, self.y_index, self.z_index, index)
            target_path = os.path.join(self.output_folder_name, filename)
            img.save(target_path, 'JPEG', quality=90)

    def run(self, images, input_x, input_y, value_x, value_y, output_folder_name, prompt, unique_id, input_z=None, value_z="", extra_pnginfo=None):
        self.output_folder_name = os.path.join(
            folder_paths.get_output_directory(),
            output_folder_name,
        )

        if 'xyz_data' in prompt[unique_id]['inputs']:
            self.x_index = prompt[unique_id]['inputs']['xyz_data']['x_index']
            self.y_index = prompt[unique_id]['inputs']['xyz_data']['y_index']
            self.z_index = prompt[unique_id]['inputs']['xyz_data']['z_index']
            self.save_images(images)
            return ()

        if os.path.exists(self.output_folder_name):
            shutil.move(self.output_folder_name, self.output_folder_name + f'_old_{int(time.time())}')

        def filter_values(value):
            return list(filter(lambda x: x != '', value.split(";")))

        def queue_new_prompt(prompt):
            data = json.dumps({
                'prompt': prompt
            }).encode('utf-8')

            # for some special network environments like AutoDL
            proxies = {"http": "", "https": ""}
            return http_client().post(SERVER_BASE_URL + '/prompt', data=data, proxies=proxies)


        batch_size = len(images)
        values_x = filter_values(value_x)
        values_y = filter_values(value_y)
        values_z = filter_values(value_z)
        new_prompt = copy.deepcopy(prompt)
        ret = []
        for ix, vx in enumerate(values_x):
            vx = vx.strip()
            row = []
            for iy, vy in enumerate(values_y):
                vy = vy.strip()
                new_prompt[input_x["node_id"]]["inputs"][input_x["widget_name"]] = vx
                new_prompt[input_y["node_id"]]["inputs"][input_y["widget_name"]] = vy

                new_prompt[unique_id]['inputs']['xyz_data'] = {
                    "source_unique_id": unique_id,
                    "output_folder_name": output_folder_name,
                    "x_index": ix,
                    "y_index": iy,
                    "z_index": -1,
                }

                ceil = []
                if (input_z and len(values_z) > 0):
                    for iz, vz in enumerate(values_z):
                        vz = vz.strip()
                        new_prompt[input_z["node_id"]]["inputs"][input_z["widget_name"]] = vz
                        new_prompt[unique_id]['inputs']['xyz_data']['z_index'] = iz
                        queue_new_prompt(new_prompt)
                        zCeil = []
                        for i in range(batch_size):
                            filename = self.get_filename(ix, iy, iz, i)
                            preview_url = self.get_preview_url(output_folder_name, filename)
                            zCeil.append({
                                "uuid": ":".join([output_folder_name, str(ix), str(iy), str(iz), str(i)]),
                                "type": "img",
                                "src": preview_url,
                            })
                        ceil.append({
                            "type": "axis",
                            "value": vz,
                            "children": zCeil,
                        })
                else:
                    queue_new_prompt(new_prompt)
                    for i in range(batch_size):
                        filename = self.get_filename(ix, iy, -1, i)
                        preview_url = self.get_preview_url(output_folder_name, filename)
                        ceil.append({
                            "uuid": ":".join([output_folder_name, str(ix), str(iy), "-1", str(i)]),
                            "type": "img",
                            "src": preview_url,
                        })

                row.append({
                    "type": "axis",
                    "value": vy,
                    "children": ceil,
                })

            ret.append({
                "type": "axis",
                "value": vx,
                "children": row,
            })

        # Check if the directory exists
        try:
            os.makedirs(self.output_folder_name, exist_ok=True)
        except Exception as e:
            raise Exception(f"Failed to create directory: {e}")

        browser_base_url = f"/browser/s/outputs/{output_folder_name}"
        retData = {
            "result": ret,
        }
        if extra_pnginfo:
            workflow_filename = "workflow.json"
            with open(f"{self.output_folder_name}/{workflow_filename}", "w", encoding="utf-8") as f:
                json.dump(extra_pnginfo['workflow'], f)
            retData["workflow"] = {
                "url": f'{browser_base_url}/{workflow_filename}',
            }

        axisConst = ["X", "Y", "Z"]
        retData["annotations"] = []
        for index, ele in enumerate([input_x, input_y, input_z]):
            if not ele:
                continue
            retData["annotations"].append({
                "axis": axisConst[index],
                "key": f"#{ele['node_id']} {ele['node_title']}",
                "type": ele['widget_name'],
            })


        target_path = f"{self.output_folder_name}/result.json"
        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(retData, f)

        return {
            "ui": {
                "result_path": [f"/browser/web/xyz_plot.html?path={browser_base_url}/result.json"],
            },
            "result": (),
        }
