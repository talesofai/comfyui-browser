class SelectInputs:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_1": [["none"], {}],
                "input_2": [["none"], {}],
                "input_3": [["none"], {}],
                "input_4": [["none"], {}],
            },
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO",
                "unique_id": "UNIQUE_ID",
            },
        }


    # {
        # "node_id": 4,
        # "path": "ckpt_name": "nieta_mix2.safetensors",
        # "class_type": "CheckpointLoaderSimple",
    # }
    RETURN_TYPES = ("INPUT", "INPUT", "INPUT", "INPUT",)
    RETURN_NAMES = ("input_1", "input_2", "input_3", "input_4",)

    FUNCTION = "run"

    OUTPUT_NODE = True

    CATEGORY = "Browser"

    def run(self, input_1, input_2, input_3, input_4, prompt={}, extra_pnginfo=None, unique_id=None):
        return (input_1, input_2, input_3, input_4)
