from unittest import TestCase
from jija.config import *


# class ConfigTests(TestCase):
#     def test_base(self):
#         self.assertFalse(ProjectConfig.INITED)
#
#         ProjectConfig()
#         self.assertTrue(ProjectConfig.INITED)
#         self.assertRaises(Exception, lambda: ProjectConfig())
#         ProjectConfig.clean()
#         self.assertFalse(ProjectConfig.INITED)
#
#         try:
#             ProjectConfig()
#         except Exception:
#             self.assertFalse(True)
#
#         self.assertTrue(ProjectConfig.INITED)
#
#         try:
#             ProjectConfig(reset_init=True)
#         except Exception:
#             self.assertFalse(True)
#
#         ProjectConfig.clean()
#
#     def test_project(self):
#         self.assertIsNone(ProjectConfig.SECRET_KEY)

    # def test_database(self):
    #     self.assertIsNone(DatabaseConfig.DATABASE)
    #     self.assertIsNone(DatabaseConfig.PASSWORD)
    #     self.assertIsNone(DatabaseConfig.USER)
    #     self.assertIsNone(DatabaseConfig.PORT)
    #     self.assertIsNone(DatabaseConfig.HOST)

    # def test_database_setup(self):
    #     config = {
    #         'database': 'test',
    #         'password': 'test',
    #         'host': 'testhost',
    #         'user': 'test',
    #         'port': 1234
    #     }
    #
    #     DatabaseConfig(**config)
    #
    #     self.assertEqual(DatabaseConfig.DATABASE, config['database'])
    #     self.assertEqual(DatabaseConfig.PASSWORD, config['password'])
    #     self.assertEqual(DatabaseConfig.HOST, config['host'])
    #     self.assertEqual(DatabaseConfig.USER, config['user'])
    #     self.assertEqual(DatabaseConfig.PORT, config['port'])
    #
    #     self.assertEqual(
    #         DatabaseConfig.CONNECTION_LINK,
    #         'postgres://{user}:{password}@{host}:{port}/{database}'.format(**config)
    #     )
    #
    #     DatabaseConfig.clean()

    # def test_network(self):
    #     self.assertIsNone(NetworkConfig.PORT)
    #     self.assertIsNone(NetworkConfig.HOST)
    #
    # def test_network_setup(self):
    #     config = {
    #         'port': 1234,
    #         'host': 'test',
    #     }
    #
    #     NetworkConfig(**config)
    #
    #     self.assertEqual(NetworkConfig.PORT, config['port'])
    #     self.assertEqual(NetworkConfig.HOST, config['host'])
    #
    #     NetworkConfig.clean()
    #
    # def test_structure(self):
    #     self.assertIsNone(StructureConfig.PROJECT_PATH)
    #     self.assertIsNone(StructureConfig.CORE_PATH)
    #     self.assertIsNone(StructureConfig.APPS_PATH)

    # def test_structure_setup(self):
    #     config = {
    #         'project_dir': 'test_project',
    #         'core_dir': 'test_core',
    #         'apps_dir': 'test_apps',
    #         'python_path': 'test_python'
    #     }
    #
    #     StructureConfig(**config)
    #
    #     self.assertEqual(StructureConfig.PROJECT_PATH, config['project_dir'])
    #     self.assertEqual(StructureConfig.CORE_PATH, config['core_dir'])
    #     self.assertEqual(StructureConfig.APPS_PATH, config['apps_dir'])
    #     self.assertEqual(StructureConfig.PYTHON_PATH, config['python_path'])
    #
    #     StructureConfig.clean()
