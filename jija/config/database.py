import jija.config
from jija.config.base import Base


class DatabaseConfig(Base):
    REQUIRED = False

    DATABASE = None
    PASSWORD = None
    USER = None
    PORT = None
    HOST = None

    def __init__(self, *, database, password, host='localhost', user='postgres', port=5432, **kwargs):
        DatabaseConfig.DATABASE = database
        DatabaseConfig.PASSWORD = password
        DatabaseConfig.USER = user
        DatabaseConfig.PORT = port
        DatabaseConfig.HOST = host

        super().__init__(**kwargs)

    @classmethod
    async def load(cls):
        from jija_orm import config

        await config.JijaORM.async_init(
            project_dir=jija.config.StructureConfig.PROJECT_PATH,
            connection=config.Connection(
                host=cls.HOST,
                port=cls.PORT,
                user=cls.USER,
                database=cls.DATABASE,
                password=cls.PASSWORD
            ),
            apps=await cls.__get_apps()
        )

    @classmethod
    async def __get_apps(cls):
        from jija_orm import config
        from jija.apps import Apps

        apps = []
        for app in Apps.apps.values():
            if app.exist('models.py'):
                apps.append(config.App(name=app.name, migration_dir=app.get_import_path('migrations')))

        return apps
