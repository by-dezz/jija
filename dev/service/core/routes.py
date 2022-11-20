from aiohttp import web


from jija import views
from jija import router

class Buba(views.View):
    async def get(self):
        from core import models
        return web.json_response(data={'asd': 123})


routes = [
    router.Endpoint('/{id}/', Buba),
]
