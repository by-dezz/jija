from aiohttp import web


class View:
    methods = ('get', 'post', 'patch', 'put', 'delete')

    def __init__(self, request: web.Request, path_params: web.UrlMappingMatchInfo):
        self.__request = request
        self.__path_params = path_params

    @classmethod
    def get_methods(cls):
        view_methods = []
        for method in cls.methods:
            if hasattr(cls, method):
                view_methods.append(method)

        return view_methods

    @classmethod
    async def construct(cls, request: web.Request):
        view = cls(request, request.match_info)
        return await view.dispatch()

    @property
    def request(self):
        return self.__request

    async def dispatch(self):
        method = self.request.method.lower()
        handler = getattr(self, method)

        return await handler()

    async def serialize(self):
        pass
