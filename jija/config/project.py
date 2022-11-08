from jija.config import base, fields


class ProjectConfig(base.Config):
    SECRET_KEY = fields.CharField(default=b'*' * 32)

    def __init__(self, *, secret_key=None):
        super().__init__(secret_key=secret_key)
