import inspect
import unittest

from aiohttp.web import Application

from jija.app import App
from jija.utils.path import Path

from tests.test_data.app.normal.middlewares import AMiddleware, BMiddleware
from tests.test_data.app.normal.commands.a_command import ACommand
from tests.test_data.app.normal.commands.b_command import BCommand


class AppTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.empty_path = Path(['tests', 'test_data', 'app', 'empty'])
        self.normal_path = Path(['tests', 'test_data', 'app', 'normal'])
        self.error_path = Path(['tests', 'test_data', 'app', 'error'])
        self.broken = Path(['tests', 'test_data', 'app', 'broken'])

    def test_database_config(self):
        app = App(name='null', path=self.normal_path, aiohttp_app=Application())
        self.assertEqual(['aerich.models', 'tests.test_data.app.normal.database'], app.database_config)

        app = App(name='null', path=self.normal_path)
        self.assertEqual(['tests.test_data.app.normal.database'], app.database_config)

        app = App(name='null', path=self.empty_path)
        self.assertEqual([], app.database_config)

        app = App(name='null', path=self.error_path)
        self.assertEqual(['tests.test_data.app.error.database'], app.database_config)

    def test_get_routes(self):
        routes = App._App__get_routes(self.empty_path)
        self.assertTrue(isinstance(routes, list))
        self.assertEqual(len(routes), 0)

        routes = App._App__get_routes(self.normal_path)
        self.assertTrue(isinstance(routes, list))
        self.assertGreater(len(routes), 0)

        routes = App._App__get_routes(self.error_path)
        self.assertTrue(isinstance(routes, list))
        self.assertEqual(len(routes), 0)

    def test_get_database(self):
        database = App._App__get_database(self.empty_path)
        self.assertIsNone(database)

        database = App._App__get_database(self.normal_path)
        self.assertTrue(inspect.ismodule(database))

    def test_get_middlewares(self):
        middlewares = App._App__get_middlewares(self.empty_path)
        self.assertTrue(isinstance(middlewares, list))
        self.assertEqual(len(middlewares), 0)

        middlewares = App._App__get_middlewares(self.normal_path)
        self.assertTrue(isinstance(middlewares, list))
        self.assertEqual(
            list(map(lambda item: type(item), [AMiddleware(), BMiddleware()])),
            list(map(lambda item: type(item), middlewares))
        )

        middlewares = App._App__get_middlewares(self.error_path)
        self.assertTrue(isinstance(middlewares, list))
        self.assertEqual(len(middlewares), 0)

    def test_get_commands(self):
        commands = App._App__get_commands(self.empty_path)
        self.assertTrue(isinstance(commands, dict))
        self.assertEqual(len(commands), 0)

        commands = App._App__get_commands(self.normal_path)
        self.assertTrue(isinstance(commands, dict))
        self.assertEqual({'a_command': ACommand, 'b_command': BCommand}, commands)

        commands = App._App__get_commands(self.error_path)
        self.assertTrue(isinstance(commands, dict))
        self.assertEqual(len(commands), 0)

    def test_is_app(self):
        self.assertFalse(App.is_app(self.empty_path))
        self.assertTrue(App.is_app(self.normal_path))
        self.assertTrue(App.is_app(self.error_path))

        self.assertFalse(App.is_app(Path(['tests', 'test_data', 'app', '__not_app'])))

    def test_get_aiohttp_app(self):
        datasets = [
            [self.empty_path, {
                'routes': 0,
                'middlewares': 0
            }],

            [self.normal_path, {
                'routes': 1,
                'middlewares': 2
            }],

            [self.error_path, {
                'routes': 0,
                'middlewares': 0
            }]
        ]

        for path, data in datasets:
            app = App(name='null', path=path)
            aiohttp_app = app.get_aiohttp_app()
            self.assertEqual(data['routes'] * 2, len(list(aiohttp_app.router.routes())))
            self.assertEqual(data['middlewares'], len(aiohttp_app.middlewares))


def get_path(section):
    return Path(['tests', 'test_data', 'broken_app']) + section


class AppBrokeTest(unittest.TestCase):
    COMMANDS = get_path('commands')
    DATABASE = get_path('database')
    MIDDLEWARES = get_path('middlewares')
    ROUTES = get_path('routes')

    def test_broke(self):
        self.assertRaises(ModuleNotFoundError, lambda: App(name='null', path=self.DATABASE))
        self.assertRaises(ModuleNotFoundError, lambda: App(name='null', path=self.COMMANDS))
        self.assertRaises(ModuleNotFoundError, lambda: App(name='null', path=self.MIDDLEWARES))
        self.assertRaises(ModuleNotFoundError, lambda: App(name='null', path=self.ROUTES))
