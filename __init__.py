import os
import server
from aiohttp import web

browser_path = os.path.dirname(__file__)
static_path = os.path.join(browser_path, 'web/build')

routes = server.PromptServer.instance.routes

@routes.get("/browser/test")
async def api_test(request):
    return web.Response(
        text='<h1>Hello!</h1>',
        content_type='text/html')

routes.static(
    '/browser/',
    static_path
)

WEB_DIRECTORY = "web"
NODE_CLASS_MAPPINGS = {}
