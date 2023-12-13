import json
import os
from os import path
from aiohttp import request, web
from typing import TypedDict, List
import shutil
import time
import subprocess
import re

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

browser_path = path.dirname(__file__)
collections_path = path.join(browser_path, 'collections')
config_path = path.join(browser_path, 'config.json')
sources_path = path.join(browser_path, 'sources')

git_remote_name = 'origin'

image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
video_extensions = ['.mp4', '.mov', '.avi', '.webm', '.mkv']

info_file_suffix = '.info'

# folder_type = 'outputs', 'collections', 'sources'
def get_parent_path(folder_type: str):
    if folder_type == 'collections':
        return collections_path
    if folder_type == 'sources':
        return sources_path

    # outputs
    return folder_paths.output_directory

# folder_type = 'outputs', 'collections', 'sources'
def get_target_folder_files(folder_path: str, folder_type: str = 'outputs'):
    if '..' in folder_path:
        return None

    parent_path = get_parent_path(folder_type)
    files: List[FileInfoDict] = []
    target_path = path.join(parent_path, folder_path)

    if not path.exists(target_path):
        return None

    folder_listing = os.scandir(target_path)
    folder_listing = sorted(folder_listing, key=lambda f: (f.is_file(), -f.stat().st_ctime))
    for item in folder_listing:
        if not path.exists(item.path):
            continue

        name = path.basename(item.path)
        ext = path.splitext(name)[1].lower()
        if name == '' or name[0] == '.':
            continue
        if item.is_file():
            if not (ext in (image_extensions + video_extensions + ['.json'])):
                continue

        created_at = item.stat().st_ctime
        info_file_path = get_info_filename(item.path)
        info_data = {}
        if path.exists(info_file_path):
            with open(info_file_path, 'r') as f:
                info_data = json.load(f)
        if item.is_file():
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
                "notes": info_data.get("notes", "")
            })

    return files


def get_info_filename(filename):
    return path.splitext(filename)[0] + info_file_suffix

def run_cmd(cmd, run_path, log_cmd=True, log_code=True, log_message=True):
    if log_cmd:
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
    if not path.exists(config_path):
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
    if not path.exists(path.join(run_path, '.git')):
        run_cmd('git init', collections_path)

def log(message):
    print('[comfyui-browser] ' + message)

def add_uuid_to_filename(filename):
    name, ext = path.splitext(filename)
    return f'{name}_{int(time.time())}{ext}'

# folder_path, folder_type
@routes.get("/browser/files")
async def api_get_files(request):
    folder_path = request.query.get('folder_path', '')
    folder_type = request.query.get('folder_type', 'outputs')
    files = get_target_folder_files(folder_path, folder_type=folder_type)

    if files == None:
        return web.Response(status=404)

    return web.json_response({
        'files': files
    })


# filename, folder_path, folder_type
@routes.delete("/browser/files")
async def api_delete_file(request):
    json_data = await request.json()
    filename = json_data['filename']
    folder_path = json_data.get('folder_path', '')
    folder_type = json_data.get('folder_type', 'outputs')

    parent_path = get_parent_path(folder_type)
    target_path = path.join(parent_path, folder_path, filename)
    if not path.exists(target_path):
        return web.json_response(status=404)

    os.remove(target_path)
    info_file_path = get_info_filename(target_path)
    if path.exists(info_file_path):
        os.remove(info_file_path)

    info_filename = get_info_filename(target_path)
    if path.exists(info_filename):
        os.remove(info_filename)

    return web.Response(status=201)


# filename, folder_path, folder_type, new_data: {}
@routes.put("/browser/files")
async def api_update_file(request):
    json_data = await request.json()
    filename = json_data['filename']
    folder_path = json_data.get('folder_path', '')
    folder_type = json_data.get('folder_type', 'outputs')
    parent_path = get_parent_path(folder_type)

    new_data = json_data.get('new_data', None)
    print(new_data)
    if not new_data:
        return web.Response(status=400)

    new_filename = new_data['filename']
    notes = new_data['notes']

    old_file_path = path.join(parent_path, folder_path, filename)
    new_file_path = path.join(parent_path, folder_path, new_filename)

    if not path.exists(old_file_path):
        return web.Response(status=404)

    if new_filename and filename != new_filename:
        shutil.move(
            old_file_path,
            new_file_path
        )
        old_info_file_path = get_info_filename(old_file_path)
        if path.exists(old_info_file_path):
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

