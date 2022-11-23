from aiohttp import web


from jija import views, response
from jija import router
from jija import serializers


class JijaSer(serializers.Serializer):
    ff = serializers.fields.CharField(required=False, min_length=9, max_length=10)
    aa = serializers.fields.IntegerField(required=False)


class Buba(views.View, views.DocMixin):
    serializers_in = views.SerializersSet(
        get=JijaSer,
        post=JijaSer
    )

    # serializers_out = views.SerializersSet()

    async def get(self):
        """description: This end-point allow to test that service is up."""
        from core import models
        print(self.data, 123)
        return web.json_response(data={'asd': 123})

    async def post(self):
        return response.Response()

    async def delete(self):
        return response.Response()


class B1(views.View):
    async def get(self):
        """
        description: This end-point allow to test that service is up.
        """
        from core import models
        return web.json_response(data={'asd': 123})


class Basd(views.View, views.DocMixin):
    """
    ahahahahhahha
    """
    async def get(self):
        """
        description: This end-point allow to test that service is up.
        """
        from core import models
        return web.json_response(data={'asd': 123})


routes = [
    router.Endpoint('/buba/{dd}/{ahhah}/', Buba),
    router.Endpoint('/1/', B1),
    router.Endpoint('/dasd/', Basd),
]
