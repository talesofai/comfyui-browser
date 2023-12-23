from os import path, mkdir
from aiohttp import web

import server

from .utils import collections_path, browser_path, sources_path
from .routes import sources, collections, config, files

browser_app = web.Application()
browser_app.add_routes([
    web.get("/files", files.api_get_files),
    web.delete("/files", files.api_delete_file),
    web.put("/files", files.api_update_file),
    web.get("/files/view", files.api_view_file),

    web.post("/collections", collections.api_add_to_collections),
    web.post("/collections/workflows", collections.api_create_new_workflow),
    web.post("/collections/sync", collections.api_sync_my_collections),

    web.get("/sources", sources.api_get_sources),
    web.post("/sources", sources.api_create_source),
    web.delete("/sources/{name}", sources.api_delete_source),
    web.post("/sources/sync/{name}", sources.api_sync_source),
    web.get("/sources/all", sources.api_get_all_sources),

    web.get("/config", config.api_get_browser_config),
    web.put("/config", config.api_update_browser_config),

    web.static("/web", path.join(browser_path, 'web/build')),
])
server.PromptServer.instance.app.add_subapp("/browser/", browser_app)

def init_path():
    if not path.exists(collections_path):
        mkdir(collections_path)

    if not path.exists(sources_path):
        mkdir(sources_path)

init_path()

WEB_DIRECTORY = "web"
NODE_CLASS_MAPPINGS = {}
