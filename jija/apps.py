import importlib
import os
import sys

import aiohttp_session
from aiohttp import web
from aiohttp_session.cookie_storage import EncryptedCookieStorage

import settings
from jija import middlewares
from jija.app import App
from jija.utils.path import Path
from jija import commands
from jija.utils.collector import collect_subclasses


class AppGetter(type):
    def __getattr__(self, item):
        app = Apps.apps.get(item)
        if app:
            return app

        raise AttributeError(item)


class Apps(metaclass=AppGetter):
    apps = {}
    commands = {
        'system': commands.COMMANDS
    }

    @classmethod
    def load(cls):
        Apps.apps['core'] = cls.__create_base_app()
        cls.__collect(Path('apps'), Apps.apps['core'])
        cls.__register_apps()

    @classmethod
    def __create_base_app(cls):
        app = web.Application()
        aiohttp_session.setup(app, EncryptedCookieStorage(getattr(settings, 'SECRET_KEY')))

        app.middlewares.extend([
            middlewares.print_request.PrintRequest(),
            middlewares.url_corrector.slash_redirect,
        ])

        base_path = Path('core')
        if cls.app_exists(base_path):
            app = App(path=base_path, aiohttp_app=app, name='core')

        return app

    @staticmethod
    def app_exists(path):
        return os.path.exists((path + 'app.py').system)

    @classmethod
    def __collect(cls, path, parent):
        for sub_app_name in os.listdir(path.system):

            next_path = path + sub_app_name
            if App.is_app(next_path):
                app = cls.get_modify_class(next_path)(path=next_path, parent=parent, name=sub_app_name)
                cls.commands[sub_app_name] = app.commands
                cls.apps[sub_app_name] = app
                cls.__collect(path + sub_app_name, app)

    @staticmethod
    def get_modify_class(path):
        module = importlib.import_module((path + 'app').python)
        modify_class = list(collect_subclasses(module, App))
        return modify_class[0] if modify_class else App

    @classmethod
    def __register_apps(cls, app=None):
        if not app:
            app = cls.apps['core']

        if not app.childes and app.name != 'core':
            app.parent.aiohttp_app.add_subapp(f'/{app.name}', app.aiohttp_app)

        for child in app.childes:
            cls.__register_apps(child)

    @classmethod
    def get_command(cls, module, command):
        if module is None:
            module = 'system'

        return cls.commands[module][command]

    @classmethod
    def run_command(cls):
        args = sys.argv
        command = args[1].split('.')
        Apps.load()

        if len(command) == 1:
            module = None
            command = command[0]
        else:
            module, command = command

        command_class = cls.get_command(module, command)
        command_obj = command_class()
        command_obj.run()
