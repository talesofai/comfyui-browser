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
                "preview": ["STRING", {"multiline": True}],
            }
        }

    @classmethod
    def VALIDATE_INPUTS(s, input_1, input_2, input_3, input_4):
        return True

    # {
        # "node_id": 4,
        # "node_type": "CheckpointLoaderSimple",
        # "widget_name": "ckpt_name",
    # }
    RETURN_TYPES = ("INPUT", "INPUT", "INPUT", "INPUT",)
    RETURN_NAMES = ("input_1", "input_2", "input_3", "input_4",)

    FUNCTION = "run"

    OUTPUT_NODE = True

    CATEGORY = "Browser"


    def run(self, input_1, input_2, input_3, input_4):
        ret = ()
        for input in [input_1, input_2, input_3, input_3]:
            node_id, node_type, widget_name = input.split("::")
            ret = ret + ({
                "node_id": node_id[1:],
                "node_type": node_type,
                "widget_name": widget_name,
            },)

        return ret
