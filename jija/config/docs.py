from jija import docs
from . import base, fields


class DocsConfig(base.Config):
    URL: str = fields.CharField(default='/docs')

    def __init__(self, url=None):
        super().__init__(url=url)

    @classmethod
    def base_app_update(cls, aiohttp_app):
        docs_setuper = docs.DocsSetup(aiohttp_app)
        aiohttp_app = docs_setuper.setup()
        return aiohttp_app
