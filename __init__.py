import json
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
collections_path = os.path.join(browser_path, 'collections')

# type = 'output' or 'collections'
def get_target_folder_files(folder_path: str, type: str = 'output'):
    parent_path = output_path
    if type == 'collections':
        parent_path = collections_path

    files: List[FileInfoDict] = []
    target_path = os.path.join(parent_path, folder_path)

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


def get_info_filename(filename):
    return os.path.splitext(filename)[0] + ".info"

@routes.get("/browser/files")
async def api_get_files_root(_):
    files = get_target_folder_files('')

    if files == None:
        return web.Response(status=404)

    return web.json_response({
        'files': files
    })


@routes.get("/browser/files/{folder_path}")
async def api_get_files_folder(request):
    files = get_target_folder_files(request.match_info['folder_path'])

    if files == None:
        return web.Response(status=404)

    return web.json_response({
        'files': files
    })


@routes.delete("/browser/files")
async def api_delete_file(request):
    json_data = await request.json()
    filename = json_data['filename']
    folder_path = json_data['folder_path'] or ''
    parent_path = output_path
    if json_data['type'] == 'collections':
        parent_path = collections_path

    target_path = os.path.join(parent_path, folder_path, filename)
    if not os.path.exists(target_path):
        return web.json_response(status=404)

    os.remove(target_path)

    info_filename = get_info_filename(target_path)
    if os.path.exists(info_filename):
        os.remove(info_filename)

    return web.Response(status=201)


@routes.put("/browser/collections/{filename}")
async def api_update_collection(request):
    json_data = await request.json()
    filename = request.match_info["filename"]
    folder_path = json_data['folder_path'] or ''

    new_filename = json_data['filename'] or filename
    notes = json_data['notes']

    if filename != new_filename:
        shutil.move(
            os.path.join(collections_path, filename),
            os.path.join(collections_path, new_filename)
        )

    if notes:
        extra = {
            "notes": notes
        }
        info_filename = get_info_filename(new_filename)
        with open(os.path.join(collections_path, info_filename), "w") as outfile:
            json.dump(extra, outfile)


@routes.get("/browser/collections")
async def api_get_collections(_):
    files = get_target_folder_files('', 'collections')

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
