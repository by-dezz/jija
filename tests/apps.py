import unittest

from jija.app import App
from jija.apps import Apps
from jija.config import BaseConfig
from jija.config.structute import StructureConfig
from jija.utils.path import Path
from tests.test_data.app.normal.app import NormalApp
from tests.test_data.apps.with_core.core.app import CustomApp


class AppsTests(unittest.TestCase):
    def test_create_base_app(self):
        BaseConfig(secret_key=b'a' * 32)

        StructureConfig(project_dir=Path(['tests', 'test_data', 'apps', 'with_core']))
        app = Apps._Apps__create_base_app()
        self.assertEqual(type(app), CustomApp)
        self.assertEqual(len(list(app.aiohttp_app.router.routes())), 2)
        self.assertEqual(len(list(app.aiohttp_app.middlewares)), 5)

        StructureConfig(project_dir=Path(['tests', 'test_data', 'apps', 'without_core']))
        app = Apps._Apps__create_base_app()
        self.assertEqual(type(app), App)
        self.assertEqual(len(list(app.aiohttp_app.router.routes())), 0)
        self.assertEqual(len(list(app.aiohttp_app.middlewares)), 3)

    def test_app_exists(self):
        normal_path = Path(['tests', 'test_data', 'app', 'normal'])
        self.assertTrue(Apps.app_exists(normal_path))

        empty_path = Path(['tests', 'test_data', 'app', 'empty'])
        self.assertFalse(Apps.app_exists(empty_path))

    def test_collect(self):
        BaseConfig(secret_key=b'a' * 32)

        StructureConfig(project_dir=Path(['tests', 'test_data', 'apps', 'with_core']))
        parent = Apps._Apps__create_base_app()
        Apps._Apps__collect(StructureConfig.apps_path, parent)
        self.assertListEqual(list(Apps.apps.keys()), ['a', 'aa', 'b', 'ba', 'bb'])
        Apps.apps = {}

        StructureConfig(project_dir=Path(['tests', 'test_data', 'apps', 'without_core']))
        parent = Apps._Apps__create_base_app()
        Apps._Apps__collect(StructureConfig.apps_path, parent)
        self.assertListEqual(list(Apps.apps.keys()), [])
        Apps.apps = {}

    def test_get_modify_class(self):
        normal_path = Path(['tests', 'test_data', 'app', 'normal'])
        self.assertEqual(Apps.get_modify_class(normal_path), NormalApp)

        error_path = Path(['tests', 'test_data', 'app', 'error'])
        self.assertEqual(Apps.get_modify_class(error_path), App)
