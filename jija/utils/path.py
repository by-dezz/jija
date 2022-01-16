import os.path


class Path:
    def __init__(self, path):
        self.__path = self.split(path)

    @staticmethod
    def split(path):
        if isinstance(path, list):
            return path

        if path.count('/'):
            return path.split('/')

        if path.count('\\'):
            return path.split('\\')

        return path.split('.')

    @property
    def python(self):
        return '.'.join(self.__path)

    @property
    def system(self):
        return os.path.join(*self.__path)

    def has_protected_nodes(self):
        for node in self.__path:
            if node.startswith('__'):
                return True

    def __add__(self, other):
        if isinstance(other, str):
            return Path(self.__path + [other])
        else:
            raise NotImplementedError()
