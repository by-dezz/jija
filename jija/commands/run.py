import asyncio
import subprocess

from jija import config
from jija.command import Command
from jija import reloader


class Run(Command):
    def __init__(self):
        super().__init__()
        self.close_event = asyncio.Event()

    async def run_watcher(self):
        reloader_instance = reloader.Reloader(config.StructureConfig.PROJECT_PATH, self.close_event)
        await reloader_instance.wait()

    async def handle(self):
        asyncio.create_task(self.run_watcher())
        while True:
            runner = subprocess.Popen([config.StructureConfig.PYTHON_PATH, 'main.py', 'runprocess'])
            self.close_event.clear()
            await self.close_event.wait()
            runner.kill()
            print()
