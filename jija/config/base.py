import jija.app


class Config:
    __REQUIRED_ADDONS = set()
    __PREF = {}

    def __init__(self, **kwargs):
        from jija import apps

        self.__class__.__PREF = kwargs
        apps.Apps.config_init_callback(self.__class__)

    @classmethod
    async def freeze(cls):
        validated_data = await cls.validate(cls.__PREF)
        cls.set_values(validated_data)

    @classmethod
    async def validate(cls, values: dict) -> dict:
        validated_data = {}
        for name, value in values.items():
            name = name.upper()
            field = getattr(cls, name)
            validated_data[name.upper()] = await field.validate(value)

        return validated_data

    @classmethod
    def set_values(cls, validated_data: dict):
        for name, value in validated_data.items():
            setattr(cls, name, value)

    @classmethod
    def core_setup(cls, app: jija.app.App):
        pass

    @classmethod
    def setup(cls, app: jija.app.App):
        pass

    @classmethod
    async def preflight(cls):
        pass
