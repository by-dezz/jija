import unittest
from unittest import mock

from pathlib import Path

from jija import app
from jija import router, views
from jija import command
from jija import middleware


class AppTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.empty_path = Path('/tests/test_data/app/empty')
        self.normal_path = Path('/tests/test_data/app/normal')
        self.error_path = Path('/tests/test_data/app/error')
        self.broken = Path('/tests/test_data/app/broken')

    def test_get_router(self):
        path = Path('test')
        app_router = app.App.get_router(path, None)
        self.assertIsInstance(app_router, router.Router)

        app_path = {
            'cls_get_import_path': lambda *_: 'test.routes',
            'cls_exist': lambda *_: True
        }

        with mock.patch.multiple(app.App, **app_path):
            routes_mock = mock.MagicMock(spec=[])
            with mock.patch.dict('sys.modules', {'test.routes': routes_mock}):
                app_router = app.App.get_router(path, None)
                self.assertIsInstance(app_router, router.Router)
                self.assertEqual(len(app_router.routes), 0)

            routes_mock = mock.MagicMock(spec=[u'routes'])
            routes_mock.routes = [router.Endpoint('/', views.View)]
            with mock.patch.dict('sys.modules', {'test.routes': routes_mock}):
                app_router = app.App.get_router(path, None)

                self.assertIsInstance(app_router, router.Router)
                self.assertEqual(len(app_router.endpoints), 1)

        app_path['CUSTOM_URL_PATH'] = '/custom'
        with mock.patch.multiple(app.App, **app_path):
            routes_mock = mock.MagicMock(spec=[u'routes'])
            routes_mock.routes = [router.Endpoint('/', views.View)]
            with mock.patch.dict('sys.modules', {'test.routes': routes_mock}):
                app_router = app.App.get_router(path, None)

                self.assertIsInstance(app_router, router.Router)
                self.assertEqual(len(app_router.endpoints), 1)
                self.assertIsInstance(app_router.endpoints[0], router.Include)
                self.assertEqual(app_router.endpoints[0].path, '/custom')

    def test_get_middlewares(self):
        path = Path('test')

        middlewares = app.App.get_middlewares(path)
        self.assertTrue(isinstance(middlewares, list))
        self.assertEqual(len(middlewares), 0)

        app_path = {
            'cls_get_import_path': lambda *_: 'test.middlewares',
            'cls_exist': lambda *_: True
        }

        with mock.patch.multiple(app.App, **app_path):
            middlewares_mock = mock.MagicMock(spec=[])
            with mock.patch.dict('sys.modules', {'test.middlewares': middlewares_mock}):
                middlewares = app.App.get_middlewares(path)
                self.assertTrue(isinstance(middlewares, list))
                self.assertEqual(len(middlewares), 0)

        class AMiddleware(middleware.Middleware):
            pass

        class NotMiddleware(list):
            pass

        class BMiddleware(middleware.Middleware):
            pass

        with mock.patch.multiple(app.App, **app_path):
            middlewares_mock = mock.MagicMock(spec=[u'AMiddleware', u'NotMiddleware', u'NotMiddleware'])
            middlewares_mock.AMiddleware = AMiddleware
            middlewares_mock.NotMiddleware = NotMiddleware
            middlewares_mock.BMiddleware = BMiddleware
            with mock.patch.dict('sys.modules', {'test.middlewares': middlewares_mock}):
                middlewares = app.App.get_middlewares(path)
                self.assertEqual(
                    list(map(lambda item: type(item), [AMiddleware(), BMiddleware()])),
                    list(map(lambda item: type(item), middlewares))
                )

    def test_get_commands(self):
        path = Path('test')

        commands = app.App.get_commands(path)
        self.assertTrue(isinstance(commands, dict))
        self.assertEqual(len(commands), 0)

        app_path = {
            'cls_get_import_path': lambda _, to: f'test.{to}',
            'cls_exist': lambda *_: True
        }

        with mock.patch.multiple(app.App, **app_path):
            commands_mock = mock.MagicMock(spec=[])
            with mock.patch.dict('sys.modules', {'test.commands.empty': commands_mock}):
                with mock.patch('os.listdir') as listdir_mock:
                    listdir_mock.return_value = ['empty.py']

                    commands = app.App.get_commands(path)
                    self.assertTrue(isinstance(commands, dict))
                    self.assertEqual(len(commands), 0)

        class ACommand(command.Command):
            pass

        class NotCommand(list):
            pass

        class BCommand(command.Command):
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

        with mock.patch.multiple(app.App, **app_path):
            with mock.patch.dict('sys.modules', mock_path):
                with mock.patch('os.listdir') as listdir_mock:
                    listdir_mock.return_value = ['a_command.py', 'not_command.py', 'b_command.py']

                    commands = app.App.get_commands(path)
                    self.assertTrue(isinstance(commands, dict))
                    self.assertEqual({'a_command': ACommand, 'b_command': BCommand}, commands)

    def test_is_app(self):
        path_mock = mock.MagicMock()
        path_mock.joinpath.return_value = path_mock
        # noinspection PyTypeHints
        path_mock.parts: mock.Mock

        # dir is file
        path_mock.is_dir.return_value = False
        path_mock.exists.return_value = True
        self.assertFalse(app.App.is_app(path_mock))
        self.assertEqual(0, path_mock.parts.call_count)

        # file is something magic
        path_mock.is_dir.return_value = True
        path_mock.exists.return_value = False
        self.assertFalse(app.App.is_app(path_mock))
        self.assertEqual(0, path_mock.parts.call_count)

        # file not exists
        path_mock.is_dir.return_value = False
        path_mock.exists.return_value = False
        self.assertFalse(app.App.is_app(path_mock))
        self.assertEqual(0, path_mock.parts.call_count)

        # actual file
        path_mock.is_dir.return_value = True
        path_mock.exists.return_value = True
        path_mock.parts = ['a', 'b', 'c']
        self.assertTrue(app.App.is_app(path_mock))

        # path part has __
        path_mock.parts = ['a', 'b', '__c']
        self.assertFalse(app.App.is_app(path_mock))

        # another path part has __
        path_mock.parts = ['__a', 'b', 'c']
        self.assertFalse(app.App.is_app(path_mock))

        # all path parts has __
        path_mock.parts = ['__a', '__b', '__c']
        self.assertFalse(app.App.is_app(path_mock))

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

    def test_get_url_prefix(self):
        app_mock = mock.MagicMock()
        app_mock.parent = None

        # Core app without custom path
        app_mock.CUSTOM_URL_PATH = None
        self.assertEqual('', app.App.get_url_prefix(app_mock))

        # Core app with custom path
        app_mock.CUSTOM_URL_PATH = '/custom'
        self.assertEqual('/custom', app.App.get_url_prefix(app_mock))

        parent_mock = mock.MagicMock()
        parent_mock.get_url_prefix.return_value = '/parent-part'
        app_mock.parent = parent_mock

        # secondary app with custom path
        parent_mock.parent = None
        app_mock.name = 'child'
        self.assertEqual('/parent-part/custom', app.App.get_url_prefix(app_mock))

        # secondary app without custom path
        app_mock.CUSTOM_URL_PATH = None
        self.assertEqual('/parent-part/child', app.App.get_url_prefix(app_mock))

        # thirded app without custom path
        parent_mock.parent = True
        self.assertEqual('/child', app.App.get_url_prefix(app_mock))

        # thirded app with custom path
        app_mock.CUSTOM_URL_PATH = '/custom'
        self.assertEqual('/custom', app.App.get_url_prefix(app_mock))


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
