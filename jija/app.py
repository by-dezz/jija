import importlib
import os
from pathlib import Path

from aiohttp import web
from jija import config

from jija.middleware import Middleware
from jija.utils.collector import collect_subclasses
from jija.command import Command


class App:
    def __init__(self, *, name, path, aiohttp_app=None, parent=None):
        """
        :type name: str
        :type path: jija.utils.path.Path
        :type aiohttp_app: web.Application
        :type parent: App
        """

        self.__parent = parent
        if parent:
            parent.add_child(self)

        self.__path = path
        self.__name = name
        self.__is_core = aiohttp_app is not None

        self.__routes = None
        self.__middlewares = None
        self.__commands = None

        self.__aiohttp_app = None

        self.__childes = []
        self.__load(aiohttp_app)

    @property
    def parent(self):
        """:rtype: App"""
        return self.__parent

    @property
    def name(self):
        """:rtype: str"""
        return self.__name

    @property
    def routes(self):
        """:rtype: list"""
        return self.__routes

    @property
    def middlewares(self):
        """:rtype: list[Middleware]"""
        return self.__middlewares

    @property
    def aiohttp_app(self):
        """:rtype: web.Application"""
        return self.__aiohttp_app

    @property
    def childes(self):
        """:rtype: list[App]"""
        return self.__childes

    @property
    def path(self):
        """:rtype: jija.utils.path.Path"""
        return self.__path

    @property
    def commands(self):
        """:rtype: list[str]"""
        return self.__commands

    def __load(self, aiohttp_app=None):
        """
        :type aiohttp_app: web.Application
        """

        self.__routes = self.__get_routes()
        self.__middlewares = self.__get_middlewares()
        self.__commands = self.__get_commands()

        self.__aiohttp_app = self.get_aiohttp_app(aiohttp_app)

    def __get_routes(self) -> list:
        if not self.exist('routes'):
            return []

        import_path = self.get_import_path('routes')
        routes_module = importlib.import_module(import_path)

        routes = getattr(routes_module, 'routes', None)
        return routes or []

    def __get_middlewares(self) -> list:
        if not self.exist('middlewares'):
            return []

        import_path = self.get_import_path('middlewares')
        middlewares_module = importlib.import_module(import_path)
        middlewares = collect_subclasses(middlewares_module, Middleware)

        return list(map(lambda middleware: middleware(), middlewares))

    def __get_commands(self) -> dict:
        if not self.exist('commands'):
            return {}

        commands = {}
        commands_path = self.__path.joinpath('commands')
        for file in os.listdir(commands_path):
            if file.endswith('.py') and not file.startswith('_'):

                import_path = self.get_import_path(f'{commands}.{file.removesuffix(".py")}')
                command_module = importlib.import_module(import_path)

                command = list(collect_subclasses(command_module, Command))
                if command:
                    commands[file.replace('.py', '')] = command[0]

        return commands

    @staticmethod
    def is_app(path):
        """
        :type path: jija.utils.path.Path
        :rtype: bool
        """

        return os.path.isdir(path.system) and os.path.exists((path + 'app.py').system) and\
               not path.has_protected_nodes()

    def get_aiohttp_app(self, aiohttp_app=None):
        """
        :type aiohttp_app: web.Application
        :rtype: web.Application
        """

        aiohttp_app = aiohttp_app or web.Application()

        aiohttp_app.middlewares.extend(self.__middlewares)
        aiohttp_app.add_routes(self.__routes)

        return aiohttp_app

    def add_child(self, child):
        """
        :type child: App
        """

        self.__childes.append(child)

    def get_import_path(self, to: str):
        modify_class_path = self.path.joinpath(to)
        return ".".join(modify_class_path.relative_to(config.StructureConfig.PROJECT_PATH).parts)

    def exist(self, name):
        return os.path.exists(f'/{self.__path}/{name}') or os.path.exists(f'/{self.__path}/{name}.py')
