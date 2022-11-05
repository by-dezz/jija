from aiohttp import web


async def buba(request):
    print(123)
    return web.json_response(data={'asd': 123})

routes = [
    web.get('/', buba)
]
