from __future__ import annotations
from typing import Union, Type


import inspect
import json

import aiohttp.http_websocket
from aiohttp import web

import jija.response
import jija.serializers
import jija.exceptions
from . import wrappers as jija_wrappers


class SimpleView:
    methods = ('get', 'post', 'patch', 'put', 'delete')
    def __init__(self, request: web.Request, app: jija.app.App):
        self.__request = request
        self.__path_params: web.UrlMappingMatchInfo = request.match_info
        self.__method = self.request.method.lower()

        self.__app = app

    @classmethod
    def get_methods(cls):
        view_methods = []
        for method in cls.methods:
            if hasattr(cls, method):
                view_methods.append(method)

        return view_methods

    @classmethod
    def construct(cls, method, app):
        view_method = getattr(cls, method)

        if not inspect.iscoroutinefunction(view_method):
            async def sync_wrapper(view, **kwargs):
                return view_method(view, **kwargs)

            handler = sync_wrapper
        else:
            handler = view_method

        wrappers = cls.get_wrappers()
        handler = cls.use_wrappers(wrappers, handler)

        async def construct_wrapper(request):
            view = cls(request, app)
            return await handler(view)

        return construct_wrapper

    @classmethod
    def get_wrappers(cls):
        return [
            *filter(
                lambda _class: (
                    issubclass(_class, jija_wrappers.Wrapper) and
                    not issubclass(_class, SimpleView) and
                    _class != jija_wrappers.Wrapper
                ),
                cls.mro()
            )
        ]

    @classmethod
    def use_wrappers(cls, wrappers: list[Type[jija_wrappers.Wrapper]], handler):
        for wrapper in reversed(wrappers):
            handler = wrapper.construct(handler)

        return handler

    @property
    def request(self) -> web.Request:
        return self.__request

    @property
    def method(self) -> str:
        return self.__method

    @property
    def app(self) -> jija.app.App:
        return self.__app

class View(
    SimpleView,
    jija_wrappers.AuthCheckWrapper,
    jija_wrappers.DataLoadWrapper,
    jija_wrappers.ForceExitWrapper,
):
    DEFAULT_AUTH_RULE = None


class SerializedView(
    View,
    jija_wrappers.SerializerWrapper,
): ...


class DocMixin:
    pass


class WSView(SimpleView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__ws = None

    @classmethod
    def get_methods(cls):
        return 'get',

    @property
    def ws(self) -> web.WebSocketResponse:
        return self.__ws

    async def get(self):
        await self.on_connect()
        await self.process()
        await self.on_close()
        return self.ws

    async def on_connect(self):
        self.__ws = web.WebSocketResponse()
        await self.ws.prepare(self.request)

    async def on_close(self):
        pass

    async def process(self):
        async for message in self.ws:
            message: aiohttp.http_websocket.WSMessage

            if message.type == web.WSMsgType.TEXT:
                await self.on_message(message.data)
            elif message.type == web.WSMsgType.ERROR:
                await self.on_error(message.data)

    async def on_message(self, message):
        pass

    async def on_error(self, error: str):
        await self.close(code=500, message=error, force=True)

    async def send(self, message: Union[dict, str, bytes]):
        if isinstance(message, dict):
            await self.ws.send_json(message)
        elif isinstance(message, bytes):
            await self.ws.send_bytes(message)
        else:
            await self.ws.send_str(message)

    async def close(self, code: int = 1000, message: Union[str, bytes, dict] = None, force=False):
        if isinstance(message, dict):
            message = json.dumps(message).encode('utf-8')
        elif isinstance(message, str):
            message = message.encode('utf-8')

        await self.ws.close(code=code, message=message)
        if force is True:
            raise jija.exceptions.ViewForceExit(self.ws)
