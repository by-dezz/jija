from aiohttp import web

import jija.app
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

    AUTH: drivers.AuthDriver = fields.InstanceField(
        instance_pattern=drivers.AuthDriver,
        required=False
    )

    def __init__(self, *, docs=None, database=None, auth=None):
        super().__init__(docs=docs, database=database, auth=auth)

    @classmethod
    def drivers(cls):
        return (
            cls.DOCS,
            cls.DATABASE,
            cls.AUTH,
        )

    @classmethod
    def core_setup(cls, app: jija.app.App):
        for item in cls.drivers():
            item and item.core_setup(app)

    @classmethod
    def setup(cls, app: jija.app.App):
        for item in cls.drivers():
            item and item.setup(app)

    @classmethod
    async def preflight(cls):
        for item in cls.drivers():
            item and await item.preflight()
