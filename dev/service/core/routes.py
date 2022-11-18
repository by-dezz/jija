from aiohttp import web

from jija import config

from jija import views
from jija import router


class Buba(views.View):
    async def get(self):
        return web.json_response(data={'asd': 123})

routes = [
    router.Endpoint('/{id}/', Buba),
]
