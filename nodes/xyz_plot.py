import requests
import json

from ..utils import SERVER_BASE_URL

class XyzPlot:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "x_input": ("INPUT",),
                "x_values": ("STRING", {"multiline": True, "placeholder": "x_values. Split by semicolon. E.g. dpmpp_2m; euler"}),
                "y_input": ("INPUT",),
                "y_values": ("STRING", {"multiline": True, "placeholder": "y_values. Split by semicolon. E.g. dpmpp_2m; euler"}),
            },
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO",
                "unique_id": "UNIQUE_ID",
            },
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()

    FUNCTION = "run"

    OUTPUT_NODE = True

    CATEGORY = "Browser"

    def run(self, image, prompt={}, extra_pnginfo=None, unique_id=None):
        print('ffffffffffff')
#         prompt['extra'] = {
            # 'browser_xyz_plot': {
                # 'unique_id': unique_id,
            # },
        # }
        # print(prompt)
        # data = json.dumps({
            # 'prompt': prompt
        # }).encode('utf-8')
        # res = requests.post(SERVER_BASE_URL + '/prompt', data=data)

        return {
            "ui":{
                "prompt": prompt,
            },
            "result": ()
        }
