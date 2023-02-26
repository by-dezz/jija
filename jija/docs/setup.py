import os
from jija import config
from aiohttp_swagger import _swagger_home
import aiohttp_swagger
from . import views


class DocsSetup:
    STATIC_PATH = os.path.abspath(os.path.join(os.path.dirname(aiohttp_swagger.__file__), "swagger_ui3"))

    def __init__(self, aiohttp_app):
        self.__aiohttp_app = aiohttp_app

    def setup(self):
        self.__aiohttp_app.router.add_route('GET', f'{config.DocsConfig.URL}/', _swagger_home)
        self.__aiohttp_app.router.add_route(
            'GET', f"{config.DocsConfig.URL.rstrip('/')}/swagger.json", views.swagger_view)

        static_route = f'{config.DocsConfig.URL}/swagger_static'

        self.__aiohttp_app.router.add_static(static_route, self.STATIC_PATH)

        self.__aiohttp_app["SWAGGER_DEF_CONTENT"] = 'asdasd'
        self.__set_template()
        return self.__aiohttp_app

    def __set_template(self):
        static_route = f'{config.DocsConfig.URL}/swagger_static'

        with open(os.path.join(self.STATIC_PATH, "index.html"), "r") as file:
            index_html = file.read()

        self.__aiohttp_app["SWAGGER_TEMPLATE_CONTENT"] = (
            index_html
            .replace("##SWAGGER_CONFIG##", f"{config.DocsConfig.URL.rstrip('/')}/swagger.json")
            .replace("##STATIC_PATH##", f"{static_route}")
            .replace("##SWAGGER_VALIDATOR_URL##", "")
        )
