from unittest import TestCase
from jija.config import *


class ConfigTests(TestCase):
    def test_base(self):
        self.assertFalse(ProjectConfig.INITED)

        ProjectConfig()
        self.assertTrue(ProjectConfig.INITED)
        self.assertRaises(Exception, lambda: ProjectConfig())
        ProjectConfig.clean()
        self.assertFalse(ProjectConfig.INITED)

        try:
            ProjectConfig()
        except Exception:
            self.assertFalse(True)

        self.assertTrue(ProjectConfig.INITED)
        ProjectConfig.clean()

    def test_project(self):
        self.assertIsNone(ProjectConfig.SECRET_KEY)

    def test_database(self):
        self.assertIsNone(DatabaseConfig.DATABASE)
        self.assertIsNone(DatabaseConfig.PASSWORD)
        self.assertIsNone(DatabaseConfig.USER)
        self.assertIsNone(DatabaseConfig.PORT)
        self.assertIsNone(DatabaseConfig.HOST)
        self.assertIsNone(DatabaseConfig.APPS)

    def test_network(self):
        self.assertIsNone(NetworkConfig.PORT)
        self.assertIsNone(NetworkConfig.HOST)

    def test_structure(self):
        self.assertIsNone(StructureConfig.PROJECT_PATH)
        self.assertIsNone(StructureConfig.CORE_PATH)
        self.assertIsNone(StructureConfig.APPS_PATH)
