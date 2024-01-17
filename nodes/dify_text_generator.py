import requests
import json

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
                "query": ["STRING", {"multiline": True}],
            }
        }

    def run(self, dify_api_endpoint, api_key, query):
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
        r = requests.post(
            dify_api_endpoint,
            headers=header,
            data=json.dumps(data),
            proxies=proxies
        )

        if not r.ok:
            raise Exception(f"Request Dify Error: {r.text}")

        content = json.loads(r.content)
        return (content["answer"], )
