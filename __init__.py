from os import path, mkdir
from aiohttp import web

import server

from .utils import collections_path, browser_path, sources_path, download_logs_path
from .routes import sources, collections, config, files, downloads
from .nodes import select_inputs, load_image_by_url, xyz_plot

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

    web.post("/downloads", downloads.api_create_new_download),
    web.get("/downloads", downloads.api_list_downloads),
    web.get("/downloads/{uuid}", downloads.api_show_download),

    web.static("/web", path.join(browser_path, 'web/build')),
])
server.PromptServer.instance.app.add_subapp("/browser/", browser_app)

for dir in [collections_path, sources_path, download_logs_path]:
    if not path.exists(dir):
        mkdir(dir)

WEB_DIRECTORY = "web"
NODE_CLASS_MAPPINGS = {
    "LoadImageByUrl //Browser": load_image_by_url.LoadImageByUrl,
    "SelectInputs //Browser": select_inputs.SelectInputs,
    "XyzPlot //Browser": xyz_plot.XyzPlot,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadImageByUrl //Browser": "Load Image By URL",
    "SelectInputs //Browser": "Select Node Inputs",
    "XyzPlot //Browser": "XYZ Plot",
}
