import jija
from aiohttp import web
from jija.command import Command


HELLO_MESSAGE = """
░░░░░██╗██╗░░░░░██╗░█████╗░     Version:    {version}
░░░░░██║██║░░░░░██║██╔══██╗     Bind at:    {bind_ad}
░░░░░██║██║░░░░░██║███████║     
██╗░░██║██║██╗░░██║██╔══██║     Apps load:  {apps_load}
╚█████╔╝██║╚█████╔╝██║░░██║     Routes len: {routes_len}
░╚════╝░╚═╝░╚════╝░╚═╝░░╚═╝
"""

class RunProcess(Command):
    def handle(self):
        from jija.apps import Apps
        from jija.config import NetworkConfig

        web.run_app(
            Apps.apps['core'].aiohttp_app,
            loop=self.loop,
            host=NetworkConfig.HOST,
            port=NetworkConfig.PORT,
            print=self.run_message
        )

    def run_message(self, *args, **kwargs):
        print(HELLO_MESSAGE.format(
            version=jija.__version__,
            bind_ad=f'http://{jija.config.NetworkConfig.HOST}:{jija.config.NetworkConfig.PORT}',
            apps_load=len(jija.apps.Apps.apps),
            routes_len=sum([len(app.aiohttp_app.router.routes()) for app in jija.apps.Apps.apps.values()])
        ))
