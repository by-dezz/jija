from jija.config import base
from jija.serializers import fields
from jija import app

from aiohttp_session.cookie_storage import EncryptedCookieStorage
import aiohttp_session
from aiohttp import web


class AuthConfig(base.Config):
    SECRET_KEY: str = fields.CharField()

    def __init__(self, *, secret_key):
        super().__init__(secret_key=secret_key)

    @classmethod
    def setup(cls, jija_app: app.App, aiohttp_app: web.Application):
        aiohttp_session.setup(aiohttp_app, EncryptedCookieStorage(cls.SECRET_KEY))
        # TODO fix this shit
        aiohttp_app.middlewares.insert(0, aiohttp_app.middlewares.pop(-1))
