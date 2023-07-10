class AuthRule:
    def check(self, request) -> bool:
        raise NotImplementedError()


class AuthRuleAllowAll(AuthRule):
    def check(self, request) -> bool:
        return True


class AuthRuleAuthenticated(AuthRule):
    def check(self, request) -> bool:
        return request.user is not None