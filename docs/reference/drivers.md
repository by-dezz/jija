## Driver
    class jija.drivers.Driver
        async def setup(self, aiohttp_app: web.Application) -> web.Application
        async def preflight(self)

#### setup
This method is calling when app is collecting.

???+ warning
    If you reimplement this method, you need to return aiohttp app, else collecting process will be broken.

#### preflight
This method is calling when app is starting.

## DatabaseDriver
    class jija.drivers.DatabaseDriver
        async def get_connection(self)
        async def migrate(self)
        async def update(self)

#### get_connection
Get connection to database.

???+ warning
    This method is unused in current version of jija and may be removed in future.

#### migrate
This method is calling when you execute `python main.py migrate` command.

#### update
This method is calling when you execute `python main.py update` command.


## DocsDriver
    class DocsDriver(base.Driver)

Yep, it's docs driver.