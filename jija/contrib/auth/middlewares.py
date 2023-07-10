from aiohttp import web
from aiohttp_session import session_middleware, AbstractStorage

from jija import middlewares


class SessionMiddleware(middlewares.Middleware):
    def __init__(self, storage: AbstractStorage):
        self._handler = session_middleware(storage)

    async def handler(self, request: web.Request, handler):
        request.user = None
        return await self._handler(request, handler)
