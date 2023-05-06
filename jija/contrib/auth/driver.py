from aiohttp import web
from aiohttp_session import AbstractStorage

import jija.contrib.auth.middlewares
from jija.drivers.auth import AuthDriver


class AiohttpSessionDriver(AuthDriver):
    def __init__(self, storage: AbstractStorage, **kwargs):
        self.storage = storage
        super().__init__(**kwargs)

    def core_setup(self, app: jija.app.App):
        app.middlewares.insert(0, jija.contrib.auth.middlewares.SessionMiddleware(self.storage))
