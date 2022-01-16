from aiohttp import web


from jija.command import Command


class RunProcess(Command):
    def handle(self):
        from jija.apps import Apps
        web.run_app(Apps.core.aiohttp_app, loop=self.loop, port=8080)
