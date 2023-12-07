import json
import os
from aiohttp import request, web
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
    notes: str

routes = server.PromptServer.instance.routes

comfy_path = os.path.dirname(folder_paths.__file__)
output_path = os.path.join(comfy_path, 'output')
browser_path = os.path.dirname(__file__)
collections_path = os.path.join(browser_path, 'collections')

image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
video_extensions = ['.mp4', '.mov', '.avi', '.webm', '.mkv']

# type = 'output' or 'collections'
def get_target_folder_files(folder_path: str, type: str = 'output'):
    if '..' in folder_path:
        return None

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
        ext = os.path.splitext(name)[1].lower()
        if not (item.is_dir() or ext in image_extensions or ext in video_extensions):
            continue

        created_at = item.stat().st_ctime
        if item.is_file():
            info_file_path = get_info_filename(item.path)
            info_data = {}
            if os.path.exists(info_file_path):
                with open(info_file_path, 'r') as f:
                    info_data = json.load(f)

            bytes = item.stat().st_size
            files.append({
                "type": "file",
                "name": name,
                "bytes": bytes,
                "created_at": created_at,
                "folder_path": folder_path,
                "notes": info_data.get("notes", "")
            })
        elif item.is_dir():
            files.append({
                "type": "dir",
                "name": name,
                "bytes": 0,
                "created_at": created_at,
                "folder_path": folder_path,
                "notes": ""
            })

    return files


def get_info_filename(filename):
    return os.path.splitext(filename)[0] + "_info.json"


# folder_path
@routes.get("/browser/files")
async def api_get_files_root(request):
    folder_path = request.query.get('folder_path', '')
    files = get_target_folder_files(folder_path)

    if files == None:
        return web.Response(status=404)

    return web.json_response({
        'files': files
    })


# filename, folder_path, type
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
    info_file_path = get_info_filename(target_path)
    if os.path.exists(info_file_path):
        os.remove(info_file_path)

    info_filename = get_info_filename(target_path)
    if os.path.exists(info_filename):
        os.remove(info_filename)

    return web.Response(status=201)


@routes.put("/browser/collections/{filename}")
async def api_update_collection(request):
    json_data = await request.json()
    filename = request.match_info.get("filename", None)
    folder_path = json_data['folder_path'] or ''

    new_filename = json_data['filename'] or filename
    notes = json_data['notes']

    old_file_path = os.path.join(collections_path, folder_path, filename)
    new_file_path = os.path.join(collections_path, folder_path, new_filename)

    if not os.path.exists(old_file_path):
        return web.Response(status=404)

    if filename != new_filename:
        shutil.move(
            old_file_path,
            new_file_path
        )
        old_info_file_path = get_info_filename(old_file_path)
        if os.path.exists(old_info_file_path):
            new_info_file_path = get_info_filename(new_file_path)
            shutil.move(
                old_info_file_path,
                new_info_file_path
            )

    if notes:
        extra = {
            "notes": notes
        }
        info_file_path = get_info_filename(new_file_path)
        with open(info_file_path, "w") as outfile:
            json.dump(extra, outfile)

    return web.Response(status=201)


@routes.get("/browser/collections")
async def api_get_collections(_):
    files = get_target_folder_files('', 'collections')

    if files == None:
        return web.Response(status=404)

    return web.json_response({
        'files': files
    })

# filename, folder_path
@routes.get("/browser/collections/view")
async def api_view_collection(request):
    folder_path = request.query.get("folder_path", '')
    filename = request.query.get("filename", None)
    if not filename:
        return web.Response(status=404)

    file_path = os.path.join(collections_path, folder_path, filename)

    if not os.path.exists(file_path):
        return web.Response(status=404)

    with open(file_path, 'rb') as f:
        media_file = f.read()

    content_type = 'application/json'
    file_extension = os.path.splitext(filename)[1].lower()
    if file_extension in image_extensions:
        content_type = f'image/{file_extension}'
    if file_extension in video_extensions:
        content_type = f'video/{file_extension}'

    return web.Response(
        body=media_file,
        content_type=content_type,
        headers={"Content-Disposition": f"filename=\"{filename}\""}
    )

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
    '/browser/web',
    os.path.join(browser_path, 'web/build')
)

WEB_DIRECTORY = "web"
NODE_CLASS_MAPPINGS = {}
