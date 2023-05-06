from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, Type, Optional

if TYPE_CHECKING:
    from jija.config.base import Config

from pathlib import Path
import importlib
import asyncio
import sys
import os

from jija.collector import collect_subclasses
from jija.command import Command
import jija.base_app.app
from jija import config


class Apps:
    apps: dict[str, jija.app.App] = {}

    __REQUIRED_CONFIGS = {
        config.StructureConfig,
        config.DriversConfig,
        config.NetworkConfig
    }

    __INITED_CONFIGS: list[Type[Config]] = []

    __SETUP_TASKS = []
    __CORE_SETUP_TASKS = []
    __PREFLIGHT_TASKS = []

    @classmethod
    def config_init_callback(cls, config_class: Type[Config]):
        cls.__INITED_CONFIGS.append(config_class)

    #     cls.__register_apps()

    @classmethod
    def __init_configs(cls):
        for config_class in cls.__REQUIRED_CONFIGS:
            if config_class not in cls.__INITED_CONFIGS:
                config_class()

        asyncio.get_event_loop().run_until_complete(cls.__freeze_configs())

    @classmethod
    async def __freeze_configs(cls):
        for config_class in cls.__INITED_CONFIGS:
            await config_class.freeze()

            assert inspect.iscoroutinefunction(config_class.preflight),\
                f'preflight method of {config_class} is not a coroutine'
            cls.__PREFLIGHT_TASKS.append(config_class.preflight)

            cls.__SETUP_TASKS.append(config_class.setup)
            cls.__CORE_SETUP_TASKS.append(config_class.core_setup)

    @classmethod
    def __collect(cls):
        cls.apps['core'] = cls.__create_base_app()
        cls.__collect_process(config.StructureConfig.APPS_PATH, cls.apps['core'])

    @classmethod
    def __create_base_app(cls) -> jija.app.App:
        base_app = jija.base_app.app.BaseApp.construct(
            name='core',
            path=Path(jija.base_app.app.__file__).parent,
            parent=None,
        )

        if cls.app_exists(config.StructureConfig.CORE_PATH):
            core_app = cls.get_modify_class(config.StructureConfig.CORE_PATH).construct(
                name='core',
                path=config.StructureConfig.CORE_PATH,
                extends=base_app
            )
        else:
            core_app = base_app

        return core_app

    @classmethod
    def __collect_process(cls, path: Path, parent: jija.app.App):
        if not path.exists():
            return

        for sub_app_name in os.listdir(path):
            sub_app_name: str

            next_path = path.joinpath(sub_app_name)
            if jija.app.App.is_app(next_path):
                jija_app = cls.get_modify_class(next_path).construct(path=next_path, parent=parent, name=sub_app_name)
                cls.apps[sub_app_name] = jija_app
                cls.__collect_process(path.joinpath(sub_app_name), jija_app)

    @classmethod
    def __setup(cls):
        cls.apps['core'].setup(cls.__SETUP_TASKS, cls.__CORE_SETUP_TASKS)

    @classmethod
    def __register(cls):
        cls.apps['core'].register()

    @classmethod
    def __preflight(cls):
        asyncio.get_event_loop().run_until_complete(asyncio.gather(*map(
            lambda item: item(), cls.__PREFLIGHT_TASKS
        )))

    @staticmethod
    def app_exists(path: Path) -> bool:
        return path.joinpath('app.py').exists()

    @staticmethod
    def get_modify_class(path: Path) -> Type[jija.app.App]:
        modify_class_path = path.joinpath('app')
        import_path = ".".join(modify_class_path.relative_to(config.StructureConfig.PROJECT_PATH).parts)

        module = importlib.import_module(import_path)
        modify_class = list(collect_subclasses(module, jija.app.App))
        return modify_class[0] if modify_class else jija.app.App

    @classmethod
    def get_command(cls, module: Optional[list[str]], command: str) -> Type[Command]:
        return cls.apps[module or 'core'].commands[command]

    @classmethod
    def run_command(cls):
        args = sys.argv
        command = args[1].split('.')

        cls.__init_configs()
        cls.__collect()
        cls.__setup()
        cls.__register()
        cls.__preflight()

        if len(command) == 1:
            module = None
            command = command[0]
        else:
            module, command = command

        command_class = cls.get_command(module, command)
        command_obj = command_class()
        command_obj.run()
