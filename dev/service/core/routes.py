from aiohttp import web


from jija import views
from jija import router

import core.models
class Buba(views.View):
    async def get(self):
        return web.json_response(data={'asd': 123})

routes = [
    router.Endpoint('/{id}/', Buba),
]
