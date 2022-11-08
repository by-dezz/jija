import unittest
from unittest import mock

from pathlib import Path

from jija.app import App
from jija import router, views
from jija.command import Command
from jija.middleware import Middleware


class AppTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.empty_path = Path('/tests/test_data/app/empty')
        self.normal_path = Path('/tests/test_data/app/normal')
        self.error_path = Path('/tests/test_data/app/error')
        self.broken = Path('/tests/test_data/app/broken')

    def test_get_router(self):
        app = App(name='test', path=Path('test'))

        app_router = app._App__get_router()
        self.assertIsInstance(app_router, router.Router)

        app.exist = mock.Mock()
        app.exist.return_value = True

        app.get_import_path = mock.Mock()
        app.get_import_path.return_value = 'test.routes'

        routes_mock = mock.MagicMock(spec=[])
        with mock.patch.dict('sys.modules', {'test.routes': routes_mock}):
            app_router = app._App__get_router()
            self.assertIsInstance(app_router, router.Router)

        routes_mock = mock.MagicMock(spec=[u'routes'])
        routes_mock.routes = [router.Endpoint('/', views.View)]
        with mock.patch.dict('sys.modules', {'test.routes': routes_mock}):
            app_router = app._App__get_router()
            self.assertIsInstance(app_router, router.Router)

    def test_get_middlewares(self):
        app = App(name='test', path=Path('test'))

        middlewares = app._App__get_middlewares()
        self.assertTrue(isinstance(middlewares, list))
        self.assertEqual(len(middlewares), 0)

        app.exist = mock.Mock()
        app.exist.return_value = True

        app.get_import_path = mock.Mock()
        app.get_import_path.return_value = 'test.middlewares'

        middlewares_mock = mock.MagicMock(spec=[])
        with mock.patch.dict('sys.modules', {'test.middlewares': middlewares_mock}):
            middlewares = app._App__get_middlewares()
            self.assertTrue(isinstance(middlewares, list))
            self.assertEqual(len(middlewares), 0)

        class AMiddleware(Middleware):
            pass

        class NotMiddleware(list):
            pass

        class BMiddleware(Middleware):
            pass

        middlewares_mock = mock.MagicMock(spec=[u'AMiddleware', u'NotMiddleware', u'NotMiddleware'])
        middlewares_mock.AMiddleware = AMiddleware
        middlewares_mock.NotMiddleware = NotMiddleware
        middlewares_mock.BMiddleware = BMiddleware
        with mock.patch.dict('sys.modules', {'test.middlewares': middlewares_mock}):
            middlewares = app._App__get_middlewares()
            self.assertEqual(
                list(map(lambda item: type(item), [AMiddleware(), BMiddleware()])),
                list(map(lambda item: type(item), middlewares))
            )

    def test_get_commands(self):
        app = App(name='test', path=Path('test'))

        commands = app._App__get_commands()
        self.assertTrue(isinstance(commands, dict))
        self.assertEqual(len(commands), 0)

        app.exist = mock.Mock()
        app.exist.return_value = True
        app.get_import_path = lambda to: f'test.{to}'

        commands_mock = mock.MagicMock(spec=[])
        with mock.patch.dict('sys.modules', {'test.commands.empty': commands_mock}):
            with mock.patch('os.listdir') as listdir_mock:
                    listdir_mock.return_value = ['empty.py']

                    commands = app._App__get_commands()
                    self.assertTrue(isinstance(commands, dict))
                    self.assertEqual(len(commands), 0)

        class ACommand(Command):
            pass

        class NotCommand(list):
            pass

        class BCommand(Command):
            pass

        a_command_mock = mock.MagicMock(spec=[u'ACommand'])
        a_command_mock.ACommand = ACommand

        not_command_mock = mock.MagicMock(spec=[u'NotCommand'])
        not_command_mock.NotCommand = NotCommand

        b_command_mock = mock.MagicMock(spec=[u'BCommand'])
        b_command_mock.BCommand = BCommand

        mock_path = {
            'test.commands.a_command': a_command_mock,
            'test.commands.not_command': not_command_mock,
            'test.commands.b_command': b_command_mock,
        }

        with mock.patch.dict('sys.modules', mock_path):
            with mock.patch('os.listdir') as listdir_mock:
                listdir_mock.return_value = ['a_command.py', 'not_command.py', 'b_command.py']

                commands = app._App__get_commands()
                self.assertTrue(isinstance(commands, dict))
                self.assertEqual({'a_command': ACommand, 'b_command': BCommand}, commands)

    def test_is_app(self):
        self.assertFalse(App.is_app(self.empty_path))
        self.assertTrue(App.is_app(self.normal_path))
        self.assertTrue(App.is_app(self.error_path))

        self.assertFalse(App.is_app(Path('/tests/test_data/app/__not_app')))

    # def test_get_aiohttp_app(self):
    #     datasets = [
    #         [self.empty_path, {
    #             'routes': 0,
    #             'middlewares': 0
    #         }],
    #
    #         [self.normal_path, {
    #             'routes': 1,
    #             'middlewares': 2
    #         }],
    #
    #         [self.error_path, {
    #             'routes': 0,
    #             'middlewares': 0
    #         }]
    #     ]
    #
    #     for path, data in datasets:
    #         app = App(name='null', path=path)
    #         aiohttp_app = app.get_aiohttp_app()
    #         self.assertEqual(data['routes'] * 2, len(list(aiohttp_app.router.routes())))
    #         self.assertEqual(data['middlewares'], len(aiohttp_app.middlewares))


def get_path(section):
    return Path('/tests/test_data/broken_app').joinpath(section)


# class AppBrokeTest(unittest.TestCase):
#     COMMANDS = get_path('commands')
#     DATABASE = get_path('database')
#     MIDDLEWARES = get_path('middlewares')
#     ROUTES = get_path('routes')
#
#     def test_broke(self):
#         self.assertRaises(ModuleNotFoundError, lambda: App(name='null', path=self.DATABASE))
#         self.assertRaises(ModuleNotFoundError, lambda: App(name='null', path=self.COMMANDS))
#         self.assertRaises(ModuleNotFoundError, lambda: App(name='null', path=self.MIDDLEWARES))
#         self.assertRaises(ModuleNotFoundError, lambda: App(name='null', path=self.ROUTES))
