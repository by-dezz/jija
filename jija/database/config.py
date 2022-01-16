class DatabaseConfig:
    database = None
    password = None
    user = None
    port = None
    host = None

    apps = {}

    connection_link = None

    def __init__(self, *, database, password, host='localhost', user='postgres', port=5432):
        DatabaseConfig.database = database
        DatabaseConfig.password = password
        DatabaseConfig.user = user
        DatabaseConfig.port = port
        DatabaseConfig.host = host

        DatabaseConfig.connection_link = f'postgres://{user}:{password}@{host}:{port}/{database}'

    @classmethod
    def load(cls):
        from jija.apps import Apps
        for app in Apps.apps.values():
            if app.database:
                cls.apps[app.name] = {
                    "models": app.database_config,
                    "default_connection": "default",
                }

    @classmethod
    def get_config(cls):
        return {
            "connections": {
                "default": cls.connection_link
            },

            "apps": cls.apps,

            'use_tz': False,
            'timezone': 'Asia/Yekaterinburg'
        }
