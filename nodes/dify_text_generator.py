import json
from ..utils import http_client

class DifyTextGenerator:
    CATEGORY = "Browser"

    RETURN_TYPES = ("STRING", )

    FUNCTION = "run"

    OUTPUT_NODE = True

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "dify_api_endpoint": ["STRING", {}],
                "api_key": ["STRING", {}],
            },
            "optional": {
                "query": ["STRING", {"multiline": True, "placeholder": "Input as the Query field."}],
                "inputs_json_str": ["STRING", {"multiline": True, "placeholder":  "JSON format. It will overwrite the query field above."}],
            },
        }

    def run(self, dify_api_endpoint, api_key, query, inputs_json_str=None):
        # for some special network environments like AutoDL
        proxies = {"http": "", "https": ""}
        header = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        data = {
            "user": "comfyui-browser",
            "response_mode": "blocking",
            "inputs" : { "query": query },
        }
        if inputs_json_str and len(inputs_json_str.strip()) > 0:
            # something weird, I have to add '{' and '}' manually
            data["inputs"] = json.loads("{" + inputs_json_str + "}")

        r = http_client().post(
            dify_api_endpoint,
            headers=header,
            data=json.dumps(data),
            proxies=proxies
        )

        if not r.ok:
            raise Exception(f"Request Dify Error: {r.text}")

        content = json.loads(r.content)
        return (content["answer"], )
