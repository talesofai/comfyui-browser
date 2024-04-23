from os import path, scandir, makedirs
import json
from aiohttp import web, ClientSession, ClientTimeout
import re
import shutil
import os, stat, errno

from ..utils import sources_path, run_cmd, browser_path, git_remote_name


def handle_remove_readonly(func, path, exc):
    excvalue = exc[1]
    if excvalue.errno == errno.EACCES:
        os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777
        func(path)
    else:
        raise

async def api_get_sources(_):
    if not path.exists(sources_path()):
        return web.json_response({
            'sources': []
        })

    sources = []
    source_list = scandir(sources_path())
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
async def api_create_source(request):
    json_data = await request.json()
    repo_url = json_data['repo_url']

    if not repo_url:
        return web.Response(status=400)

    makedirs(sources_path(), exist_ok=True)

    pattern = r'[\:\/]([a-zA-Z0-9-_]+)\/([a-zA-Z0-9-_]+)(\.git)?'
    ret = re.search(pattern, repo_url)
    author = ret.group(1)
    name = ret.group(2)
    if not (author and name):
        return web.Response(status=400, text='wrong url')

    cmd = f'git clone --depth 1 {repo_url} {author}-{name}'
    ret = run_cmd(cmd, sources_path())
    if ret.returncode != 0:
        return web.Response(status=400, text=ret.stdout + ret.stderr)

    return web.Response(status=201)


# name
async def api_delete_source(request):
    name = request.match_info.get('name', None)

    if not name:
        return web.Response(status=401)

    target_path = path.join(sources_path(), name)
    if not path.exists(target_path):
        return web.Response(status=404)

    shutil.rmtree(target_path, onerror=handle_remove_readonly)
    return web.Response(status=200)

# name
async def api_sync_source(request):
    name = request.match_info.get('name', None)

    if not name:
        return web.Response(status=401)
    if not path.exists(path.join(sources_path(), name)):
        return web.Response(status=404)

    cmd = f'git pull'
    ret = run_cmd(cmd, path.join(sources_path(), name))

    if ret.returncode == 0:
        return web.Response(status=200)
    else:
        return web.Response(status=400, text=ret.stdout + ret.stderr)

async def api_get_all_sources(_):
    source_url = 'https://github.com/talesofai/comfyui-browser/raw/main/data/sources.json'
    file_path = path.join(browser_path, 'data/sources.json')
    timeout = ClientTimeout(connect=2, total=4)

    sources = {
        "sources": []
    }
    try:
        async with ClientSession(timeout=timeout) as session:
            async with session.get(source_url) as resp:
                if resp.ok:
                    ret = await resp.text()
                    sources = json.loads(ret)
    except:
        with open(file_path, 'r', encoding="utf-8") as f:
            sources = json.load(f)

    return web.json_response(sources)
