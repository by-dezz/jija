import functools
import inspect
import json
from typing import Union, Optional, Type

import jija.exceptions


class Wrapper:
    @classmethod
    def construct(cls, handler):
        @functools.wraps(handler)
        async def wrapper(view):
            cls.__init__(view)
            return await cls.wrapper(view, handler)

        return wrapper

    async def wrapper(self: Union['jija.views.SimpleView', 'Wrapper'], handler, **kwargs):
        return await handler(self, **kwargs)


class ForceExitWrapper(Wrapper):
    async def wrapper(self, handler, **kwargs):
        try:
            return await handler(self, **kwargs)

        except jija.exceptions.ViewForceExit as exception:
            return exception.response


class DataLoadWrapper(Wrapper):
    def __init__(self: Union['jija.views.SimpleView', 'DataLoadWrapper']):
        self.__data = {}

    @property
    def data(self: Union['jija.views.SimpleView', 'DataLoadWrapper']):
        return self.__data

    async def wrapper(self: Union['jija.views.SimpleView', 'DataLoadWrapper'], handler, **kwargs):
        self.__data = {
            **await self.parse_body(),
            **self.parse_path(),
            **self.parse_query()
        }

        return await handler(self, **kwargs)

    async def parse_body(self: Union['jija.views.SimpleView', 'DataLoadWrapper']) -> dict:
        if self.request.method.lower() != 'get':
            try:
                return await self.request.json()
            except json.JSONDecodeError:
                return {}

        return {}

    def parse_path(self: Union['jija.views.SimpleView', 'DataLoadWrapper']) -> dict:
        return dict(self.request.match_info)

    def parse_query(self: Union['jija.views.SimpleView', 'DataLoadWrapper']) -> dict:
        data = {}

        for key in set(self.request.query.keys()):
            value = self.request.query.getall(key)
            if len(value) == 1:
                value = value[0]

            data[key] = value

        return data


class AuthCheckWrapper(Wrapper):
    async def wrapper(self: Union['jija.views.View', 'AuthCheckWrapper'], handler, **kwargs):
        auth_rule = self.get_auth_rule()
        if auth_rule is not None and not auth_rule.check(self.request):
            return jija.response.JsonResponse({'error': 'Unauthorized'}, status=401)

        return await handler(self, **kwargs)

    def get_auth_rule(
            self: Union['jija.views.View', 'AuthCheckWrapper']
    ) -> Optional['jija.drivers.auth.rules.AuthRule']:
        return (
                self.DEFAULT_AUTH_RULE or
                self.app.DEFAULT_AUTH_RULE or
                jija.config.DriversConfig.AUTH.default_auth_rule
        )()


    @property
    def user(self: Union['jija.views.View', 'AuthCheckWrapper']):
        # noinspection PyUnresolvedReferences
        return self.request.user


class SerializerWrapper(Wrapper):
    def __init__(self):
        self.__serializers = None

    @classmethod
    def construct(cls, handler):
        serializers = cls.get_serializers(handler)
        handler.__serializers__ = serializers
        async def wrapper(view):
            cls.__init__(view)
            cls.serializers = serializers
            return await cls.wrapper(view, handler)

        return wrapper

    @staticmethod
    def get_serializers(handler):
        serializers = {}
        for name, arg in inspect.signature(handler).parameters.items():
            if name == 'self':
                continue

            if issubclass(arg.annotation, jija.serializers.Serializer):
                serializers[name] = arg.annotation

        return serializers

    @property
    def serializers(self):
        return self.__serializers

    @serializers.setter
    def serializers(self, value):
        if not self.__serializers:
            self.__serializers = value
        else:
            raise ValueError('Serializers already set')

    async def wrapper(self: Union['jija.views.SimpleView', 'SerializerWrapper'], handler, **kwargs):
        try:
            data = await self.serialize()
            return await handler(self, **data)

        except jija.serializers.SerializeError as error:
            return jija.response.JsonResponse(error.serializer.errors, status=400)


    async def serialize(
            self: Union['jija.views.SimpleView', 'DataLoadWrapper', 'SerializerWrapper']
    ) -> dict['jija.serializers.Serializer']:

        data = {}
        for name, serializer_class in self.serializers.items():
            serializer = serializer_class(self.data)
            await serializer.in_serialize()

            if not serializer.valid:
                raise jija.serializers.SerializeError(serializer)

            data[name] = serializer

        return data
