import unittest
from jija.utils.path import Path


class PathTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path_lists = [
            ['this', 'is', 'python', 'path.py'],
            ['this', 'is', 'dir', 'path']
        ]

    def test_split(self):
        for index, is_python in enumerate((True, False)):
            result = self.path_lists[index].copy()
            if result[-1].endswith('.py'):
                result[-1] = result[-1][:-3]

            path_win = '\\'.join(self.path_lists[index])
            path_linux = '/'.join(self.path_lists[index])
            path_python = '.'.join(self.path_lists[index])

            self.assertEqual(Path.split(self.path_lists[index]), (result, is_python))
            self.assertEqual(Path.split(path_win), (result, is_python))
            self.assertEqual(Path.split(path_linux), (result, is_python))
            self.assertEqual(Path.split(path_python), (result, is_python))

    def test_transform(self):
        for path_list in self.path_lists:
            path = Path(path_list)

            try:
                self.assertEqual(path.system, '/'.join(path_list))
            except AssertionError:
                self.assertEqual(path.system, '\\'.join(path_list))

            python_path = '.'.join(path_list)
            if python_path.endswith('.py'):
                python_path = python_path[:-3]
            self.assertEqual(path.python, python_path)

    def test_has_protected_nodes(self):
        default_path = Path(['this', 'is', 'default', 'path'])
        protected_path = Path(['this', 'is', '__protected', 'path'])

        self.assertFalse(default_path.has_protected_nodes())
        self.assertTrue(protected_path.has_protected_nodes())

    def test_add(self):
        error_path = Path(self.path_lists[0])
        normal_path = Path(self.path_lists[1])

        self.assertRaises(TypeError, lambda: error_path + 'test')
        self.assertRaises(NotImplementedError, lambda: normal_path + 1)
        self.assertEqual([*self.path_lists[1], 'new'], (normal_path + 'new')._Path__path)