# filename, folder_path, folder_type
@routes.get("/browser/files/view")
async def api_view_file(request):
    folder_type = request.query.get("folder_type", "outputs")
    folder_path = request.query.get("folder_path", "")
    filename = request.query.get("filename", None)
    if not filename:
        return web.Response(status=404)

    parent_path = get_parent_path(folder_type)
    file_path = path.join(parent_path, folder_path, filename)

    if not path.exists(file_path):
        return web.Response(status=404)

    with open(file_path, 'rb') as f:
        media_file = f.read()

    content_type = 'application/json'
    file_extension = path.splitext(filename)[1].lower()
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

    if not path.exists(collections_path):
        os.mkdir(collections_path)

    source_file_path = path.join(folder_paths.output_directory, folder_path, filename)
    if not path.exists(source_file_path):
        return web.Response(status=404)

    new_filepath = path.join(
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

    new_filepath = path.join(
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
    if not path.exists(config_path):
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

@routes.get("/browser/sources")
async def api_get_sources(_):
    if not path.exists(sources_path):
        return web.json_response({
            'sources': []
        })

    sources = []
    source_list = os.scandir(sources_path)
    source_list = sorted(source_list, key=lambda f: (-f.stat().st_ctime))
    for item in source_list:
        if not path.exists(item.path):
            continue

        if item.is_file():
            continue

        cmd = f'git remote get-url {git_remote_name}'
        ret = run_cmd(cmd, path.join(item.path), log_cmd=False, log_code=False, log_message=False)
        if not (ret.returncode == 0 and len(ret.stdout) > 0):
            continue

        url = ret.stdout.split('\n')[0]
        name = path.basename(item.path)
        created_at = item.stat().st_ctime
        sources.append({
            "name": name,
            "created_at": created_at,
            "url": url
        })

    return web.json_response({
        'sources': sources
    })

# repo_url
@routes.post("/browser/sources")
async def api_create_source(request):
    json_data = await request.json()
    repo_url = json_data['repo_url']

    if not repo_url:
        return web.Response(status=400)

    pattern = r'[\:\/]([a-zA-Z0-9-_]+)\/([a-zA-Z0-9-_]+)(\.git)?'
    ret = re.search(pattern, repo_url)
    author = ret.group(1)
    name = ret.group(2)
    if not (author and name):
        return web.Response(status=400, text='wrong url')

    cmd = f'git clone --depth 1 {repo_url} {author}-{name}'
    ret = run_cmd(cmd, sources_path)
    if ret.returncode != 0:
        return web.Response(status=400, text=ret.stdout + ret.stderr)

    return web.Response(status=201)


# name
@routes.delete("/browser/sources/{name}")
async def api_delete_source(request):
    name = request.match_info.get('name', None)

    if not name:
        return web.Response(status=401)
    if not path.exists(path.join(sources_path, name)):
        return web.Response(status=404)

    cmd = f'rm -rf {name}'
    ret = run_cmd(cmd, sources_path)

    if ret.returncode == 0:
        return web.Response(status=200)
    else:
        return web.Response(status=400, text=ret.stdout + ret.stderr)

# name
@routes.post("/browser/sources/sync/{name}")
async def api_sync_source(request):
    name = request.match_info.get('name', None)

    if not name:
        return web.Response(status=401)
    if not path.exists(path.join(sources_path, name)):
        return web.Response(status=404)

    cmd = f'git pull'
    ret = run_cmd(cmd, path.join(sources_path, name))

    if ret.returncode == 0:
        return web.Response(status=200)
    else:
        return web.Response(status=400, text=ret.stdout + ret.stderr)


routes.static(
    '/browser/web',
    path.join(browser_path, 'web/build')
)

WEB_DIRECTORY = "web"
NODE_CLASS_MAPPINGS = {}
