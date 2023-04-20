from aiohttp import web

from jija.config import base
from jija.serializers import fields
from jija import drivers


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
