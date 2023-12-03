import os
from aiohttp import web
from typing import TypedDict, List
import shutil

import server
import folder_paths

class FileInfoDict(TypedDict):
    type: str
    name: str
    bytes: int
    created_at: float
    folder_path: str

routes = server.PromptServer.instance.routes

comfy_path = os.path.dirname(folder_paths.__file__)
output_path = os.path.join(comfy_path, 'output')
browser_path = os.path.dirname(__file__)

def get_target_folder_files(folder_path: str):
    files: List[FileInfoDict] = []
    target_path = os.path.join(output_path, folder_path)

    if not os.path.exists(target_path):
        return None

    folder_listing = os.scandir(target_path)
    folder_listing = sorted(folder_listing, key=lambda f: f.stat().st_ctime, reverse=True)
    for item in folder_listing:
        if not os.path.exists(item.path):
            continue
        name = os.path.basename(item.path)
        created_at = item.stat().st_ctime
        if item.is_file():
            bytes = item.stat().st_size
            files.append({
                "type": "file",
                "name": name,
                "bytes": bytes,
                "created_at": created_at,
                "folder_path": folder_path,
            })
        elif item.is_dir():
            files.append({
                "type": "dir",
                "name": name,
                "bytes": 0,
                "created_at": created_at,
                "folder_path": folder_path,
            })

    return files

@routes.get("/browser/files")
async def api_files_root(_):
    files = get_target_folder_files('')

    if files == None:
        return web.Response(status=404)

    return web.json_response({
        'files': files
    })

@routes.get("/browser/files/{folder_path}")
async def api_files_folder(request):
    files = get_target_folder_files(request.match_info['folder_path'])

    if files == None:
        return web.Response(status=404)

    return web.json_response({
        'files': files
    })

# filename, folder_path
@routes.post("/browser/collections")
async def api_add_to_collections(request):
    json_data = await request.json()
    filename = json_data['filename']
    folder_path = json_data['folder_path'] or ''
    collections_path = os.path.join(browser_path, 'collections')
    if not os.path.exists(collections_path):
        os.mkdir(collections_path)

    source_file_path = os.path.join(output_path, folder_path, filename)
    if not os.path.exists(source_file_path):
        return web.Response(status=404)

    shutil.copy(source_file_path, collections_path)

    return web.Response(status=201)

routes.static(
    '/browser/',
    os.path.join(browser_path, 'web/build')
)

WEB_DIRECTORY = "web"
NODE_CLASS_MAPPINGS = {}
