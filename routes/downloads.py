from os import path
import shutil
import requests
import time
import asyncio
import json
from aiohttp import web
from tqdm import tqdm

import folder_paths

from ..utils import download_logs_path, log

def parse_options_header(content_disposition):
    param, options = '', {}
    split_header = content_disposition.split(';')

    # Extract the first parameter
    if len(split_header) > 0:
        param = split_header[0].strip()

    # Extract the options
    for option in split_header[1:]:
        option_split = option.split('=')
        if len(option_split) == 2:
            key = option_split[0].strip()
            value = option_split[1].strip().strip('"')
            options[key] = value

    return param, options


# credit: https://gist.github.com/phineas-pta/d73f9a035b05f8e923af8c01df057175
async def download_by_requests(uuid:str, download_url:str, save_in:str, filename:str="", overwrite:bool=False, chunk_size:int=1):
    log_file_path = path.join(download_logs_path, uuid + '.json')
    base_info = {
        'uuid': uuid,
        'download_url': download_url,
        'save_in': save_in,
        'filename': filename,
        'overwrite': overwrite,
        'result': '',
        'total_size': 0,
        'downloaded_size': 0,
    }
    with open(log_file_path, 'w') as log_file:
        json.dump(base_info, log_file)

    HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}

    with requests.get(download_url, headers=HEADERS, stream=True) as resp:
        MISSING_FILENAME = f"unkwown_{uuid}"
        # get file name
        if filename == "":
            if content_disposition := resp.headers.get("Content-Disposition"):
                param, options = parse_options_header(content_disposition)
                if param == "attachment":
                    filename = options.get("filename", MISSING_FILENAME)
            else:
                fileext = path.splitext(filename)[-1]
                if fileext != "":
                    filename = path.basename(download_url)
        if filename == "":
            filename = MISSING_FILENAME

        base_info['filename'] = filename
        with open(log_file_path, 'w') as log_file:
            json.dump(base_info, log_file)

        target_path = path.join(folder_paths.models_dir, save_in, filename)
        if not overwrite and path.exists(target_path):
            base_info['result'] = f'{target_path} already exists'
            return

        # download file
        tmp_target_path = target_path + '.downloading'
        TOTAL_SIZE = int(resp.headers.get("Content-Length", 0))
        CHUNK_SIZE = chunk_size * 10**6
        base_info['total_size'] = TOTAL_SIZE
        base_info['result'] = resp.reason
        log('download to ' + target_path)
        with (
            open(tmp_target_path, mode="wb") as file,
            open(log_file_path, 'w') as log_file,
            tqdm(total=TOTAL_SIZE, desc=f"download {filename}", unit="B", unit_scale=True) as bar,
        ):
            for data in resp.iter_content(chunk_size=CHUNK_SIZE):
                size = file.write(data)
                bar.update(size)
                base_info['downloaded_size'] += size
                log_file.seek(0)
                json.dump(base_info, log_file)
                log_file.write('\n' * 2)

        shutil.move(tmp_target_path, target_path)


# download_url, filename, save_in, overwrite
async def api_create_new_download(request):
    json_data = await request.json()
    download_url = json_data.get('download_url', None)
    save_in = json_data.get('save_in', None)
    filename = json_data.get('filename', '')
    overwrite = json_data.get('overwrite', False)

    if not (download_url and save_in):
        return web.Response(status=400)

    if '..' in save_in:
        return web.Response(status=400)

    asyncio.create_task(download_by_requests(str(int(time.time())), download_url, save_in, filename, overwrite))

    return web.json_response(status=201)
