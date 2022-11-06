from jija import views

from aiohttp import web


class Router:
    def __init__(self, endpoints):
        self.__routes = self.__generate_routes(endpoints)

    @property
    def routes(self):
        return self.__routes

    @staticmethod
    def __generate_routes(endpoints):
        result = []
        for endpoint in endpoints:
            result.extend(endpoint.generate_routes())

        return result


class AbsEndpoint:
    def generate_routes(self, prefix=''):
        raise NotImplementedError()


class Endpoint(AbsEndpoint):
    def __init__(self, path, view):
        if not issubclass(view, views.View):
            raise AttributeError(f'view must be a subclass of "jija.views.View", got {type(view)}')

        self.__path = path
        self.__view = view

    def generate_routes(self, prefix=''):
        result = []
        for method in self.__view.get_methods():
            result.append(web.route(method, f'{prefix}{self.__path}', self.__view.construct))

        return result


class Include(AbsEndpoint):
    def __init__(self, path, endpoints):
        self.__path = path
        self.__endpoints = endpoints

    def generate_routes(self, prefix=''):
        result = []
        for endpoint in self.__endpoints:
            result.extend(endpoint.generate_routes(prefix))

        return result
