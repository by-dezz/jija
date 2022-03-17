import unittest

from jija.app import App
from jija.apps import Apps
from jija import config
from jija.config import base
from jija.utils.collector import collect_subclasses
from jija.utils.path import Path
from tests.test_data.app.normal.app import NormalApp
from tests.test_data.apps.with_core.core.app import CustomApp


class AppsTests(unittest.TestCase):
    def doCleanups(self):
        config.ProjectConfig.clean()
        config.StructureConfig.clean()

    def test_init_configs(self):
        configs = [config_class for config_class in collect_subclasses(config, config.base.Base)]

        for config_class in configs:
            self.assertFalse(config_class.INITED)

        self.assertRaises(TypeError, Apps._Apps__init_configs)
        config.DatabaseConfig(database='test', password='test')
        Apps._Apps__init_configs()

        for config_class in configs:
            self.assertTrue(config_class.INITED)

        for config_class in configs:
            self.assertFalse(config_class.clean())

    def test_create_base_app(self):
        config.ProjectConfig(secret_key=b'a' * 32)

        config.StructureConfig(project_dir=Path(['tests', 'test_data', 'apps', 'with_core']))
        app = Apps._Apps__create_base_app()
        self.assertEqual(type(app), CustomApp)
        self.assertEqual(len(list(app.aiohttp_app.router.routes())), 2)
        self.assertEqual(len(list(app.aiohttp_app.middlewares)), 5)
        config.StructureConfig.clean()

        config.StructureConfig(project_dir=Path(['tests', 'test_data', 'apps', 'without_core']))
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
        config.ProjectConfig(secret_key=b'a' * 32)

        config.StructureConfig(project_dir=Path(['tests', 'test_data', 'apps', 'with_core']))
        parent = Apps._Apps__create_base_app()
        Apps._Apps__collect(config.StructureConfig.APPS_PATH, parent)
        self.assertListEqual(list(Apps.apps.keys()), ['a', 'aa', 'b', 'ba', 'bb'])
        Apps.apps = {}
        config.StructureConfig.clean()

        config.StructureConfig(project_dir=Path(['tests', 'test_data', 'apps', 'without_core']))
        parent = Apps._Apps__create_base_app()
        Apps._Apps__collect(config.StructureConfig.APPS_PATH, parent)
        self.assertListEqual(list(Apps.apps.keys()), [])
        Apps.apps = {}

    def test_get_modify_class(self):
        normal_path = Path(['tests', 'test_data', 'app', 'normal'])
        self.assertEqual(Apps.get_modify_class(normal_path), NormalApp)

        error_path = Path(['tests', 'test_data', 'app', 'error'])
        self.assertEqual(Apps.get_modify_class(error_path), App)
