from aiohttp import web

from jija.config import base
from jija.serializers import fields
from jija import drivers
from jija import app


class DriversConfig(base.Config):
    DOCS: drivers.DocsDriver = fields.InstanceField(
        instance_pattern=drivers.DocsDriver,
        required=False,
    )

    DATABASE: drivers.DatabaseDriver = fields.InstanceField(
        instance_pattern=drivers.DatabaseDriver,
        required=False
    )

    def __init__(self, *, docs=None, database=None):
        super().__init__(docs=docs, database=database)

    @classmethod
    def drivers(cls):
        return (
            cls.DOCS,
            cls.DATABASE,
        )

    @classmethod
    def core_setup(cls, jija_app, aiohttp_app: web.Application):
        for item in cls.drivers():
            item and item.core_setup(jija_app, aiohttp_app)

    @classmethod
    def setup(cls, jija_app: app.App, aiohttp_app: web.Application):
        for item in cls.drivers():
            item and item.setup(jija_app, aiohttp_app)

    @classmethod
    async def preflight(cls):
        for item in cls.drivers():
            item and await item.preflight()
