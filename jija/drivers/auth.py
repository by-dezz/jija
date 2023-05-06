from aiohttp import web

import jija.app
from jija.drivers.base import Driver
from jija.auth import rules


class AuthDriver(Driver):
    def __init__(self, default_auth_rule: rules.AuthRule = rules.AuthRuleAllowAll, **kwargs):
        self.__default_auth_rule = default_auth_rule

    @property
    def default_auth_rule(self):
        return self.__default_auth_rule

    # def setup(self, app: jija.app.App):
    #     if app.DEFAULT_AUTH_RULE is None:
    #         app.DEFAULT_AUTH_RULE = self.default_auth_rule

    async def create_user(self, login, password):
        raise NotImplementedError()

    async def get_user(self, request: web.Request):
        raise NotImplementedError()

    async def authenticate(self, user, request: web.Request):
        raise NotImplementedError()

    async def deauthenticate(self, user, request: web.Request):
        raise NotImplementedError()
