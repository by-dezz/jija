import re
import typing

from aiohttp import web
from typing import List

from jija import views, serializers


class DocsProcessor:
    FIELD_MAPPING = {
        serializers.fields.CharField: 'string',
        serializers.fields.IntegerField: 'integer',
    }

    def __init__(self, aiohttp_app: web.Application):
        self.__aiohttp_app = aiohttp_app

    async def create_json(self):
        paths = await self.__parse_router()

        return {
            'openapi': '3.0.1',
            'paths': paths,
        }

    async def __parse_router(self) -> dict:
        paths = {}
        for endpoint in self.__aiohttp_app['JIJA_ROUTER'].endpoints:
            if issubclass(endpoint.view, views.DocMixin):
                path_params = re.findall(r'{(\w*)}', endpoint.path)
                paths[endpoint.path] = await self.__parse_view(endpoint.view, path_params)

        return paths

    async def __parse_view(self, view: typing.Type[views.View], path_params: List[str]):
        methods = {}
        for method in view.get_methods():
            methods[method] = {
                'summary': getattr(view, method).__doc__,
                'tags': [view.__name__],

                "responses": {
                    "default": {}
                }
            }

            serializer_in = await view.get_in_serializer(method)
            if serializer_in:
                if method == 'get':
                    methods[method]['parameters'] = self.__parse_serializer_in_get(serializer_in, path_params)

                else:
                    methods[method].update(self.__parse_serializer_in(serializer_in, path_params))

        return methods

    @staticmethod
    def __parse_serializer_in_get(serializer: serializers.Serializer, path_params: List[str]):
        fields = []

        for path_param in path_params:
            fields.append({
                'name': path_param,
                'in': 'path',
                'required': True,
                "schema": {'type': 'string'}
            })

        for name, field in serializer.get_fields().items():
            fields.append({
                'name': name,
                'in': 'query',
                'required': field.required,
                "schema": field.doc_get_schema()
            })

        return fields

    @staticmethod
    def __parse_serializer_in(serializer: serializers.Serializer, path_params: List[str]):
        fields = serializer.get_fields()

        parameters = []
        for path_param in path_params:
            parameters.append({
                'name': path_param,
                'in': 'path',
                'required': True,
                "schema": {'type': 'string'}
            })

        required = []
        properties = {}
        for name, field in fields.items():
            if field.required:
                required.append(name)

            properties[name] = field.doc_get_schema()

        return {
            "requestBody": {
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "required": required,
                            "properties": properties
                        }
                    }
                }
            },

            'parameters': parameters
        }
