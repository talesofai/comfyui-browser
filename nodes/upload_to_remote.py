import threading
import asyncio
import json
from PIL import Image
from PIL.PngImagePlugin import PngInfo
import numpy as np
import io
import base64
from ..utils import http_client, log

class UploadToRemote:
    CATEGORY = "Browser"

    RETURN_TYPES = ()
    RETURN_NAMES = ()

    FUNCTION = "run"

    OUTPUT_NODE = True


    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "remote_url": ["STRING", {}],
                "extension": (['jpeg', 'webp', 'png', 'jpg', 'gif'], ),
                "quality": ("INT", {"default": 85, "min": 1, "max": 100, "step": 1}),
                "embed_workflow": (["false", "true"],),
            },
            "optional": {
                "images": ["IMAGE", {}],
                "extra": ["STRING", {"forceInput": True}],
                "track_id": ["STRING", {"placeholder": "Optional. Post it as the track_id field."}],
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "prompt": "PROMPT",
            }
        }


    def run(self, remote_url, extension='jpeg', quality=85, images=[], extra='', embed_workflow='false', track_id=None, unique_id=None, prompt=None):
        def process_images(images, extension='jpeg', quality=85, embed_workflow='false', prompt=None):
            results = list()
            for image in images:
                i = 255. * image.cpu().numpy()
                img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

                # Delegate metadata/pnginfo
                if extension == 'webp':
                    img_exif = img.getexif()
                    if embed_workflow == 'true' and prompt is not None:
                        img_exif[0x010f] = "Prompt:" + json.dumps(prompt)
                    exif_data = img_exif.tobytes()
                else:
                    metadata = PngInfo()
                    if embed_workflow == 'true' and prompt is not None:
                        metadata.add_text("prompt", json.dumps(prompt))
                    exif_data = metadata

                output = io.BytesIO()
                if extension in ["jpg", "jpeg"]:
                    img.convert('RGB').save(output, quality=quality, optimize=True, format="JPEG")
                elif extension == 'webp':
                    img.convert('RGB').save(output, quality=quality, exif=exif_data, format="WEBP")
                else:
                    img.save(output, pnginfo=exif_data, optimize=True, format="PNG")
                image_bytes = output.getvalue()
                image_base64 = base64.b64encode(image_bytes)
                image_base64_str = image_base64.decode('utf-8')
                results.append(image_base64_str)

            return results

        async def callback(images, extra, remote_url, extension='jpeg', quality=85, embed_workflow='false', track_id=None, unique_id=None, prompt=None):
            data = {
                "images": process_images(images, extension, quality, embed_workflow, prompt),
                "extra": extra,
            }
            if track_id:
                data['track_id'] = track_id
            if unique_id:
                data['unique_id'] = unique_id

            headers = {
                "Content-Type": "application/json",
            }
            data = json.dumps(data).encode('utf-8')
            log(f"uploading {track_id} to {remote_url}")
            res = http_client().post(remote_url, data=data, headers=headers)
            log(f"uploaded {track_id}: {res.status_code} {res.text}")
            # TODO: check the response


        threading.Thread(
            target=asyncio.run,
            args=(callback(images, extra, remote_url, extension, quality, embed_workflow, track_id, unique_id, prompt),),
        ).start()

        return ()
