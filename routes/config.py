from aiohttp import web
import json

from ..utils import get_config, git_remote_name, run_cmd, git_init, \
    collections_path, config_path

async def api_get_browser_config(_):
    config = get_config()

    return web.json_response(config)

# git_repo
async def api_update_browser_config(request):
    json_data = await request.json()
    config = get_config()
    git_repo = json_data.get('git_repo', config.get('git_repo'))

    git_init()

    if git_repo == '':
        ret = run_cmd(f'git remote remove {git_remote_name}', collections_path())
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

def set_config(config):
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f)

def git_set_remote_url(remote_url, run_path = collections_path()):
    ret = run_cmd('git remote', run_path)

    if git_remote_name in ret.stdout.split('\n'):
        return run_cmd(f'git remote set-url {git_remote_name} {remote_url}', run_path)
    else:
        return run_cmd(f'git remote add {git_remote_name} {remote_url}', run_path)
