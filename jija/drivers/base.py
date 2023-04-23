from aiohttp import web
from jija import app


class Driver:
    def core_setup(self, jija_app: app.App, aiohttp_app: web.Application):
        pass

    def setup(self, jija_app: app.App, aiohttp_app: web.Application):
        pass

    async def preflight(self):
        pass
