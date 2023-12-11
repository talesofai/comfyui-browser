import json
import os
from aiohttp import request, web
from typing import TypedDict, List
import shutil
import time
import subprocess

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

browser_path = os.path.dirname(__file__)
collections_path = os.path.join(browser_path, 'collections')
config_path = os.path.join(browser_path, 'config.json')

git_remote_name = 'origin'

image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
video_extensions = ['.mp4', '.mov', '.avi', '.webm', '.mkv']

info_file_suffix = '.info'


# type = 'output' or 'collections'
def get_target_folder_files(folder_path: str, type: str = 'output'):
    if '..' in folder_path:
        return None

    parent_path = folder_paths.output_directory
    if type == 'collections':
        parent_path = collections_path

    files: List[FileInfoDict] = []
    target_path = os.path.join(parent_path, folder_path)

    if not os.path.exists(target_path):
        return None

    folder_listing = os.scandir(target_path)
    folder_listing = sorted(folder_listing, key=lambda f: (f.is_file(), -f.stat().st_ctime))
    for item in folder_listing:
        if not os.path.exists(item.path):
            continue

        name = os.path.basename(item.path)
        ext = os.path.splitext(name)[1].lower()
        if name == '' or name[0] == '.':
            continue
        if item.is_file():
            if not (ext in (image_extensions + video_extensions + ['.json'])):
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
    return os.path.splitext(filename)[0] + info_file_suffix

def run_cmd(cmd, run_path, log_code=True, log_message=True):
    log(f'running: {cmd}')
    ret = subprocess.run(
        f'cd {run_path} && {cmd}',
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="UTF-8"
    )
    if log_code:
        if ret.returncode == 0:
            log('successed')
        else:
            log('failed')
    if log_message:
        if (len(ret.stdout) > 0 or len(ret.stderr) > 0):
            log(ret.stdout + ret.stderr)

    return ret


def get_config():
    if not os.path.exists(config_path):
        return {}

    with open(config_path, 'r') as f:
        return json.load(f)

def set_config(config):
    with open(config_path, 'w') as f:
        json.dump(config, f)

def git_set_remote_url(remote_url, run_path = collections_path):
    ret = run_cmd('git remote', run_path)

    if git_remote_name in ret.stdout.split('\n'):
        return run_cmd(f'git remote set-url {git_remote_name} {remote_url}', run_path)
    else:
        return run_cmd(f'git remote add {git_remote_name} {remote_url}', run_path)

def git_init(run_path = collections_path):
    if not os.path.exists(os.path.join(run_path, '.git')):
        run_cmd('git init', collections_path)

def log(message):
    print('[comfyui-browser] ' + message)

def add_uuid_to_filename(filename):
    name, ext = os.path.splitext(filename)
    return f'{name}_{int(time.time())}{ext}'

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
    parent_path = folder_paths.output_directory
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
    folder_path = json_data.get('folder_path', '')

    new_filename = json_data.get('filename', filename)
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
        content_type = f'image/{file_extension[1:]}'
    if file_extension in video_extensions:
        content_type = f'video/{file_extension[1:]}'

    return web.Response(
        body=media_file,
        content_type=content_type,
        headers={"Content-Disposition": f"filename=\"{filename}\""}
    )

# filename, folder_path
@routes.post("/browser/collections")
async def api_add_to_collections(request):
    json_data = await request.json()
    filename = json_data.get('filename')
    if not filename:
        return web.Response(status=404)

    folder_path = json_data.get('folder_path', '')

    if not os.path.exists(collections_path):
        os.mkdir(collections_path)

    source_file_path = os.path.join(folder_paths.output_directory, folder_path, filename)
    if not os.path.exists(source_file_path):
        return web.Response(status=404)

    new_filepath = os.path.join(
        collections_path,
        add_uuid_to_filename(filename)
    )

    shutil.copy(source_file_path, new_filepath)

    return web.Response(status=201)

# filename, content
@routes.post("/browser/collections/workflows")
async def api_create_new_workflow(request):
    json_data = await request.json()
    filename = json_data.get('filename')
    content = json_data.get('content')

    if not (filename and content):
        return web.Response(status=404)

    new_filepath = os.path.join(
        collections_path,
        add_uuid_to_filename(filename)
    )
    with open(new_filepath, 'w') as f:
        f.write(content)

    return web.Response(status=201)

@routes.get("/browser/config")
async def api_get_browser_config(_):
    config = get_config()

    return web.json_response(config)

# git_repo
@routes.put("/browser/config")
async def api_update_browser_config(request):
    json_data = await request.json()
    config = get_config()
    git_repo = json_data.get('git_repo', config.get('git_repo'))

    git_init()

    if git_repo == '':
        ret = run_cmd(f'git remote remove {git_remote_name}', collections_path)
        if not ret.returncode == 0:
            return web.json_response(
                { 'message': ret.stderr },
                status=500,
            )

        set_config({ 'git_repo': git_repo })
        return web.Response(status=200)

    ret = git_set_remote_url(git_repo)
    if not ret.returncode == 0:
        return web.json_response(
            { 'message': ret.stderr },
            status=500,
        )

    set_config({ 'git_repo': git_repo })
    return web.Response(status=200)

@routes.post("/browser/collections/sync")
async def api_sync_my_collections(_):
    if not os.path.exists(config_path):
        return web.Response(status=404)

    config = get_config()
    git_repo = config.get('git_repo')
    if not git_repo:
        return web.Response(status=404)

    git_init()

    cmd = 'git status -s'
    ret = run_cmd(cmd, collections_path)
    if len(ret.stdout) > 0:
        cmd = f'git add . && git commit -m "sync by comfyui-browser at {int(time.time())}"'
        ret = run_cmd(cmd, collections_path)
        if not ret.returncode == 0:
            return web.json_response(
                { 'message': "\n".join([ret.stdout, ret.stderr]) },
                status=500,
            )

    cmd = f'git fetch {git_remote_name} -v'
    ret = run_cmd(cmd, collections_path)
    if not ret.returncode == 0:
        return web.json_response(
            { 'message': "\n".join([ret.stdout, ret.stderr]) },
            status=500,
        )

    cmd = 'git branch --show-current'
    ret = run_cmd(cmd, collections_path)
    branch = ret.stdout.replace('\n', '')

    cmd = f'git merge {git_remote_name}/{branch}'
    ret = run_cmd(cmd, collections_path, log_code=False)

    cmd = f'git push {git_remote_name} {branch}'
    ret = run_cmd(cmd, collections_path)
    if not ret.returncode == 0:
        return web.json_response(
            { 'message': "\n".join([ret.stdout, ret.stderr]) },
            status=500,
        )

    return web.Response(status=200)

routes.static(
    '/browser/web',
    os.path.join(browser_path, 'web/build')
)

WEB_DIRECTORY = "web"
NODE_CLASS_MAPPINGS = {}
