from __future__ import annotations
import typing

import jija.views
import jija.app

from aiohttp import web


class Router:
    def __init__(self, endpoints):
        self.__endpoints = endpoints

    @property
    def endpoints(self):
        return self.__endpoints

    def construct_routes(self, app: jija.app.App):
        result = []
        for endpoint in self.endpoints:
            result.extend(endpoint.construct_routes(app))

        return result

    def __repr__(self):
        return f'<{self.__class__.__name__}: {len(self.endpoints)} endpoints>'

    def __str__(self):
        return self.__repr__()

    def __add__(self, other):
        if not isinstance(other, Router):
            raise TypeError(f'Can not add "Router" to {type(other)}')

        return Router(self.endpoints + other.endpoints)


class AbsEndpoint:
    def construct_routes(self, jija_app, prefix=''):
        raise NotImplementedError()


class Endpoint(AbsEndpoint):
    def __init__(self, path, view: typing.Type[jija.views.SimpleView]):
        if not issubclass(view, jija.views.SimpleView):
            raise AttributeError(f'view must be a subclass of "jija.views.ViewBase", got {view}')

        self.__path = path
        self.__view = view

    @property
    def path(self) -> str:
        return self.__path

    @property
    def view(self) -> typing.Type[jija.views.SimpleView]:
        return self.__view

    def construct_routes(self, app: jija.app.App, prefix: str = ''):
        result = []
        for method in self.__view.get_methods():
            result.append(web.route(method, f'{prefix}{self.__path}', self.__view.construct(method, app)))

        return result


class Include(AbsEndpoint):
    def __init__(self, path, endpoints):
        if path[-1] == '/':
            raise ValueError('Include path must ends without "/"')

        self.__path = path
        self.__endpoints = endpoints

    @property
    def path(self):
        return self.__path

    @property
    def endpoints(self):
        return self.__endpoints

    def construct_routes(self, app: jija.app.App, prefix=''):
        result = []
        for endpoint in self.__endpoints:
            result.extend(endpoint.construct_routes(app, f'{self.__path}{prefix}'))

        return result
